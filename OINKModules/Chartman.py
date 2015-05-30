from PyQt4 import QtGui, QtCore
from Graphinator import Graphinator

class Chartman(QtGui.QWidget):
	"""A Widget that displays the daily report
	graphs.
	"""
	def __init__(self):
		super(Chartman, self).__init__(self)
		self.createUI()
		self.createEvents()
		self.graphinator_thread = Graphinator()

	def createUI(self):
		
	def createEvents(self):
		self.graphinator_thread.compiledImages.connect(self.showGraphs)
		
	def changeDate(self, query_date):
		self.graphinator_thread.setNewDate(query_date)
		
	def showGraphs(self, file_names_list):
		
