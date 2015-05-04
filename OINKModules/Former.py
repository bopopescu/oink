import time

from PyQt4 import QtCore

import MOSES

class Former(QtCore.QThread):
	"""
"""
	gotBUValues = QtCore.pyqtSignal(list)
	gotSupCValues = QtCore.pyqtSignal(list)
	gotCatValues = QtCore.pyqtSignal(list)
	gotSubCValues = QtCore.pyqtSignal(list)
	gotVertValues = QtCore.pyqtSignal(list)
	gotBrandValues = QtCore.pyqtSignal(list)
	gotProgress = QtCore.pyqtSignal(int, str)
	def __init__(self, userID, password, BU=None, SupC=None, Cat=None, SubC=None, Vert=None, Brand=None):
		super(Former, self).__init__()
		self.userID = userID
		self.password = password
		self.BU = None if BU is None else BU
		self.SupC = None if SupC is None else SupC
		self.Cat = None if Cat is None else Cat
		self.SubC = None if Cat is None else Cat
		self.Vert = None if Vert is None else Vert
		self.Brand = None if Brand is None else Brand
		self.mutex = QtCore.QMutex()
		self.condition = QtCore.QWaitCondition()
		if not self.isRunning():
			self.start(QtCore.QThread.LowPriority)

	def __del__(self):
		self.mutex.lock()
		self.condition.wakeOne()
		self.mutex.unlock()
		self.wait()

	def run(self):
		self.mutex.unlock()
		self.getAll(self.BU, self.SupC, self.Cat, self.SubC, self.Vert, self.Brand)
		self.mutex.lock()

	def getAll(self, BU=None, SupC=None, Cat=None, SubC=None, Vert=None, Brand=None):
		#I don't know why I'll need to push brand here. I'll plan something later.
		self.getBUValues()
		self.getSupCValues(BU)
		self.getCatValues(SupC)
		self.getSubCValues(Cat)
		self.getVertValues(SubC)
		self.getBrandValues()

	def getBUValues(self):
		BU_values = MOSES.getBUValues(self.userID, self.password)
		#print "BU: ", len(BU_values)
		self.gotBUValues.emit(BU_values)
	
	def getSupCValues(self, BU=None):
		SupC_values = MOSES.getSuperCategoryValues(self.userID, self.password)
		#print "Super-Category: ", len(SupC_values)
		self.gotSupCValues.emit(SupC_values)

	def getCatValues(self, SupC = None):
		Cat_values = MOSES.getCategoryValues(self.userID, self.password)
		#print "Category: ", len(Cat_values)
		self.gotCatValues.emit(Cat_values)
	
	def getSubCValues(self, Cat = None):
		SubC_values = MOSES.getSubCategoryValues(self.userID, self.password)
		#print "Sub-Category: ", len(SubC_values)
		self.gotSubCValues.emit(SubC_values)

	def getVertValues(self, SubC = None):
		Vert_values = MOSES.getVerticalValues(self.userID, self.password)
		#print "Verticals: ", len(Vert_values)
		self.gotVertValues.emit(Vert_values)
	
	def getBrandValues(self, Vert = None):
		Brand_values = MOSES.getBrandValues(self.userID, self.password)
		#print "Brand: ", len(Brand_values)
		self.gotBrandValues.emit(Brand_values)
	