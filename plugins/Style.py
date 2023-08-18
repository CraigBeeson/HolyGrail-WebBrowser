import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

toolTip = "Customize Browser\nAppearance."
app = None

#default stylesheet
defaultSS = """QMenuButton{background-color:darkslategray;color:lightgray;}
QToolButton{background-color:darkslategray;border-style:outset;border-width:1px;border-color:dimgray;color:lightgray;}
QToolBar{background-color:darkslategray;color:lightgray;border:2px solid black;spacing:3px;icon-size:400px;}
QMenuBar{background-color:darkslategray;color:lightgray;border:2px solid black;}
QMenuBar::item::selected{background-color:dimgray;color:black;}
QLineEdit{background-color:darkslategray;color:lightgray;border:1px solid black;}
QDockWidget{border:1px solid black;color:lightgray;background:darkslategray;}
QCheckBox{border:1px solid black;background:darkslategray;color:lightgray}
QGroupBox{border:1px solid black;background:darkslategray;color:lightgray}
QStatusBar{background:darkslategray;color:lightgray}
QMenu{background-color:darkslategray;}
QMenu::item{background-color:darkslategray;color:lightgray}
QMenu::item:selected{background-color:dimgray;color:black;}
QLabel{color:lightgray;}
QTabBar::tab{color:lightgray;background:darkslategray;}
QTabBar::tab:selected{background:dimgray;color:black;}
QToolTip{color:lightgray;background:darkslategray;border:2px solid black;}
QStatusBar{color:lightgray;background:darkslategray;}
QProgressBar{color:lightgray;}
"""
#list of colors for user to pick from
colors = ["aliceblue",
"antiquewhite",
"aqua",
"aquamarine",
"azure",
"beige",
"bisque",
"black",
"blanchedalmond",
"blue",
"blueviolet",
"brown",
"burlywood",
"cadetblue",
"chartreuse",
"chocolate",
"coral",
"cornflowerblue",
"cornsilk",
"crimson",
"cyan",
"darkblue",
"darkcyan",
"darkgoldenrod",
"darkgray",
"darkgreen",
"darkgrey",
"darkkhaki",
"darkmagenta",
"darkolivegreen",
"darkorange",
"darkorchid",
"darkred",
"darksalmon",
"darkseagreen",
"darkslateblue",
"darkslategray",
"darkslategrey",
"darkturquoise",
"darkviolet",
"deeppink",
"deepskyblue",
"dimgray",
"dimgrey",
"dodgerblue",
"firebrick",
"floralwhite",
"forestgreen",
"fuchsia",
"gainsboro",
"ghostwhite",
"gold",
"goldenrod",
"gray",
"grey",
"green",
"greenyellow",
"honeydew",
"hotpink",
"indianred",
"indigo",
"ivory",
"khaki",
"lavender",
"lavenderblush",
"lawngreen",
"lemonchiffon",
"lightblue",
"lightcoral",
"lightcyan",
"lightgoldenrodyellow",
"lightgray",
"lightgreen",
"lightgrey",
"lightpink",
"lightsalmon",
"lightseagreen",
"lightskyblue",
"lightslategray",
"lightslategrey",
"lightsteelblue",
"lightyellow",
"lime",
"limegreen",
"linen",
"magenta",
"maroon",
"mediumaquamarine",
"mediumblue",
"mediumorchid",
"mediumpurple",
"mediumseagreen",
"mediumslateblue",
"mediumspringgreen",
"mediumturquoise",
"mediumvioletred",
"midnightblue",
"mintcream",
"mistyrose",
"moccasin",
"navajowhite",
"navy",
"oldlace",
"olive",
"olivedrab",
"orange",
"orangered",
"orchid",
"palegoldenrod",
"palegreen",
"paleturquoise",
"palevioletred",
"papayawhip",
"peachpuff",
"peru",
"pink",
"plum",
"powderblue",
"purple",
"red",
"rosybrown",
"royalblue",
"saddlebrown",
"salmon",
"sandybrown",
"seagreen",
"seashell",
"sienna",
"silver",
"skyblue",
"slateblue",
"slategray",
"slategrey",
"snow",
"springgreen",
"steelblue",
"tan",
"teal",
"thistle",
"tomato",
"turquoise",
"violet",
"wheat",
"white",
"whitesmoke",
"yellow",
"yellowgreen"]

def main(HolyGrail):
	global app
	app = HolyGrail
	#creates stylesheet.txt if it doesn't exist
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","a") as f:
		f.close()
	#if stylesheet is empty, then it gets the default written to it
	if os.stat(os.getcwd() + "\\Settings\\StyleSheet.txt").st_size == 0:
		with open(os.getcwd() + "\\Settings\\StyleSheet.txt","a") as f:
			f.write(defaultSS)
			f.close()
	styleSheet = ""
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		for line in f:
			styleSheet += line
	#sets stylesheet for app
	QApplication.instance().setStyleSheet(styleSheet)
	#adds button for customizing stylesheet
	styleBtn = QAction('Styles', HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Settings"),objectName="Styles")
	styleBtn.triggered.connect(styleMenu)
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Settings").addAction(styleBtn)
#removes functionality
def end(HolyGrail):
	QApplication.instance().setStyleSheet("")
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Settings").removeAction(HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Settings").findChild(QAction,"Styles"))
	HolyGrail.findChild(QMenuBar,"Util Bar").findChild(QMenu,"Settings").findChild(QAction,"Styles").deleteLater()
	try:
		HolyGrail.findChild(QDockWidget,"Style Dock").close()
		HolyGrail.findChild(QDockWidget,"Style Dock").deleteLater()
	except:
		pass
#creates dock widget with comboboxes for editing styles
def styleMenu():
	global app
	try:
		app.findChild(QDockWidget,"Style Dock").close()
		app.findChild(QDockWidget,"Style Dock").deleteLater()
	except:
		pass
	styles = QGroupBox("",objectName="Style Options")
	grid = QGridLayout()
	grid.addWidget(QLabel("Background Color"),0,0)
	style1 = QComboBox()
	style1.addItems(colors)
	style1.activated.connect(backgroundColor)
	grid.addWidget(style1,0,1)
	grid.addWidget(QLabel("Font Color"),1,0)
	style2 = QComboBox()
	style2.addItems(colors)
	style2.activated.connect(fontColor)
	grid.addWidget(style2,1,1)
	grid.addWidget(QLabel("Border Color"),2,0)
	style3 = QComboBox()
	style3.addItems(colors)
	style3.activated.connect(borderColor)
	grid.addWidget(style3,2,1)
	grid.addWidget(QLabel("Button Border Color"),3,0)
	style3 = QComboBox()
	style3.addItems(colors)
	style3.activated.connect(buttonBorder)
	grid.addWidget(style3,3,1)
	style4 = QComboBox()
	style4.addItems(colors)
	style4.activated.connect(selectedBGColor)
	grid.addWidget(style4,4,1)
	grid.addWidget(QLabel("Selected background Color"),4,0)
	style5 = QComboBox()
	style5.addItems(colors)
	style5.activated.connect(selectedColor)
	grid.addWidget(style5,5,1)
	grid.addWidget(QLabel("Selected Font Color"),5,0)
	styles.setLayout(grid)
	styleWidget = QDockWidget('Style Options', app, objectName="Style Dock")
	styleWidget.setWidget(styles)
	app.addDockWidget(Qt.RightDockWidgetArea,styleWidget)
#edits font color of selected menus
def selectedColor(color):
	color = (colors[color])
	stylesheet = []
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		stylesheet = f.readlines()
		for i in range(0,len(stylesheet)):
			if "selected" not in stylesheet[i]:
				continue
			temp = stylesheet[i][stylesheet[i].index("{"):stylesheet[i].index("}")]
			temp = temp.split(";")
			for j in range(0,len(temp)):
				temp1 = temp[j].split(":")
				if "color" in temp1[0]:
					temp1[1] = color
				temp[j] = ":".join(temp1)
			temp = ";".join(temp)
			stylesheet[i] = stylesheet[i][0:stylesheet[i].index("{")] + temp + "}"
		f.close()
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","w") as f:
		f.writelines("\n".join(stylesheet))
		f.close()
	styleSheet = ""
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		for line in f:
			styleSheet += line
	QApplication.instance().setStyleSheet(styleSheet)
#edits background color of selected menus
def selectedBGColor(color):
	color = (colors[color])
	stylesheet = []
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		stylesheet = f.readlines()
		for i in range(0,len(stylesheet)):
			if "selected" not in stylesheet[i]:
				continue
			temp = stylesheet[i][stylesheet[i].index("{"):stylesheet[i].index("}")]
			temp = temp.split(";")
			for j in range(0,len(temp)):
				temp1 = temp[j].split(":")
				if "background" in temp1[0]:
					temp1[1] = color
				temp[j] = ":".join(temp1)
			temp = ";".join(temp)
			stylesheet[i] = stylesheet[i][0:stylesheet[i].index("{")] + temp + "}"
		f.close()
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","w") as f:
		f.writelines("\n".join(stylesheet))
		f.close()
	styleSheet = ""
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		for line in f:
			styleSheet += line
	QApplication.instance().setStyleSheet(styleSheet)
#sets background color of widgets
def backgroundColor(color):
	color = (colors[color])
	stylesheet = []
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		stylesheet = f.readlines()
		for i in range(0,len(stylesheet)):
			if "selected" in stylesheet[i]:
				continue
			temp = stylesheet[i][stylesheet[i].index("{"):stylesheet[i].index("}")]
			temp = temp.split(";")
			for j in range(0,len(temp)):
				temp1 = temp[j].split(":")
				if "background" in temp1[0]:
					temp1[1] = color
				temp[j] = ":".join(temp1)
			temp = ";".join(temp)
			stylesheet[i] = stylesheet[i][0:stylesheet[i].index("{")] + temp + "}"
		f.close()
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","w") as f:
		f.writelines("\n".join(stylesheet))
		f.close()
	styleSheet = ""
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		for line in f:
			styleSheet += line
	QApplication.instance().setStyleSheet(styleSheet)
#sets font color of widgets
def fontColor(color):
	color = (colors[color])
	stylesheet = []
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		stylesheet = f.readlines()
		for i in range(0,len(stylesheet)):
			if "selected" in stylesheet[i]:
				continue
			temp = stylesheet[i][stylesheet[i].index("{")+1:stylesheet[i].index("}")]
			temp = temp.split(";")
			for j in range(0,len(temp)):
				temp1 = temp[j].split(":")
				if "color" == temp1[0]:
					temp1[1] = color
				temp[j] = ":".join(temp1)
			temp = ";".join(temp)
			stylesheet[i] = stylesheet[i][0:stylesheet[i].index("{")+1] + temp + "}"
		f.close()
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","w") as f:
		f.writelines("\n".join(stylesheet))
		f.close()
	styleSheet = ""
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		for line in f:
			styleSheet += line
	QApplication.instance().setStyleSheet(styleSheet)
#changes color of most borders
def borderColor(color):
	color = (colors[color])
	stylesheet = []
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		stylesheet = f.readlines()
		for i in range(0,len(stylesheet)):
			temp = stylesheet[i][stylesheet[i].index("{")+1:stylesheet[i].index("}")]
			temp = temp.split(";")
			for j in range(0,len(temp)):
				temp1 = temp[j].split(":")
				if "border" == temp1[0]:
					temp1[1] = temp1[1].split(" ")
					temp1[1][2] = color
					temp1[1] = " ".join(temp1[1])
				temp[j] = ":".join(temp1)
			temp = ";".join(temp)
			stylesheet[i] = stylesheet[i][0:stylesheet[i].index("{")+1] + temp + "}"
		f.close()
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","w") as f:
		f.writelines("\n".join(stylesheet))
		f.close()
	styleSheet = ""
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		for line in f:
			styleSheet += line
	QApplication.instance().setStyleSheet(styleSheet)
#changes color of button borders
def buttonBorder(color):
	color = (colors[color])
	stylesheet = []
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		stylesheet = f.readlines()
		for i in range(0,len(stylesheet)):
			temp = stylesheet[i][stylesheet[i].index("{")+1:stylesheet[i].index("}")]
			temp = temp.split(";")
			for j in range(0,len(temp)):
				temp1 = temp[j].split(":")
				if "border-color" == temp1[0]:
					temp1[1] = color
				temp[j] = ":".join(temp1)
			temp = ";".join(temp)
			stylesheet[i] = stylesheet[i][0:stylesheet[i].index("{")+1] + temp + "}"
		f.close()
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","w") as f:
		f.writelines("\n".join(stylesheet))
		f.close()
	styleSheet = ""
	with open(os.getcwd() + "\\Settings\\StyleSheet.txt","r") as f:
		for line in f:
			styleSheet += line
	QApplication.instance().setStyleSheet(styleSheet)