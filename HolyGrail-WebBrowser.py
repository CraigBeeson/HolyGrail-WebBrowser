import sys
import re
import TabbedBrowser
import Utility
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import importlib
import pkgutil
import os

import plugins

class MainWindow(QMainWindow):
	
	closing = pyqtSignal()
	
	def __init__(self):
		super(MainWindow, self).__init__()
		#checks if directory is in files
		if not os.path.isdir(os.getcwd()+"\\Settings"):
			os.mkdir(os.getcwd()+"\\Settings")
		self.browser = TabbedBrowser.TabbedBrowser()
		self.setCentralWidget(self.browser)
		self.showMaximized()
		#access functions in the utility.py file
		self.UtilityFuncs = Utility
		#status bar
		self.setStatusBar(QStatusBar(objectName="Stat Bar"))
		self.findChild(QStatusBar,"Stat Bar").addWidget(QLabel("Version: 0.2.0"))
		#utility bar
		self.setMenuBar(QMenuBar(objectName="Util Bar"))
		#settings button
		self.findChild(QMenuBar,"Util Bar").addMenu(QMenu("Settings",self.findChild(QMenuBar,"Util Bar"),objectName="Settings"))
		# navbar
		self.addToolBar(QToolBar(objectName="Nav Bar"))
		# sends the browser to the previous url
		back_btn = QAction('Back', self)
		back_btn.triggered.connect(self.browser.back)
		self.findChild(QToolBar,"Nav Bar").addAction(back_btn)
		#sends the browser to the next url
		forward_btn = QAction('Forward', self)
		forward_btn.triggered.connect(self.browser.forward)
		self.findChild(QToolBar,"Nav Bar").addAction(forward_btn)
		#reload webpage
		reload_btn = QAction('Reload', self)
		reload_btn.triggered.connect(self.browser.reload)
		self.findChild(QToolBar,"Nav Bar").addAction(reload_btn)
		#go to the home page, default is https://www.python.org/
		home_btn = QAction('Home', self)
		home_btn.triggered.connect(self.navigate_home)
		self.findChild(QToolBar,"Nav Bar").addAction(home_btn)
		#for user input urls or a local html file
		url_bar = QLineEdit(objectName="Url Bar")
		url_bar.returnPressed.connect(self.navigate_to_url)
		self.findChild(QToolBar,"Nav Bar").addWidget(url_bar)
		#updates the string in the line edit when webpage changes i.e. clicking a link in a web page
		self.browser.urlChanged.connect(self.update_url)
		#manage plugins
		#iterates through files in the plugins folder
		self.pluginList = {
			name: importlib.import_module(name)
			for finder, name, ispkg
			in self.iter_namespace(plugins)
		}
		#creates plugins button
		plugBtn = QAction("Plug-ins", self)
		plugBtn.triggered.connect(self.displayPlugs)
		#creates settings menu in the menubar
		self.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Settings").addAction(plugBtn)
		#creates plugins.txt if it does not already exist
		with open(os.getcwd()+"\\Settings\\plugins.txt","a+") as f:
			f.close()
		for i in self.pluginList.keys():
			inFile = False
			#enables plugin thats already enabled in settings
			#or if it is not in plugins.txt it gets added to the textfile
			with open(os.getcwd()+"\\Settings\\plugins.txt","r+") as f:
				for line in f:
					#modify line for reading
					temp = line.strip("\n")
					temp = temp.split(":")
					#if plug-in name is in the file
					if temp[0] == i:
						inFile = True
						#activate plug-in if true
						if temp[1] == "True":
							self.pluginList[i].main(self)
				f.close()
			#if not found in file it gets appended to the file
			if not inFile:
				with open(os.getcwd()+"\\Settings\\plugins.txt","a+") as f:
					f.write(i+":"+"False\n")
					f.close()
	#displaysplugs	
	def displayPlugs(self):
		#tries to close plug-in dock, prevents making duplicates
		try:
			self.findChild(QDockWidget,"Plug Dock").close()
			self.findChild(QDockWidget,"Plug Dock").deleteLater()
		except:
			pass
		plugs = QGroupBox("",objectName="Plug-ins")
		box = QVBoxLayout()
		#iterates through the pluginList
		for i in self.pluginList.keys():
			#checkbox for associated plugin
			plug = QCheckBox(re.sub("plugins.","",i))
			plug.setToolTip(self.pluginList[i].toolTip)
			#reads state of the plugin and then sets an enabled plugin to checked
			with open(os.getcwd()+"\\Settings\\plugins.txt","r") as f:
				for line in f:
					temp = line.strip("\n")
					temp = temp.split(":")
					if temp[0] == i:
						if temp[1] == "True":
							plug.setCheckState(2)
				f.close()
			#connects state to the operate plugin function 'OpPlugin'
			plug.stateChanged.connect(lambda state,i=i: self.OpPlugin(state, i))
			box.addWidget(plug)
		plugs.setLayout(box)
		plugWidget = QDockWidget('Plug-ins', self, objectName = "Plug Dock")
		plugWidget.setWidget(plugs)
		self.addDockWidget(Qt.RightDockWidgetArea,plugWidget)
	
	#enables/disables plugin
	def OpPlugin(self, state, plugin):
		data = []
		#opens plug in text
		with open(os.getcwd()+"\\Settings\\plugins.txt","r") as f:
			#stores the file contents
			data = f.readlines()
			#sets the plugin based on the state of checkbox
			for i in range(0,len(data)):
				temp = data[i].strip("\n")
				temp = temp.split(":")
				#checks if plugin being changed matches the plugin on that line
				if temp[0] == plugin:
					#if state is 2(check) or 1(dash)
					if state:
						temp[1] = "True"
					else:
						temp[1] = "False"
					#rewrites the line in data
					data[i] = ":".join(temp) + "\n"
			f.close()
		with open(os.getcwd()+"\\Settings\\plugins.txt","w+") as f:
			#rewrites file with updated data
			f.writelines(data)
			f.close()
		#runs the plugin or ends the plugin
		if state:
			self.pluginList[plugin].main(self)
		else:
			self.pluginList[plugin].end(self)

	def navigate_home(self):
		self.browser.setUrl(self.browser.home)

	def navigate_to_url(self):
		url = self.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").text()
		self.browser.setUrl(QUrl(url))

	def update_url(self, q):
		self.findChild(QToolBar,"Nav Bar").findChild(QLineEdit,"Url Bar").setText(q.toString())

	def iter_namespace(self,ns_pkg):
		# Specifying the second argument (prefix) to iter_modules makes the
		# returned name an absolute name instead of a relative one. This allows
		# import_module to work without having to do additional modification to
		# the name.
		return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")
	
	#allows for the use of functions that you want to be called on close of the program
	def closeEvent(self,event):
		self.closing.emit()
		QMainWindow().closeEvent(event)

app = QApplication(sys.argv)
QApplication.setApplicationName('Holy Grail - Web Browser')
window = MainWindow()
window.app = app
app.exec_()