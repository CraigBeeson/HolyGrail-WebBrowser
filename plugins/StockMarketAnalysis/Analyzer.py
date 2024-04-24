import pandas
import datetime
import os
import re
import sys
import matplotlib
import pickle

from . import AIUsage

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class Analyzer():
	def __init__(self,file,app,AI):
		#set up properties to use elsewhere
		self.app = app
		self.AI = AI
		self.file = file
		self.html = "<title>" + file.split("/")[-1] + "</title><br/><body style=\"background-color:rgb(0,0,0);color:rgb(0,125,0);max-width:960;margin:auto;\"><br/>"
		self.fileContents = pandas.read_csv(file)
		self.columns = ["Date", "Open/Close", "Open/Low", "Close/Low", "Open/High", "Close/High", "Close/Adj", "Volume"]
		self.columns0 = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
		self.dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		self.days = [pandas.DataFrame(columns = self.columns), pandas.DataFrame(columns = self.columns), pandas.DataFrame(columns = self.columns),
pandas.DataFrame(columns = self.columns), pandas.DataFrame(columns = self.columns)]
		self.days0 = [pandas.DataFrame(columns = self.columns0), pandas.DataFrame(columns = self.columns0), pandas.DataFrame(columns = self.columns0),
pandas.DataFrame(columns = self.columns0), pandas.DataFrame(columns = self.columns0)]
		self.setUpDays()
		self.createOutputInfo()
		self.saveOutput()
	#set up data based on day of the week
	def setUpDays(self):
		for i in range(0, len(self.fileContents)):
			temp = self.fileContents["Date"][i].split('-')
			day = datetime.date(int(temp[0]), int(temp[1]), int(temp[2])).weekday()
			self.days[day].loc[len(self.days[day].index)] = [
self.fileContents["Date"][i],
((self.fileContents["Close"][i] - self.fileContents["Open"][i])/self.fileContents["Open"][i]) * 100, 
((self.fileContents["Low"][i] - self.fileContents["Open"][i])/self.fileContents["Open"][i]) * 100, 
((self.fileContents["Low"][i] - self.fileContents["Close"][i])/self.fileContents["Close"][i]) * 100, 
((self.fileContents["High"][i] - self.fileContents["Open"][i])/self.fileContents["Open"][i]) * 100, 
((self.fileContents["High"][i] - self.fileContents["Close"][i])/self.fileContents["Close"][i]) * 100, 
((self.fileContents["Adj Close"][i] - self.fileContents["Close"][i])/self.fileContents["Close"][i]) * 100, 
self.fileContents["Volume"][i]
]
			self.days0[day].loc[len(self.days0[day].index)] = [self.fileContents["Date"][i],self.fileContents["Open"][i],self.fileContents["High"][i],
self.fileContents["Low"][i],self.fileContents["Close"][i],self.fileContents["Adj Close"][i],self.fileContents["Volume"][i]
]
	#generates output info
	def createOutputInfo(self):
		self.html += "<br/>Disclaimer: THIS IS NOT FINANCIAL ADVICE!!!!!!!!!!!!!!!!<br/>\tUse this information at your own risk!<br/><br/><br/>"
		#passes data to the useAI function to process the data and then generate
		#a prediction from the ai
		temp = AIUsage.useAI(self.AI,self.fileContents)
		self.html += "<br/>AI Generated Predictions For The Next Business Day.<br/>"
		self.html += "<br/>Open: " + str(temp[0][0])
		self.html += "<br/>High: " + str(temp[0][1])
		self.html += "<br/>Low: " + str(temp[0][2])
		self.html += "<br/>Close: " + str(temp[0][3]) + "<br/>"
		#print tables of the different days of the week
		for i in range(0,len(self.days)):
			self.html += self.dayNames[i]
			self.html += "<br/>"
			self.html += self.days0[i].to_html()
			self.html += "<br/>"
			self.html += self.days0[i].describe().to_html()
			self.html += "<br/>"
			self.html += self.days[i].to_html()
			self.html += "<br/>"
			self.html += self.days[i].describe().to_html()
			self.html += "<br/>"
		#delete graphs currently up
		try:
			app.findChild(QDockWidget,"Graph Dock").close()
			app.findChild(QDockWidget,"Graph Dock").deleteLater()
		except:
			pass
		#generate graphs
		canvasArray = []
		graphDocks = []
		for i in range(1,len(self.columns)):
			canvasArray.append(MplCanvas(self, width=10, height=8, dpi=100))
			canvasArray[i-1].axes.ticklabel_format(style = 'plain')
			axes = self.makeAxes(self.columns[i],self.days)
			for j in range(0,len(axes[0])):
				canvasArray[i-1].axes.plot(axes[0][j],axes[1][j],label=self.dayNames[j])
				canvasArray[i-1].axes.legend(loc='upper left')
			graphDocks.append(QDockWidget("Graph of " + re.sub(".csv","",self.file.split("/")[-1]) + "'s " + self.columns[i],self.app,objectName="Graph Dock"))
			graphDocks[i-1].setWidget(canvasArray[i-1])
			self.app.addDockWidget(Qt.RightDockWidgetArea,graphDocks[i-1])
		canvasArray = []
		graphDocks = []
		for i in range(1,len(self.columns0)):
			canvasArray.append(MplCanvas(self, width=10, height=8, dpi=100))
			canvasArray[i-1].axes.ticklabel_format(style = 'plain')
			axes0 = self.makeAxes(self.columns0[i],self.days0)
			for j in range(0,len(axes0[0])):
				canvasArray[i-1].axes.plot(axes0[0][j],axes0[1][j],label=self.dayNames[j])
				canvasArray[i-1].axes.legend(loc='upper left')
			graphDocks.append(QDockWidget("Graph of " + re.sub(".csv","",self.file.split("/")[-1]) + "'s " + self.columns0[i],self.app,objectName="Graph Dock"))
			graphDocks[i-1].setWidget(canvasArray[i-1])
			self.app.addDockWidget(Qt.RightDockWidgetArea,graphDocks[i-1])
	#saves the html content so view later
	def saveOutput(self):
		self.html += "</body>"
		with open(os.getcwd()+"\\StockFiles\\" + re.sub(".csv", ".html", self.file.split("/")[-1]),"w") as f:
			f.write(self.html)
		self.app.browser.newTab(QUrl(re.sub("\\\\","/", os.getcwd()+"\\StockFiles\\" + re.sub(".csv", ".html", self.file.split("/")[-1]))))
	#generate axes
	def makeAxes(self,column,tables):
		finalXAxes = []
		finalYAxes = []
		for i in tables:
			xaxis = []
			yaxis = []
			for j in range(0,len(i),10):
				xaxis.append(datetime.datetime.strptime(i["Date"][j], '%Y-%m-%d'))
				if j==0:
					yaxis.append(i[column][j])
				else:
					temp = 0
					for k in range(0,10):
						temp += i[column][j-k]
					temp /= 10
					yaxis.append(round(temp,2))
			finalXAxes.append(xaxis)
			finalYAxes.append(yaxis)
		return finalXAxes,finalYAxes

class MplCanvas(FigureCanvasQTAgg):

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		super(MplCanvas, self).__init__(fig)