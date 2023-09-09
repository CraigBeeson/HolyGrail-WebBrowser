import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from . import EditorDock

toolTip = "Use html editor"
app = None

def main(HolyGrail):
	global app
	app = HolyGrail
	if not app.UtilityFuncs.getSetting("EditorFilePath"):
		app.UtilityFuncs.updateSettings("EditorFilePath", os.getcwd())
	#adds menu labeled file to the menu bar
	if HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File") == None:
		HolyGrail.findChild(QMenuBar,"Util Bar").addMenu(QMenu("File",HolyGrail.findChild(QMenuBar,"Util Bar"),objectName="File"))
	#adds menu labeled file to the menu bar
	if HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File") == None:
		HolyGrail.findChild(QMenuBar,"Util Bar").addMenu(QMenu("File",HolyGrail.findChild(QMenuBar,"Util Bar"),objectName="File"))
	devAction = QAction("Edit HTML File",HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File"),objectName="Edit html")
	devAction.triggered.connect(loadHTMLFile)
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").addAction(devAction)
	devAction0 = QAction("Edit New File",HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File"),objectName="Edit new html")
	devAction0.triggered.connect(openNewFile)
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").addAction(devAction0)

#removes the functionality
def end(HolyGrail):
	if HolyGrail.findChild(QDockWidget,"Editor Dock") != None:
		HolyGrail.findChild(QDockWidget,"Editor Dock").deleteLater()
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").findChild(QAction, "Edit html").deleteLater()
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").findChild(QAction, "Edit new html").deleteLater()
	if len(HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").actions()) == 1:
		HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"File").deleteLater()

def openNewFile():
	global app
	if app.findChild(QDockWidget,"Editor Dock") != None:
		app.findChild(QDockWidget,"Editor Dock").tabs.newTab()
	else:
		#creates a new tab with associated file and sets up the dock widget
		editDock = EditorDock.EditorDock("HolyGrail-Editor",app,objectName="Editor Dock")
		editDock.tabs.newTab()
		app.addDockWidget(Qt.BottomDockWidgetArea,editDock)

def loadHTMLFile():
	global app
	#opens file dialogue to choose file for editing
	fileDialog = QFileDialog(app,"Holy Grail - Choose HTML Page",app.browser.downloadDestination)
	fileDialog.setFileMode(QFileDialog.AnyFile)
	#appears to work, but doesn't show any files
#	fileDialog.setNameFilter("Web Doc (*.html,*.mhtml)")
	if fileDialog.exec_():
		file = fileDialog.selectedFiles()[0]
		#creates a browser tab to view the associated file
		app.browser.newTab(QUrl(file))
		#if the editor dock already exists, creates a new tab
		if app.findChild(QDockWidget,"Editor Dock") != None:
			app.findChild(QDockWidget,"Editor Dock").tabs.newTab(file)
		else:
			#creates a new tab with associated file and sets up the dock widget
			editDock = EditorDock.EditorDock("HolyGrail-Editor",app,objectName="Editor Dock")
			editDock.tabs.newTab(file=file)
			app.addDockWidget(Qt.BottomDockWidgetArea,editDock)
	fileDialog.deleteLater()