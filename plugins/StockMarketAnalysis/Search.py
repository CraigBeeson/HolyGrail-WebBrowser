import re
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from . import Analyzer

class GetStockLine(QLineEdit):
	def __init__(self, *args, **kwargs):
		super(GetStockLine, self).__init__()
		self.setParent(args[0])
		self.AI = args[1]
		self.setObjectName(kwargs["objectName"])
		self.setToolTip("Search for\n stock info.")
		self.profile = QWebEngineProfile(self)
		self.profile.downloadRequested.connect(self.downloadHandler)
		self.scraper = QWebEngineView()
		self.scraper.setPage(QWebEnginePage(self.profile, self.scraper))
		self.returnPressed.connect(self.findStocks)
		
	def findStocks(self):
		stock = self.text()
		self.scraper.setUrl(QUrl("https://finance.yahoo.com/quote/" + stock + "/history?p=" + stock))
		self.scraper.loadFinished.connect(self.downloadInfo)
	
	def downloadInfo(self, fin):
		self.scraper.loadFinished.disconnect(self.downloadInfo)
		self.scraper.page().toHtml(self.getLink)
		
	def getLink(self, html):
		link = re.search("https://query.*?true" ,html)
		link = str(link.group())
		link = re.sub("&amp;","&",link)
		link = re.sub("period1=.*?&","period1=0&",link)
		self.scraper.setUrl(QUrl(link))
	#handles downloads
	def downloadHandler(self, download):
		download.setPath(os.getcwd() + "\\StockFiles\\" + download.suggestedFileName())
		progressBar = QProgressBar()
		progressBar.setFormat(download.suggestedFileName())
		self.parent().parent().parent().findChild(QStatusBar,"Stat Bar").addWidget(progressBar)
		#no max is set with download progress because theres not always an initial size
		#such as saving a webpage
		download.downloadProgress.connect(lambda recvd,total,progressBar=progressBar: self.updateDownloadProgress(recvd,total,progressBar))
		download.finished.connect(lambda progressBar=progressBar,file=download.path(): self.downloadFinished(progressBar,file))
		download.accept()
	#deletes the progress bar when download is finished
	def downloadFinished(self,progressBar,file):
		progressBar.deleteLater()
		Analyzer.Analyzer(file,self.parent().parent().parent(),self.AI)
		self.scraper.setUrl(QUrl("https://www.google.com/"))
	#keeps the progress bar up to date on the download progress
	def updateDownloadProgress(self,recvd,total,progressBar):
		progressBar.setMaximum(total)
		progressBar.setValue(recvd)
