import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

toolTip = "Add zoom adjustment\nButtons."
app = None

def main(HolyGrail):
	global app
	app = HolyGrail
	#sets up the zoom in button
	zInBtn = QAction(HolyGrail,objectName = "Zoom in")
	zInBtn.triggered.connect(zoomIn)
	zInBtn.setToolTip("Zoom +")
	zInIcon = QImage(os.getcwd()+"//Icons//zoom in.svg")
	zInBtn.setIcon(QIcon(QPixmap.fromImage(zInIcon)))
	HolyGrail.findChild(QToolBar,"Nav Bar").addAction(zInBtn)
	#sets up the zoom reset button
	zResetBtn = QAction(HolyGrail,objectName = "Zoom reset")
	zResetBtn.triggered.connect(resetZoom)
	zResetIcon = QImage(os.getcwd()+"//Icons//normalZoom.svg")
	zResetBtn.setToolTip("Zoom 1:1")
	zResetBtn.setIcon(QIcon(QPixmap.fromImage(zResetIcon)))
	HolyGrail.findChild(QToolBar,"Nav Bar").addAction(zResetBtn)
	#sets up the zoom out button
	zOutBtn = QAction(HolyGrail,objectName = "Zoom out")
	zOutBtn.triggered.connect(zoomOut)
	zOutBtn.setToolTip("Zoom -")
	zOutIcon = QImage(os.getcwd()+"//Icons//zoom out.svg")
	zOutBtn.setIcon(QIcon(QPixmap.fromImage(zOutIcon)))
	HolyGrail.findChild(QToolBar,"Nav Bar").addAction(zOutBtn)
#removes functionality	
def end(HolyGrail):
	HolyGrail.findChild(QAction,"Zoom in").deleteLater()
	HolyGrail.findChild(QAction,"Zoom out").deleteLater()
	HolyGrail.findChild(QAction,"Zoom reset").deleteLater()

def zoomIn():
	global app
	app.browser.currentWidget().setZoomFactor(.05 + app.browser.currentWidget().zoomFactor())
	

def zoomOut():
	global app
	app.browser.currentWidget().setZoomFactor(-.05 + app.browser.currentWidget().zoomFactor())

def resetZoom():
	global app
	app.browser.currentWidget().setZoomFactor(1.0)