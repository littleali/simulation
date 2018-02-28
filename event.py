class Event:
	_ID = 0
	def __init__(self , _time , _direction , _destination):
		self.id = self._ID 
		self.__class__._ID += 1
		self.time = _time
		self.direction = _direction
		self.destination = _destination
	def getTime(self):
		return self.time

	def getDestination(self):
		return self.destination





	def getId(self):
		return self.id

	def getDirection(self):
		return self.direction

	def __cmp__(self, other):
         return cmp(self.time, other.time)
