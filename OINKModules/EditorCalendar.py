#!usr/bin/python2
# -*- coding: utf-8 -*-
#Bacon Widget Class definition
from PyQt4 import QtGui

class EditorCalendar(QtGui.QCalendarWidget):
	def __init__(self):
		super(EditorCalendar, self).__init__()
		self.setMinimumSize(200,200)
		pass
