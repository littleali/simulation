import util
from event import Event
from eventlist import EventList
import numpy as np

class Floor:
	def __init__(self , _number ):
		self.num = _number
		self.rate = list(list(util.read_parameter("floors.parameter"))[self.num])
		print "boooogh 3 : " , list(str(util.read_parameter("floors.parameter")))


		self.endtime = int(util.read_parameter("simulation.endtime"))
		self.destination_distribution =list(util.read_parameter("floors.destination_distribution"))
		self.destination_distribution.pop(self.num)
		# self.waiting_upward

	def generate_events(self):
		## generating random interArrivalTimes
		elist = []
		interval = self.endtime / len(self.rate)
		t = float(0)
		while t < self.endtime:
			print " boogh 1 " , self.rate
			mu = self.rate[int(t/interval)]
			print " booooooooooooooogh " , mu
			t = np.random.exponential(mu) + t
			destination = self.generate_destination()
			direction = 1
			if destination  < self.num :
				direction = -1
			event = Event(t , direction , destination )
			elist.append(event)
		return elist

	def generate_destination(self):
		total = sum(float(w) for c, w in self.destination_distribution)
		r = random.uniform(0, total)
		upto = 0
		for c, w in choices:
		  if upto + float(w) > r:
		     return c
		  upto += float(w)