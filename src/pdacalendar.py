from __future__ import print_function

import datetime
import time
import sys
import os.path
from mpi4py import MPI
import requests
import logging
import json

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
        print("initializing")
        # c = Calendar()
        a = Actor(rank, comm)
        while True:
            print("hi")
            msg = a.recv()
            # print("i am " + str(rank) + " received message " + msg.msg["msg"] + " from " + str(msg.sender) + " tag: " + str(msg.msg_type) + " time: " + str(msg.msg["date"]))
            print("i am " + str(rank) + " received message " + str(msg.msg) + " from " + str(msg.sender) + " tag: " + str(msg.msg_type))
            sys.stdout.flush()
            # a.send(msg.reply(msg.msg, msg.msg_type))

            if msg.msg_type == Msg_type.NEW_EVENT:
                # geo lookup
                address = msg.msg['location'].address
                key = 'AIzaSyCp1gIoicaGeLz2JBxkL9Mb-fal9bEVLkI'
                r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, key)).json()
                logging.debug(r)
                msg.msg['location'].lat = r['results'][0]['geometry']['location']['lat']
                msg.msg['location'].lon = r['results'][0]['geometry']['location']['lng']
                logging.debug(msg.msg)
                print(msg.msg_type)
                # broadcasting new event
                # send to weatherman
                msg.get_msg_type = Msg_type.NEW_EVENT
                msg.sender = rank
                msg.receiver = Dest.WEATHERMAN
                print("hello6")
                a.send(msg)

                # send to navigator
                msg.sender = rank
                msg.receiver = Dest.NAVIGATOR
                a.send(msg)

                # send to TIMEKEEPER
                msg.sender = rank
                msg.receiver = Dest.TIMEKEEPER
                a.send(msg)

    def add_event(self, start_time, end_time):
        pass

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
