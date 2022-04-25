import csv
try:
    import simplejson as json
except ImportError:
    import json
from flask import Flask,request,Response,render_template
import psycopg2

app = Flask(__name__)

@app.route('/')
def renderPage():
  return render_template("index.html")

@app.route('/preferences')
def preferences():
  con = psycopg2.connect(
            database = "postgres",
            user = "farnazzamiri",
            password = "pgadmin")
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
