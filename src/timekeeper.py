import logging
import sys
from apscheduler.schedulers.background import BackgroundScheduler



# self defined modules
from destination_enum import Dest
from msg_enum import Msg_type
from actor import Actor
from message import Message

class Timekeeper:
	def __init__(self):
		pass

	def run(rank, comm):
		a = Actor(rank, comm)
		t = Timekeeper()

		while True:
			msg = a.recv()

			if msg.msg_type == Msg_type.INITIALIZED:
				print("{} initialized".format(Dest(msg.sender).name))
			elif msg.msg_type == Msg_type.UPDATE_ESTIMATE:
				print("update estimate message received")
				print(msg.msg)
			elif msg.msg_type == Msg_type.UPDATE_WEATHER:
				print("received update weather")
				print(msg.msg)

			sys.stdout.flush()

		def set_up_job(self):
			pass

