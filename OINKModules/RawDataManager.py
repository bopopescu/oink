from __future__ import division
import os
import math
import datetime
import sys

from PyQt4 import QtGui, QtCore
from CopiableQTableWidget import CopiableQTableWidget
from CheckableComboBox import CheckableComboBox
from CategorySelector import CategorySelector
from ImageButton import ImageButton
from FSNTextEdit import FSNTextEdit
from FilterForm import FilterForm

import MOSES

class RawDataManager(QtGui.QWidget):
	def __init__(self, user_id, password, *args, **kwargs):
		super(RawDataManager, self).__init__(*args, **kwargs)
		self.user_id, self.password = user_id, password
		self.createUI()
		self.mapEvents()

	def createUI(self):
		self.raw_data_filter_form = FilterForm()
		self.fsn_entry_field = FSNTextEdit()
		self.raw_data_table = CopiableQTableWidget(0,0)
		
		