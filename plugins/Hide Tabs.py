from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

toolTip = "Adds ctrl+T shortcut\nto hide out of focus\ntabs."
shortcut = None
app = None
hidden = False

def main(HolyGrail):
	global app
	global shortcut
	app = HolyGrail
	#creates shortcut
	shortcut = QShortcut(QKeySequence("Ctrl+T"),HolyGrail)
	#assigns shortcut activation to the hidetabs func
	shortcut.activated.connect(hideTabs)

def end(HolyGrail):
	global hidden
	#unhides tabs
	if hidden:
		hideTabs()
	#deletes shortcut
	shortcut.deleteLater()

def hideTabs():
	global app
	global hidden
	#hides and unhides tabs
	if hidden:
		for i in range(0,app.browser.count()):
			app.browser.setTabVisible(i,True)
		hidden = False
	else:
		for i in range(0,app.browser.count()):
			if i != app.browser.currentIndex():
				app.browser.setTabVisible(i,False)
		hidden = True