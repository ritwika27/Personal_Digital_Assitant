#dummy file for message test purposes


from mpi4py import MPI
from msg_enum import Msg_type
from destination_enum import Dest
import sys
import time
from datetime import datetime
from actor import Actor
from message import Message
import requests

api_file = open("APIkey.txt", "r")
api_key = api_file.read()
api_file.close()

url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"

user_location = "paint branch dr"

class Navigator:
    def __init__(self):
      self.locations = {}
        
    def generate_intialized_msg(self, event_id):
        return {"event_id": event_id, "msg": "navigator_intialized", "date": datetime.now()}
    def generate_navigator_msg(self, event_id, travel_time):
        return {"event_id": event_id, "travel_time": travel_time, "msg": "navigator_info", "date": datetime.now()}


    def run(rank, comm):
        n = Navigator()
        a = Actor(rank, comm)
        m = Message(msg = n.generate_intialized_msg(2), receiver = Dest.SCHEDULER, msg_type=Msg_type.INITIALIZED, sender = rank)
        a.send(m)
        i = 0
        
        while True:
            msg = a.recv()

            tag = msg.get_msg_type()
            print("i am " + str(rank) + " received message " + msg.msg["msg"] + " from " + str(msg.get_sender()) + " tag: " + str(tag))
            print(msg.msg)

            if tag == Msg_type.REQUEST_ESTIMATE:
                r = requests.get(url + "origins=" + user_location + "&destinations=" + msg["location"] + "&key=" + api_key)
                # print(r.json())
                time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
                event_id = msg["event_id"]
                n_msg = n.generate_navigator_msg(event_id, time)
                navigator_msg = Message(msg = n_msg, receiver = Dest.SCHEDULER, msg_type=Msg_type.UPDATE_ESTIMATE, sender = rank )
                a.send(navigator_msg)

                sys.stdout.flush()
                time.sleep(1) 

                # msg.msg["msg"] = "ping"
                # if i < 2:
                #     a.send(msg.reply(msg.msg, msg.msg_type))
                # i = i + 1

