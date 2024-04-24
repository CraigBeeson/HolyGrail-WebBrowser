import os
import sys
import tensorflow
import numpy
import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from . import Search
from . import NeuralNetwork
sys.modules['NeuralNetwork'] = NeuralNetwork

toolTip = "View data\n analytics of\n stocks."

#AI is loaded here to prevent having to load with every use, just a little more efficient
stockModel = tensorflow.keras.models.load_model(os.getcwd() + "\\plugins\\stockmarketanalysis\\AI\\Stock.ai")

def main(HolyGrail):
	if not os.path.isdir(os.getcwd()+"\\StockFiles"):
		os.mkdir(os.getcwd()+"\\StockFiles")
	menu = QMenu("Stocks",HolyGrail.findChild(QMenuBar, "Util Bar"),objectName="Stock Menu")
	line = QWidgetAction(menu,objectName="Stock Action")
	line.setDefaultWidget(Search.GetStockLine(HolyGrail,stockModel,objectName = "Stock Line"))
	menu.addAction(line)
	HolyGrail.findChild(QMenuBar, "Util Bar").addMenu(menu)
	

def end(HolyGrail):
	menu = HolyGrail.findChild(QMenuBar, "Util Bar").findChild(QMenu,"Stock Menu").deleteLater()