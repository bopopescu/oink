from PyQt4 import QtGui, QtCore
from OINKModules.AnimalFarm import AnimalFarm
import sys
class quoter(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
		self.label = QtGui.QLabel("Nothing yet.")
		style = """
		.QLabel {
			background-color: black;
			font: garamond;
			font-size: 14 px;
			color: white;
		}
		"""
		self.setStyleSheet(style)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.quote_thread = AnimalFarm()
		self.setCentralWidget(self.label)
		self.resize(1300,30)
		self.move(0,740)
		self.quote_thread.quoteSent.connect(self.updateLabel)
		self.show()
	def updateLabel(self, text):
		self.label.setText(text)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = quoter()

	sys.exit(app.exec_())
