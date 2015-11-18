from PyQt4 import QtGui, QtCore
from AnimalFarm import AnimalFarm

class Taunter(QtGui.QTextEdit):
    def __init__(self):
        super(Taunter, self).__init__()
        self.quote_thread = AnimalFarm()
        self.quote_thread.quoteSent.connect(self.showText)
        self.setMaximumHeight(50)
        self.setReadOnly(True)
    def showText(self, text):
        self.setText(text)
        self.moveCursor(QtGui.QTextCursor.End)
        self.setToolTip(text)

