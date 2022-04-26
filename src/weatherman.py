from mpi4py import MPI
from msg_enum import Msg_type
from destination_enum import Dest
import sys
import time
from datetime import datetime
from actor import Actor
from message import Message
from weather_collection import *

# test (lat, lon) values
gl_lat = 35
gl_lon = -85

class Weatherman:
    def __init__(self):
      self.events = {}
        
    def generate_intialized_msg(self, event_id):
        return {"event_id": event_id, "msg": "weatherman_intialized", "date": datetime.now()}
    def generate_weather_msg(self, event_id, temp, humidity, wind_speed):
        return {"event_id": event_id, "temp": temp, "humidity(%)": humidity, "wind_speed": wind_speed, "msg": "weather_info", "date": datetime.now()}

    def calculate_delay(loc):
        #TODO use location object to create a new estimate based on update hourly data
        pass

    def run(rank, comm):
        w = Weatherman()
        a = Actor(rank, comm)
        m = Message(msg = w.generate_intialized_msg(2), receiver = Dest.TIMEKEEPER, msg_type=Msg_type.INITIALIZED, sender = rank)
        a.send(m)
        i = 0
        while True:
            msg = a.recv()
            tag = msg.get_msg_type()
            # print(tag)
            # print("i am " + str(rank) + " received message " + str(msg.msg) + " from " + str(msg.sender) + " tag: " + str(msg.msg_type))

            if tag == Msg_type.NEW_EVENT:
                event_id = msg.msg["event_id"]
                w.events[event_id] = [msg.msg["title"], msg.msg["location"], msg.msg["start_time"], msg.msg["end_time"]]
                
                curr_weather = get_current_weather_info(msg.msg["location"].lat, msg.msg["location"].lon, msg.msg["start_time"] )
                #curr_weather = get_current_weather_info(gl_lat, gl_lon)
                w_msg = w.generate_weather_msg(0, curr_weather[0], curr_weather[1], curr_weather[2])
                weather_msg = Message(msg = w_msg, receiver = Dest.TIMEKEEPER, msg_type=Msg_type.UPDATE_WEATHER, sender = rank )
                a.send(weather_msg)

                #TODO: create triggers 

            elif tag == Msg_type.UPDATE_ESTIMATE:
                #TODO: get updates on weather based on time info
                pass

            sys.stdout.flush()
            time.sleep(1)
            

            # msg.msg["msg"] = "ping"
            # if i < 2:
            #     a.send(msg.reply(msg.msg, msg.msg_type))
            # i = i + 1



