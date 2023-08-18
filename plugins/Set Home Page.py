from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

toolTip = "Adds button to set\ncurrent page as the\nhome page."
app = None

def main(HolyGrail):
	global app
	app = HolyGrail
	#checks for page menu, adds if it doesn't exist
	if HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page") == None:
		HolyGrail.findChild(QMenuBar,"Util Bar").addMenu(QMenu("Page",HolyGrail.findChild(QMenuBar,"Util Bar"),objectName="Page"))
	#adds button for setting home page
	homeBtn = QAction("Set Home Page",HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page"),objectName="Set Home")
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page").addAction(homeBtn)
	#updates settings to contain the custom home page
	if not HolyGrail.UtilityFuncs.getSetting("Home Page"):
		HolyGrail.UtilityFuncs.updateSettings("Home Page", HolyGrail.browser.home.toString())
	#updates browsers home page to the one stored in the settings
	HolyGrail.browser.home = QUrl(HolyGrail.UtilityFuncs.getSetting("Home Page"))
	homeBtn.triggered.connect(setHomePage)
#removes functionality
def end(HolyGrail):
	global app
	app = None
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page").findChild(QAction,"Set Home").deleteLater()
	HolyGrail.browser.home = QUrl("https://www.python.org/")
#sets home page to the current active tab's url
def setHomePage():
	global app
	app.browser.home = app.browser.currentWidget().url()
	app.UtilityFuncs.updateSettings("Home Page",app.browser.home.toString())