import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

toolTip = "Enables search\nengine use with\nUrl bar."
searchEngines = ["google","bing","yahoo","yandex","duckduckgo","baidu","ask","naver"]
currentEngine = "google"
engineUrl = ""
app = None

def main(HolyGrail):
	global searchEngines
	global currentEngine
	global app
	app = HolyGrail
	#sets current engine to the one chosen in settings
	currentEngine = HolyGrail.UtilityFuncs.getSetting("Search Engine")
	#if one hasn't been assigned then the default is google
	if not currentEngine:
		HolyGrail.UtilityFuncs.updateSettings("Search Engine","google")
		currentEngine = "google"
	#sets up combobox for selecting search engine
	engineSel = QComboBox(objectName = "Search Selection")
	engineSel.addItems(searchEngines)
	engineSel.setCurrentIndex(searchEngines.index(currentEngine))
	engineSel.activated.connect(updateCurEngine)
	HolyGrail.findChild(QToolBar,"Nav Bar").addWidget(engineSel)
	#connects to url changed to manage if user is searching
	HolyGrail.browser.urlChanged.connect(searchCheck)
#removes functionality
def end(HolyGrail):
	HolyGrail.browser.urlChanged.disconnect(searchCheck)
	HolyGrail.findChild(QToolBar,"Nav Bar").findChild(QComboBox,"Search Selection").deleteLater()
#adjusts the current engine and updates engine in settings
def updateCurEngine(selection):
	global searchEngines
	global currentEngine
	currentEngine = searchEngines[selection]
	app.UtilityFuncs.updateSettings("Search Engine",currentEngine)

def searchCheck(url):
	global currentEngine
	global app
	global engineUrl
	url = url.toString()
	#checks if user input a website(or if the improved url changed it to a website)
	if "https://" not in url and url != "about:blank":
		#search url without the search
		engineUrl = "https://www." + currentEngine + ".com/search?q="
		#adds the search to the url
		url = url.split(" ")
		url = "+".join(url)
		engineUrl += url
	#failed url will bring up about blank, so we update the url
	#to the search after about blank so it stays instead of being
	#replaced by about blank
	if url == "about:blank":
		app.browser.setUrl(QUrl(engineUrl))
		engineUrl = ""