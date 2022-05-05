from __future__ import print_function

import datetime
import time
import sys
import os.path
from mpi4py import MPI
import requests
import logging
import json

import psycopg2

# self defined modules
from destination_enum import Dest
from msg_enum import Msg_type
from actor import Actor
from message import Message

# # google related modules
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError


api_file = open("APIkey.txt", "r")
api_key = api_file.read()
api_file.close()


class Calendar:
	def __init__(self):
		self.user_location = None

	def run(rank, comm):
		c = Calendar()
		a = Actor(rank, comm)
		a.send(Message(msg=0, sender = rank, receiver = Dest.TIMEKEEPER, msg_type=Msg_type.INITIALIZED))
		while True:
			msg = a.recv()
			# print("i am " + str(rank) + " received message " + msg.msg["msg"] + " from " + str(msg.sender) + " tag: " + str(msg.msg_type) + " time: " + str(msg.msg["date"]))
			print("i am " + str(rank) + " received message " + str(msg.msg) + " from " + str(msg.sender) + " tag: " + str(msg.msg_type))
			sys.stdout.flush()

			if msg.msg_type == Msg_type.NEW_EVENT:
				# geo lookup
				address = msg.msg['location'].address
				r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, api_key)).json()
				logging.debug(r)
				msg.msg['location'].lat = r['results'][0]['geometry']['location']['lat']
				msg.msg['location'].lon = r['results'][0]['geometry']['location']['lng']
				logging.debug(msg.msg)

				# add event into database before forwarding message to other modules
				# assuming those should not be None
				# TODO fix it
				c.add_event(msg.msg['event_id'], 
								"placeholder", #preferences
								msg.msg['user_location'].address, 
								msg.msg['user_location'].lat, 
								msg.msg['user_location'].lon,
								msg.msg['location'].address,
								msg.msg['location'].lat,
								msg.msg['location'].lon,
								msg.msg['start_time'],
								msg.msg['end_time'],
								"01/01/2000", #fake date TODO: remove it
								msg.msg['event_description']
								)

				msg.sender = rank
				# broadcasting new event
				a.broadcast(m, exclude=[Dest.WEB])
		elif msg.msg_type == Msg_type.UPDATE_USER_LOCATION:
				c.user_location = msg.msg

	def add_event(self, 
			event_id, 
			preferences, 
			user_location, 
			user_lat, 
			user_long, 
			event_location, 
			event_lat, 
			event_long, 
			event_start_time, 
			event_end_time, 
			event_title, 
			event_description,
			event_passed):
		try:
			con = psycopg2.connect(
					database = "pda",
					user = "postgres",
					password = "pdapassword"
					# database = "postgres",
					# user = "farnazzamiri",
					# password = "pgadmin"
					)
			print(con)
			cur = con.cursor()

			cur.execute(f"""
			INSERT INTO public."userData"(event_id, preferences, user_location, user_lat, user_long, event_location, event_lat, event_long, event_start_time, 
			event_end_time, event_title, event_description, event_passed) 
			VALUES ({event_id}, '{preferences}', '{user_location}', {user_lat}, {user_long}, '{event_location}', {event_lat}, {event_long}, 
			'{event_start_time}', '{event_end_time}', '{event_title}', '{event_description}', '{event_passed}'); 
			""")
			#   pref = cur.fetchall()
			con.commit()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if con is not None:
				con.close()
		# add_event(1, 'bus', 'democracy blvd', 39.022797, -77.151316, 'college park', 38.991385, -76.937700, '2022-06-11 11:00:00', '2022-06-11 12:00:00', 'work', 'asadasdasd', 0)
        
	def update_event(column_name, column_value, event_id):
		try:
			con = psycopg2.connect(
					database = "pda",
					user = "postgres",
					password = "pdapassword"
					# database = "postgres",
					# user = "farnazzamiri",
					# password = "pgadmin"
					)
			print(con)
			cur = con.cursor()

			cur.execute(f"""
				UPDATE public."userData"
				SET {column_name} = '{column_value}'
				WHERE event_id = {event_id}
				""")
			#   pref = cur.fetchall()
			con.commit()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if con is not None:
				con.close()
		# update_event('user_location', 'Old georgetown Rd', 3)

    def get_closest_event():
			try:
				con = psycopg2.connect(
						database = "pda",
						user = "postgres",
						password = "pdapassword"
						# database = "postgres",
						# user = "farnazzamiri",
						# password = "pgadmin"
						)
				print(con)
				cur = con.cursor()

				cur.execute(f"""
					SELECT *
					FROM public."userData"
					ORDER BY event_passed DESC, event_start_time
					FETCH FIRST ROW ONLY;
				""")
				ev = cur.fetchall()
				con.commit()
				cur.close()
			except (Exception, psycopg2.DatabaseError) as error:
				print(error)
			finally:
				if con is not None:
					con.close()
					data = json.dumps(ev, default=str)
					print(data)

		# ev and data return the closest event

		def delete_event(self, event_id):
			try:
				con = psycopg2.connect(
						database = "pda",
						user = "postgres",
						password = "pdapassword"
						# database = "postgres",
						# user = "farnazzamiri",
						# password = "pgadmin"
						)
				print(con)
				cur = con.cursor()

				cur.execute(f"""
					DELETE FROM public."userData"
					WHERE event_id = {event_id}; 
					""")
				con.commit()
				cur.close()
			except (Exception, psycopg2.DatabaseError) as error:
				print(error)
			finally:
				if con is not None:
					con.close()

		def search_by_start_time_range(self, rangeStart, rangeEnd):
			try:
				con = psycopg2.connect(
						database = "pda",
						user = "postgres",
						password = "pdapassword"
						# database = "postgres",
						# user = "farnazzamiri",
						# password = "pgadmin"
						)
				print(con)
				cur = con.cursor()

				cur.execute(f""" 
					SELECT * 
					FROM public."userData" 
					WHERE event_start_time 
					BETWEEN '{rangeStart}' AND '{rangeEnd}';
				""")
				ev = cur.fetchall()
				con.commit()
				cur.close()
			except (Exception, psycopg2.DatabaseError) as error:
				print(error)
			finally:
				if con is not None:
					con.close()
					data = json.dumps(ev, default=str)
					print(data)
			# search_by_start_time_range('2022-06-11 11:00:00', '2022-06-11 12:00:00')

		def get_previous_event_id(self, event_start_time):
			try:
				con = psycopg2.connect(
						database = "pda",
						user = "postgres",
						password = "pdapassword"
						# database = "postgres",
						# user = "farnazzamiri",
						# password = "pgadmin"
						)
				print(con)
				cur = con.cursor()

				cur.execute(f"""
					WITH cte AS (
					SELECT
					event_id, preferences, user_location, user_lat, user_long,
					event_location, event_lat, event_long, event_start_time,
					event_end_time, event_title, event_description, event_passed,
					LAG(event_id,1) OVER (
					ORDER BY event_start_time) previous_event_id,
					LAG(event_start_time,1) OVER (
					ORDER BY event_start_time) previous_event_start_time
					FROM public."userData"
					)
					SELECT previous_event_id FROM cte WHERE event_start_time = '{event_start_time}';
				""")
				ev = cur.fetchall()
				con.commit()
				cur.close()
			except (Exception, psycopg2.DatabaseError) as error:
				print(error)
			finally:
				if con is not None:
					con.close()
					data = json.dumps(ev, default=str)
					print(data)

				# This function inputs an event start time and outputs the event id of the previous event
				# get_previous_event_id('2022-06-11 14:00:00')

