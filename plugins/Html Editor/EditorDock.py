from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from . import tabbedEditor

#not much here, yet
class EditorDock(QDockWidget):
	def __init__(self, *args, **kwargs):
		super(EditorDock, self).__init__()
		self.tabs = tabbedEditor.tabbedEditor(self,objectName="Editor")
		#stuff to display the tabs
		box = QVBoxLayout()
		box.addWidget(self.tabs)
		editorGroup = QGroupBox()
		editorGroup.setLayout(box)
		self.setWidget(editorGroup)