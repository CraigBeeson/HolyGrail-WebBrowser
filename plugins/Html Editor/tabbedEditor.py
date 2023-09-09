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
		editorMenu.addMenu(File)
		self.setCornerWidget(editorMenu, Qt.TopRightCorner)
		
	def loadFile(self):
		fileDialog = QFileDialog(self,"Holy Grail - Choose HTML Page",self.filePath)
		fileDialog.setFileMode(QFileDialog.AnyFile)
		if fileDialog.exec_():
			self.newTab(fileDialog.selectedFiles()[0])
	#triggers save text of the current active widget
	def saveText(self):
		self.currentWidget().saveText()
	#creates new tab with associated file
	#plan to update for if no file(i.e. open new file)
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
			if self.count():
				for i in range(1,self.count()+2):
					isValid = True
					for j in range(0,self.count()):
						if self.tabText(j) == "new " + str(i):
							isValid = False
					if isValid:
						self.addTab(textEdit,"new " + str(i))
						break
			else:
				self.addTab(textEdit,"new 1")
	#closes a tab
	def closeTab(self,index):
		self.widget(index).deleteLater()
		self.removeTab(index)