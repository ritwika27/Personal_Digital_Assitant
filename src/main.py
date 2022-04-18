from mpi4py import MPI
from dreamer_enum import Dreamer
from pdacalendar import Calendar

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == Dreamer.SCHEDULER:
    c = Calendar()
    c.run(rank, comm)
elif rank == Dreamer.WEATHERMAN:
    print("i am rank 1")
