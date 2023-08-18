from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

toolTip = "Removes need to\ntype exact Url."
app = None

def main(HolyGrail):
	global app
	app = HolyGrail
	#replaces the url bar to use improved url function
	HolyGrail.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").returnPressed.disconnect(HolyGrail.navigate_to_url)
	HolyGrail.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").returnPressed.connect(ImprovedUrl)

def end(HolyGrail):
	#sets the url bar to use default function
	HolyGrail.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").returnPressed.connect(HolyGrail.navigate_to_url)
	HolyGrail.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").returnPressed.disconnect(ImprovedUrl)

def ImprovedUrl():
	global app
	url = app.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").text()
	#adds some strings to the user input if not contained
	#i.e. python.org becomes https://www.python.org
	if " " not in url and "." in url:
		if "www." not in url and "https://" not in url:
			url = "https://www." + url
		elif "https://" in url and "www." not in url:
			url = url[0:8] + "www." + url[8:]
		elif "www." in url and "https://" not in url:
			url = "https://" + url
	app.browser.setUrl(QUrl(url))