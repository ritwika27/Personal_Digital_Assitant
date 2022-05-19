from mpi4py import MPI
import logging

from destination_enum import Dest
from pdacalendar import Calendar
from dummy_process import Dummy
from weatherman import Weatherman
from timekeeper import Timekeeper
from navigator import Navigator


from server import *

comm = MPI.COMM_WORLD
rank = comm.Get_rank()


logging.basicConfig(filename="var/logger_{}.log".format(Dest(rank).name), level=logging.DEBUG)


count = 0

while count < 5:
  try:
    if rank == Dest.SCHEDULER:
      Calendar.run(rank, comm)
    elif rank == Dest.WEATHERMAN:
      Weatherman.run(rank, comm)
    elif rank == Dest.WEB:
      flaskrun(rank, comm)
    elif rank == Dest.TIMEKEEPER:
      Timekeeper.run(rank, comm)
    elif rank == Dest.NAVIGATOR:
      Navigator.run(rank, comm)
  except:
    count = count + 1

