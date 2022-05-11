import logging
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta



# self defined modules
from destination_enum import Dest
from msg_enum import Msg_type
from actor import Actor
from message import Message
from event import Event

class Timekeeper:
  def __init__(self, actor):
    self.next_event = None
    self.events = {}
    self.scheduler = BackgroundScheduler()
    self.scheduler.start()
    self.actor = actor

  def run(rank, comm):
    a = Actor(rank, comm)
    t = Timekeeper(a)

    while True:
      msg = a.recv()

      if msg.msg_type == Msg_type.INITIALIZED:
        print("{} initialized".format(Dest(msg.sender).name))
      elif msg.msg_type == Msg_type.NEW_EVENT:
        t.events[msg.msg.event_id] = msg.msg
      elif msg.msg_type == Msg_type.UPDATE_ESTIMATE or msg.msg_type == Msg_type.RESPONSE_ESTIMATE:
        if msg.msg.event_id in t.events:
          event = t.events[msg.msg.event_id]
          event.estimate = msg.msg.estimate
          t.set_up_job(event)
      elif msg.msg_type == Msg_type.UPDATE_EVENT_WEATHER:
        if msg.msg.event_id in t.events:
          event = t.events[msg.msg.event_id]
          event.weather = msg.msg.weather #contains all weather information, to extract only precipitation: msg.msg.weather.pop

      sys.stdout.flush()

  def set_up_job(self, event):
    scheduled_time = max(event.start_time - event.estimate * 2,
                        event.start_time - (event.start_time - datetime.now())/2)
    if scheduled_time >= event.start_time:
      self.invalid_event(event)
      return
    if scheduled_time - event.start_time <= timedelta(minutes = 5):
      self.notify_user(event) 
    elif scheduled_time - event.start_time <= timedelta(minutes = 30):
      scheduled_time = event.start_time - timedelta(minutes = 5)
      self.scheduler.add_job(self.update_event, 'date', run_date = scheduled_time, args=[event])
    else:
      self.scheduler.add_job(self.update_event, 'date', run_date = scheduled_time, args=[event])
    logging.info("set up done, will be executed {}".format(scheduled_time))

  def notify_user(self, event):
    msg = Message(msg = {'estimate': event.estimate, 'msg': "should leave"}, msg_type = Msg_type.UPDATE_ESTIMATE, sender = self.actor.rank, receiver = Dest.WEB)
    self.actor.isend(msg)

  def invalid_event(self, event):
    #TODO: handle this case
    print("ERROR: event starts too soon")
    logging.error("event starts too soon")

  def update_event(self, event, update):
    # scheduled_time = event.start_time - timedelta(minutes = 30)
    # self.scheduler.add_job(self.update_event_5min, 'date', run_date = scheduled_time, args=[event])
    #msg = self.gen_update_request_msg(event)
    logging.info("at 30 minutes prior to event")
    self.actor.isend(Message(msg = event, msg_type=Msg_type.REQUEST_ESTIMATE, sender = self.actor.rank, receiver = Dest.NAVIGATOR))

  # def gen_update_request_msg(self, event):
  #   msg = {"event_id": event.event_id,
  #       "prefernece": event.preference,
  #       "location": event.event_location}
  #   return msg
