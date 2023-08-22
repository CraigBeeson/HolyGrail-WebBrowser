import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

toolTip = "Adds bookmark \n support."
app = None

def main(HolyGrail):
	global app
	app = HolyGrail
	#creates file if it does not exist
	with open(os.getcwd()+"\\Settings\\Bookmarks.txt","a+") as f:
		f.close()
	#checks if the menubar already has the page menu, adds if it does not
	if HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page") == None:
		HolyGrail.findChild(QMenuBar,"Util Bar").addMenu(QMenu("Page",HolyGrail.findChild(QMenuBar,"Util Bar"),objectName="Page"))
	#adds the bookmark action
	bookmarkBtn = QAction("Add to bookmarks",HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page"),objectName="Bookmark")
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page").addAction(bookmarkBtn)
	bookmarkBtn.triggered.connect(mark)
	#adds action to view bookmarks
	showBtn = QAction("View Bookmarks",HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page"),objectName="Show Marks")
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page").addAction(showBtn)
	showBtn.triggered.connect(showMarks)

def end(HolyGrail):
	
	#delete the actions added to the page menu
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page").findChild(QAction,"Bookmark").deleteLater()
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page").findChild(QAction,"Show Marks").deleteLater()
	if len(HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page").actions()) == 2:
		HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Page").deleteLater()
	#if the dock widget created by the action to view book marks
	#is open then this will close and delete it
	try:
		HolyGrail.findChild(QDockWidget,"Mark Dock").close()
		HolyGrail.findChild(QDockWidget,"Mark Dock").deleteLater()
	except:
		pass
	
def mark():
	global app
	#saves bookmark of the current open tab
	bookmark = app.browser.currentWidget().url().toString() + "\n"
	title = app.browser.currentWidget().title() + "\n"
	with open(os.getcwd()+"\\Settings\\Bookmarks.txt","a") as f:
		f.write(bookmark)
		f.write(title)
		f.close()

def showMarks():
	global app
	#closes unopened view bookmarks dock
	try:
		app.findChild(QDockWidget,"Mark Dock").close()
		app.findChild(QDockWidget,"Mark Dock").deleteLater()
	except:
		pass
	marks = QGroupBox("",objectName="Bookmarks")
	box = QGridLayout()
	markUrls = []
	with open(os.getcwd()+"\\Settings\\Bookmarks.txt","r") as f:
		markUrls = f.readlines()
		f.close()
	#assigns label text based on title of the bookmarked page
	#the link is assigned to open a new window in the browser
	#instead of with your default os
	for i in range(0,len(markUrls),2):
		label = QLabel("<a href=\"" + markUrls[i].strip("\n") + "\">" + markUrls[i+1].strip("\n") + "</a>")
		label.setTextInteractionFlags(Qt.TextBrowserInteraction)
		label.setOpenExternalLinks(False)
		label.setToolTip(markUrls[i].strip("\n"))
		temp = markUrls[i].strip("\n")
		label.linkActivated.connect(lambda url=temp: app.browser.newTab(QUrl(url)))
		box.addWidget(label,i,0)
		#add button for deleting bookmarks
		delBtn = QPushButton("")
		delBtn.setIcon(app.style().standardIcon(QStyle.SP_TitleBarCloseButton))
		delBtn.pressed.connect(lambda index=i: delMark(index))
		box.addWidget(delBtn,i,1)
	#create/open dock widget showing book marks
	marks.setLayout(box)
	markWidget = QDockWidget("Book Marks", app, objectName = "Mark Dock")
	markWidget.setWidget(marks)
	app.addDockWidget(Qt.LeftDockWidgetArea,markWidget)

def delMark(index):
	markUrls = []
	#reads the bookmarks
	with open(os.getcwd()+"\\Settings\\Bookmarks.txt","r") as f:
		markUrls = f.readlines()
		f.close()
	#deletes the bookmark at the index and the title located at the index + 1
	del markUrls[index:index+2]
	#writes the updated list of bookmarks
	with open(os.getcwd()+"\\Settings\\Bookmarks.txt","w") as f:
		data = ""
		for i in markUrls:
			data += i
		f.write(data)
		f.close()
	#shows updated list
	showMarks()