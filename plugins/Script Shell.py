import code
import threading
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

toolTip = "Enables Python\nInterpreter."
shell = None
app = None

def main(HolyGrail):
	global shell
	global app
	app = HolyGrail
	#create and then start qthread that runs the interpreter
	shell = Shell()
	shell.start()
#closes and deletes thread holding object
def end(HolyGrail):
	global shell
	shell.terminate()
	shell.deleteLater()
	print("Interpreter Closed")
#custom qthread class to run the interpreter
class Shell(QThread):
	global app
	def run(self):
		#code lib used for interactive console
		code.InteractiveConsole(locals=globals()).interact(banner="Holy Grail Interpreter\n[*] Use 'app' to reference mainwindow [*]")