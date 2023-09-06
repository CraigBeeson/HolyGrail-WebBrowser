from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

#class from the code editor example
class LineNumberArea(QWidget):
	def __init__(self,*args,**kwargs):
		super(LineNumberArea,self).__init__()
		self.setParent(args[0])
	
	def sizeHint(self):
		return QSize(self.parent().lineNumberAreaWidth(), 0)

	def paintEvent(self,event):
		self.parent().lineNumberAreaPaintEvent(event)