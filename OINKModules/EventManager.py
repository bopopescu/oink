import os
import datetime
import numpy
from PyQt4 import QtCore, QtGui

import MOSES
from EventManagerThread import EventManagerThread

class EventManager(QtGui.QWidget):
	def __init__(self, user_id, password):
		QtGui.QWidget.__init__()
		self.event_manager_thread = EventManagerThread()
		self.createUI()
		self.mapEvents()
	def createUI(self):
		self.event_list = QtGui.QListWidget()

		self.event_form = QtGui.QWidget()
		self.layout = QtGui.QHBoxLayout()
		self.