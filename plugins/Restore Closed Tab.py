from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

toolTip = "Adds a restore\nprevious tab\nfunction."
app = ""
previousTab = ""

def main(HolyGrail):
	global app
	app = HolyGrail
	#connects to when a tab closes and saves the url
	HolyGrail.browser.tabClosed.connect(savePage)
	#checks for page menu adds if doesnt exist
	if HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page") == None:
		HolyGrail.findChild(QMenuBar,"Util Bar").addMenu(QMenu("Page",HolyGrail.findChild(QMenuBar,"Util Bar"),objectName="Page"))
	#adds reopen closed tab button
	reopenBtn = QAction("Reopen Closed Tab",HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page"),objectName="ROT")
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page").addAction(reopenBtn)
	reopenBtn.triggered.connect(openPreviousTab)

def end(HolyGrail):
	#removes added functionality
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page").findChild(QAction,"ROT").deleteLater()
	HolyGrail.browser.tabClosed.disconnect(savePage)
#saves url when a tab is closed
def savePage(url):
	global previousTab
	previousTab = url
#opens the saved previous tab
def openPreviousTab():
	global previousTab
	app.browser.newTab(previousTab)
	previousTab = ""