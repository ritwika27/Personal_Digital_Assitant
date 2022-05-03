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
import signal

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

# Open up DB connection
con = psycopg2.connect(
    #database = "postgres",
    #user = "farnazzamiri",
    #password = "pgadmin"
    database = "pda",
    user = "postgres",
    password = "pdapassword"
)

def gen_new_event_msg(address, start_time, end_time, title):
  event_id = int(time.time())
  location = Location(address = address)
  msg = {'event_id': event_id,
         'location': location,
         'title': title,
         'start_time': datetime.strptime(start_time, time_format),
         'end_time': datetime.strptime(end_time, time_format)}
  return Message(msg = msg, sender = actor.rank, msg_type = Msg_type.NEW_EVENT, receiver = Dest.SCHEDULER)


@app.route('/')
def renderPage():
  return render_template("calendar.html")

@app.route('/addEvent', methods=['GET', 'POST'])
def addEvent():
  print(request)
  # print(datetime.strptime(request.values['start'], time_format))
  actor.isend(gen_new_event_msg(request.values['address'], request.values['start'], request.values['end'], request.values['title']))

  # TODO send message to calendar
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
