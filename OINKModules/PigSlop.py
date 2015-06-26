from PyQt4 import QtGui, QtCore


class PigSlop():
	def __init__(self):
		super(PigSlop,self).__init__()
	def createUI(self):
	def populateReport(self):
	def limitEndDate(self):

class SlopServer(QtCore.QThread):
	gotFeedbackSummary() = QtCore.pyqtSignal(list)
	gotProgress() = QtCore.pyqtSignal()
	def __init__(self):
	def run(self):
	def __del__(self):
	def getFeedbackBetween(self, start_date, end_date, entity_type = None):
	def getHelpfulnessDataBetween(self, start_date, end_date, entity_type)