import logging
import sys
from apscheduler.schedulers.background import BackgroundScheduler



# self defined modules
from destination_enum import Dest
from msg_enum import Msg_type
from actor import Actor
from message import Message
from event import Event

class Timekeeper:
  def __init__(self):
    self.next_event = None
    self.events = {}

  def run(rank, comm):
    a = Actor(rank, comm)
    t = Timekeeper()

    while True:
      msg = a.recv()

      if msg.msg_type == Msg_type.INITIALIZED:
        print("{} initialized".format(Dest(msg.sender).name))
      elif msg.msg_type == Msg_type.NEW_EVENT:
        self.events[msg.msg.event_id] = msg.msg
      elif msg.msg_type == Msg_type.UPDATE_ESTIMATE:
        if msg.msg['event_id'] in self.events:
          event = self.events[msg.msg['event_id']]
          event.estimate = 
          self.set_up_job()
      elif msg.msg_type == Msg_type.UPDATE_WEATHER:
        print("received update weather")
        print(msg.msg)

      sys.stdout.flush()

  def set_up_job(self, event):
    scheduler = BackgroundScheduler()
    scheduled_time = event.start_time - event.estimate * 2
    scheduler.add_job(self.update_event, 'date', run_date = scheduled_time, args=[event])
    print("set up down, will be executed {}".format(scheduled_time))
    sys.stdout.flush()
    scheduler.start()

  def update_event(self, event):
    print("I got this!!")
    print(event.__str__())
    sys.stdout.flush()

