from PyQt4 import QtGui, QtCore
import datetime
from AnimalFarm import AnimalFarm

class Taunter(QtGui.QTextEdit):
    def __init__(self):
        super(Taunter, self).__init__()
        self.quote_thread = AnimalFarm()
        self.quote_thread.quoteSent.connect(self.showText)
        self.setMaximumHeight(50)
        self.setReadOnly(True)
        style = """
            background-color: #F2F2F2;
            border: 0;
            font: 12px white;
        """
        self.setStyleSheet(style)
    def showText(self, text):
        self.setText("<font color='black'><i>%s:</i> </font><font color='#2E64FE'><b>%s</b></font>"%(datetime.datetime.now(), text))
        self.moveCursor(QtGui.QTextCursor.End)
        self.setToolTip(text)

