from mpi4py import MPI
from msg_enum import Msg_type
from destination_enum import Dest
import sys
import time
from datetime import datetime
from actor import Actor
from message import Message
from weather_collection import *
from location import Location



class Weatherman:
  def __init__(self):
    self.events = {}
    self.curr_location = Location()
    self.curr_weather = Weather()
    self.earliest_event_id = 0
    self.next_event = None
    self.time_last_notification = 0
    self.last_alert_msg = ""
    self.notification_flags = {'temp': False, 'pop': False, 'humidity': False, 'wind_speed': False}
    
        
  def generate_intialized_msg(self, event_id):
    return {"event_id": event_id, "msg": "weatherman_intialized", "date": datetime.now()}

  def generate_weather_notifcation(self, notif):
    return {"alert_msg": notif["alert_msg"], "notification": notif["notification"],  "is_alert": notif["is_alert"]}

  def run(rank, comm):
    w = Weatherman()
    a = Actor(rank, comm)
    m = Message(msg = w.generate_intialized_msg(Dest.WEATHERMAN), receiver = Dest.TIMEKEEPER, msg_type=Msg_type.INITIALIZED, sender = rank)
    a.send(m)
    i = 0
    while True:
      msg = a.recv()
      if msg == None: continue
      tag = msg.get_msg_type()

      # message processing 

      if tag == Msg_type.NEW_EVENT:
        event = msg.msg
        event_id = event.event_id
        # update earliest event
        if w.earliest_event_id > event_id:
          w.earliest_event_id = event_id
          w.next_event = event
        # add to the list of events
        w.events[event_id] = event
        event.weather = get_weather_info(event.event_location, event.start_time)
        weather_msg = Message(msg = event, receiver = Dest.TIMEKEEPER, msg_type=Msg_type.UPDATE_EVENT_WEATHER, sender = rank )
        a.broadcast(weather_msg, exclude=[Dest.NAVIGATOR, Dest.SCHEDULER])

      elif tag == Msg_type.DELETE_EVENT:
        if msg.msg in w.events:
          del w.events[msg.msg]

      elif tag == Msg_type.REQUEST_WEATHER:
        event = msg.msg
        event.weather = get_weather_info(event.event_location, event.start_time)
        weather_msg = Message(msg = event, receiver = Dest.TIMEKEEPER, msg_type=Msg_type.UPDATE_EVENT_WEATHER, sender = rank )
        a.broadcast(weather_msg, exclude=[Dest.NAVIGATOR, Dest.SCHEDULER])

      elif tag == Msg_type.UPDATE_USER_LOCATION:
        #reset current location
        w.curr_location = msg.msg
        weather = get_current_weather_info(w.curr_location)
        w.curr_weather = weather
        weather_msg = Message(msg = w.curr_weather, receiver = Dest.WEB, msg_type=Msg_type.UPDATE_CURRENT_WEATHER, sender = rank )
        a.send(weather_msg)
            
      # check whether a notification needs to be sent (there is an alert or trigger out of bounds)
      # if so send a notification to WEB otherwise do nothing
      alert = check_weather(w)
      if alert["notify"]: 
        n = w.generate_weather_notifcation(alert)
        notif_msg = Message(msg = n, receiver = Dest.WEB, msg_type=Msg_type.WEATHER_NOTIFICATION, sender = rank )
        a.send(notif_msg)
      sys.stdout.flush()
