#!/usr/bin/python2
# -*- coding: utf-8 -*-
import itertools
import math
import datetime
import os

import numpy
import matplotlib

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
from StyCleaner import StyCleaner
from FarmHand import FarmHand
from PiggyBankWithFilter import PiggyBankWithFilter
from SwineHerd import SwineHerd
from ImageButton import ImageButton

import MOSES

class Vindaloo(QtGui.QMainWindow):
    def __init__(self, user_id, password):
        super(QtGui.QMainWindow,self).__init__()
        self.user_id = user_id
        self.password = password
        self.category_tree = MOSES.getCategoryTree(self.user_id, self.password)
        MOSES.createLoginStamp(self.user_id, self.password)
        self.createUI()
        self.createEvents()

    def createUI(self):
        self.main_widget = QtGui.QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.daily_porker_button = QtGui.QPushButton("Daily Porker")
        self.daily_porker_button.setToolTip("Click here to pull the report.")
        self.seeker_button = QtGui.QPushButton("Seeker")
        self.seeker_button.setToolTip("Click here to search for an FSN or ItemID in the PiggyBank and FSN Dump.")
        self.sty_cleaner_button = QtGui.QPushButton("Sty Cleaner")
        self.sty_cleaner_button.setToolTip("Click here to summarize the clarifications sheet.")
        self.farmhand_button = QtGui.QPushButton("Farm Hand")
        self.farmhand_button.setToolTip("Click here to view feedback report(s).")
        self.piggy_bank_button = QtGui.QPushButton("Piggy Bank")
        self.piggy_bank_button.setToolTip("Click here to pull Piggy Bank data.")
        self.swine_herd_button = QtGui.QPushButton("Swine Herd")
        self.swine_herd_button.setToolTip("Click here to view the Head Count Report")
        self.swine_button = QtGui.QPushButton("Swine")
        self.swine_button.setToolTip("Click here to get data and images from Flipkart.")

        self.calc_button = ImageButton(os.path.join("Images","calculator.png"),48, 48, os.path.join("Images","calculator_mouseover.png"))
        self.calc_button.setToolTip("Click to open the Efficiency Calculator")
        self.calc_button.setFlat(True)

        self.leaves_button = ImageButton(os.path.join("Images","leave.png"), 48, 48, os.path.join("Images","leave_mouseover.png"))
        self.leaves_button.setToolTip("Click to open the leave approval system")
        self.leaves_button.setFlat(True)

        self.tna_button = ImageButton(os.path.join("Images","tna.png"),48, 48, os.path.join("Images","tna_mouseover.png"))
        self.tna_button.setToolTip("Click to open the training needs analysis tool")
        self.tna_button.setFlat(True)

        self.relaxation_button = ImageButton(os.path.join("Images","relaxation.png"),48, 48, os.path.join("Images","relaxation_mouseover.png"))
        self.relaxation_button.setToolTip("Click to open the relaxation approval system")
        self.relaxation_button.setFlat(True)

        self.escalation_button = ImageButton(os.path.join("Images","alert.png"), 48, 48, os.path.join("Images","alert_mouseover.png"))
        self.escalation_button.setToolTip("Click to open the escalation tracker")
        self.escalation_button.setFlat(True)

        buttons_layout = QtGui.QHBoxLayout()
        buttons_layout.addWidget(self.calc_button, 0)
        buttons_layout.addWidget(self.leaves_button, 0)
        buttons_layout.addWidget(self.tna_button, 0)
        buttons_layout.addWidget(self.relaxation_button, 0)
        buttons_layout.addWidget(self.escalation_button, 0)


        self.layout = QtGui.QGridLayout()
        self.layout.addLayout(buttons_layout, 0,0,1,3, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.daily_porker_button, 1, 0)
        self.layout.addWidget(self.farmhand_button, 1, 1)
        self.layout.addWidget(self.piggy_bank_button, 1, 2)
        self.layout.addWidget(self.swine_herd_button, 2, 0)
        self.layout.addWidget(self.seeker_button, 2, 1)
        self.layout.addWidget(self.sty_cleaner_button, 2, 2)

        self.main_widget.setLayout(self.layout)

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
        self.setStyleSheet(style_string)
        self.show()
    
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
    
    def createEvents(self):
        """Vindaloo."""
        self.piggy_bank_button.clicked.connect(self.openPiggyBank)
        self.daily_porker_button.clicked.connect(self.openDailyPorker)
        self.farmhand_button.clicked.connect(self.openFarmHand)
        self.sty_cleaner_button.clicked.connect(self.openStyCleaner)
        self.swine_herd_button.clicked.connect(self.openSwineHerd)
        self.seeker_button.clicked.connect(self.openSeeker)

    def openPiggyBank(self):
        self.piggy_bank = PiggyBankWithFilter(self.user_id, self.password)
        self.piggy_bank.show()
    
    def openDailyPorker(self):
        self.daily_porker = DailyPorker(self.user_id, self.password, self.category_tree)
        self.daily_porker.show()

    def openFarmHand(self):
        self.farm_hand = FarmHand(self.user_id, self.password)
        self.farm_hand.show()
    
    def openStyCleaner(self):
        #self.alertMessage("StyCleaner", "We clean the shiz.")
        self.sty_cleaner = StyCleaner()
        self.sty_cleaner.show()
    
    def openSwineHerd(self):
        self.swine = SwineHerd()
        self.swine.show()
    
    def openSeeker(self):
        #self.alertMessage("Seeker", "Porko Dormeins Nunquam Titlandus")
        self.seeker = Seeker(self.user_id, self.password)
        self.seeker.show()
        
    def alertMessage(self, title, message):
        """Vindaloo."""
        QtGui.QMessageBox.about(self, title, message)

    def notify(self,title,message):
        """Vindaloo."""
        self.trayIcon.showMessage(title,message)

    def closeEvent(self,event):
        self.askToClose = QtGui.QMessageBox.question(self, 'Close VINDALOO?', "Are you sure you'd like to quit?\nVindaloo was developed for TLs to extract data effortlessly from the OINK database.\nKeep Vindaloo open if you want to be able to extract data from the Piggy Bank, get reports, plot daily graphs and find data in the OINK Database.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if self.askToClose == QtGui.QMessageBox.Yes:
            MOSES.createLogoutStamp(self.user_id, self.password)
            super(Vindaloo, self).closeEvent(event)
        else:
            event.ignore()


if __name__ == "__main__":
    import sys, MOSES
    app = QtGui.QApplication([])
    u, p = MOSES.getbbc()
    vin = Vindaloo(u,p)
    sys.exit(app.exec_())