from mpi4py import MPI
from destination_enum import Dest
from message import Message
import sys
import time


class Actor():
    def __init__(self, rank, comm):
        self.rank = rank
        self.comm = comm

    def isend(self, msg):
        assert isinstance(msg, Message)
        comm.isend(msg.msg, dest=msg.dest, tag=msg.tag)

    # def send(msg, dest=dest, tag=tag)
    #     comm.send(msg, dest=dest, tag=tag)

    def send(self, msg):
        assert isinstance(msg, Message)
        print(msg.get_receiver())
        print(msg.get_msg_type())
        self.comm.send(msg.get_msg(), dest=msg.get_receiver(), tag=msg.get_msg_type())

    def irecv(self):
        self.comm.irecv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        return 

    def wait(self):
        status = MPI.Status()
        msg = self.comm.wait(status)
        tag = status.Get_tag()
        return Message(msg=msg, msg_type=tag, sender=satus.Get_source(), receiver=self.rank)

    def recv(self):
        status = MPI.Status()
        msg = self.comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        tag = status.Get_tag()
        return Message(msg=msg, msg_type=tag, sender=status.Get_source(), receiver=self.rank)


