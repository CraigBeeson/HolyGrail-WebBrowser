from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

from . import HtmlHighlighter
from . import LineNumbers

class HtmlEditor(QPlainTextEdit):
	
	def __init__(self, *args, **kwargs):
		super(HtmlEditor, self).__init__()
		#assigns a highlighter for syntax highlighting
		self.highlighter = HtmlHighlighter.HtmlHighlighter(self.document())
		self.file = ""
		#also code from the qt code editor example
		self.lines = LineNumbers.LineNumberArea(self)
		self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
		self.updateRequest.connect(self.updateLineNumberArea)
		self.cursorPositionChanged.connect(self.highlightCurrentLine)
		self.updateLineNumberAreaWidth(0)
		self.highlightCurrentLine()
	#saves the contents of the text editor to the associated file
	def saveText(self):
		if self.file:
			with open(self.file,"w") as f:
				f.write(self.toPlainText())
				f.close()
		else:
			fileDialog = QFileDialog(self,"Holy Grail - Choose HTML Page",self.parent().parent().filePath)
			fileDialog.setFileMode(QFileDialog.AnyFile)
			if fileDialog.exec_():
				self.file = fileDialog.selectedFiles()[0]
				with open(self.file,"w") as f:
					f.write(self.toPlainText())
					f.close()
			self.parent().parent().setTabText(self.parent().currentIndex(),self.file.split("/")[-1])
			self.parent().parent().updateFilePath.emit("/".join(self.file.split("/")[0:len(self.file.split("/"))-1]))

#code below is copied from https://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html
#######################################################
	def lineNumberAreaWidth(self):
		digits = 1
		maxLines = max(1, self.blockCount())
		while (maxLines >= 10):
			maxLines /= 10
			digits += 1
		space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
		
		return space
	
	def updateLineNumberAreaWidth(self,integer):
		self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
	
	def updateLineNumberArea(self,rect,dy):
		if dy:
			self.lines.scroll(0, dy)
		else:
			self.lines.update(0, rect.y(), self.lines.width(), rect.height())
		if (rect.contains(self.viewport().rect())):
			self.updateLineNumberAreaWidth(0)
	
	def resizeEvent(self,e):
		cr = self.contentsRect()
		self.lines.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
		
	def highlightCurrentLine(self):
		extraSelections = list()
		if (not self.isReadOnly()):
			selection = QTextEdit().ExtraSelection()
			lineColor = QColor(Qt.black)
			lineColor.setAlpha(50)
			selection.format.setBackground(lineColor)
			selection.format.setProperty(QTextFormat.FullWidthSelection, True)
			selection.cursor = self.textCursor()
			selection.cursor.clearSelection()
			extraSelections.append(selection)
		self.setExtraSelections(extraSelections)
		
	def lineNumberAreaPaintEvent(self,event):
		painter = QPainter(self.lines)
		painter.fillRect(event.rect(), Qt.lightGray)
		block = self.firstVisibleBlock()
		blockNumber = block.blockNumber()
		top = qRound(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
		bottom = top + qRound(self.blockBoundingRect(block).height())
		while block.isValid() and top <= event.rect().bottom():
			if block.isVisible() and bottom >= event.rect().top():
				number = str(blockNumber+1)
				painter.setPen(Qt.black)
				painter.drawText(0, top, self.lines.width(), self.fontMetrics().height(), Qt.AlignRight, number)
				
			block = block.next()
			top = bottom
			bottom = top + qRound(self.blockBoundingRect(block).height())
			blockNumber += 1
			