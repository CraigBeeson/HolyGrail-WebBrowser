import sys
from PyQt5.QtWebEngineCore import *
if "3.11" == sys.version[0:4]:
	from . import Interceptor

toolTip = "Prevent harmful\nrequests"

def main(HolyGrail):
	try:
		HolyGrail.browser.profile.setUrlRequestInterceptor(Interceptor.Interceptor(HolyGrail.browser))
	except:
		print("Requires Python 3.11")

def end(HolyGrail):
	HolyGrail.browser.profile.setUrlRequestInterceptor(None)