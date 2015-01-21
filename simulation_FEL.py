from Queue import PriorityQueue as pq
import numpy as np
import math

NUMBER_OF_ELEVATOR = 3
CAPACITY_OF_EACH_ELEVATOR = 5
DURATION_OF_SIMULATION_IN_SECONDS = 50000
ARRIVAL_RATE_COLLECTION= [70.33 , 46.82 , 30.96]
MEAN_SERVICE_TIME = 31
MIN_SERVICE_TIME = 7
MAX_SERVICE_TIME = 140
SIGMA_SERVICE_TIME = 34.7

MEAN_WAITING_TIME = 23.84
MIN_WAITING_TIME = 0
MAX_WAITING_TIME = 103
SIGMA_WAITING_TIME = 25.68

NUMBER_OF_REPLICATION = 15





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


avg_waiting_time = []
avg_system_time = []
avg_service_time = []



class Simulation:
	def __init__(self ,  duration  ,  arrival_miu  ,  elevator_num):
		# this queue contains the Feuture Event List and at first populate with arrival times
		elevator_free_times = [] 
		for i in range(elevator_num):
			elevator_free_times.append(0)
		self.ARRIVAL = "arrival"
		self.DEPARTURE = "departure"
		self.ELEVATOR_ARRIVAL = "elevatorArrival"
		self.MAX_ELEVATOR_CAPACITY = CAPACITY_OF_EACH_ELEVATOR
		self.FEL = self.generateArrival(duration , arrival_miu)
		self.simulate(duration  ,  elevator_free_times)


	def generateArrival( seed , duration  , arrival):
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


	def simulate(self ,duration   , elevator_free_times):
		t = 0 
		arrivalTimes = {}
		enterTimes = {}
		departureTimes = {}
		waitingQueue = EventList()
		isKeyPressed = False
		while t < duration and self.FEL.hasNext():
			event = self.FEL.getMin()
			t = event.getTime()
			################### ARRIVAL 
			if event.getType() == self.ARRIVAL:
				if not isKeyPressed:
					time = t
					index = 0
					all_busy = True
					first_free_time = elevator_free_times[0]
					for idx ,  eft in enumerate(elevator_free_times):
						if eft < t:
							all_busy = False
							index = idx
							break
						if eft <= first_free_time :
							index = idx
						first_free_time = min(eft , first_free_time)

					if all_busy:
						time = first_free_time

					while True:
						temp = np.random.normal(MEAN_WAITING_TIME , SIGMA_WAITING_TIME)
						if temp > MIN_WAITING_TIME and temp < MAX_WAITING_TIME :
							time = time + temp
							break 
					elevatorEvent = Event(self.ELEVATOR_ARRIVAL , time , index )
					self.FEL.addEvent(elevatorEvent)
				waitingQueue.addEvent(event)
				arrivalTimes[event.getId()] = event.getTime()


			################## DEPARTURE
			elif event.getType() == self.DEPARTURE:
				departureTimes[event.getId()] = event.getTime()



			################## ELEVATOR ARRIVAL

			elif event.getType() == self.ELEVATOR_ARRIVAL:
				max_departure_time = 0 
				for i in range( 0  , self.MAX_ELEVATOR_CAPACITY):
					if waitingQueue.hasNext():
						tmp = waitingQueue.getMin()
						time = 0 
						while True:
							temp = np.random.normal(MEAN_SERVICE_TIME , SIGMA_SERVICE_TIME)
							if temp > MIN_SERVICE_TIME and temp < MAX_SERVICE_TIME:
								time = t + temp
								break 
						max_departure_time = max(max_departure_time , time)
						depEvent = Event(self.DEPARTURE , time  , tmp.getId())
						self.FEL.addEvent(depEvent)
						enterTimes[tmp.getId()] =  t
						isKeyPressed = False
				elevator_free_times[event.getId()] = max_departure_time

				if waitingQueue.hasNext():
					isKeyPressed = True
					time = t
					all_busy = True
					index = 0
					first_free_time = elevator_free_times[0]
					for idx ,  eft in enumerate(elevator_free_times):
						if eft < t:
							all_busy = False
							index = idx 
							break
						if eft <= first_free_time :
							index = idx
						first_free_time = min(eft , first_free_time)

					if all_busy:
						time = first_free_time

					while True:
						temp = np.random.normal(MEAN_WAITING_TIME , SIGMA_WAITING_TIME)
						if temp > MIN_WAITING_TIME and temp < MAX_WAITING_TIME:
							time = t + temp
							break 
					elevatorEvent = Event(self.ELEVATOR_ARRIVAL , time , index)
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

		print "\tMax system time :" , max_system_time
		print "\tMax service time :" , max_service_time
		print "\tMax waiting time :" , max_waiting_time

		print "\tMin system time :" , min_system_time
		print "\tMin service time :" , min_service_time
		print "\tMin waiting time :" , min_waiting_time
		# print waitingTimes
		# print systemTimes
		# print serviceTimes

		# print "arrival times :" , arrivalTimes
		# print "enter times :"  , enterTimes 
		# print "departure times :"  , departureTimes
		print "\tMean waiting times :" , np.mean(waitingTimes)
		print "\tMean system times :" , np.mean(systemTimes)
		print "\tMean service times :" , np.mean(serviceTimes)

		avg_service_time.append(np.mean(serviceTimes))
		avg_system_time.append(np.mean(systemTimes))
		avg_waiting_time.append(np.mean(waitingTimes))







for i in range(NUMBER_OF_REPLICATION) :
	print "<<<<<<<<<<<<<<<<<<<<<<<<<<<" ,i + 1 , "th simulation results", ">>>>>>>>>>>>>>>>>>>>>>>>>>>"
	simulation = Simulation(DURATION_OF_SIMULATION_IN_SECONDS  , ARRIVAL_RATE_COLLECTION 
		 , NUMBER_OF_ELEVATOR)

print "<<<<<<<<<<<<<<<<<<<<<<<<<<<" , "total results", ">>>>>>>>>>>>>>>>>>>>>>>>>>>"

print "\t\tTotal mean waiting times :" , np.mean(avg_waiting_time)
print "\t\tTotal mean system times :" , np.mean(avg_system_time)
print "\t\tTotal mean service times :" , np.mean(avg_service_time)


print "######## Total mean waiting times standad error is : ########" , math.sqrt(np.var(avg_waiting_time))/(NUMBER_OF_ELEVATOR - 1)
print "######## Total mean system times standard error is : ########" , math.sqrt(np.var(avg_system_time))/(NUMBER_OF_REPLICATION - 1)
print "######## Total mean service times standard error is : ########" , math.sqrt(np.var(avg_service_time))/(NUMBER_OF_REPLICATION -1)



