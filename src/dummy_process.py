#dummy file for message test purposes


from mpi4py import MPI
from msg_enum import Msg_type
from destination_enum import Dest
import sys
import time
from datetime import datetime
from actor import Actor
from message import Message


class Dummy:
    def __init__(self):
        pass

    def run(rank, comm):
        d = Dummy()
        a = Actor(rank, comm)
        m = Message(msg = d.generate_location_msg(1, 12, 13), receiver = Dest.SCHEDULER, msg_type=Msg_type.NEW_LOCATION, sender = rank)
        a.send(m)
        i = 0
        
        while True:
            msg = a.recv()

            tag = msg.get_msg_type()
            print("i am " + str(rank) + " received message " + msg.msg["msg"] + " from " + str(msg.get_sender()) + " tag: " + str(tag))
            print(msg.msg)
            sys.stdout.flush()
            time.sleep(1)
            msg.msg["msg"] = "ping"
            

            if i < 2:
                a.send(msg.reply(msg.msg, msg.msg_type))
            i = i + 1


    def generate_location_msg(self, event_id, latitude, longitude):
        return {"event_id": event_id, "latitude": latitude, "longitude": longitude, "msg": "ping", "date": datetime.now()}
