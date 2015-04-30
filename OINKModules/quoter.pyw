from PyQt4 import QtGui
from OINKModules.AnimalFarm import AnimalFarm

class quoter(QtGui.QMainWindow):
	def __init__(self):
		self.label = QtGui.QLabel("Nothing yet.")
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.quote_thread = AnimalFarm()
		self.quote_thread.quoteSent.connect(self.updateLabel)
		self.show()
	def updateLabel(self, text):
		self.label.setText(text)

if __name__ == "__main__":
	app = QtGui.QApplication([])
	window = quoter()
	
	sys.exit(app.exec_())
