import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

toolTip = "Store persistent\nBrowser data and\nthe cache."

def main(HolyGrail):
	#checks for folder, creates folder if it doesn't exist
	if not os.path.isdir(os.getcwd()+"\\Data"):
		os.mkdir(os.getcwd()+"\\Data")
	#turns off isOffTheRecord
	if HolyGrail.browser.profile.isOffTheRecord():
		HolyGrail.browser.profile = HolyGrail.browser.profile.defaultProfile()
	#set cache/persistent data and cookies to store in the 'Data' folder
	HolyGrail.browser.profile.setPersistentStoragePath(os.getcwd()+"\\Data")
	HolyGrail.browser.profile.setPersistentCookiesPolicy(QWebEngineProfile(os.getcwd()+"\\Data").persistentCookiesPolicy())
	HolyGrail.browser.profile.setCachePath(os.getcwd()+"\\Data")

def end(HolyGrail):
	#turns on isOffTheRecord
	HolyGrail.browser.profile.setPersistentStoragePath(QWebEngineProfile().persistentStoragePath())
	HolyGrail.browser.profile.setPersistentCookiesPolicy(QWebEngineProfile().persistentCookiesPolicy())
	HolyGrail.browser.profile = QWebEngineProfile()
	
