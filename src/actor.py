from mpi4py import MPI
from destination_enum import Dest
from message import Message
from msg_enum import Msg_type
import sys
import time
import logging


class Actor():
    def __init__(self, rank, comm):
        self.rank = rank
        self.comm = comm

    def isend(self, msg):
        logging.info("{} sending to {}, tag {}".format(Dest(self.rank).name, Dest(msg.receiver).name, Msg_type(msg.msg_type).name))
        logging.debug(msg.__str__())
        assert isinstance(msg, Message)
        self.comm.isend(msg.msg, dest=msg.receiver, tag=msg.msg_type)
        
    # broadcast msg to all destinations
    def broadcast(self, msg, exclude = []):
        r = msg.receiver
        for d in Dest:
            if d != self.rank and d not in exclude:
                msg.receiver = d
                self.isend(msg)
        msg.receiver = r


    # def send(msg, dest=dest, tag=tag)
    #     comm.send(msg, dest=dest, tag=tag)

    def send(self, msg):
        logging.info("{} sending to {}, tag {}".format(Dest(self.rank).name, Dest(msg.receiver).name, Msg_type(msg.msg_type).name))
        logging.debug(msg.__str__())
        assert isinstance(msg, Message)
        self.comm.send(msg.get_msg(), dest=msg.get_receiver(), tag=msg.get_msg_type())

    def irecv(self):
        self.comm.irecv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        return 

    def wait(self):
        status = MPI.Status()
        msg = self.comm.wait(status)
        tag = status.Get_tag()
        logging.info("{} received to {}, tag {}".format(Dest(self.rank).name, Dest(status.Get_source()).name, Msg_type(tag).name))
        logging.debug(msg.__str__())
        return Message(msg=msg, msg_type=tag, sender=status.Get_source(), receiver=self.rank)

    def recv(self):
        status = MPI.Status()
        msg = self.comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        tag = status.Get_tag()
        logging.info("{} received to {}, tag {}".format(Dest(self.rank).name, Dest(status.Get_source()).name, Msg_type(tag).name))
        logging.debug(msg.__str__())
        return Message(msg=msg, msg_type=tag, sender=status.Get_source(), receiver=self.rank)


