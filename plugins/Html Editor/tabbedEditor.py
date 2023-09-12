from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

from . import HtmlTextEdit

class tabbedEditor(QTabWidget):

	updateFilePath = pyqtSignal(str)

	def __init__(self, *args, **kwargs):
		super(tabbedEditor, self).__init__()
		#gives close tab button and then functionality for that button
		self.setParent(args[0])
		self.filePath = ""
		self.setTabsClosable(True)
		self.tabCloseRequested.connect(self.closeTab)
		#creates shortcut
		saveShortcut = QShortcut(QKeySequence("Ctrl+S"),self)
		#assigns shortcut activation to the hidetabs func
		saveShortcut.activated.connect(self.saveText)
		#menu for the editor
		editorMenu = QMenuBar(objectName = "Editor Menu")
		File = QMenu("File",self,objectName = "File")
		saveAction = QAction("Save",File)
		saveAction.triggered.connect(self.saveText)
		File.addAction(saveAction)
		newAction = QAction("New File",File)
		newAction.triggered.connect(self.newTab)
		File.addAction(newAction)
		loadAction = QAction("Load File",File)
		loadAction.triggered.connect(self.loadFile)
		File.addAction(loadAction)
		debugAction = QAction("Docked Debugger",File)
		debugAction.triggered.connect(self.debugConsole)
		File.addAction(debugAction)
		editorMenu.addMenu(File)
		self.setCornerWidget(editorMenu, Qt.TopRightCorner)
	#creates a console to view debugging information without having to tab over to the terminal
	def debugConsole(self,signal):
		if (self.parent().parent().parent().findChild(QDockWidget,"Debugger") == None):
			debugDock = QDockWidget("Debugger",self.parent().parent().parent(),objectName="Debugger")
			box = QVBoxLayout()
			#uses a plaintextedit to display the debug info
			debugger = QPlainTextEdit()
			#no need to edit debug info
			debugger.setReadOnly(True)
			box.addWidget(debugger)
			debugGroup = QGroupBox()
			debugGroup.setLayout(box)
			debugDock.setWidget(debugGroup)
			#connects to the browsers signal that outputs the debugger info
			self.parent().parent().parent().browser.JSErrorMsgSig.connect(debugger.appendPlainText)
			#adds dockwidget to main app
			self.parent().parent().parent().addDockWidget(Qt.LeftDockWidgetArea,debugDock)
	#loads file for editing without opening a browser tab
	def loadFile(self):
		fileDialog = QFileDialog(self,"Holy Grail - Choose HTML Page",self.filePath)
		fileDialog.setFileMode(QFileDialog.AnyFile)
		if fileDialog.exec_():
			self.newTab(fileDialog.selectedFiles()[0])
	#triggers save text of the current active widget
	def saveText(self):
		self.currentWidget().saveText()
	#creates new tab for editing, either with an associated file or none if opening a new blank tab
	def newTab(self, file=""):
		if file:
			textEdit = HtmlTextEdit.HtmlEditor()
			textEdit.file = file
			self.addTab(textEdit,file.split("/")[-1])
			data = ""
			with open(file,"r") as f:
				data = f.readlines()
				f.close()
			data = "".join(data)
			textEdit.setPlainText(data)
		else:
			textEdit = HtmlTextEdit.HtmlEditor()
			textEdit.setPlainText("")
			#if there are tabs open, it iterates through to create serialized new tabs
			#i.e. 'new 1' 'new 2' etc
			#if there are tabs in the editor
			if self.count():
				#since we are starting tab naming at 1 we add +1 to the range
				#in case all open tabs are 'new n' we'll need to loop one more time
				#this results in +2 to the range
				for i in range(1,self.count()+2):
					#name is valid unless it is found
					isValid = True
					for j in range(0,self.count()):
						if self.tabText(j) == "new " + str(i):
							isValid = False
							break
					if isValid:
						self.addTab(textEdit,"new " + str(i))
						break
			#if editor has no tabs then a 'new 1' tab is created
			else:
				self.addTab(textEdit,"new 1")
	#closes a tab
	def closeTab(self,index):
		self.widget(index).deleteLater()
		self.removeTab(index)