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

import MOSES

class RawDataManager(QtGui.QWidget):
    def __init__(self, user_id, password, *args, **kwargs):
        super(RawDataManager, self).__init__(*args, **kwargs)
        self.user_id, self.password = user_id, password
        self.createUI()
        self.mapEvents()

    def createUI(self):
        #self.raw_data_filter_form = FilterForm()
        self.fsn_entry_field = FSNTextEdit()
        self.raw_data_table = CopiableQTableWidget(0,0)
        self.upload_raw_data_button = QtGui.QPushButton("Upload Raw Data from File")
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.upload_raw_data_button)
        self.setLayout(layout)
        self.show()

    def mapEvents(self):
        self.upload_raw_data_button.clicked.connect(self.uploadRawData)

    def uploadRawData(self):
        data_file_name = str(QtGui.QFileDialog.getOpenFileName(self,"Open Data File",os.getcwd(),("MS Excel Spreadsheet (*.xlsx)")))
        if data_file_name is not None:
            if os.path.exists(data_file_name):
                xl_file = pd.ExcelFile(data_file_name)
                if "Raw Data" in xl_file.sheet_names:
                    raw_data_frame = xl_file.parse("Raw Data")
                    self.alertMessage("Success!","Read %d rows of Raw Data from the file."%raw_data_frame.shape[0])
                    accepted_rows, rejected_rows, failed_rows = MOSES.uploadRawDataFromDataFrame(self.user_id, self.password, raw_data_frame)
                    message = "Successfully uploaded %d of %d rows of raw data into the server. %d were rejected by editors and uploaded into the rejected raw data table, and %d failed."%(accepted_rows, raw_data_frame.shape[0], rejected_rows, failed_rows)
                    print message
                    self.alertMessage("Done!" ,message)
                else:
                    self.alertMessage("Invalid raw data file.","""The given raw data file doesn't seem to have any sheet named "Raw Data".""")
    
    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

