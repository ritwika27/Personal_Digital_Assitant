import csv
try:
  import simplejson as json
except ImportError:
  import json
from flask import Flask,request,Response,render_template, redirect, url_for
import psycopg2
import sys
import time
import logging
from datetime import datetime, timezone, timedelta
import signal

# self defined modules
from actor import Actor
from message import Message
from msg_enum import Msg_type
from destination_enum import Dest
from location import Location
from event import Event

time_format = "%Y-%m-%dT%H:%M"

app = Flask(__name__)

# mpi
actor = None

# notifications from backend entities
pending_notifs = []
weather = {
  "updated": False,
  "content": tuple(),
}

# Open up DB connection
con = psycopg2.connect(
    #database = "postgres",
    #user = "farnazzamiri",
    #password = "pgadmin"
    database = "pda",
    user = "postgres",
    password = "pdapassword"
)

# user location info
user_lat = None
user_lon = None

def gen_new_event_msg(
    address,
    start_time,
    end_time,
    title,
    user_lat,
    user_lon,
    event_description,
    preference
    ):
  event_id = start_time.timestamp()
  location = Location(address = address)
  user_location = Location(lat = user_lat, lon=user_lon)

  e = Event(event_id, preference, None, location, user_location, start_time, end_time, title, event_description)

  return Message(msg = e, sender = actor.rank, msg_type = Msg_type.NEW_EVENT, receiver = Dest.SCHEDULER)


@app.route('/')
def renderPage():
  cur = con.cursor()
  cur.execute(f"""
        SELECT event_title, event_start_time, event_end_time, event_description, event_location, event_id
        FROM public."userData";
  """)
  events = cur.fetchall()
  cur.execute(f"""
        SELECT event_title, event_start_time, event_end_time, event_description, event_location, event_id
        FROM public."userData"
        WHERE event_start_time > now() AT TIME ZONE 'UTC'
        ORDER BY event_start_time
        FETCH FIRST ROW ONLY;
  """);
  upcoming = cur.fetchone()
  cur.close()

  # TODO: Swap cursor execution out for messages to/from pdacalendar
  # TODO: Plug in actual estimate from database
  def mapData(event):
    # Set to UTC
    start_time_withtz = event[1].replace(tzinfo=timezone.utc)
    end_time_withtz = event[2].replace(tzinfo=timezone.utc)

    # Localize to the local timezone (i.e. EST)
    start_time_withtz = start_time_withtz.astimezone()
    end_time_withtz = end_time_withtz.astimezone()

    return {
      "id": event[5],
      "name": event[0],
      "time": start_time_withtz.strftime("%d %b %Y %H:%M"),
      "end": end_time_withtz.strftime("%d %b %Y %H:%M"),
      "estimate": "soon-ish?",
      "duration": (event[2] - event[1]).total_seconds() / 60,
      "location": event[4],
      "desc": event[3]
    }
  eventData = list(map(mapData, events))
  upcomingData = mapData(upcoming)

  # TODO: Add weather of upcoming event to the item, probably via `upcomingData["weather"] = ???`
  #       Which could be a tuple or something i.e. ("link/to/weather/icon.jpg", "48-55deg", "30% Rain")

  return render_template("calendar.html", eventData=json.dumps(eventData), upcoming=upcomingData)

@app.route('/addEvent', methods=['GET', 'POST'])
def addEvent():
  if actor == None:
    print("running webserver independently, ignoring sending message")
    return redirect(url_for('renderPage'))

  start_utc = (
    datetime.fromisoformat(request.values['start'])
    .astimezone()
    .astimezone(timezone.utc)
  )
  end_utc = (
    datetime.fromisoformat(request.values['end'])
    .astimezone()
    .astimezone(timezone.utc)
  )
  sys.stdout.flush()

  actor.send(
      gen_new_event_msg(
          request.values['address'],
          start_utc,
          end_utc,
          request.values['title'],
          user_lat,
          user_lon,
          request.values['description'],
          'placeholder' #TODO: change to actual value
          ))

  return redirect(url_for('renderPage'))

@app.route('/updateEvent', methods=['GET', 'POST'])
def editEvent():
  print(request)
  return redirect(url_for('renderPage'))

@app.route('/deleteEvent', methods=['GET', 'POST'])
def deleteEvent():
  print(request)
  return redirect(url_for('renderPage'))

@app.route('/checkUpdates')
def checkUpdates():
  updates = dict()
  if actor:
    while actor.iprobe():
      msg = actor.recv()
      if msg.msg_type == Msg_type.UPDATE_ESTIMATE:
        pending_notifs.append(msg.msg['msg'])
        print("got update estimate messgae")
      else:
        # TODO: do something for weather
        print("got weather msg, ignoring")
        print(msg.msg.__str__())
  sys.stdout.flush()

  if len(pending_notifs) > 0:
    updates["notifs"] = {
      "notif": pending_notifs.pop(),
      "more": len(pending_notifs) > 0
    }
  else: updates["notifs"] = { "notif": "", "more": False }

  if weather["updated"]:
    updates["weather"] = weather.content;
    weather["updated"] = False

  return Response(json.dumps(updates), status=200, mimetype='application/json')

@app.route('/relayPosition', methods=['POST'])
def relayPosition():
  logging.debug("From user: lat: {}\tlon: {}".format(request.json['lat'], request.json['lon']))
  print("location updated")
  global user_lat
  global user_lon
  user_lat = request.json['lat']
  user_lon = request.json['lon']
  logging.info(
      "relay postion: lat: {}\tlon: {}".format(user_lat, user_lon))
  l = Location(lat = user_lat, lon = user_lon)
  l.coord_to_addr()
  m = Message(msg = l, msg_type=Msg_type.UPDATE_USER_LOCATION, sender=actor.rank, receiver=Dest.SCHEDULER)
  actor.broadcast(m)
  return Response(status=204)

@app.route('/preferences')
def preferences():
  cur = con.cursor()
  cur.execute(f"""
        SELECT *
        FROM
            public."userData";
        """)
  pref = cur.fetchall()
  cur.close()

  print(pref)
  sys.stdout.flush()
  data = json.dumps(pref, default=str)
  resp = Response(data, status=200, mimetype='application/json')
  msg = Message(msg = data, receiver = Dest.SCHEDULER, msg_type=Msg_type.NEW_EVENT, sender = actor.rank)
  actor.isend(msg)
  print(resp)
  return resp

if __name__ == "__main__":
  app.run(debug=True,port=8000)
  signal.signal(singal.SIGINT, lambda s, f: con.close())

def flaskrun(rank, comm):
  global actor
  actor = Actor(rank, comm)
  app.run(debug=False, port=8000)
