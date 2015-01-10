import util
from floor import Floor
from event import Event
from eventlist import EventList
from elevator import Elevator


class Singleton(object):
  _instances = {}
  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
        class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
    return class_._instances[class_]


class Building(Singleton):
	pass
	def __init__(self):
		print "booogh"
		self.floors = []
		self.elevators = []
		self.time = 0
		for i in range (int(util.read_parameter("floors.number"))):
			self.floors.append(Floor(i))
			util.log("Floor " + str(i) + "created")
		for i in range (int(util.read_parameter("elevators.number"))):
			capacities = (list(util.read_parameter("elevators.capacity")))
			idle_floors = (list(util.read_parameter("elevators.idle_floor")))
			speeds = (list(util.read_parameter("elevators.speed")))
			elv = Elevator()
			elv.set_capacity(capacities[i])
			elv.set_idle_floor(idle_floors[i])
			elv.set_speed(speeds[i])
			self.elevators.append(elv)
			util.log("Elevator " + str(i) + "created")
		self.eventList = EventList
		for floor in self.floors:
			for event in floor.generate_events():
				self.eventList.addEvent(event)

	def update():
		# while self.eventList.seeMin().getTime() == self.time :
			 
		# #updates the state of bulding for next second
		# self.time = self.time + 1
		return 

print "before"
b = Building()
print "end"

print "2before"
d = Building()
print "2end"
