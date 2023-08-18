#Browser History Plug-in
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
"""
Probably have to create a custom QCompleter in order to show fill
suggestions that match in the middle versus beginning
"""
toolTip = "Saves browser history\nand adds autofill\nsuggestions."
app = None

#main plug-in function
def main(HolyGrail):
	global app
	app = HolyGrail
	#constructs history file
	with open(os.getcwd()+"\\Settings\\History.txt","a+") as f:
		f.close()
	#when the url is changed, updates the browser history
	HolyGrail.browser.urlChanged.connect(updateHistory)
	#whenever text is changed in the browser the suggested words are updated
	HolyGrail.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").textChanged.connect(updateWords)
	#sets up the completer
	completer = QCompleter([], HolyGrail.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar"),objectName = "Hcompleter")
	completer.setCaseSensitivity(Qt.CaseInsensitive)
	HolyGrail.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").setCompleter(completer)

#end the plug-in functionality if turned off
def end(HolyGrail):
	#disconnects connected signals
	HolyGrail.browser.urlChanged.disconnect(updateHistory)
	HolyGrail.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").textChanged.disconnect(updateWords)
	#sets completer to NoneType object, might delete the object(not sure how qt works in this regards since it wasn't added as a widget) since there are no more references to it
	HolyGrail.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").setCompleter(None)
#refreshes the QCompleter's wordlist
def updateCompleter(wordList):
	global app
	app.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").findChild(QCompleter,"Hcompleter").model().setStringList(wordList)


def updateWords(text):
	#peruses browser history to find suggested sites
	with open(os.getcwd()+"\\Settings\\History.txt","r") as f:
		#wordlist is defined as a set to avoid duplicates
		wordList = set()
		#if text isnt blank then it adds suggested addresses based on the text
		if text != "":
			for line in f:
				if len(wordList) >= 5:
					f.close()
					updateCompleter(wordList)
					return
				else:
					if text in line:
						wordList.add(line.strip("\n"))
		#if text is blank adds the first 5 sites in the browser history
		else:
			for line in f:
				if len(wordList) >= 5:
					f.close()
					updateCompleter(wordList)
					return
				else:
					wordList.add(line.strip("\n"))
		f.close()
		updateCompleter(wordList)

#updates browser history
def updateHistory(url):
	url = url.toString()
	#checks if url is already in textfile
	with open(os.getcwd()+"\\Settings\\History.txt","r") as f:
		for line in f:
			if line.strip("\n") == url:
				return
	#appends new url to textfile
	with open(os.getcwd()+"\\Settings\\History.txt","a+") as f:
		f.write(url + "\n")
		f.close()