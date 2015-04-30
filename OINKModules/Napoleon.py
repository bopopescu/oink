import sys
import os
import datetime as dt

from PyQt4 import QtGui, QtCore

class Napoleon(QtGui.QMainWindow):
	"""Napoleon Class Definition.
	Napoleon includes a set of tools for Bigbrother, including options to launch PORK, BACON, VINDALOO,
	to rebuild the database, to take backups, to send mails of backups etc.
	"""
	def __init__(self, userID, password):
		super(QtGui.QMainWindow, self).__init__()
		self.create_widgets()
		self.userID, self.password = userID, password

	def create_widgets():
		self.pork_button = QtGui.QPushButton("PORK")
		self.vindaloo_button = QtGui.QPushButton("Vindaloo")
		self.bacon_button = QtGui.QPushButton("Bacon")
		self.host_id_label = QtGui.QLabel("Host ID:")
		self.host_id = QtGui.QLabel("Shows Host ID")
		self.host_id_change_button = QtGui.QPushButton("Change Host ID")
		self.user_management_button = QtGui.QPushButton("Open User Management")
		self.connection_monitor = QtGui.QPushButton("View Server Connection Statuses")
