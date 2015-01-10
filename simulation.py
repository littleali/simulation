from Queue import PriorityQueue as pq
import numpy as np


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
	def __init__(self , seed , duration  , elevator_lambda , service_lambda , lambda_array):
		# this queue contains the Feuture Event List and at first populate with arrival times
		np.random.seed(seed)
		self.ARRIVAL = "arrival"
		self.DEPARTURE = "departure"
		self.ELEVATOR_ARRIVAL = "elevatorArrival"
		self.MAX_ELEVATOR_CAPACITY = 5
		self.FEL = self.generateArrival(seed , duration  , lambda_array)
		self.simulate(seed , duration , elevator_lambda , service_lambda)


	def generateArrival(self, seed , duration  , lambda_array):
		## generating random interArrivalTimes
		elist = EventList()
		interval = duration / len(lambda_array)
		t = 0 
		while t < duration:
			mu = lambda_array[int(t/interval)]
			t = np.random.exponential(mu) + t
			event = Event(self.ARRIVAL , t)
			elist.addEvent(event)
		return elist


	def simulate(self , seed , duration , elevator_lambda  , service_lambda):
		t = 0 
		arrivalTimes = []
		enterTimes = []
		departureTimes = []
		waitingQueue = EventList()
		isKeyPressed = False

		while t < duration and self.FEL.hasNext():
			event = self.FEL.getMin()
			t = event.getTime()
			if event.getType() == self.ARRIVAL:
				if not isKeyPressed:
					elevatorEvent = Event(self.ELEVATOR_ARRIVAL , t + np.random.exponential(elevator_lambda))
					self.FEL.addEvent(elevatorEvent)
				waitingQueue.addEvent(event)
				arrivalTimes.append(event.getTime())

			elif event.getType() == self.DEPARTURE:
				departureTimes.append(event.getTime())


			elif event.getType() == self.ELEVATOR_ARRIVAL:
				for i in range( 0  , self.MAX_ELEVATOR_CAPACITY):
					if waitingQueue.hasNext():
						tmp = waitingQueue.getMin()
						depEvent = Event(self.DEPARTURE , t + np.random.exponential(service_lambda))
						self.FEL.addEvent(depEvent)
						enterTimes.append(t)
						isKeyPressed = False
				if waitingQueue.hasNext():
					isKeyPressed = True
					elevatorEvent = Event(self.ELEVATOR_ARRIVAL , t + np.random.exponential(elevator_lambda))
					self.FEL.addEvent(elevatorEvent)	

		self.printResult(arrivalTimes , enterTimes , departureTimes )


	def printResult(self , arrivalTimes , enterTimes , departureTimes):
		serviceTimes= []
		systemTimes = []
		waitingTimes = []
		for i in range (len(departureTimes)):
			# print "result of " , i + 1 , " th person:"
			serviceTimes.append(departureTimes[i] - enterTimes[i])
			# print "serviceTime : " , serviceTimes[i]
			systemTimes.append(departureTimes[i] - arrivalTimes[i])
			# print "systemTime : " , systemTimes[i]
			waitingTimes.append(enterTimes[i] - arrivalTimes[i])
			# print "waitingTime : " , waitingTimes[i]


		# print "arrival times :" , arrivalTimes
		# print "enter times :"  , enterTimes 
		# print "departure times :"  , departureTimes
		# print "waiting times :" , waitingTimes
		# print "system times :" , systemTimes
		# print "service times :" , serviceTimes

		print "mean waiting times :" , np.mean(waitingTimes)
		print "mean service times :" , np.mean(serviceTimes)
		print "mean system times :" , np.mean(systemTimes)






simulation = Simulation(3 , 50  , 30 , 50 , [10 , 7 , 5 , 9])





