import csv
try:
    import simplejson as json
except ImportError:
    import json
from flask import Flask,request,Response,render_template, redirect, url_for
import psycopg2
import sys
import time
from datetime import datetime

# self defined modules
from actor import Actor
from message import Message
from msg_enum import Msg_type
from destination_enum import Dest
from location import Location

time_format = "%Y-%m-%dT%H:%M"

app = Flask(__name__)

# mpi
actor = None

# notifications from backend entities
pending_notifs = ["testing first notification"]

def gen_new_event_msg(address, start_time, end_time, title, user_lat, user_lon):
    event_id = int(time.time())
    location = Location(address = address)
    user_location = Location(lat = user_lat, lon=user_lon)
    msg = {'event_id': event_id,
           'location': location,
           'title': title,
           'start_time': datetime.strptime(start_time, time_format),
           'end_time': datetime.strptime(end_time, time_format),
           'user_location': user_location
           }
    return Message(msg = msg, sender = actor.rank, msg_type = Msg_type.NEW_EVENT, receiver = Dest.SCHEDULER)


@app.route('/')
def renderPage():
  return render_template("calendar.html")

@app.route('/addEvent', methods=['GET', 'POST'])
def addEvent():
  print(request)
  # print(datetime.strptime(request.values['start'], time_format))
  # TODO: change last None to actual location
  actor.isend(gen_new_event_msg(request.values['address'], request.values['start'], request.values['end'], request.values['title'], None, None))

  return redirect(url_for('renderPage'))

@app.route('/checkNotifs')
def checkNotifs():
  if len(pending_notifs) > 0:
    return {
        "notif": pending_notifs.pop(),
        "more": len(pending_notifs) > 0
    }
  else: return { "notif": "", "more": False }

@app.route('/relayPosition', methods=['POST'])
def relayPosition():
  print("lat:", request.json['lat'],
        "\nlon:", request.json['lon'])
  # TODO: Maybe save these? Or call some function for them?
  return Response(status=204)

@app.route('/preferences')
def preferences():
  sys.stdout.flush()
  con = psycopg2.connect(
            #database = "postgres",
            #user = "farnazzamiri",
            #password = "pgadmin"
            database = "pda",
            user = "postgres",
            password = "pdapassword"
            )
  cur = con.cursor()

  cur.execute(f"""
        SELECT *
        FROM
            public."userData";
        """)
  pref = cur.fetchall()

  cur.close()
  con.close()

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

def flaskrun(rank, comm):
    global actor
    actor = Actor(rank, comm)
    app.run(debug=False, port=8000)
