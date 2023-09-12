import os
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

toolTip = "Adds some basic\nFile Options"
app = None

def main(HolyGrail):
	global app
	app = HolyGrail
	#adds menu labeled file to the menu bar
	if HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File") == None:
		HolyGrail.findChild(QMenuBar,"Util Bar").addMenu(QMenu("File",HolyGrail.findChild(QMenuBar,"Util Bar"),objectName="File"))
	#adds the menu item to choose download destination if youre unhappy with the default
	fileAction = QAction("Download Destination",HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File"),objectName="Down Dest")
	fileAction.triggered.connect(changeDownloadDirectory)
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").addAction(fileAction)
	#a convenient way to open html files instead of typing the html file path into the browser
	fileAction0 = QAction("Open html file",HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File"),objectName="Open html")
	fileAction0.triggered.connect(loadHTMLFile)
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").addAction(fileAction0)
	#if this plug-in was used previously then it loads the previously set download directory
	if HolyGrail.UtilityFuncs.getSetting("Download Directory"):
		HolyGrail.browser.downloadDestination = HolyGrail.UtilityFuncs.getSetting("Download Directory")

def end(HolyGrail):
	#destroys the file menu options
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").findChild(QAction,"Down Dest").deleteLater()
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").findChild(QAction,"Open html").deleteLater()
	if len(HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").actions()) == 2:
		HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").deleteLater()
#function for changing download directory
def changeDownloadDirectory():
	global app
	#opens file dialog for choosing a directory for downloads
	fileDialog = QFileDialog(app,"Holy Grail - Choose Download Folder",app.browser.downloadDestination)
	fileDialog.setFileMode(QFileDialog.Directory)
	directory = ""
	if fileDialog.exec_():
		directory = fileDialog.selectedFiles()[0] + "//"
	#if a directory is chosen then the destination and associated setting are selected
	if directory:
		app.browser.downloadDestination = directory
		app.UtilityFuncs.updateSettings("Download Directory",directory)
	fileDialog.deleteLater()
#open a file in a tab, supposed to filter to only show web doc files
def loadHTMLFile():
	global app
	fileDialog = QFileDialog(app,"Holy Grail - Choose HTML Page",app.browser.downloadDestination)
	fileDialog.setFileMode(QFileDialog.AnyFile)
	#appears to work, but doesn't show any files
#	fileDialog.setNameFilter("Web Doc (*.html,*.mhtml)")
	if fileDialog.exec_():
		file = fileDialog.selectedFiles()[0]
		app.browser.newTab(QUrl(file))
	fileDialog.deleteLater()