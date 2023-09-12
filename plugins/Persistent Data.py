import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

toolTip = "Store persistent\nBrowser data and\nthe cache."

def main(HolyGrail):
	if not os.path.isdir(os.getcwd()+"\\Data"):
		os.mkdir(os.getcwd()+"\\Data")
	if HolyGrail.browser.profile.isOffTheRecord():
		HolyGrail.browser.profile = HolyGrail.browser.profile.defaultProfile()
	HolyGrail.browser.profile.setPersistentStoragePath(os.getcwd()+"\\Data")
	HolyGrail.browser.profile.setPersistentCookiesPolicy(QWebEngineProfile(os.getcwd()+"\\Data").persistentCookiesPolicy())
	HolyGrail.browser.profile.setCachePath(os.getcwd()+"\\Data")

def end(HolyGrail):
	HolyGrail.browser.profile.setPersistentStoragePath(QWebEngineProfile().persistentStoragePath())
	HolyGrail.browser.profile.setPersistentCookiesPolicy(QWebEngineProfile().persistentCookiesPolicy())
	HolyGrail.browser.profile = QWebEngineProfile()
	