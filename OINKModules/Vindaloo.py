#!/usr/bin/python2
# -*- coding: utf-8 -*-
import itertools
import math
import datetime
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
import MOSES

class Vindaloo(QtGui.QMainWindow):
    def __init__(self, user_id, password):
        super(QtGui.QMainWindow,self).__init__()
        self.user_id = user_id
        self.password = password
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
        self.porklid_button = QtGui.QPushButton("Porklid")
        self.porklid_button.setToolTip("Click here to generate graphical report(s).")
        self.piggy_bank_button = QtGui.QPushButton("Piggy Bank")
        self.piggy_bank_button.setToolTip("Click here to pull Piggy Bank data.")
        self.swine_herd_button = QtGui.QPushButton("Swine Herd")
        self.swine_herd_button.setToolTip("Click here to view the Head Count Report")

        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.daily_porker_button, 0, 0)
        self.layout.addWidget(self.porklid_button, 0, 1)
        self.layout.addWidget(self.piggy_bank_button, 0, 2)
        self.layout.addWidget(self.swine_herd_button, 1, 0)
        self.layout.addWidget(self.seeker_button, 1, 1)
        self.layout.addWidget(self.sty_cleaner_button, 1, 2)

        self.main_widget.setLayout(self.layout)

        self.setWindowTitle("VINDALOO - %s, Server: %s, User: %s (%s)" %(MOSES.version(),MOSES.getHostID(), self.user_id, MOSES.getEmpName(self.user_id) if self.user_id != "bigbrother" else "Administrator"))
        self.resize(500, 100)
        self.center()
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('Images\PORK_Icon.png'), self)
        self.trayIcon.show()
        self.statusBar().showMessage("All animals are created equal, but some animals are created more equal than others.")
        style_string = """
        .QWidget, .QPushButton, .QStatusBar, .QMessageBox, .QLabel{
            background-color: #0088D6;
            color: white;
            font: 8pt;
        }
        .QWidget, .QPushButton{
            font: 14pt;    
        }
        .QStatusBar {
            background-color: #FDDE2E;
            color: #0088D6;
            font: 9pt italic;
        
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
        self.porklid_button.clicked.connect(self.openPorklid)
        self.sty_cleaner_button.clicked.connect(self.openStyCleaner)
        self.swine_herd_button.clicked.connect(self.openSwineHerd)
        self.seeker_button.clicked.connect(self.openSeeker)

    def openPiggyBank(self):
        self.alertMessage("Piggy Bank", "This little piggy went to market...")
    
    def openDailyPorker(self):
        self.alertMessage("The Daily Porker", "I'm a Porkitzer Prize winning journalist!")
        self.daily_porker = DailyPorker(self.user_id, self.password)
        self.daily_porker.show()
    def openPorklid(self):
        self.alertMessage("Porklid", "Euclid gave us geometry. Porklid gave us graphical nightmares.")
    
    def openStyCleaner(self):
        #self.alertMessage("StyCleaner", "We clean the shiz.")
        self.sty_cleaner = StyCleaner()
        self.sty_cleaner.show()
    
    def openSwineHerd(self):
        self.alertMessage("SwineHerd","The lord is my swineherd, and I shall not want.")
    
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