from Queue import PriorityQueue as pq
from event import Event

class EventList:
	def __init__(self ):
		self.event_queue = pq()

	def addEvent(self , event):
		self.event_queue.put(event)
	def getMin(self):
		return self.event_queue.get()
	def hasNext(self):
		return not self.event_queue.empty()
	def getSize(self):
		return self.event_queue.qsize()
	def seeMin(self):
		event = self.event_queue.get()
		self.event_queue.put(event)
		return event