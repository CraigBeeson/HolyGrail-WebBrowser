import code
import threading
import sys
import os
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

toolTip = "Enables Python\nInterpreter. Useful for\nWeb Scraping"
shell = None
app = None
signals = None
scraper = None

def main(HolyGrail):
	global shell
	global app
	global signals
	global scraper
	app = HolyGrail
	#create and then start qthread that runs the interpreter
	shell = Shell()
	shell.start()
	#set up for interacting with the main thread
	signals = ThreadSignals()
	scraper = ScrapingBrowser()
	signals.setUrlSignal.connect(scraper.setUrl)
	
#closes and deletes thread holding object
def end(HolyGrail):
	global shell
	shell.terminate()
	shell.deleteLater()
	signals.deleteLater()
	scraper.deleteLater()
	print("Interpreter Closed")

#this function exists to demonstrate how to pull the current page's html
#also useful if you would rather look at the html in the console instead of the browser
def currentPageHtml():
	app.browser.currentWidget().page().toHtml(print)
#basic scraper function, mainly to be used as an example
#accepts string 
def basicScraping(url,keywords):
	signals.setUrlSignal.emit(QUrl(url))
	#give time to load url
	time.sleep(5)
	scraper.page().toHtml(lambda html,keywords=keywords: scanHtml(html, keywords))
	
#scans each line of the html for any lines that contain a keyword
def scanHtml(html, keywords):
	html = html.split("\n")
	lines = []
	for i in html:
		for j in keywords:
			if j in i:
				lines.append(i)
				break
	print(("\n").join(lines))

#custom qthread class to run the interpreter
class Shell(QThread):
	global app
	
	def run(self):
		#code lib used for interactive console
		code.InteractiveConsole(locals=globals()).interact(banner="Holy Grail Interpreter\n[*] basicScraping(url,[keywords]) [*]")

#signal class for handling communication
class ThreadSignals(QObject):
    setUrlSignal = pyqtSignal(QUrl)

#browser class, can be modified as needed
class ScrapingBrowser(QWebEngineView):
	
	def __init__(self):
		super(QWebEngineView, self).__init__()