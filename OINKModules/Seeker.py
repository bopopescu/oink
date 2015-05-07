#PigDog
from PyQt4 import QtGui, QtCore
import MOSES

class Seeker(QtGui.QDialog):
	def __init__(self):
		searcher = SearcherThread()

class SearcherThread(QtCore.QThread):
	foundSomething = QtCore.pyqtSignal(str, str, str, str)
