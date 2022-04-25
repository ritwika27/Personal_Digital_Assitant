import csv
try:
    import simplejson as json
except ImportError:
    import json
from flask import Flask,request,Response,render_template, redirect, url_for
import psycopg2

app = Flask(__name__)

@app.route('/')
def renderPage():
  return render_template("calendar.html")

@app.route('/addEvent', methods=['GET', 'POST'])
def addEvent():
  print(request)
  return redirect(url_for('renderPage'))

@app.route('/preferences')
def preferences():
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
  data = json.dumps(pref, default=str)
  resp = Response(data, status=200, mimetype='application/json')
  print(resp)
  return resp

if __name__ == "__main__":
  app.run(debug=True,port=8000)

def flaskrun(rank, comm):
    app.run(debug=True, port=8000)
