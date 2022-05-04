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

# google related modules
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


api_file = open("APIkey.txt", "r")
api_key = api_file.read()
api_file.close()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Calendar:
    def __init__(self):
        pass
        # self.creds = None
        # # The file token.json stores the user's access and refresh tokens, and is
        # # created automatically when the authorization flow completes for the first
        # # time.
        # if os.path.exists('token.json'):
        #     self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # # If there are no (valid) credentials available, let the user log in.
        # if not self.creds or not self.creds.valid:
        #     if self.creds and self.creds.expired and self.creds.refresh_token:
        #         self.creds.refresh(Request())
        #     else:
        #         flow = InstalledAppFlow.from_client_secrets_file(
        #                 'credentials.json', SCOPES)
        #         self.creds = flow.run_local_server(port=0)
        #     # Save the credentials for the next run
        #     with open('token.json', 'w') as token:
        #         token.write(self.creds.to_json())

    def run(rank, comm):
        c = Calendar()
        a = Actor(rank, comm)
        a.send(Message(msg=0, sender = rank, receiver = Dest.TIMEKEEPER, msg_type=Msg_type.INITIALIZED))
        while True:
            msg = a.recv()
            # print("i am " + str(rank) + " received message " + msg.msg["msg"] + " from " + str(msg.sender) + " tag: " + str(msg.msg_type) + " time: " + str(msg.msg["date"]))
            print("i am " + str(rank) + " received message " + str(msg.msg) + " from " + str(msg.sender) + " tag: " + str(msg.msg_type))
            sys.stdout.flush()
            # a.send(msg.reply(msg.msg, msg.msg_type))

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
                        "placeholder", #user_location
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
            event_date, 
            event_description):
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
                    INSERT INTO public."userData"(event_id, preferences, user_location, user_lat, user_long, event_location, event_lat, event_long, 
                                                event_start_time, event_end_time, event_date, event_description)
                    VALUES ({event_id}, '{preferences}', '{user_location}', {user_lat}, {user_long}, '{event_location}', {event_lat}, {event_long}, 
                                        '{event_start_time}', '{event_end_time}', '{event_date}', '{event_description}');
                    """)
            #   pref = cur.fetchall()
            con.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()
# add_event(3, 'bus', 'Tuckerman Ln', 39.0368225, -77.1363598, 'College park', 38.9902899, -76.9356509, '9:30:00', '10:30:00', '05-22-2022', 'work meeting')
        
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
                    WHERE user_id = {event_id}
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

    def sync(self):
        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                    maxResults=10, singleEvents=True,
                    orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
        except HttpError as error:
            print('An error occurred: %s' % error)


    def test(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                    maxResults=10, singleEvents=True,
                    orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)
