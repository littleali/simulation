class Elevator:
	_ID = 0
	def __init__(self):
		self.id = self._ID 
		self.__class__._ID += 1
		self.location = 0
		self.passenger = []
		self.destination = 0
		self.capacity = 0
		self.speed = 0
		self.waiting_floors = []

	def get_id(self):
		return self.id

	def add_waiting_floor(self , _number):
		self.waiting_floors.append(_number)

	def remove_waiting_floor(self , _number):
		self.waiting_floors  = filter(lambda t: t != _number, self.waiting_floors)

	def set_capacity(self , _cap):
		self.capacity = _cap

	def set_speed(self , _speed):
		self.speed = _speed

	def get_speed(self ):
		return self.speed

	def get_capacity(self):
		return self.capacity

	def set_idle_floor(self , _idle):
		self.idle_floor = _idle

	def get_idle_floor(self):
		return self.idle_floor

	def has_space(self):
		return self.capacity > len(self.passenger) - 1

	def add_passenger(_id , _destination):
		self.passenger.append((_id , _destination ))

	def set_destination(self , _dest):
		self.destination = _dest

	def get_destination(self):
		self.destination

	def set_direction(self , _dir):
		sefl.direction = _dir

	def get_direction(self):
		return self.direction

	def get_location(self ):
		return self.location

	def update(self):

		# TODO generate stub to handle update in each second
		return 