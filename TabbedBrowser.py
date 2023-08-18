import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class TabbedBrowser(QTabWidget):

	urlChanged = pyqtSignal(QUrl)
	tabClosed = pyqtSignal(QUrl)

	def __init__(self):
		super(TabbedBrowser, self).__init__()
		#checks for and creates downloads directory
		if not os.path.isdir(os.getcwd()+"\\Downloads"):
			os.mkdir(os.getcwd()+"\\Downloads")
		#sets default download path to the above directory
		self.downloadDestination = os.getcwd()+"\\Downloads\\"
		#add close buttons for tabs
		self.setTabsClosable(True)
		self.currentChanged.connect(self.focusChanged)
		self.tabCloseRequested.connect(self.closeTab)
		#adds a button for creating new tabs
		self.newTabButton = QToolButton(self)
		self.newTabButton.setText('+')
		font = self.newTabButton.font()
		font.setBold(True)
		font.setPointSize(16)
		self.newTabButton.setFont(font)
		self.setCornerWidget(self.newTabButton, Qt.TopLeftCorner)
		self.newTabButton.resize(QSize(20,15))
		self.newTabButton.setMinimumSize(QSize(25,24))
		self.newTabButton.clicked.connect(self.newTabBtnPress)
		#sets default home page
		self.home = QUrl("https://www.python.org")
		#creates new tab set to home
		self.newTab(self.home)
	#updates url to current page
	def focusChanged(self):
		if self.currentWidget():
			self.urlChange(self.currentWidget().url())
		else:
			self.urlChange(QUrl(""))
	#for button to create new tab
	def newTabBtnPress(self,arg):
		self.newTab(self.home)
	#for button to close tab
	def closeTab(self,index):
		self.tabClosed.emit(self.widget(index).url())
		self.widget(index).deleteLater()
		self.removeTab(index)
	#new tab creation
	def newTab(self,url=""):
		#makes tab with new webengine view
		tab = QWebEngineView()
		if url:
			tab.setUrl(url)
		#set up tab for necessary functionality
		tab.urlChanged.connect(self.urlChange)
		tab.loadFinished.connect(self.updateTitle)
		tab.createWindow = self.handleNewWindow
		tab.page().profile().downloadRequested.connect(self.downloadHandler)
		self.addTab(tab,"new tab")
		#gives focus to new tab
		self.setCurrentWidget(tab)
		return tab
	#handles download requests
	def downloadHandler(self, download):
		download.setPath(self.downloadDestination+download.suggestedFileName())
		progressBar = QProgressBar()
		progressBar.setFormat(download.suggestedFileName())
		self.parent().findChild(QStatusBar,"Stat Bar").addWidget(progressBar)
		#no max is set with download progress because theres not always an initial size
		#such as saving a webpage
		download.downloadProgress.connect(lambda recvd,total,progressBar=progressBar: self.updateDownloadProgress(recvd,total,progressBar))
		download.finished.connect(lambda progressBar=progressBar: self.downloadFinished(progressBar))
		download.accept()
	#deletes the progress bar when download is finished
	def downloadFinished(self,progressBar):
		progressBar.deleteLater()
	#keeps the progress bar up to date on the download progress
	def updateDownloadProgress(self,recvd,total,progressBar):
		progressBar.setMaximum(total)
		progressBar.setValue(recvd)
	#for uses such as right clicking open link in new tab/window
	def handleNewWindow(self,pageType):
		#open in new window requested, creates a new browser window to use
		if pageType == 0:
			newWindow = self.parent().__class__()
			return newWindow.browser.widget(0)
		#open in new tab requested, opens new tab
		elif pageType == 1:
			return self.newTab()
	#updates title of tab to match title of associated website
	def updateTitle(self, loaded):
		for i in range(0,self.count()):
			self.setTabText(i,self.widget(i).page().title())
			
	#preserves urlChanged signal to work from tab widget
	def urlChange(self, url):
		self.urlChanged.emit(url)
	#sets url of current tab
	def setUrl(self, url):
		if self.currentWidget():
			self.currentWidget().setUrl(url)
		else:
			self.newTab(url)
	#sends the current qwebengineview back
	def back(self):
		self.currentWidget().back()
	#sends the current qwebengineview forward
	def forward(self):
		self.currentWidget().forward()
	#reloads the current qwebengineview
	def reload(self):
		self.currentWidget().reload()