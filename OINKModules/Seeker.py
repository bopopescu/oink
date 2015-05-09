#PigDog
from PyQt4 import QtGui, QtCore
from __future__ import division
import MySQLdb
import MySQLdb.cursorclass

class Seeker(QtGui.QDialog):
	def __init__(self):
		searcher = SearcherThread()
		self.createUI()
		searcher.foundSomething.connect(self.populateTable)
		searcher.sendProgress.connect(self.summarize)

	def createUI(self):
		self.label_fsns = QtGui.QLabel("FSNs:")
		self.text_edit_fsns = QtGui.QTextEdit()
		self.label_options = QtGui.QLabel("Options")
		self.combobox_options = QtGui.QComboBox()
		self.combobox_options.addItems(["Find","Filter Only Uniques"])
		self.button_process = QtGui.QPushButton("Process")
		self.table_output = QtGui.QTableWidget()
		self.progress_bar = QtGui.QProgressBar()
		progress_bar_style = """
            .QProgressBar {
                 text-align: center;
             }"""
		self.progress_bar.setStyleSheet(progress_bar_style)
	
	def summarize(self, activity, progress):
        self.progress_bar.setFormat("%s @ %s" %(activity, datetime.datetime.now()))
        self.progress_bar.setValue(int(progress*100))

    def populateTable(self, data):


class SearcherThread(QtCore.QThread):
	foundSomething = QtCore.pyqtSignal(list, str)
	sendProgress = QtCore.pyqtSignal(str, float)

	def __init__(self):
		QtCore.QThread.__init__(self)
		conn = MySQLdb.connect(host="172.17.188.139", user="bigbrother", passwd="orwell", db="oink", cursorclass=MySQLdb.cursors.DictCursor)
		cursor = conn.cursor()
	def __del__(self):
		conn.close()
	def run(self):
		self.mutex.unlock()
		self.mutex.lock()
	def find(self, fsns):
		data = []
		total = len(fsns)
		counter = 1
		for fsn in fsns:
			sqlcmdstring = """SELECT * FROM piggybank WHERE FSN="%s";""" %fsn
			cursor.execute(sqlcmdstring)
			d = cursor.fetchall()
			if len(d)>0:
				data.append(d)
				self.foundSomething.emit(data)
				self.sendProgress.emit("Processing", (counter/total))
			
			counter += 1
			
