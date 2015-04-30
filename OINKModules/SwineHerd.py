#SwineHerd
import time

from PyQt4 import QtCore
import pandas
import SWINE

class SwineHerd(QtCore.QThread):
	gotData = QtCore.pyqtSignal(dict)

	def __init__(self, FSN_list=None, retrieve=None):
		super(SwineHerd, self).__init__()
		self.mutex = QtCore.QMutex()
		if FSN_list is not None:
			self.FSNs = FSN_list
		else:
			self.FSNs = []
		self.condition = QtCore.QWaitCondition()
		if not self.isRunning():
			self.start(QtCore.QThread.LowPriority)

	def setFSNs(self, FSN_list):
		self.FSNs.append(FSN_list)

	def __del__(self):
		self.mutex.lock()
		self.condition.wakeOne()
		self.mutex.unlock()
		self.wait()

	def run(self):
		scraped_data_list = {}
		initial_FSN_list = []
		while True:
			old_list = scraped_data_list
			for FSN in self.FSNs:
				data = SWINE.scrapeFlipkart(FSN)
				scraped_data_list.update({FSN: data})
			if initial_FSN_list != self.FSNs:
				#If a new FSN has been added to the list, emit the scraped data.
				self.gotBrand.emit(scraped_data_list)
				initial_FSN_list = self.FSNs
			time.sleep(10)



