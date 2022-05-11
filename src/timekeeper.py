import logging
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, timezone
import time



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
      elif msg.msg_type == Msg_type.DELETE_EVENT:
        # remove this event from scheduler
        event_id = msg.msg
        if event_id in t.events:
          event = t.events[msg.msg]
          if event.job:
            event.job.remove()
          del t.events[event_id]
      sys.stdout.flush()

  def set_up_job(self, event):
    estimate_departure_time = event.start_time - event.estimate
    print("event start time {}".format(event.start_time))
    scheduled_time = max(event.start_time - event.estimate * 2,
                        (event.start_time - event.estimate) - ((event.start_time - event.estimate) - datetime.now().astimezone())/2)
    print("scheduled time {}".format(scheduled_time))
    if scheduled_time >= event.start_time:
      self.invalid_event(event)
      return
    if scheduled_time - estimate_departure_time <= timedelta(minutes = 10):
      self.notify_user(event) 
      event.job = self.scheduler.add_job(self.event_expire, 'date', run_date = event.start_time, args=[event])
    elif scheduled_time - estimate_departure_time <= timedelta(minutes = 30):
      scheduled_time = estimate_departure_time - timedelta(minutes = 10)
      event.job = self.scheduler.add_job(self.update_event, 'date', run_date = scheduled_time, args=[event])
    else:
      event.job = self.scheduler.add_job(self.update_event, 'date', run_date = scheduled_time, args=[event])
    logging.info("set up done, will be executed {}".format(scheduled_time))

  def notify_user(self, event):
    leave_msg = "You should leave for {}\t that starts at {}\t. The estimated travel time is {}\t".format(
      event.title, str(event.start_time), str(event.estimate))
    msg = Message(msg = {'estimate': event.estimate, 'msg': leave_msg}, msg_type = Msg_type.UPDATE_ESTIMATE, sender = self.actor.rank, receiver = Dest.WEB)
    self.actor.isend(msg)

  def invalid_event(self, event):
    #TODO: handle this case
    print("ERROR: event starts too soon")
    logging.error("event starts too soon")

  def event_expire(self, event):
    self.actor.broadcast(Message(msg = event.event_id, sender = self.actor.rank, receiver = Dest.SCHEDULER, msg_type = Msg_type.EVENT_EXPIRED), [Dest.WEB])
    event.job = None
    if event.event_id in self.events:
      del self.events[event.event_id]

  def update_event(self, event, update):
    # scheduled_time = event.start_time - timedelta(minutes = 30)
    # self.scheduler.add_job(self.update_event_5min, 'date', run_date = scheduled_time, args=[event])
    #msg = self.gen_update_request_msg(event)
    logging.info("at {} minutes prior to event", event.estimate)
    self.actor.isend(Message(msg = event, msg_type=Msg_type.REQUEST_ESTIMATE, sender = self.actor.rank, receiver = Dest.NAVIGATOR))

  # def gen_update_request_msg(self, event):
  #   msg = {"event_id": event.event_id,
  #       "prefernece": event.preference,
  #       "location": event.event_location}
  #   return msg
