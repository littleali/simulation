from Queue import PriorityQueue as pq
import numpy as np

class Event:
	
	def __init__(self , eventType , time , person_id):
		self.id = person_id
		self.time = time
		self.eventType = eventType
	def getTime(self):
		return self.time
	def getType(self):
		return self.eventType
	def __cmp__(self, other):
         return cmp(self.time, other.time)
	def getId(self):
		return self.id




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

# =================
# this code check correctness of Event and EventList
# =================
# first = Event("arrival1" , 2.5)
# second = Event("arrival" , 2.6)
# elist = EventList()
# elist.addEvent(second)
# elist.addEvent(first)

# while elist.hasNext():
# 	print elist.getSize()
# 	print elist.getMin().getType()


class Simulation:
	def __init__(self , seed , duration  ,  arrival_miu ,elevator_miu , elevator_sigma):
		# this queue contains the Feuture Event List and at first populate with arrival times
		np.random.seed(seed)
		self.ARRIVAL = "arrival"
		self.DEPARTURE = "departure"
		self.ELEVATOR_ARRIVAL = "elevatorArrival"
		self.MAX_ELEVATOR_CAPACITY = 5
		self.FEL = self.generateArrival(seed , duration , arrival_miu)
		self.simulate(seed , duration , elevator_miu , arrival_miu , elevator_sigma)


	def generateArrival(self, seed , duration  , arrival):
		## generating random interArrivalTimes
		elist = EventList()
		t = 0 
		counter = 0
		batch = duration / len(arrival)
		top = 0 
		for i in range( len(arrival)):
			while t < top + batch:
				mu = arrival[i]
				t = np.random.exponential(mu) + t
				counter += 1
				event = Event("arrival" , t , counter)
				elist.addEvent(event)
			top = top + duration
		return elist


	def simulate(self , seed , duration , elevator_miu  , arrival_miu , elevator_sigma):
		t = 0 
		arrivalTimes = {}
		enterTimes = {}
		departureTimes = {}
		waitingQueue = EventList()
		isKeyPressed = False
		while t < duration and self.FEL.hasNext():
			event = self.FEL.getMin()
			t = event.getTime()
			if event.getType() == self.ARRIVAL:
				if not isKeyPressed:
					time = 0 
					while True:
						temp = np.random.normal(elevator_miu , elevator_sigma)
						if temp > elevator_miu - elevator_sigma:
							time = t + temp
							break 
					elevatorEvent = Event(self.ELEVATOR_ARRIVAL , time , -1 )
					self.FEL.addEvent(elevatorEvent)
				waitingQueue.addEvent(event)
				arrivalTimes[event.getId()] = event.getTime()

			elif event.getType() == self.DEPARTURE:
				departureTimes[event.getId()] = event.getTime()


			elif event.getType() == self.ELEVATOR_ARRIVAL:
				for i in range( 0  , self.MAX_ELEVATOR_CAPACITY):
					if waitingQueue.hasNext():
						tmp = waitingQueue.getMin()
						time = 0 
						while True:
							temp = np.random.normal(elevator_miu , elevator_sigma)
							if temp > elevator_miu - elevator_sigma:
								time = t + temp
								break 
						depEvent = Event(self.DEPARTURE , time  , tmp.getId())
						self.FEL.addEvent(depEvent)
						enterTimes[tmp.getId()] =  t
						isKeyPressed = False
				if waitingQueue.hasNext():
					isKeyPressed = True
					time = 0 
					while True:
						temp = np.random.normal(elevator_miu , elevator_sigma)
						if temp > elevator_miu - elevator_sigma:
							time = t + temp
							break 
					elevatorEvent = Event(self.ELEVATOR_ARRIVAL , time , -1)
					self.FEL.addEvent(elevatorEvent)	

		self.printResult(arrivalTimes , enterTimes , departureTimes )


	def printResult(self , arrivalTimes , enterTimes , departureTimes):
		serviceTimes= []
		systemTimes = []
		waitingTimes = []
		max_waiting_time = 0
		max_service_time = 0
		max_system_time = 0
		min_waiting_time = 1000000
		min_service_time = 1000000
		min_system_time = 1000000
		for i in range (1 , len(departureTimes)):
			# print "result of " , i + 1 , " th person:"
			if i in departureTimes and i in enterTimes and i in arrivalTimes:
				serviceTimes.append(departureTimes[i] - enterTimes[i])
				max_service_time =  max(max_service_time , departureTimes[i] - enterTimes[i])
				min_service_time =  min(min_service_time , departureTimes[i] - enterTimes[i])
				# print "serviceTime : " , serviceTimes[i]
				systemTimes.append(departureTimes[i] - arrivalTimes[i])
				max_system_time = max(max_system_time , departureTimes[i] - arrivalTimes[i])
				min_system_time = min(min_system_time , departureTimes[i] - arrivalTimes[i])
				# print "systemTime : " , systemTimes[i]
				waitingTimes.append(enterTimes[i] - arrivalTimes[i])
				max_waiting_time = max(max_waiting_time , enterTimes[i] - arrivalTimes[i])
				min_waiting_time = min(min_waiting_time , enterTimes[i] - arrivalTimes[i])
				# print "waitingTime : " , waitingTimes[i]

		print "max system time :" , max_system_time
		print "max service time :" , max_service_time
		print "max waiting time :" , max_waiting_time

		print "min system time :" , min_system_time
		print "min service time :" , min_service_time
		print "min waiting time :" , min_waiting_time
		# print waitingTimes
		# print systemTimes
		# print serviceTimes

		# print "arrival times :" , arrivalTimes
		# print "enter times :"  , enterTimes 
		# print "departure times :"  , departureTimes
		print "waiting times :" , np.mean(waitingTimes)
		print "system times :" , np.mean(systemTimes)
		print "service times :" , np.mean(serviceTimes)








simulation = Simulation(2 , 50000  , [40 , 20 , 60] , 60 , 20)





