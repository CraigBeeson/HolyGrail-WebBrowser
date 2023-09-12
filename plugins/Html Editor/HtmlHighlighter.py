from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

class HtmlHighlighter(QSyntaxHighlighter):
	def highlightBlock(self, text):
		#format for text inside html < > tags
		tagsFormat = QTextCharFormat()
		tagsFormat.setForeground(QColor("darkorange"))
		#expression for any sub strings that start and end with '<' '>'
		expression = QRegularExpression("<.*>")
		#creates iterable of matches
		i = expression.globalMatch(text)
		while i.hasNext():
			match = i.next()
			#sets format
			self.setFormat(match.capturedStart(), match.capturedLength(), tagsFormat)
		#format for text outside of tags
		equalFormat = QTextCharFormat()
		equalFormat.setForeground(QColor("white"))
		expression = QRegularExpression("=")
		i = expression.globalMatch(text)
		while i.hasNext():
			match = i.next()
			self.setFormat(match.capturedStart(), match.capturedLength(), equalFormat)
		#format for text inside of ' " '
		stringFormat = QTextCharFormat()
		stringFormat.setForeground(QColor("mediumseagreen"))
		expression = QRegularExpression("\".*\"")
		i = expression.globalMatch(text)
		while i.hasNext():
			match = i.next()
			self.setFormat(match.capturedStart(), match.capturedLength(), stringFormat)
		#format for text inside of " ' "
		stringFormat = QTextCharFormat()
		stringFormat.setForeground(QColor("mediumseagreen"))
		expression = QRegularExpression("'.*'")
		i = expression.globalMatch(text)
		while i.hasNext():
			match = i.next()
			self.setFormat(match.capturedStart(), match.capturedLength(), stringFormat)
		#format for script tags
		stringFormat = QTextCharFormat()
		stringFormat.setForeground(QColor("deepskyblue"))
		expression = QRegularExpression("<script>.*</script>")
		i = expression.globalMatch(text)
		while i.hasNext():
			match = i.next()
			self.setFormat(match.capturedStart(), match.capturedLength(), stringFormat)
		#format for php tags
		stringFormat = QTextCharFormat()
		stringFormat.setForeground(QColor("violet"))
		expression = QRegularExpression("<?.*?>")
		i = expression.globalMatch(text)
		while i.hasNext():
			match = i.next()
			self.setFormat(match.capturedStart(), match.capturedLength(), stringFormat)
		#format for html comments
		stringFormat = QTextCharFormat()
		stringFormat.setForeground(QColor("lightpink"))
		expression = QRegularExpression("<!--.*-->")
		i = expression.globalMatch(text)
		while i.hasNext():
			match = i.next()
			self.setFormat(match.capturedStart(), match.capturedLength(), stringFormat)