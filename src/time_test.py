
from datetime import datetime, timedelta

from timekeeper import Timekeeper
from event import Event
from location import Location
import time

t = Timekeeper()
l = Location()
e = Event(100, "car", l, l, datetime.now() + timedelta(minutes = 1), datetime.now() + timedelta(minutes = 20), "title", "desc")
e.estimate = timedelta(seconds = 10)

t.set_up_job(e)

try:
  while True:
    time.sleep(2)
except (KeyboardInterrupt, SystemExit):
  scheduler.shutdown()
