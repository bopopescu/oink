from __future__ import division
import os
import datetime

from PyQt4 import QtGui, QtCore
import pandas as pd

from CheckableComboBox import CheckableComboBox
from CopiableQTableWidget import CopiableQTableWidget
import MOSES

class LeaveApproval(QtGui.QWidget):
	def __init__(self, user_id, password):
		super(LeaveApproval, self).__init__()
		self.user_id, self.password = user_id, password
		pass