from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from . import tabbedEditor

#not much here, yet
class EditorDock(QDockWidget):
	def __init__(self, *args, **kwargs):
		super(EditorDock, self).__init__()
		self.setParent(args[1])
		self.tabs = tabbedEditor.tabbedEditor(self,objectName="Editor")
		self.tabs.filePath = self.parent().UtilityFuncs.getSetting("EditorFilePath")
		self.tabs.updateFilePath.connect(self.updateFP)
		#stuff to display the tabs
		box = QVBoxLayout()
		box.addWidget(self.tabs)
		editorGroup = QGroupBox()
		editorGroup.setLayout(box)
		self.setWidget(editorGroup)
		self.setObjectName(kwargs["objectName"])
	#updates file path
	def updateFP(self,file):
		self.parent().UtilityFuncs.updateSettings("EditorFilePath", file)
		self.tabs.filePath = file