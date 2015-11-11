import os
import sys
import math
import time
import glob
from __future__ import division
import datetime

from PyQt4 import QtGui, QtCore
from ImageButton import ImageButton

class SharinganButton(ImageButton):
	def __init__(self, *args, **kwargs):
		super(SharinganButton, self).__init__(*args, **kwargs)
		self.createUI()
		self.mapEvents()
	def createUI(self):
		self.show()
	def mapEvents(self):
		pass
