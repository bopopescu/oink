from __future__ import division
import os
import math
import datetime
import sys
import pandas as pd
import xlsxwriter

from PyQt4 import QtGui, QtCore
from CopiableQTableWidget import CopiableQTableWidget
from CheckableComboBox import CheckableComboBox
from CategorySelector import CategorySelector
from ImageButton import ImageButton
from FSNTextEdit import FSNTextEdit
from FilterForm import FilterForm
from RawDataUploaderThread import RawDataUploaderThread
from ProgressBar import ProgressBar

class RawDataManager(QtGui.QWidget):
    def __init__(self, user_id, password, *args, **kwargs):
        super(RawDataManager, self).__init__(*args, **kwargs)
        self.user_id, self.password = user_id, password
        self.raw_data_thread = RawDataUploaderThread(self.user_id, self.password)
        self.createUI()
        self.mapEvents()

    def createUI(self):
        #self.raw_data_filter_form = FilterForm()
        self.fsn_entry_field = FSNTextEdit()
        self.raw_data_table = CopiableQTableWidget(0,0)
        self.upload_raw_data_button = QtGui.QPushButton("Upload Raw Data from File")
        self.progress_bar = ProgressBar()
        self.progress_log = QtGui.QTextEdit()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.upload_raw_data_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_log)
        self.setLayout(layout)
        self.setWindowTitle("Raw Data Uploader")
        #self.setIcon(QtGui.QIcon(os.path.join(MOSES.getPathToImages,"PORK_Icon.png")))
        self.show()

    def mapEvents(self):
        self.upload_raw_data_button.clicked.connect(self.uploadRawData)
        self.raw_data_thread.sendActivity.connect(self.displayActivity)
        self.raw_data_thread.sendMessage.connect(self.displayMessage)

    def displayActivity(self, progress, eta, accepted, rejected, failed, pending):
        self.progress_bar.setValue(progress)
        message = "%d Accepted, %d Rejected, %d Failed, %d Pending. ETA: %s"%(accepted, rejected, failed, pending, eta)
        self.displayMessage(message)

    def displayMessage(self, message):
        self.progress_log.append("%s: <b>%s</b>"%(datetime.datetime.now(),message))
        self.progress_log.moveCursor(QtGui.QTextCursor.End)


    def uploadRawData(self):
        self.upload_raw_data_button.setEnabled(False)
        data_file_name = str(QtGui.QFileDialog.getOpenFileName(self,"Open Data File",os.getcwd(),("MS Excel Spreadsheet (*.xlsx)")))
        if data_file_name is not None:
            if os.path.exists(data_file_name):
                xl_file = pd.ExcelFile(data_file_name)
                if "Raw Data" in xl_file.sheet_names:
                    raw_data = xl_file.parse("Raw Data")
                    self.raw_data_thread.setDataFrame(raw_data)
                else:
                    self.alertMessage("Invalid raw data file.","""The given raw data file doesn't seem to have any sheet named "Raw Data".""")
                    
    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

