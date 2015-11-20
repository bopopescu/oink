from __future__ import division
import os
import sys
import random
import datetime

from PyQt4 import QtGui, QtCore
import pandas as pd

import MOSES
from ProgressBar import ProgressBar

class ArticleEntryForm(QtGui.QWidget):
	def __init__(self, user_id, password):
		super(FSNLineEdit, self)__init__()
		self.user_id, self.password = 