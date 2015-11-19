#!/usr/bin/python2
# -*- coding: utf-8 -*-
import itertools
import math
import datetime
import os

import numpy
import matplotlib
import pandas as pd

from PyQt4 import QtGui, QtCore
from PassResetDialog import PassResetDialog
from EfficiencyCalculator import EfficiencyCalculator
from DateSelectorWidget import DateSelectorWidget
from FilterBox import FilterBox
from PiggyBank import PiggyBank
from PiggyBanker import PiggyBanker
from Former import Former
from DailyPorker import DailyPorker
from OINKMethods import version
from Seeker import Seeker
from Graphite import Graphite
#from StyCleaner import StyCleaner
from FarmHand import FarmHand
from PiggyBankWithFilter import PiggyBankWithFilter
from SwineHerd import SwineHerd
from ImageButton import ImageButton
from IconButton import IconButton
from TNAViewer import TNAViewer
from UserManager import UserManager
from OverrideTool import OverrideTool
from RawDataManager import RawDataManager
from LeaveApproval import LeaveApproval
from Taunter import Taunter
import MOSES

class Vindaloo(QtGui.QMainWindow):
    def __init__(self, user_id, password, category_tree=None, employees_list=None, brand_list=None):
        super(QtGui.QMainWindow,self).__init__()
        self.user_id = user_id
        self.password = password
        if category_tree is None:
            self.category_tree = MOSES.getCategoryTree(self.user_id, self.password)
        else:
            self.category_tree = category_tree
        if employees_list is None:
            self.employees_list = MOSES.getEmployeesList(self.user_id, self.password)
        else:
            self.employees_list = employees_list
        if brand_list is None:
            self.brand_list = MOSES.getBrandValues(self.user_id, self.password)
        else:
            self.brand_list = brand_list 

        MOSES.createLoginStamp(self.user_id, self.password)
        self.createUI()

    def makeButton(self, label, button_image_base_name, tooltip, connected_function):
        width, height = 40, 40
        button = IconButton(
                            label, 
                            os.path.join("Images","%s.png"%button_image_base_name),
                            width, 
                            height,
                            os.path.join("Images","%s_mouseover.png"%button_image_base_name)
                        )
        button.setToolTip(tooltip)
        button.setFlat(True)
        button.clicked.connect(connected_function)
        return button

    def createUI(self):
        self.main_widget = QtGui.QWidget()
        self.setCentralWidget(self.main_widget)

        self.daily_porker_button = self.makeButton(
                                                "Reports",
                                                "newspaper",
                                                "Click here to pull reports.", 
                                                self.openDailyPorker
                                            )
        self.seeker_button = self.makeButton(
                                        "Find FSNs",
                                        "find",
                                        "Click here to search for an FSN or ItemID in the PiggyBank and FSN Dump.", 
                                        self.openSeeker
                                       )
        self.sty_cleaner_button = self.makeButton(
                                            "Clarifications",
                                            "stycleaner",
                                            "Click here to summarize the clarifications sheet.", 
                                            self.openStyCleaner
                                        )
        self.farmhand_button = self.makeButton(
                                            "Helpfulness",
                                            "farmhand",
                                            "Click here to view feedback report(s).", 
                                            self.openFarmHand
                                        )
        self.piggy_bank_button = self.makeButton(
                                            "Piggy Bank",
                                            "piggybank",
                                            "Click here to pull Piggy Bank data.", 
                                            self.openPiggyBank
                                        )
        self.calc_button = self.makeButton(
                                        "Efficiency Calculator",
                                        "calculator",
                                        "Click to open the Efficiency Calculator.", 
                                        self.openCalculator
                                    )
        self.leaves_button = self.makeButton(
                                        "Leave and Relaxations",
                                        "leave",
                                        "Click to open the leave and relaxation approval system.", 
                                        self.openLeaveManager
                                    )
        self.tna_button = self.makeButton(
                                        "Training Needs Analysis",
                                        "tna",
                                        "Click to open the training needs analysis tool.",
                                        self.openTNAViewer
                                    )
        self.user_management_button = self.makeButton(
                                                    "User Management",
                                                    "users",
                                                    "Click to open the user management tool.",
                                                    self.openUserManagement
                                                )
        self.category_tree_button = self.makeButton(
                                                "Targets and Category Tree",
                                                "category_tree",
                                                "Click to open the category tree manager.",
                                                self.openCategoryTreeManager
                                            )
        self.override_button = self.makeButton(
                                            "Approve FSN Override",
                                            "override",
                                            "Click to open the FSN override tool and allow writers to report FSNs that have already been worked on", 
                                            self.openOverrideTool
                                        )
        self.upload_raw_data_button = self.makeButton(
                                                "Upload Raw Data",
                                                "upload_raw_data",
                                                "Click to upload Raw Data.", 
                                                self.openRawDataUploader)

        buttons_layout = QtGui.QHBoxLayout()

        layout = QtGui.QGridLayout()
        layout.addWidget(self.daily_porker_button, 0, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        layout.addWidget(self.piggy_bank_button, 0, 1, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        layout.addWidget(self.tna_button, 0, 2, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        layout.addWidget(self.calc_button, 0, 3, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        layout.addWidget(self.leaves_button, 0, 4, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        layout.addWidget(self.override_button, 1, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        layout.addWidget(self.user_management_button,1,1, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        layout.addWidget(self.category_tree_button,1,2, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        layout.addWidget(self.farmhand_button, 1, 3, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        #layout.addWidget(self.head_count_button, 2, 0)
        layout.addWidget(self.seeker_button, 1, 4, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        layout.addWidget(self.sty_cleaner_button, 2, 1, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        layout.addWidget(self.upload_raw_data_button, 2, 2, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        layout.addWidget(Taunter(),3,0,1,5, QtCore.Qt.AlignTop)

        self.main_widget.setLayout(layout)

        self.setWindowTitle("VINDALOO - %s, Server: %s, User: %s (%s)" %(MOSES.version(),MOSES.getHostID(), self.user_id, MOSES.getEmpName(self.user_id) if self.user_id != "bigbrother" else "Administrator"))
        self.resize(500, 100)
        self.center()
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('Images\PORK_Icon.png'), self)
        self.trayIcon.show()
        self.statusBar().showMessage("Send not to ask for whom the bell tolls. It tolls for thee...")
        style_string = """
        .QWidget, .QPushButton, .QStatusBar, .QMessageBox, .QLabel{
            background-color: #0088D6;
            color: white;
            font: 10pt;
        }
        .QWidget, .QPushButton{
            font: 14pt;
        }
        .QStatusBar {
            background-color: #FDDE2E;
            color: #0088D6;
            font: italic 10pt;
        }
        .QPushButton:hover {
            background-color: #FDDE2E;
            color: #0088D6;
            font: 14pt;
        }
        """
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowShadeButtonHint)
        #self.setStyleSheet(style_string)
        self.show()
    
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
    
    def openCategoryTreeManager(self):
        self.alertMessage("Category Manager.","This feature is Unavailable.")

    def openRawDataUploader(self):
        self.raw_data_manager = RawDataManager(self.user_id, self.password)
        self.raw_data_manager.show()

    def openOverrideTool(self):
        self.overrider = OverrideTool(self.user_id, self.password)

    def openTNAViewer(self):
        self.alertMessage("TNA Viewer.","This feature is still in development, some features may not work as expected.")
        self.tna_viewer = TNAViewer(self.user_id, self.password, self.category_tree)

    def openCalculator(self):
        self.calc = EfficiencyCalculator(self.user_id, self.password, self.category_tree)

    def openEscalationTracker(self):
        self.alertMessage("Feature Unavailable.","This feature is Unavailable.")

    def openRelaxationTracker(self):
        self.alertMessage("Feature Unavailable.","This feature is Unavailable.")
    
    def openLeaveManager(self):
        self.leave_manager = LeaveApproval(self.user_id, self.password)
    
    def openUserManagement(self):
        self.alertMessage("User Manager.","This feature is still in development, some features may not work as expected.")
        self.user_manager = UserManager(self.user_id, self.password)
        self.user_manager.show()

    def openPiggyBank(self):
        self.piggy_bank = PiggyBankWithFilter(self.user_id, self.password, self.category_tree, self.brand_list)
        self.piggy_bank.show()
    
    def openDailyPorker(self):
        self.daily_porker = DailyPorker(self.user_id, self.password, self.category_tree)
        self.daily_porker.show()

    def openFarmHand(self):
        self.farm_hand = FarmHand(self.user_id, self.password)
        self.farm_hand.show()
    
    def openStyCleaner(self):
        self.alertMessage("StyCleaner", "Sty Cleaner has been disabled. Contact admin, or use the stycleaner.py file in the OINKMethods folder in the source to run it.")
        #self.sty_cleaner = ()
        #self.sty_cleaner.show()
        
    def openSeeker(self):
        self.seeker = Seeker(self.user_id, self.password)
        self.seeker.show()
        
    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    def notify(self,title,message):
        self.trayIcon.showMessage(title,message)

    def closeEvent(self,event):
        self.askToClose = QtGui.QMessageBox.question(self, 'Close VINDALOO?', "Are you sure you'd like to quit?\nVindaloo was developed for TLs to extract data effortlessly from the OINK database.\nKeep Vindaloo open if you want to be able to extract data from the Piggy Bank, get reports, plot daily graphs and find data in the OINK Database.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if self.askToClose == QtGui.QMessageBox.Yes:
            MOSES.createLogoutStamp(self.user_id, self.password)
            super(Vindaloo, self).closeEvent(event)
        else:
            event.ignore()


if __name__ == "__main__":
    print "Not allowed."