from mpi4py import MPI
from destination_enum import Dest
from message import Message
import sys
import time
import logging


class Actor():
    def __init__(self, rank, comm):
        self.rank = rank
        self.comm = comm

    def isend(self, msg):
        logging.info("{} sending to {}".format(self.rank, msg.receiver))
        logging.debug(msg)
        assert isinstance(msg, Message)
        self.comm.isend(msg.msg, dest=msg.receiver, tag=msg.msg_type)

    # def send(msg, dest=dest, tag=tag)
    #     comm.send(msg, dest=dest, tag=tag)

    def send(self, msg):
        logging.info("{} sending to {}".format(self.rank, msg.receiver))
        logging.debug(msg)
        assert isinstance(msg, Message)
        self.comm.send(msg.get_msg(), dest=msg.get_receiver(), tag=msg.get_msg_type())

    def irecv(self):
        self.comm.irecv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        return 

    def wait(self):
        status = MPI.Status()
        msg = self.comm.wait(status)
        tag = status.Get_tag()
        logging.info("{} received from {} tag {}".format(self.rank, msg.sender, tag))
        logging.debug(msg)
        return Message(msg=msg, msg_type=tag, sender=status.Get_source(), receiver=self.rank)

    def recv(self):
        status = MPI.Status()
        msg = self.comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        tag = status.Get_tag()
        logging.info("{} received from {} tag {}".format(self.rank, status.Get_source(), tag))
        logging.debug(msg)
        return Message(msg=msg, msg_type=tag, sender=status.Get_source(), receiver=self.rank)


