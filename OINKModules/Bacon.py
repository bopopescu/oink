#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
import datetime
import sys
import math

from PyQt4 import QtGui, QtCore

from PassResetDialog import PassResetDialog
from OINKMethods import version
from ProgressBar import ProgressBar
from AuditPercentageMonitor import AuditPercentageMonitor
from QualityAnalyser import QualityAnalyser
from EditorMetricsViewer import EditorMetricsViewer
from EditorCalendar import EditorCalendar
from AuditToolBox import AuditToolBox
from ImageLabel import ImageLabel
from ImageButton import ImageButton
from TNAViewer import TNAViewer
from PiggyBankWithFilter import PiggyBankWithFilter
from RawDataManager import RawDataManager
from Seeker import Seeker
import MOSES
from Taunter import Taunter


class Bacon(QtGui.QMainWindow):
    """"""
    def __init__(self, user_id, password, category_tree, employees_list, brand_list):
        super(Bacon, self).__init__()
        self.user_id = user_id
        self.password = password
        self.category_tree = category_tree
        self.employees_list = employees_list
        self.brand_list = brand_list
        self.current_processing_date = MOSES.getLastWorkingDate(self.user_id, self.password,datetime.date.today(),"All")
        self.createUI()
        self.mapEvents()
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def createUI(self):
        """"""
        path_to_images = MOSES.getPathToImages()
        self.raw_data_uploader_button = ImageButton(
                                                os.path.join(path_to_images,"upload_raw_data.png"),
                                                48,
                                                48, os.path.join(path_to_images,"upload_raw_data_mouseover.png"))
        self.tna_viewer_button = ImageButton(
                                                os.path.join(path_to_images,"tna.png"),
                                                48,
                                                48,
                                                os.path.join(path_to_images,"tna_mouseover.png")
                                                )
        self.piggybank_button = ImageButton(
                                                os.path.join(path_to_images,"piggybank.png"),
                                                48,
                                                48,
                                                os.path.join(path_to_images,"piggybank_mouseover.png")
                                                )
        self.seeker_button = ImageButton(
                                                os.path.join(path_to_images,"find.png"),
                                                48,
                                                48,
                                                os.path.join(path_to_images,"find_mouseover.png")
                                                )

        self.taunter = Taunter()
        self.bacon_icon = ImageButton(
                                                os.path.join(path_to_images,"quality.png"),
                                                150,
                                                150,
                                                os.path.join(path_to_images,"quality_mouseover.png")
                                                )
        self.bacon_icon.setToolTip("Get to work, Poozers.")
        
        row_1 = QtGui.QHBoxLayout()
        row_1.addWidget(self.raw_data_uploader_button)
        row_1.addWidget(self.tna_viewer_button)
        row_1.addWidget(self.piggybank_button)
        row_1.addWidget(self.seeker_button)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.bacon_icon,0,QtCore.Qt.AlignHCenter)
        layout.addLayout(row_1,1)
        layout.addWidget(self.taunter,0)

        self.main_widget = QtGui.QWidget()
        self.main_widget.setLayout(layout)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("BACON - Version %s. Server: %s. User: %s (%s)."%(version(), MOSES.getHostID(), self.user_id,MOSES.getEmpName(self.user_id) if self.user_id != "bigbrother" else "Administrator"))
        icon_file_name_path = os.path.join(path_to_images,'PORK_Icon.png')
        self.setWindowIcon(QtGui.QIcon(icon_file_name_path))
        self.show()

    def mapEvents(self):
        """"""
        self.raw_data_uploader_button.clicked.connect(self.openRawDataManager)
        self.piggybank_button.clicked.connect(self.openPiggyBank)
        self.tna_viewer_button.clicked.connect(self.openTNAViewer)
        self.seeker_button.clicked.connect(self.openSeeker)
    
    def openRawDataManager(self):
        self.raw_data_manager = RawDataManager(self.user_id, self.password)

    def openPiggyBank(self):
        self.piggy_bank = PiggyBankWithFilter(self.user_id, self.password, self.category_tree, self.brand_list)

    def openTNAViewer(self):
        self.tna_viewer = TNAViewer(self.user_id, self.password, self.category_tree)
    def openSeeker(self):
        self.seeker = Seeker(self.user_id, self.password)



if __name__ == "__main__":
    u, p = MOSES.getBigbrotherCredentials()
    app = QtGui.QApplication(sys.argv)
    QtGui.qApp.setStyle(QtCore.QString(u'Plastique'))
    bacon = Bacon(u,p)
    sys.exit(app.exec_())



