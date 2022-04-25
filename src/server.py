import csv
try:
    import simplejson as json
except ImportError:
    import json
from flask import Flask,request,Response,render_template
import psycopg2
import sys

# self defined modules
from actor import Actor
from message import Message
from msg_enum import Msg_type
from destination_enum import Dest


app = Flask(__name__)

# mpi
actor = None


@app.route('/')
def renderPage():
  print("response")
  return render_template("index.html")

@app.route('/preferences')
def preferences():
  print("in preferences")
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
  msg = Message(msg = data, receiver = Dest.SCHEDULER, msg_type=Msg_type.NEW_LOCATION, sender = actor.rank)
  actor.isend(msg)
  print(resp)
  return resp

if __name__ == "__main__":
  app.run(debug=True,port=8000)

def flaskrun(rank, comm):
    global actor
    actor = Actor(rank, comm)
    app.run(debug=False, port=8000)
