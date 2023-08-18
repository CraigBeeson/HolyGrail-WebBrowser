import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

toolTip = "Restore unclosed\n     tabs."
app = None

def main(HolyGrail):
	global app
	app = HolyGrail
	HolyGrail.closing.connect(saveTabs)
	#opens a tab for each saved url
	with open(os.getcwd()+"\\Settings\\PreviousTabs.txt","a+") as f:
		f.seek(0)
		urls = f.readlines()
		if urls:
			for i in urls:
				i = i.strip("\n")
				HolyGrail.browser.newTab(QUrl(i))
			HolyGrail.browser.widget(0).deleteLater()
		f.close()
	
	
def end(HolyGrail):
	#disables functionality
	HolyGrail.closing.disconnect(saveTabs)
	with open(os.getcwd()+"\\Settings\\PreviousTabs.txt","w+") as f:
		f.close()
	
def saveTabs():
	global app
	#saves a url for each tab
	urls=""
	for i in range(0,app.browser.count()):
			urls += app.browser.widget(i).url().toString() + "\n"
	with open(os.getcwd()+"\\Settings\\PreviousTabs.txt","w+") as f:
		f.write(urls)
		f.close()