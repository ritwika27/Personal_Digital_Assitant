#dummy file for message test purposes


from mpi4py import MPI
from msg_enum import Msg_type
from destination_enum import Dest
import sys
import time
import logging
from datetime import datetime, timedelta
from actor import Actor
from message import Message
from location import Location
import requests

api_file = open("APIkey.txt", "r")
api_key = api_file.read()
api_file.close()

url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"

user_location = "greenbelt station, maryland"
transport_mode = "driving"
# driving/ walking/ bicycling/ transit

class Navigator:
  def __init__(self):
    self.locations = {}
    self.curr_location = Location()
    self.earliest_event_id = 0
    self.next_event = None
        
  def generate_intialized_msg(self, rank):
    return {"rank": rank, "msg": "navigator_intialized", "date": datetime.now()}

  # def generate_navigator_msg(self, event_id, travel_time):
  #   return {"event_id": event_id, "travel_time": travel_time,  "msg": "navigator_info", "date": datetime.now()}

  def get_travel_time_estimate(self,user_location, address, transport_mode):
    r = requests.get(url + "origins=" + user_location + "&destinations=" + address + "&mode=" + transport_mode + "&departure_time=now" + "&key=" + api_key)
    logging.debug(r.json()) 
    if transport_mode=="driving":
      time = timedelta(seconds = r.json()["rows"][0]["elements"][0]["duration_in_traffic"]["value"])
    else:
      time = timedelta(seconds = r.json()["rows"][0]["elements"][0]["duration"]["value"])
    return time

  def run(rank, comm):
    n = Navigator()
    a = Actor(rank, comm)
    m = Message(msg = n.generate_intialized_msg(Dest.NAVIGATOR), receiver = Dest.TIMEKEEPER, msg_type=Msg_type.INITIALIZED, sender = rank)
    a.send(m)
    i = 0

    while True:
      msg = a.recv()
      if msg == None: continue
      tag = msg.get_msg_type()

      if tag == Msg_type.NEW_EVENT:
        event = msg.msg
        event_id = event.event_id
        #set next earliest event
        if n.earliest_event_id > event_id:
          n.earliest_event_id = event_id
          n.next_event = event
        #store new event
        n.locations[event_id] = event.event_location
        #get _estimate
        event.estimate = n.get_travel_time_estimate(n.curr_location.address, event.event_location.address, event.preference)
        navigator_msg = Message(msg = event, receiver = Dest.TIMEKEEPER, msg_type=Msg_type.RESPONSE_ESTIMATE, sender = rank)
        a.send(navigator_msg)

      elif tag == Msg_type.REQUEST_ESTIMATE:
        event = msg.msg
        # get estimate
        event.estimate = n.get_travel_time_estimate(n.curr_location.address, event.event_location.address, event.preference)
        navigator_msg = Message(msg = event, receiver = Dest.TIMEKEEPER, msg_type=Msg_type.RESPONSE_ESTIMATE, sender = rank )
        a.send(navigator_msg) 

      elif tag == Msg_type.UPDATE_USER_LOCATION:
        n.curr_location = msg.msg
        # if there is no next event, cant update estimate
        if n.next_event == None:
          continue
        address = n.next_event.event_location.address
        time = n.get_travel_time_estimate(n.curr_location.address, address, n.next_event.preference)
        n.next_event.estimate = time
        navigator_msg = Message(msg = n.next_event, receiver = Dest.TIMEKEEPER, msg_type=Msg_type.UPDATE_ESTIMATE, sender = rank )
        a.send(navigator_msg)               
