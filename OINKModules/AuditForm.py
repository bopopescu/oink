from __future__ import division
import os
import datetime
import math
from PyQt4 import QtGui
import MOSES


class AuditForm(QtGui.QWidget):
	"""Audit form for use with Bacon."""
	def __init__(self, user_id, password):
		super(AuditForm, self).__init__()
		self.user_id, self.password = user_id, password
		self.createUI()
		self.mapEvents()
		self.