from mpi4py import MPI
from destination_enum import Dest
from pdacalendar import Calendar
from dummy_process import Dummy
from weatherman import Weatherman

from server import *

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == Dest.SCHEDULER:
    # c = Calendar()
    Calendar.run(rank, comm)
elif rank == Dest.WEATHERMAN:
    # Dummy.run(rank, comm)
    Weatherman.run(rank, comm)
elif rank == Dest.WEB:
    flaskrun(rank, comm)

# elif rank == Dest.TIMEKEEPER:
    # Timekeeper.run(rank, comm)

