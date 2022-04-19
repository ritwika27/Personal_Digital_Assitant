#dummy file for message test purposes


from mpi4py import MPI
from msg_enum import Msg_type
from destination_enum import Dest
import sys
import time

class Dummy:
    def __init__(self):
        pass

    def run(rank, comm):
        d = Dummy()
        comm.isend(d.generate_location_msg(1, 12, 13), dest=Dest.SCHEDULER, tag=Msg_type.NEW_LOCATION)
        status = MPI.Status()
        while True:
            msg = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status = status)
            tag = status.Get_tag()
            print("i am " + str(rank) + " received message " + msg["msg"] + " from " + str(status.Get_source()) + " tag: " + str(tag))
            print(msg)
            sys.stdout.flush()
            time.sleep(5)
            msg["msg"] = "ping"
            comm.isend(msg, dest=Dest.SCHEDULER, tag=Msg_type.NEW_LOCATION)


    def generate_location_msg(self, event_id, latitude, longitude):
        return {"event_id": event_id, "latitude": latitude, "longitude": longitude, "msg": "ping"}
