from mpi4py import MPI
from destination_enum import Dest
import sys
import time


class Actor():
    def __init__(self, rank, comm):
        self.rank = rank
        self.comm = comm

    def isend(msg, dest, tag):
        comm.isend(msg, dest=dest, tag=tag)

    def send(msg, desk=desk, tag=tag)
        comm.send(msg, dest=dest, tag=tag)

    def irecv():
        status = MPI.Status()
        msg = self.comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        tag = status.Get_tag()
        return 
