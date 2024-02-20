import pandas
import datetime
import numpy
import re
import threading

"""
Just an AI I created based on the simple definition of nodes and weights
This AI was more accurate when using a multiplier method vs just adding the weights
Still it was a fun learning project, may return this to the multiplier method
or just rewrite it with keras
"""

class NeuralNetwork():
	def __init__(self):
		self.dataTable = None
		weightsArray = []
		determinatesArray = []
		valuesArray = []
		inputsArray = []
		statesArray = []
		self.dayOfTheWeekNeurons = self.setUpNeurons(1, 5, True)
		self.dayOfTheMonthNeurons = self.setUpNeurons(1, 31, False)
		self.weekOfTheMonthNeurons = self.setUpNeurons(1, 5, True)
		self.weekOfTheYearNeurons = self.setUpNeurons(1, 52, True)
		self.monthOfTheYearNeurons = self.setUpNeurons(1, 12, False)
		self.previousCloseNeurons = self.setUpNeurons(.01, 100001, True)
		self.previousHighNeurons = 	self.setUpNeurons(.01, 100001, True)
		self.previousLowNeurons = self.setUpNeurons(.01, 100001, True)
		self.previousOpenNeurons = self.setUpNeurons(.01,100001, True)
		self.previousOpenHighNeurons = self.setUpNeurons(.01, 2501, True)
		self.previousOpenLowNeurons = self.setUpNeurons(.01, 2501, True)
		self.previousCloseHighNeurons = self.setUpNeurons(.01, 2501, True)
		self.previousCloseLowNeurons = self.setUpNeurons(.01, 2501, True)
		self.previousOpenCloseNeurons = self.setUpNeurons(.01, 2501, True)
		self.previousVolumeNeurons = self.setUpNeurons(10000, 100001, True)
		self.avgCloseHighNeurons = self.setUpNeurons(.01, 2501, True)
		self.avgCloseLowNeurons = self.setUpNeurons(.01, 2501, True)
		self.avgCloseNeurons = self.setUpNeurons(.01, 100001, True)
		self.avgHighNeurons = self.setUpNeurons(.01, 100001, True)
		self.avgLowNeurons = self.setUpNeurons(.01, 100001, True)
		self.avgOpenHighNeurons = self.setUpNeurons(.01, 2501, True)
		self.avgOpenLowNeurons = self.setUpNeurons(.01, 2501, True)
		self.avgOpenNeurons = self.setUpNeurons(.01, 100001, True)
		self.avgVolumeNeurons = self.setUpNeurons(10000, 100001, True)
		self.recentDownsNeurons = self.setUpNeurons(1, 121, True)
		self.recentUpsNeurons = self.setUpNeurons(1, 121, True)
		
		#dictionary for simplifying the training/prediction functions
		self.neuronDict = {
			#set of neurons for a key
			"self.avgLowNeurons" : {
				#input tells how to handle the values
				"input" : ["avg", "Low"],
				#value is for replacing the 2nd element in input
				#with the value from the corresponding columns
				"value" : ["Low"]
				},
			"self.avgHighNeurons" : {
				"input" : ["avg", "High"],
				"value" : ["High"]
				},
			"self.avgCloseNeurons" : {
				"input" : ["avg", "Close"],
				"value" : ["Close"]
				},
			"self.avgOpenNeurons" : {
				"input" : ["avg", "Open"],
				"value" : ["Open"]
				},
			"self.avgCloseHighNeurons" : {
				"input" : ["avg", "Close/High"],
				"value" : ["Close", "High"]
				},
			"self.avgCloseLowNeurons" : {
				"input" : ["avg", "Close/Low"],
				"value" : ["Low", "Close"]
				},
			"self.avgOpenHighNeurons" : {
				"input" : ["avg", "Open/High"],
				"value" : ["Open", "High"]
				},
			"self.avgOpenLowNeurons" : {
				"input" : ["avg", "Open/Low"],
				"value" : ["Low", "Open"]
				},
			"self.avgVolumeNeurons" : {
				"input" : ["avg", "Volume"],
				"value" : ["Volume"]
				},
			"self.previousCloseNeurons" : {
				"input" : ["prev", "Close"],
				"value" : ["Close"]
				},
			"self.previousOpenHighNeurons" : {
				"input" : ["prev", "Open/High"],
				"value" : ["High", "Open"]
				},
			"self.previousOpenLowNeurons" : {
				"input" : ["prev", "Open/Low"],
				"value" : ["Low", "Open"]
				},
			"self.previousCloseHighNeurons" : {
				"input" : ["prev", "Close/High"],
				"value" : ["High", "Close"]
				},
			"self.previousCloseLowNeurons" : {
				"input" : ["prev", "Close/Low"],
				"value" : ["Low", "Close"]
				},
			"self.previousOpenCloseNeurons" : {
				"input" : ["prev", "Open/Close"],
				"value" : ["Close", "Open"]
				},
			"self.previousHighNeurons" : {
				"input" : ["prev", "High"],
				"value" : ["High"]
				},
			"self.previousLowNeurons" : {
				"input" : ["prev", "Low"],
				"value" : ["Low"]
				},
			"self.previousOpenNeurons" : {
				"input" : ["prev", "Open"],
				"value" : ["Open"]
				},
			"self.previousVolumeNeurons" : {
				"input" : ["prev", "Volume"],
				"value" : ["Volume"]
				},
			"self.dayOfTheMonthNeurons" : {
				"input" : ["dayOfMonth"],
				"value" : ["Date"]
				},
			"self.dayOfTheWeekNeurons" : {
				"input" : ["dayOfWeek"],
				"value" : ["Date"]
				},
			"self.weekOfTheMonthNeurons" : {
				"input" : ["weekOfMonth"],
				"value" : ["Date"]
				},
			"self.monthOfTheYearNeurons" : {
				"input" : ["monthOfYear"],
				"value" : ["Date"]
				},
			"self.weekOfTheYearNeurons" : {
				"input" : ["weekOfYear"],
				"value" : ["Date"]
				},
			"self.recentDownsNeurons" : {
				"input" : ["recent", "Downs"],
				"value" : []
				},
			"self.recentUpsNeurons" : {
				"input" : ["recent", "Ups"],
				"value" : []
				}
		}
	
	#sets the self.dataTable from a csv file
	def loadDataTable(self, file):
		self.dataTable = pandas.read_csv(file)
	
	#creates a neuron set
	def setUpNeurons(self, increment, neuronCount, start0):
		array = []
		#each output (open, low, high, close, volume)
		for i in range(0,5):
			array.append([])
			#for weights, trigger, states
			for j in range(0,3):
				array[i].append([])
				for k in range(0,neuronCount):
					if j == 0:
						array[i][j].append(0.0)
					elif j == 1:
						if start0:
							array[i][j].append(k * increment)
						else:
							array[i][j].append((k+1) * increment)
					else:
						array[i][j].append(False)
		return numpy.array(array)
	
	#resets the truth values of the neuron sets
	def resetNeurons(self):
		threads = []
		for i in self.neuronDict.keys():
			temp = eval(i)
			threads.append(threading.Thread(target=self.resetNeuronsSubFunc,args=(temp,)))
		for i in threads:
			i.start()
		for i in threads:
			i.join()
	
	def resetNeuronsSubFunc(self,neuronSet):
		for j in range(0,5):
			neuronSet[j][2] = False
	
	#makes a guess based on the supplied row from the data set
	def makeGuess(self,row):
		date = self.dataTable["Date"][row-1].split('-')
		date = datetime.date(int(date[0]), int(date[1]), int(date[2])).toordinal()
		valid = False
		while not valid:
			if (datetime.date.fromordinal(date).weekday()) >= 5:
				date += 1
			else:
				valid = True
		for i in self.neuronDict.keys():
			threads = []
			if self.neuronDict[i]["input"][0] == "avg":
				threads.append(threading.Thread(target=self.calculateAvg,args=(i,row)))
			elif self.neuronDict[i]["input"][0] == "recent":
				if self.neuronDict[i]["input"][1] == "Ups":
					threads.append(threading.Thread(target=self.countChange,args=(i,row,True)))
				else:
					threads.append(threading.Thread(target=self.countChange,args=(i,row,False)))
			elif self.neuronDict[i]["input"][0] == "weekOfYear":
				threads.append(threading.Thread(target=self.weekOfYear,args=(i,date)))
			elif self.neuronDict[i]["input"][0] == "weekOfMonth":
				threads.append(threading.Thread(target=self.weekOfMonth,args=(i,date)))
			elif self.neuronDict[i]["input"][0] == "monthOfYear":
				threads.append(threading.Thread(target=self.monthOfYear,args=(i,date)))
			elif self.neuronDict[i]["input"][0] == "dayOfMonth":
				threads.append(threading.Thread(target=self.dayOfMonth,args=(i,date)))
			elif self.neuronDict[i]["input"][0] == "dayOfWeek":
				threads.append(threading.Thread(target=self.dayOfWeek,args=(i,date)))
			elif self.neuronDict[i]["input"][0] == "prev":
				threads.append(threading.Thread(target=self.calculatePrev,args=(i,row)))
		for i in threads:
			i.start()
		for i in threads:
			i.join()
		guesses = [0,0,0,0,0]
		for i in self.neuronDict.keys():
			temp = eval(i)
			for k in range(0,len(temp)):
				for j in range(0,len(temp[k][0])):
					if temp[k][2][j]:
						guesses[k] += temp[k][0][j]
		return guesses
	
	def dayOfWeek(self,key,date):
		day = datetime.date.fromordinal(date).weekday()
		self.adjustTruths(day,eval(key),singular=True)
	
	def dayOfMonth(self,key,date):
		day = datetime.date.fromordinal(date).day
		self.adjustTruths(day,eval(key),singular=True)
	
	def weekOfYear(self,key,date):
		week = datetime.date.fromordinal(date).isocalendar().week
		self.adjustTruths(week,eval(key),singular=True)
		
	def monthOfYear(self,key,date):
		month = datetime.date.fromordinal(date).month
		self.adjustTruths(month,eval(key),singular=True)
		
	def weekOfMonth(self,key,date):
		week = datetime.date.fromordinal(date).day // 7
		self.adjustTruths(week,eval(key),singular=True)
		
	def countChange(self,key,row,positive):
		count = 0
		for j in range(1,121):
			if self.dataTable["Open"][row-j] >= self.dataTable["Close"][row-j]:
				if positive:
					count += 1
			else:
				if not positive:
					count += 1
		self.adjustTruths(count,eval(key))
	
	def calculatePrev(self,key,row):
		temp = self.neuronDict[key]["input"][1]
		for j in self.neuronDict[key]["value"]:
			temp = re.sub(j, str(self.dataTable[j][row-1]),temp)
		prev = eval(temp)
		self.adjustTruths(prev,eval(key))
	
	#calculates 120 average values
	def calculateAvg(self,key,row):
		avg = 0
		for j in range(1,121):
			temp = self.neuronDict[key]["input"][1]
			for k in self.neuronDict[key]["value"]:
				temp = re.sub(k, str(self.dataTable[k][row-j]),temp)
			avg += eval(temp)
		avg /= 120
		self.adjustTruths(avg,eval(key))
					
	#adjusts the truth values of a neuron set based on the passed value
	def adjustTruths(self,value,neuronSet,singular=False):
		if not singular:
			for j in range(0,len(neuronSet[0][2])):
				if value >= (neuronSet[0][1][j]):
					for k in range(0,len(neuronSet)):
						neuronSet[k][2][j] = True
		else:
			for j in range(0,len(neuronSet[0][2])):
				if value == (neuronSet[0][1][j]):
					neuronSet[0][2][j] = True
					neuronSet[1][2][j] = True
					neuronSet[2][2][j] = True
					neuronSet[3][2][j] = True
					neuronSet[4][2][j] = True
	#trains the ai
	def train(self):
		for i in range(121, len(self.dataTable)):
			temp = self.makeGuess(i)
			activeCount = 0
			for j in self.neuronDict.keys():
				for k in eval(j)[0][2]:
					if k:
						activeCount += 1
			#each output (open, low, high, close, volume)
			weightAdjustments = [(self.dataTable["Open"][i] - temp[0])/activeCount,(self.dataTable["Low"][i] - temp[1])/activeCount,(self.dataTable["High"][i] - temp[2])/activeCount,
(self.dataTable["Close"][i] - temp[3])/activeCount,(self.dataTable["Volume"][i] - temp[4])/activeCount]
			threads = []
			for j in self.neuronDict.keys():
				temp = eval(j)
				threads.append(threading.Thread(target=self.adjustWeights,args=(temp,weightAdjustments)))
			for j in threads:
				j.start()
			for j in threads:
				j.join()
			self.resetNeurons()
	#adjusts neuron weights
	def adjustWeights(self,neuronSet,weightAdjustments):
		for i in range(0,len(neuronSet[0][2])):
			if neuronSet[0][2][i]:
				neuronSet[0][0][i] += weightAdjustments[0]
				neuronSet[1][0][i] += weightAdjustments[1]
				neuronSet[2][0][i] += weightAdjustments[2]
				neuronSet[3][0][i] += weightAdjustments[3]
				neuronSet[4][0][i] += weightAdjustments[4]
