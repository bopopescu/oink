#!/usr/bin/python2
# -*- coding: utf-8 -*-
import getpass
from PyQt4 import QtGui, QtCore
import numpy
import math
from EfficiencyCalculator import EfficiencyCalculator
from WeekCalendar import WeekCalendar
from LeavePlanner import LeavePlanner
from OINKUIMethods import passwordResetter
from AnimalFarm import AnimalFarm
from PiggyBanker import PiggyBanker
from Porker import Porker
from PiggyBank import PiggyBank
import OINKMethods as OINKM

import MOSES
import datetime


class Pork(QtGui.QMainWindow):
    def __init__(self, userID, password):
        """PORK initializer. Takes the userID and password"""
        super(QtGui.QMainWindow, self).__init__()
        #pork_style = open("stylesheet.css",'r').read()
        #print pork_style
        #self.setStyleSheet(open("stylesheet.css",'r').read())
        #store the variables so they are accessible elsewhere in this class.
        self.userID = userID
        self.password = password
        MOSES.createLoginStamp(self.userID, self.password)
        self.clip = QtGui.QApplication.clipboard()
        self.mapThreads()

        #Create the widgets and arrange them as needed.
        self.mainWidget = QtGui.QWidget()
        self.setCentralWidget(self.mainWidget)
        self.quote_thread = AnimalFarm()
        self.quote_thread.quoteSent.connect(self.updateStatusBar)
        self.widgetGenerator()
        self.widgetLayout()
        #Create all visual and usability aspects of the program.
        self.mapToolTips()
        self.setEvents()
        self.createActions()
        self.createTabOrder()
        self.addMenus()
        self.setVisuals()
        self.refreshStatsTable()
        #Initialize the application with required details.
        self.category_tree = MOSES.getCategoryTree(self.userID, self.password)
        self.populateBU()
        #self.populateTable()
        self.populateClarification()
        self.initForm()
        #self.porker_thread.getStatsData(self.getActiveDate())
        #Final set up.
        self.currentFSNDataList = []
        #self.displayEfficiency()
        #Ignorance is bliss.
        #self.setFocusPolicy(QtCore.Qt.NoFocus)

    def focusInEvent(self, event):
        print "Pork Focus in"

    def FocusOutEvent(self, event):
        print "Pork Focus out"

    def widgetGenerator(self):
        """PORK Window."""
        #creates all the widgets
        #Create the tab widget, adds tabs and creates all the related widgets and layouts.
        self.piggybank = PiggyBank()
        self.tabs = QtGui.QTabWidget()
        self.stats = QtGui.QWidget()
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Welcome to P.O.R.K. Big Brother is watching you.")
        self.menu = self.menuBar()
        self.stats_table = QtGui.QTableWidget(0, 0, self)
        self.stats_table.setToolTip("This report displays your statistics for the last working date.\nIf you've selected a Monday, this will show you\nyour data for last Friday, provided you weren't on leave on that day.\nIf you were, it'll search for the date\non which you last worked and show you that.")
        self.stats_table.setMinimumHeight(170)
        self.refresh_stats_button = QtGui.QPushButton("Refresh Statistics")
        self.stats_progress_bar = QtGui.QProgressBar()
        progressbar_style = """
            .QProgressBar {
                 border: 0.5px solid black;
                 border-radius: 5px;
                 text-align: center;
             }

            .QProgressBar::chunk {
                 background-color: #0088D6;
                 width: 20px;
             }""" #05B8CC
        self.stats_progress_message = QtGui.QLabel("Awaiting signals.")

        self.stats_progress_message.setStyleSheet("QLabel { font-size: 10px }")
        self.stats_progress = QtGui.QWidget()
        self.stats_progress_layout = QtGui.QGridLayout()
        self.stats_progress_layout.addWidget(self.stats_progress_bar,0,0)
        self.stats_progress_layout.addWidget(self.stats_progress_message,0,0)
        self.stats_progress.setLayout(self.stats_progress_layout)

        self.stats_progress_bar.setRange(0,1)
        self.stats_progress_bar.setStyleSheet(progressbar_style)
        self.stats_layout = QtGui.QVBoxLayout()
        self.stats_layout.addWidget(self.stats_table)
        self.stats_layout.addWidget(self.refresh_stats_button)
        self.stats_layout.addWidget(self.stats_progress)
        self.stats.setLayout(self.stats_layout)
        self.tabs.addTab(self.stats, "Writer Statistics")
        self.tabs.addTab(self.piggybank, "Piggy Bank")

        style = "font-size: 12px; font-weight: bold;"

        self.hide_piggy_button = QtGui.QPushButton(">")
        self.hide_piggy_button.setStyleSheet(style)
        self.hide_piggy_button.setCheckable(True)
        self.hide_piggy_button.setMinimumHeight(70)
        self.hide_piggy_button.setMaximumHeight(70)
        self.hide_piggy_button.setMinimumWidth(30)
        self.hide_piggy_button.setMaximumWidth(30)
        self.hide_piggy_button.clicked.connect(self.hide_piggy)

        self.hide_form_button = QtGui.QPushButton("<")
        self.hide_form_button.setStyleSheet(style)
        self.hide_form_button.setCheckable(True)
        self.hide_form_button.setMinimumHeight(70)
        self.hide_form_button.setMaximumHeight(70)
        self.hide_form_button.setMinimumWidth(30)
        self.hide_form_button.setMaximumWidth(30)
        self.hide_form_button.clicked.connect(self.hide_form)


        self.hide_buttons = QtGui.QButtonGroup()
        self.hide_buttons.addButton(self.hide_form_button)
        self.hide_buttons.addButton(self.hide_piggy_button)
        self.hide_buttons.setExclusive(False)

        #initialize Calendar
        self.workCalendar = WeekCalendar(self.userID, self.password)
        self.workCalendar.setMinimumWidth(400)
        self.workCalendar.setMinimumHeight(250)
        #initialize buttons to modify values
        self.buttonAddFSN = QtGui.QPushButton('Add', self)
        self.buttonAddFSN.setCheckable(True)
        self.buttonAddFSN.setMinimumWidth(40)
        self.buttonAddFSN.setMinimumHeight(30)
        self.buttonAddFSN.setMaximumHeight(30)

        self.buttonModifyFSN = QtGui.QPushButton('Modify', self)
        self.buttonModifyFSN.setMinimumWidth(50)
        self.buttonModifyFSN.setMinimumHeight(30)
        self.buttonModifyFSN.setMaximumHeight(30)
        self.buttonModifyFSN.setCheckable(True)

        self.buttonCopyFields = QtGui.QPushButton("Copy Fields")
        self.buttonCopyFields.setMinimumWidth(70)
        self.buttonCopyFields.setMinimumHeight(30)
        self.buttonCopyFields.setMaximumHeight(30)


        self.formModifierButtons = QtGui.QButtonGroup()
        self.formModifierButtons.addButton(self.buttonAddFSN)
        self.formModifierButtons.addButton(self.buttonModifyFSN)

        self.efficiencyProgress = QtGui.QProgressBar()
        self.efficiencyProgress.setRange(0,100)
        self.efficiencyProgress.setMinimumWidth(200)

        self.efficiencyProgress.setStyleSheet(progressbar_style)

        self.efficiencyProgress.setTextVisible(True)
        #Create all the widgets associated with the form.
        self.labelFSN = QtGui.QLabel("FSN:")
        self.lineEditFSN = QtGui.QLineEdit(self)
        self.lineEditFSN.setMaximumWidth(150)
        self.labelType = QtGui.QLabel("Description Type:")
        self.comboBoxType = QtGui.QComboBox()
        self.comboBoxType.setMaximumWidth(150)
        self.comboBoxType.addItems(MOSES.getDescriptionTypes(self.userID,self.password))
        self.comboBoxType.setToolTip("Select the description type.")

        self.labelSource = QtGui.QLabel("Source:")
        self.comboBoxSource = QtGui.QComboBox()
        self.comboBoxSource.setMaximumWidth(150)
        self.comboBoxSource.addItems(MOSES.getSources(self.userID,self.password))
        #self.labelPriority = QtGui.QLabel("Priority:")
        #self.comboBoxPriority = QtGui.QComboBox()
        #self.priorityList = ["Normal","High"]
        #self.comboBoxPriority.addItems(self.priorityList)
        self.labelBU = QtGui.QLabel("Business Unit:")
        self.comboBoxBU = QtGui.QComboBox(self)
        self.comboBoxBU.setMaximumWidth(150)
        self.labelSuperCategory = QtGui.QLabel("Super Category:")
        self.comboBoxSuperCategory = QtGui.QComboBox(self)
        self.comboBoxSuperCategory.setMaximumWidth(150)
        self.labelCategory = QtGui.QLabel("Category:")
        self.comboBoxCategory = QtGui.QComboBox(self)
        self.comboBoxCategory.setMaximumWidth(150)
        self.labelSubCategory = QtGui.QLabel("Sub-Category:")
        self.comboBoxSubCategory = QtGui.QComboBox(self)
        self.comboBoxSubCategory.setMaximumWidth(150)
        self.labelBrand = QtGui.QLabel("Brand:")
        self.lineEditBrand = QtGui.QLineEdit(self)
        self.lineEditBrand.setMaximumWidth(150)
        self.labelVertical = QtGui.QLabel("Vertical:")
        self.comboBoxVertical = QtGui.QComboBox(self)
        self.comboBoxVertical.setMaximumWidth(150)
        self.labelWordCount = QtGui.QLabel("Word Count:")
        self.spinBoxWordCount = QtGui.QSpinBox(self)
        self.spinBoxWordCount.setMaximumWidth(150)
        self.spinBoxWordCount.setRange(0,250000)
        self.spinBoxWordCount.setSingleStep(1)

        self.labelUploadLink = QtGui.QLabel("Upload Link:")
        self.lineEditUploadLink = QtGui.QLineEdit(self)
        self.lineEditUploadLink.setMaximumWidth(150)
        self.labelRefLinks = QtGui.QLabel("Reference Links:")
        self.lineEditRefLink = QtGui.QLineEdit(self)
        self.lineEditRefLink.setMaximumWidth(150)
        self.labelGuidelines = QtGui.QLabel("Guidelines:")
        self.textEditGuidelines = QtGui.QTextEdit(self)
        self.textEditGuidelines.setMaximumHeight(50)
        self.textEditGuidelines.setMinimumHeight(50)
        self.textEditGuidelines.setMaximumWidth(300)
        self.textEditGuidelines.isReadOnly()
        self.labelClarifications = QtGui.QLabel("Clarifications:")
        self.lineEditClarification = QtGui.QLineEdit(self)
        self.lineEditClarification.setMaximumWidth(50)
        self.comboBoxClarification = QtGui.QComboBox(self)
        self.comboBoxClarification.setMaximumWidth(50)
        self.buttonAddClarification = QtGui.QPushButton("+")
        self.buttonAddClarification.setMaximumWidth(20)
        #styler = """image: url(Images\ok.png)"""
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                            QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setMaximumWidth(300)
        #self.buttonBox.Ok.setStyleSheet(styler)
        self.buttonBox.setMaximumHeight(40)


    def widgetLayout(self):
        """PORK Window."""
        #Begin the form's layout.
        self.formLayout = QtGui.QGridLayout()
        self.formLayout.addWidget(self.labelFSN,0,0)
        self.formLayout.addWidget(self.lineEditFSN,0,1)
        self.formLayout.addWidget(self.labelType,1,0)
        self.formLayout.addWidget(self.comboBoxType,1,1)
        self.formLayout.addWidget(self.labelSource,2,0)
        self.formLayout.addWidget(self.comboBoxSource,2,1)
        #self.formLayout.addWidget(self.labelPriority,3,0)
        #self.formLayout.addWidget(self.comboBoxPriority,3,1)
        self.formLayout.addWidget(self.labelBU,4,0)
        self.formLayout.addWidget(self.comboBoxBU,4,1)
        self.formLayout.addWidget(self.labelSuperCategory,5,0)
        self.formLayout.addWidget(self.comboBoxSuperCategory,5,1)
        self.formLayout.addWidget(self.labelCategory,6,0)
        self.formLayout.addWidget(self.comboBoxCategory,6,1)
        self.formLayout.addWidget(self.labelSubCategory,7,0)
        self.formLayout.addWidget(self.comboBoxSubCategory,7,1)
        self.formLayout.addWidget(self.labelVertical,8,0)
        self.formLayout.addWidget(self.comboBoxVertical,8,1)
        self.formLayout.addWidget(self.labelBrand,9,0)
        self.formLayout.addWidget(self.lineEditBrand,9,1)
        self.formLayout.addWidget(self.labelWordCount,10,0)
        self.formLayout.addWidget(self.spinBoxWordCount,10,1)
        self.formLayout.addWidget(self.labelUploadLink,11,0)
        self.formLayout.addWidget(self.lineEditUploadLink,11,1)
        self.formLayout.addWidget(self.labelRefLinks,12,0)
        self.formLayout.addWidget(self.lineEditRefLink,12,1)
        ###############SpecialLayoutForClarifications##############
        self.clarificationRow = QtGui.QHBoxLayout()
        self.clarificationRow.addWidget(self.labelClarifications,2)
        self.clarificationRow.addWidget(self.lineEditClarification,2)
        self.clarificationRow.addWidget(self.comboBoxClarification,2)
        self.clarificationRow.addWidget(self.buttonAddClarification,1)
        ###########################################################
        self.formLayout.addLayout(self.clarificationRow,13,0,1,2)
        self.formLayout.addWidget(self.labelGuidelines,14,0,1,2)
        self.formLayout.addWidget(self.textEditGuidelines,15,0,1,2)
        self.formLayout.addWidget(self.buttonBox,16,0,1,2)
        ######################--------------------#################
        #Create a layout for the buttons.
        self.buttonsLayout = QtGui.QGridLayout()
        self.buttonsLayout.addWidget(self.buttonAddFSN,0,0)
        self.buttonsLayout.addWidget(self.buttonModifyFSN,0,1)
        self.buttonsLayout.addWidget(self.buttonCopyFields,0,2)

        #set the buttons above the form's layout.
        self.finalFormLayout = QtGui.QVBoxLayout()
        self.finalFormLayout.addLayout(self.buttonsLayout)
        self.finalFormLayout.addLayout(self.formLayout)
        self.finalFormLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.form = QtGui.QWidget()
        self.form.setLayout(self.finalFormLayout)
        ###Set the form's layout adjacent to the QTableWidget.



        #Create the piggy bank widget and layout.
        self.piggyLayout = QtGui.QVBoxLayout()
        self.piggyLayout.addWidget(self.workCalendar,1)
        self.piggyLayout.addWidget(self.tabs,3)
#        self.piggyLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.piggyWidget = QtGui.QWidget()
        self.piggyWidget.setLayout(self.piggyLayout)
        #Create the collapsible buttons layout
        self.hider_buttons_layout = QtGui.QVBoxLayout()
        self.hider_buttons_layout.addStretch(3)
        self.hider_buttons_layout.addWidget(self.hide_piggy_button)
        self.hider_buttons_layout.addWidget(self.hide_form_button)
        self.hider_buttons_layout.addStretch(3)
        self.hider_buttons_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.hider_buttons_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        #create the penultimate layout.
        self.penultimateLayout = QtGui.QHBoxLayout()
        self.penultimateLayout.addWidget(self.piggyWidget,8)
        self.penultimateLayout.addLayout(self.hider_buttons_layout,1)
        self.penultimateLayout.addWidget(self.form,2)
        self.penultimateLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        #create the final layout.
        self.finalLayout = QtGui.QGridLayout()
        self.finalLayout.addWidget(self.menu,0,0,1,5)
        self.finalLayout.addLayout(self.penultimateLayout,1,0,5,5)
        self.finalLayout.addWidget(self.efficiencyProgress,6,0,1,5)
        self.finalLayout.addWidget(self.status_bar,7,0,1,5)

        #self.finalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        #self.finalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        #Investigate later.
        self.mainWidget.setLayout(self.finalLayout)

    def mapToolTips(self):
        """PORK Window."""
        self.piggybank.setToolTip("Piggy Bank for %s" % self.getActiveDateString())
        self.workCalendar.setToolTip("Select a date to display the Piggy Bank.")
        self.buttonAddFSN.setToolTip("Click this button to add an FSN for %s" % self.getActiveDateString())
        self.lineEditFSN.setToolTip("Type the FSN or SEO article topic here.")
        self.comboBoxType.setToolTip("Select the description type.")
        self.comboBoxSource.setToolTip("Select the description's source.")
        self.comboBoxSuperCategory.setToolTip("Select the Super-Category of the FSN here.")
        self.comboBoxCategory.setToolTip("Select the category of the FSN here.")
        self.comboBoxSubCategory.setToolTip("Select the sub-category of the FSN here.")
        self.comboBoxVertical.setToolTip("Select the vertical of the FSN here.")
        self.lineEditBrand.setToolTip("Type the FSN's brand here.\nFor Books, use the writer's name as the brand where appropriate.\nContact your TL for assistance.")
        self.spinBoxWordCount.setToolTip("Type the word count of the article here.")
        self.lineEditUploadLink.setToolTip("If you are not using an FSN or an ISBN, please paste the appropriate upload link here.")
        self.lineEditRefLink.setToolTip("Paste the reference link(s) here.\nMultiple links can be appended by using a comma or a semi-colon.\nAvoid spaces like the plague.")
        self.lineEditClarification.setToolTip("Use the drop down menu adjacent to this box to append clarifications.\nIf a clarification is unavailable, please append it to this list by using a comma.")

    def displayPorkerProgress(self, activity, eta, completed):
        if completed:
            #print "Completed one porker cycle."
            self.stats_progress_bar.setRange(0,1)
            self.stats_progress_message.setText("Last Updated at %s" % datetime.datetime.strftime(datetime.datetime.now(),"%H:%M:%S"))
        else:
            #print "Porker at work. Message : ", activity
            self.stats_progress_bar.setRange(0,0)
            self.stats_progress_message.setText("   %s Possible ETA: %s" %(activity, datetime.datetime.strftime(eta,"%H:%M:%S")))

    def keyPressEvent(self, e):
        """PORK Window: Found this code online. Go through it and try to improve it."""
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            selected = self.piggybank.selectedRanges()
            if e.key() == QtCore.Qt.Key_S:
                self.say = QtGui.QMessageBox.question(self,"All Animals are created equal.","But some animals are <b>more</b> equal than others.", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if e.key() == QtCore.Qt.Key_C: #copy
                s = '\t'+"\t".join([str(self.piggybank.horizontalHeaderItem(i).text()) for i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1)])
                s = s + '\n'
                for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
                    s += str(r+1) + '\t'
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(self.piggybank.item(r,c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)

    def createTabOrder(self):
        """PORK Window."""
        self.setTabOrder(self.workCalendar, self.buttonAddFSN)
        #self.setTabOrder(self.piggybank,self.buttonAddFSN)
        self.setTabOrder(self.buttonAddFSN, self.buttonModifyFSN)
        self.setTabOrder(self.buttonModifyFSN, self.lineEditFSN)
        self.setTabOrder(self.lineEditFSN, self.comboBoxType)
        self.setTabOrder(self.comboBoxType, self.comboBoxSource)
        self.setTabOrder(self.comboBoxSource, self.comboBoxBU)
        #self.setTabOrder(self.comboBoxSource, self.comboBoxPriority)
        #self.setTabOrder(self.comboBoxPriority, self.comboBoxBU)
        self.setTabOrder(self.comboBoxBU, self.comboBoxSuperCategory)
        self.setTabOrder(self.comboBoxSuperCategory, self.comboBoxCategory)
        self.setTabOrder(self.comboBoxCategory, self.comboBoxSubCategory)
        self.setTabOrder(self.comboBoxSubCategory, self.comboBoxVertical)
        self.setTabOrder(self.comboBoxVertical, self.lineEditBrand)
        self.setTabOrder(self.lineEditBrand, self.spinBoxWordCount)
        self.setTabOrder(self.spinBoxWordCount, self.lineEditUploadLink)
        self.setTabOrder(self.lineEditUploadLink,self.lineEditRefLink)
        self.setTabOrder(self.lineEditRefLink, self.comboBoxClarification)
        self.setTabOrder(self.comboBoxClarification, self.buttonAddClarification)
        self.setTabOrder(self.buttonAddClarification, self.buttonBox)
        #self.setTabOrder(self.buttonBox,self.lineEditFSN)

    def addMenus(self):
        """PORK Window."""
        self.fileMenu = self.menu.addMenu("&File")
        self.toolsMenu = self.menu.addMenu("&Tools")
        self.commMenu = self.menu.addMenu("Co&mmunication")
        self.helpMenu = self.menu.addMenu("&Help")
        self.exportMenu = self.fileMenu.addMenu("E&xport")
        self.fileMenu.addAction(self.resetPassword_action)
        self.KRAMenu = self.toolsMenu.addMenu("&KRA Tools")
        #self.KRAMenu.addAction(self.viewKRATable)
        #self.KRAMenu.addAction(self.generateKRAReport)
        self.qualityMenu = self.toolsMenu.addMenu("Quality Reports")
        self.openEffCalcOption = self.toolsMenu.addAction(self.openEffCalc)
        self.askForLeave = self.commMenu.addAction(self.applyLeave)
        self.askEditor = self.commMenu.addAction(self.callAskAnEditor)
        self.askTL = self.commMenu.addAction(self.callAskYourTL)
        self.viewStyleSheet = self.toolsMenu.addAction(self.callStyleSheet)
        self.chatmessenger = self.toolsMenu.addAction(self.callOpenChat)

    def createActions(self):
        """PORK Window."""
        #self.exitAction = QtGui.QAction(QIcon('exit.png'),"&Exit",self)
        #self.exitAction.setToolTip("Click to Exit.")
        #self.exitAction.triggered.connect(self.closeEvent)
        #Close event doesn't close it.
        #And qApp.exit doesn't call CloseEvent. I can't bypass closeEvent, that's how I prevent multiple instances.
        self.resetPassword_action = QtGui.QAction("Reset password", self)
        self.resetPassword_action.triggered.connect(self.reset_password)
        self.applyLeave = QtGui.QAction(QtGui.QIcon('Images\AskForLeave.png'),\
            "Apply For Leaves or Relaxation in Targets",self)

        self.applyLeave.setToolTip("Click to apply for a leave or for a relaxation of your targets.")
        self.applyLeave.triggered.connect(self.applyForLeave)
        self.openEffCalc = QtGui.QAction(QtGui.QIcon('Images\Efficiency_Icon.png'),\
            "Efficiency Calculator",self)
        self.openEffCalc.setToolTip(\
            "Click to open the efficiency calculator.")
        self.openEffCalc.triggered.connect(self.showEfficiencyCalc)
        self.callAskAnEditor = QtGui.QAction(QtGui.QIcon("Images\AskAnEditor_Icon.png"),\
            "Ask An Editor",self)
        self.callAskAnEditor.setToolTip(\
            "Post a question to the editors.")
        self.callAskAnEditor.triggered.connect(self.AskAnEditor)
        self.callAskYourTL = QtGui.QAction(QtGui.QIcon("Images\AskYourTL_Icon.png"),\
                    "Ask Your TL",self)
        self.callAskYourTL.setToolTip(\
            "Post a question for your TL.")
        self.callAskYourTL.triggered.connect(self.askTL)

        self.callStyleSheet = QtGui.QAction(QtGui.QIcon("Images\StyleSheet_Icon.png"),\
            "View Style Sheet",self)
        self.callStyleSheet.triggered.connect(self.openStyleSheet)
        self.callStyleSheet.setToolTip(\
            "View the Content Team Style Sheet")
        self.callOpenChat = QtGui.QAction(QtGui.QIcon("Images\Chat_Icon.png"),\
                        "Open Messenger",self)
        self.callOpenChat.triggered.connect(self.openChat)

    def setVisuals(self):
        """PORK Window: Sets all the visual aspects of the PORK Main Window."""
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.setWindowTitle("P.O.R.K. v%s - Server : %s, User: %s (%s)" % (MOSES.version(), MOSES.getHostID(), self.userID, MOSES.getEmpName(self.userID)))
        self.center()
        self.expand()
        self.show()
        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('Images\Pork_Icon.png'),self)
        self.trayIcon.show()

    def initForm(self):
        """PORK Window: Method to initialize the form."""
        self.buttonAddFSN.setChecked(True)
        self.comboBoxType.setCurrentIndex(3)
        self.comboBoxSource.setCurrentIndex(1)
        self.comboBoxSuperCategory.setCurrentIndex(-1)
        self.lineEditRefLink.setText("NA")
        self.comboBoxCategory.setCurrentIndex(-1)
        self.comboBoxSubCategory.setCurrentIndex(-1)
        self.comboBoxVertical.setCurrentIndex(-1)
        self.lineEditBrand.setText("")
        self.lineEditClarification.setText("NA")
        self.comboBoxClarification.setCurrentIndex(-1)
        #self.comboBoxPriority.setCurrentIndex(-1)

    def setEvents(self):
        """PORK Window."""
        self.workCalendar.clicked[QtCore.QDate].connect(self.changedDate)
        self.workCalendar.currentPageChanged.connect(self.calendarPageChanged)
        self.piggybank.cellClicked.connect(self.cellSelected)
        self.piggybank.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.buttonBox.accepted.connect(self.validateAndSendToPiggy)
        self.comboBoxBU.currentIndexChanged['QString'].connect(self.populateSuperCategory)
        self.comboBoxSuperCategory.currentIndexChanged['QString'].connect(self.populateCategory)
        self.comboBoxCategory.currentIndexChanged['QString'].connect(self.populateSubCategory)
        self.comboBoxSubCategory.currentIndexChanged['QString'].connect(self.populateBrandVertical)
        self.comboBoxVertical.currentIndexChanged['QString'].connect(self.getVerticalGuidelines)
        self.lineEditFSN.editingFinished.connect(self.FSNEditFinishTriggers)
        self.lineEditFSN.textChanged.connect(self.FSNEditFinishTriggers)
        self.comboBoxType.currentIndexChanged['QString'].connect(self.FSNEditFinishTriggers)
        self.buttonBox.rejected.connect(self.clearAll)
        self.buttonAddClarification.clicked.connect(self.addClarification)
        self.buttonCopyFields.clicked.connect(self.copyCommonFields)
        self.refresh_stats_button.clicked.connect(self.refreshStatsTable)

    def notify(self,title,message):
        """PORK Window: Method to show a tray notification"""
        self.trayIcon.showMessage(title,message)

    def applyForLeave(self):
        """PORK Window: Method to call the leave planner dialog."""
        #print "Applying for a leave!" #debug
        leaveapp = LeavePlanner(self.userID,self.password)
        if leaveapp.exec_():
            #print "Success!" #debug
            self.alertMessage('Success', "Successfully submitted the request.")
        return True

    def reset_password(self):
        """Opens a password reset method and allows the user to reset his/her password."""
        self.password = passwordResetter(self.userID, self.password)

    def viewEscalations(self):
        """PORK Window."""
        self.featureUnavailable()

    def openChat(self):
        """PORK Window."""
        self.featureUnavailable()

    def showEfficiencyCalc(self):
        """PORK Window."""
        calculator = EfficiencyCalculator(self.userID, self.password)
        if calculator.exec_():
            print "Calculator has successfully executed.!"

    def updateStatsTable(self, stats_data):
        """PORK Window method that updates the writer's statistics sheet.
        This should be triggered along with the populateTable method
        when the date is changed."""
        #get data for last working date (lwd)
        self.last_working_date = stats_data["LWD"]
        self.lwd_efficiency = stats_data["LWD Efficiency"]
        self.lwd_CFM = stats_data["LWD CFM"]
        self.lwd_GSEO = stats_data["LWD GSEO"]
        #get data for current week (cw)
        self.current_week = stats_data["Current Week"]
        self.cw_efficiency = stats_data["CW Efficiency"]
        self.cw_CFM = stats_data["CW CFM"]
        self.cw_GSEO = stats_data["CW GSEO"]
        #get data for current month (cm)
        self.current_month = stats_data["Current Month"]
        self.cm_efficiency = stats_data["CM Efficiency"]
        self.cm_CFM = stats_data["CM CFM"]
        self.cm_GSEO = stats_data["CM GSEO"]
        #get data for current quarter (cq)
        self.current_quarter = stats_data["Current Quarter"]
        self.cq_efficiency = stats_data["CQ Efficiency"]
        self.cq_CFM = stats_data["CQ CFM"]
        self.cq_GSEO = stats_data["CQ GSEO"]
        self.current_half_year = stats_data["Current Half Year"]
        self.chy_efficiency = stats_data["CHY Efficiency"]
        self.chy_CFM = stats_data["CHY CFM"]
        self.chy_GSEO = stats_data["CHY GSEO"]
        

        self.stats_table.setRowCount(5)
        self.stats_table.setColumnCount(4)

        red = QtGui.QColor(231, 90, 83)
        green = QtGui.QColor(60, 179, 113)
        blue = QtGui.QColor(23, 136, 216)
        blue1 = QtGui.QColor(1, 172, 218)

        self.stats_table_headers = ["Timeframe","Efficiency", "CFM", "GSEO"]
        self.stats_table.setHorizontalHeaderLabels(self.stats_table_headers)

        if (self.lwd_efficiency is None): 
            lwd_efficiency_item = QtGui.QTableWidgetItem("-")
        elif type(self.lwd_efficiency) == str:
            lwd_efficiency_item = QtGui.QTableWidgetItem(self.lwd_efficiency)
        else:
            self.lwd_efficiency = numpy.around(self.lwd_efficiency, 3)
            lwd_efficiency_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.lwd_efficiency))
            if 0.000 <= self.lwd_efficiency < 100.000:
                lwd_efficiency_item.setBackgroundColor(red)
            elif 100.000 <= self.lwd_efficiency < 105.000:
                lwd_efficiency_item.setBackgroundColor(green)
            elif 105.000 <= self.lwd_efficiency < 110.000:
                lwd_efficiency_item.setBackgroundColor(blue)
            else:
                lwd_efficiency_item.setBackgroundColor(blue1)
        
        if (self.lwd_CFM is None):
            lwd_CFM_item = QtGui.QTableWidgetItem("-")
        elif type(self.lwd_CFM) == str:
            lwd_CFM_item = QtGui.QTableWidgetItem(self.lwd_CFM)
        else:
            self.lwd_CFM = numpy.around(self.lwd_CFM, 3)
            lwd_CFM_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.lwd_CFM))
            if 0.000 <= self.lwd_CFM < 95.000:
                lwd_CFM_item.setBackgroundColor(red)
            elif 95.000 <= self.lwd_CFM < 98.000:
                lwd_CFM_item.setBackgroundColor(green)
            elif 98.000 <= self.lwd_CFM < 100.000:
                lwd_CFM_item.setBackgroundColor(blue)
            elif self.lwd_CFM == 100.000:
                lwd_CFM_item.setBackgroundColor(blue1)

        if (self.lwd_GSEO is None):
            lwd_GSEO_item = QtGui.QTableWidgetItem("-")
        elif type(self.lwd_GSEO) == str:
            lwd_GSEO_item = QtGui.QTableWidgetItem(self.lwd_GSEO)
        else:
            self.lwd_GSEO = numpy.around(self.lwd_GSEO, 3)
            lwd_GSEO_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.lwd_GSEO))
            if 0.000 <= self.lwd_GSEO < 95.000:
                lwd_GSEO_item.setBackgroundColor(red)
            elif 95.000 <= self.lwd_GSEO < 98.000:
                lwd_GSEO_item.setBackgroundColor(green)
            elif 98.000 <= self.lwd_GSEO < 100.000:
                lwd_GSEO_item.setBackgroundColor(blue)
            elif self.lwd_GSEO == 100.000:
                lwd_GSEO_item.setBackgroundColor(blue1)

        if (self.cw_efficiency is None):
            cw_efficiency_item = QtGui.QTableWidgetItem("-")
        elif type(self.cw_efficiency) == str:
            cw_efficiency_item = QtGui.QTableWidgetItem(self.cw_efficiency)
        else:
            self.cw_efficiency = numpy.around(self.cw_efficiency, 3)
            cw_efficiency_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.cw_efficiency))
            if 0.000 <= self.cw_efficiency < 100.000:
                cw_efficiency_item.setBackgroundColor(red)
            elif 100.000 <= self.cw_efficiency < 105.000:
                cw_efficiency_item.setBackgroundColor(green)
            elif 105.000 <= self.cw_efficiency < 110.000:
                cw_efficiency_item.setBackgroundColor(blue)
            else:
                cw_efficiency_item.setBackgroundColor(blue1)
        
        if (self.cw_CFM is None):
            cw_CFM_item = QtGui.QTableWidgetItem("-")
        elif type(self.cw_CFM) == str:
            cw_CFM_item = QtGui.QTableWidgetItem(self.cw_CFM)
        else:
            self.cw_CFM = numpy.around(self.cw_CFM, 3)
            cw_CFM_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.cw_CFM))
            if 0.000 <= self.cw_CFM < 95.000:
                cw_CFM_item.setBackgroundColor(red)
            elif 95.000 <= self.cw_CFM < 98.000:
                cw_CFM_item.setBackgroundColor(green)
            elif 98.000 <= self.cw_CFM < 100.000:
                cw_CFM_item.setBackgroundColor(blue)
            elif self.cw_CFM == 100.000:
                cw_CFM_item.setBackgroundColor(blue1)

        if (self.cw_GSEO is None):
            cw_GSEO_item = QtGui.QTableWidgetItem("-")
        elif type(self.cw_GSEO) == str:
            cw_GSEO_item = QtGui.QTableWidgetItem(self.cw_GSEO)
        else:
            self.cw_GSEO = numpy.around(self.cw_GSEO, 3)
            cw_GSEO_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.cw_GSEO))
            if 0.000 <= self.cw_GSEO < 95.000:
                cw_GSEO_item.setBackgroundColor(red)
            elif 95.000 <= self.cw_GSEO < 98.000:
                cw_GSEO_item.setBackgroundColor(green)
            elif 98.000 <= self.cw_GSEO < 100.000:
                cw_GSEO_item.setBackgroundColor(blue)
            elif self.cw_GSEO == 100.000:
                cw_GSEO_item.setBackgroundColor(blue1)

        if (self.cm_efficiency is None):
            cm_efficiency_item = QtGui.QTableWidgetItem("-")
        elif type(self.cm_efficiency) == str:
            cm_efficiency_item = QtGui.QTableWidgetItem(self.cm_efficiency)
        else:
            self.cm_efficiency = numpy.around(self.cm_efficiency, 3)
            cm_efficiency_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.cm_efficiency))
            if 0.000 <= self.cm_efficiency < 100.000:
                cm_efficiency_item.setBackgroundColor(red)
            elif 100.000 <= self.cm_efficiency < 105.000:
                cm_efficiency_item.setBackgroundColor(green)
            elif 105.000 <= self.cm_efficiency < 110.000:
                cm_efficiency_item.setBackgroundColor(blue)
            else:
                cm_efficiency_item.setBackgroundColor(blue1)
        
        if (self.cm_CFM is None):
            cm_CFM_item = QtGui.QTableWidgetItem("-")
        elif type(self.cm_CFM) == str:
            cm_CFM_item = QtGui.QTableWidgetItem(self.cm_CFM)
        else:
            self.cm_CFM = numpy.around(self.cm_CFM, 3)
            cm_CFM_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.cm_CFM))
            if 0.000 <= self.cm_CFM < 95.000:
                cm_CFM_item.setBackgroundColor(red)
            elif 95.000 <= self.cm_CFM < 98.000:
                cm_CFM_item.setBackgroundColor(green)
            elif 98.000 <= self.cm_CFM < 100.000:
                cm_CFM_item.setBackgroundColor(blue)
            elif self.cm_CFM == 100.000:
                cm_CFM_item.setBackgroundColor(blue1)

        if (self.cm_GSEO is None):
            cm_GSEO_item = QtGui.QTableWidgetItem("-")
        elif type(self.cm_GSEO) == str:
            cm_GSEO_item = QtGui.QTableWidgetItem(self.cm_GSEO)
        else:
            self.cm_GSEO = numpy.around(self.cm_GSEO, 3)
            cm_GSEO_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.cm_GSEO))
            if 0.000 <= self.cm_GSEO < 95.000:
                cm_GSEO_item.setBackgroundColor(red)
            elif 95.000 <= self.cm_GSEO < 98.000:
                cm_GSEO_item.setBackgroundColor(green)
            elif 98.000 <= self.cm_GSEO < 100.000:
                cm_GSEO_item.setBackgroundColor(blue)
            elif self.cm_GSEO == 100.000:
                cm_GSEO_item.setBackgroundColor(blue1)

        if (self.cq_efficiency is None):
            cq_efficiency_item = QtGui.QTableWidgetItem("-")
        elif type(self.cq_efficiency) == str:
            cq_efficiency_item = QtGui.QTableWidgetItem(self.cq_efficiency)
        else:
            self.cq_efficiency = numpy.around(self.cq_efficiency, 3)
            cq_efficiency_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.cq_efficiency))
            if 0.000 <= self.cq_efficiency < 100.000:
                cq_efficiency_item.setBackgroundColor(red)
            elif 100.000 <= self.cq_efficiency < 105.000:
                cq_efficiency_item.setBackgroundColor(green)
            elif 105.000 <= self.cq_efficiency < 110.000:
                cq_efficiency_item.setBackgroundColor(blue)
            else:
                cq_efficiency_item.setBackgroundColor(blue1)
        
        if (self.cq_CFM is None):
            cq_CFM_item = QtGui.QTableWidgetItem("-")
        elif type(self.cq_CFM) == str:
            cq_CFM_item = QtGui.QTableWidgetItem(self.cq_CFM)
        else:
            self.cq_CFM = numpy.around(self.cq_CFM, 3)
            cq_CFM_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.cq_CFM))
            if 0.000 <= self.cq_CFM < 95.000:
                cq_CFM_item.setBackgroundColor(red)
            elif 95.000 <= self.cq_CFM < 98.000:
                cq_CFM_item.setBackgroundColor(green)
            elif 98.000 <= self.cq_CFM < 100.000:
                cq_CFM_item.setBackgroundColor(blue)
            elif self.cq_CFM == 100.000:
                cq_CFM_item.setBackgroundColor(blue1)

        if (self.cq_GSEO is None):
            cq_GSEO_item = QtGui.QTableWidgetItem("-")
        elif type(self.cq_GSEO) == str:
            cq_GSEO_item = QtGui.QTableWidgetItem(self.cq_GSEO)
        else:
            self.cq_GSEO = numpy.around(self.cq_GSEO, 3)
            cq_GSEO_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.cq_GSEO))
            if 0.000 <= self.cq_GSEO < 95.000:
                cq_GSEO_item.setBackgroundColor(red)
            elif 95.000 <= self.cq_GSEO < 98.000:
                cq_GSEO_item.setBackgroundColor(green)
            elif 98.000 <= self.cq_GSEO < 100.000:
                cq_GSEO_item.setBackgroundColor(blue)
            elif self.cq_GSEO == 100.000:
                cq_GSEO_item.setBackgroundColor(blue1)

        if (self.chy_efficiency is None):
            chy_efficiency_item = QtGui.QTableWidgetItem("-")
        elif type(self.chy_efficiency) == str:
            chy_efficiency_item = QtGui.QTableWidgetItem(self.chy_efficiency)
        else:
            self.chy_efficiency = numpy.around(self.chy_efficiency, 3)
            chy_efficiency_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.chy_efficiency))
            if 0.000 <= self.chy_efficiency < 100.000:
                chy_efficiency_item.setBackgroundColor(red)
            elif 100.000 <= self.chy_efficiency < 105.000:
                chy_efficiency_item.setBackgroundColor(green)
            elif 105.000 <= self.chy_efficiency < 110.000:
                chy_efficiency_item.setBackgroundColor(blue)
            else:
                chy_efficiency_item.setBackgroundColor(blue1)
        
        if (self.chy_CFM is None):
            chy_CFM_item = QtGui.QTableWidgetItem("-")
        elif type(self.chy_CFM) == str:
            chy_CFM_item = QtGui.QTableWidgetItem(self.chy_CFM)
        else:
            self.chy_CFM = numpy.around(self.chy_CFM, 3)
            chy_CFM_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.chy_CFM))
            if 0.000 <= self.chy_CFM < 95.000:
                chy_CFM_item.setBackgroundColor(red)
            elif 95.000 <= self.chy_CFM < 98.000:
                chy_CFM_item.setBackgroundColor(green)
            elif 98.000 <= self.chy_CFM < 100.000:
                chy_CFM_item.setBackgroundColor(blue)
            elif self.chy_CFM == 100.000:
                chy_CFM_item.setBackgroundColor(blue1)

        if (self.chy_GSEO is None):
            chy_GSEO_item = QtGui.QTableWidgetItem("-")
        elif type(self.chy_GSEO) == str:
            chy_GSEO_item = QtGui.QTableWidgetItem(self.chy_GSEO)
        else:
            self.chy_GSEO = numpy.around(self.chy_GSEO, 3)
            chy_GSEO_item = QtGui.QTableWidgetItem(str("%6.3f%%" %self.chy_GSEO))
            if 0.000 <= self.chy_GSEO < 95.000:
                chy_GSEO_item.setBackgroundColor(red)
            elif 95.000 <= self.chy_GSEO < 98.000:
                chy_GSEO_item.setBackgroundColor(green)
            elif 98.000 <= self.chy_GSEO < 100.000:
                chy_GSEO_item.setBackgroundColor(blue)
            elif self.chy_GSEO == 100.000:
                chy_GSEO_item.setBackgroundColor(blue1)


        self.stats_table.setItem(0,0,QtGui.QTableWidgetItem(str(self.last_working_date)))
        self.stats_table.setItem(0,1,lwd_efficiency_item)
        self.stats_table.setItem(0,2,lwd_CFM_item)
        self.stats_table.setItem(0,3,lwd_GSEO_item)
        self.stats_table.setItem(1,0,QtGui.QTableWidgetItem(("Week: %d" %self.current_week)))
        self.stats_table.setItem(1,1,cw_efficiency_item)
        self.stats_table.setItem(1,2,cw_CFM_item)
        self.stats_table.setItem(1,3,cw_GSEO_item)
        self.stats_table.setItem(2,0,QtGui.QTableWidgetItem(("Month: %d" %self.current_month)))
        self.stats_table.setItem(2,1,cm_efficiency_item)
        self.stats_table.setItem(2,2,cm_CFM_item)
        self.stats_table.setItem(2,3,cm_GSEO_item)
        self.stats_table.setItem(3,0,QtGui.QTableWidgetItem(("Quarter: %s" %self.current_quarter)))
        self.stats_table.setItem(3,1,cq_efficiency_item)
        self.stats_table.setItem(3,2,cq_CFM_item)
        self.stats_table.setItem(3,3,cq_GSEO_item)
        self.stats_table.setItem(4,0,QtGui.QTableWidgetItem(("Half-Year: %s" %self.current_half_year)))
        self.stats_table.setItem(4,1,chy_efficiency_item)
        self.stats_table.setItem(4,2,chy_CFM_item)
        self.stats_table.setItem(4,3,chy_GSEO_item)

        self.stats_table.setStyleSheet("gridline-color: rgb(0, 0, 0); font: Georgia 18 pt;")
        self.stats_table.resizeColumnsToContents()
        self.stats_table.resizeRowsToContents()
    
    def openStyleSheet(self):
        """PORK Window."""
        self.featureUnavailable()

    def AskAnEditor(self):
        """PORK Window."""
        self.featureUnavailable()

    def askTL(self):
        """PORK Window."""
        self.featureUnavailable()

    def featureUnavailable(self):
        """PORK Window."""
        self.notify("Feature unavailable.", "That feature is still in development. Thank you for your patience.")

    def changedDate(self):
        """PORK Window."""
        new_date = self.getActiveDate()
        self.piggybanker_thread.setDate(new_date)
        self.piggybanker_thread.getPiggyBank()
        self.porker_thread.setDate(new_date)
        self.porker_thread.getEfficiency()
        self.mapToolTips()
        self.FSNEditFinishTriggers()
        self.refreshStatsTable()

    def refreshStatsTable(self):
        self.porker_thread.stats_date = self.getActiveDate()
        self.porker_thread.sentStatsData = False
        self.porker_thread.sentDatesData = False
        self.porker_thread.mode = 3
        

    def populateTableThreaded(self, data, efficiencies):
        #print "Got %d Articles from the piggybanker_thread." %len(data)
        self.piggybank.setData(data, efficiencies)
        self.piggybank.displayData()

    def getActiveDateFileString(self):
        """PORK Window."""
        date = self.workCalendar.selectedDate()
        return "CSVs\\" + str(date.toString('yyyyMMdd')) + ".pork"

    def getActiveDateString(self):
        """PORK Window."""
        date = self.workCalendar.selectedDate()
        return str(date.toString('dddd, dd MMMM yyyy'))

    def getActiveDate(self):
        """PORK Window."""
        """Returns the python datetime for the selected date in the calendar."""
        dateAsQDate = self.workCalendar.selectedDate()
        dateString = str(dateAsQDate.toString('dd/MM/yyyy'))
        dateAsDateTime = OINKM.getDate(dateString)
        return dateAsDateTime

    def displayEfficiencyThreaded(self, efficiency):
        """PORK Window."""
        #print "Received %f efficiency." % efficiency
        #self.alertMessage("Efficiency","Efficiency is %0.2f%%" % (efficiency*100))
        self.efficiencyProgress.setFormat("%0.02f%%" %(efficiency*100))
        #print "Integer value of efficiency = %d" % efficiency
        if math.isnan(efficiency):
            efficiency = 0.0
        efficiency = int(efficiency*100) #this works
        if efficiency > 100:
            self.efficiencyProgress.setRange(0,efficiency)
            new_style = """
            .QProgressBar {
                 border: 2px solid grey;
                 border-radius: 5px;
                 text-align: center;
             }
            .QProgressBar::chunk {
                 background-color: #05B8CC;
                 width: 20px;
             }"""
            self.efficiencyProgress.setStyleSheet(new_style)
        elif 99 <= efficiency <= 100:
            new_style = """
            .QProgressBar {
                 border: 0.5px solid black;
                 border-radius: 5px;
                 text-align: center;
             }
            .QProgressBar::chunk {
                 background-color: #008000;
                 width: 20px;
             }"""
            self.efficiencyProgress.setRange(0,efficiency)
            self.efficiencyProgress.setStyleSheet(new_style)
        else:
            new_style = """
            .QProgressBar {
                 border: 0.5px solid black;
                 border-radius: 5px;
                 text-align: center;
             }
            .QProgressBar::chunk {
                 background-color: #FF0000;
                 width: 20px;
             }"""
            self.efficiencyProgress.setRange(0,100)
            self.efficiencyProgress.setStyleSheet(new_style)
        self.efficiencyProgress.setValue(efficiency)

    def submit(self):
        """PORK Window."""
        """Method to send the FSN data to SQL."""
        #print "Sending data to MOSES."
        data = self.getFSNDataDict()
        if data != []:
            MOSES.addToPiggyBank(data, self.userID, self.password)
        else:
            print "I got nothing!"

    def populateBU(self):
        """PORK Window."""
        self.comboBoxBU.clear()
        bus = list(set(self.category_tree["BU"]))
        bus.sort()
        self.comboBoxBU.addItems(bus)
        self.comboBoxBU.setCurrentIndex(-1)

    def populateSuperCategory(self):
        """PORK Window."""
        self.comboBoxSuperCategory.clear()
        bu = str(self.comboBoxBU.currentText())
        filtered_category_tree = self.category_tree.loc[self.category_tree["BU"] == bu]
        super_categories = list(set(filtered_category_tree["Super-Category"]))
        super_categories.sort()
        self.comboBoxSuperCategory.addItems(super_categories)

    def populateCategory(self):
        """PORK Window."""
        self.comboBoxCategory.clear()
        super_category = str(self.comboBoxSuperCategory.currentText())
        filtered_category_tree = self.category_tree.loc[self.category_tree["Super-Category"] == super_category]
        categories = list(set(filtered_category_tree["Category"]))
        categories.sort()
        self.comboBoxCategory.addItems(categories)

    def populateSubCategory(self):
        """PORK Window."""
        self.comboBoxSubCategory.clear()
        category = str(self.comboBoxCategory.currentText())
        filtered_category_tree = self.category_tree.loc[self.category_tree["Category"] == category]
        sub_categories = list(set(filtered_category_tree["Sub-Category"]))
        sub_categories.sort()
        self.comboBoxSubCategory.addItems(sub_categories)

    def populateBrandVertical(self):
        """PORK Window."""
        self.comboBoxVertical.clear()
        sub_category = str(self.comboBoxSubCategory.currentText())
        filtered_category_tree = self.category_tree.loc[self.category_tree["Sub-Category"] == sub_category]
        verticals = list(set(filtered_category_tree["Vertical"]))
        verticals.sort()
        self.comboBoxVertical.addItems(verticals)
        self.textEditGuidelines.clear()

    def populateClarification(self):
        """PORK Window."""
        self.comboBoxClarification.addItems(MOSES.getClarifications(self.userID,self.password))

    def addClarification(self):
        """PORK Window."""
        if self.lineEditClarification.text() == "NA":
            self.lineEditClarification.clear()
        if str(self.lineEditClarification.text()).find(str(self.comboBoxClarification.currentText())) == -1:
            self.lineEditClarification.insert(str(self.comboBoxClarification.currentText()) + ";")

    def getVerticalGuidelines(self):
        """PORK Window."""
        self.selectedVertical = str(self.comboBoxVertical.currentText())
        try:
            if self.selectedVertical == "BlockConstruction":
                self.textEditGuidelines.clear()
                self.textEditGuidelines.append("Construction blocks teach kids about patterns, cognitive skills and improve their creativity. For more information, read up on Lego and see how many various amateur and professional models exist. It has ascended into an art form. Children aside, some adults wouldn't mind playing with them.")
            else:
                self.textEditGuidelines.clear()
                self.textEditGuidelines.append("There are no guidelines for %s. Please ask your TL if there's anything vertical specific that you need to write." % self.selectedVertical)
        except:
            self.notify("Error", "No vertical has been selected.")

    def closeEvent(self,event):
        """PORK Window."""
        self.askToClose = QtGui.QMessageBox.question(self, 'Close P.O.R.K?', "Are you sure you'd like to quit?\nPlease keep this application open when you're working since it guides you through the process and helps you interact with your process suppliers and customers.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if self.askToClose == QtGui.QMessageBox.Yes:
            MOSES.createLogoutStamp(self.userID, self.password)
            super(Pork, self).closeEvent(event)
        else:
            event.ignore()

    def FSNEditFinishTriggers(self):
        """This should run after the FSN is entered. But it needs type too."""
        self.lineEditFSN.setStyleSheet(".QLineEdit {background-color: white;}")
        fsnString = str(self.lineEditFSN.text()).strip()
        fsn_type = str(self.comboBoxType.currentText()).replace(",",";").strip()
        #print fsnString, fsn_type
        if OINKM.check_if_FSN(fsnString):
            #print "I got an FSN. I'm going to check!"
            isDuplicate = MOSES.checkDuplicacy(fsnString, fsn_type, self.getActiveDate())
            override_status, override_count = MOSES.checkForOverride(fsnString, self.getActiveDate(), self.userID, self.password)
            if isDuplicate == "Local":
                #set background to red. If possible, highlight the FSN in the table displayed.
                self.notify("Duplicate FSN", "You've just reported that FSN!")
                self.lineEditFSN.setStyleSheet(".QLineEdit {background-color:red;}")
            elif (isDuplicate == "Global") and not override_status:
                #set background to orange. Give a notification that this has been written before.
                self.notify("Duplicate FSN", "Someone has already reported that FSN. If you're instructed to change the article, then please ask your TL to raise an override request.")
                #print "Setting bg to orange and triggering notification!"
                self.lineEditFSN.setStyleSheet(".QLineEdit {background-color:orange;}")
            elif (isDuplicate == "Global") and (override_status):
                #reset background to white.
                self.lineEditFSN.setStyleSheet(".QLineEdit {background-color: yellow;}")
                self.generateUploadLink(fsnString)
                
            elif not isDuplicate:
                self.lineEditFSN.setStyleSheet(".QLineEdit {background-color: white;}")
                self.generateUploadLink(fsnString)
                

    def generateUploadLink(self, fsnString):
        """PORK Window."""
        """if (len(str(self.lineEditUploadLink.text())) == 0) and (str(self.lineEditUploadLink.text()).count(' ') <= 0):
                                    fsnString = str(self.lineEditFSN.text()).strip()
                                    if (len(fsnString) == 13) or (len(fsnString) == 16):"""
        self.lineEditUploadLink.setText("http://www.flipkart.com/search?q=" + fsnString)

    def validateForm(self):
        """PORK Window."""
        self.listData = self.fsnData()
        self.done = 0
        for value in self.listData:
            if len(value) == 0:
                self.done = self.done + 1
        if (self.done==0):
            return True
        else:
            return False

    def validateAndSendToPiggy(self):
        """PORK Window."""
        #FIX
        """This method checks if the given data is complete, and then if the data is for today, 
        it allows addition or modification."""
        completion = False
        allowAddition = False
        mode = self.getMode()
        selected_date = self.getActiveDate()
        last_working_date = MOSES.getLastWorkingDate(self.userID, self.password)
        #print "Trying to validateAndSendToPiggy. The last working date is :", last_working_date
        dates_user_is_allowed_to_manipulate = [datetime.date.today(), last_working_date]
        #TEMPORARILY DISABLED.
        #if selected_date not in dates_user_is_allowed_to_manipulate:
            #allowAddition = False
            #self.alertMessage("Not Allowed", "You cannot make changes to dates other than your last working date and today.")
        if mode == "Addition": #CHANGE TO ELIF LATER
            fsnData = self.getFSNDataDict()
            fsn = fsnData["FSN"]
            fsntype = fsnData["Description Type"]
            isDuplicate = MOSES.checkDuplicacy(fsn, fsntype, self.getActiveDate())
            override_status, override_count = MOSES.checkForOverride(fsn, selected_date, self.userID, self.password)
            if isDuplicate == "Local":
                self.alertMessage("Repeated FSN","You just reported that FSN today!")
            elif (isDuplicate == "Global") and not override_status:
                self.alertMessage("Repeated FSN","That FSN was already reported before by a writer. If your TL has instructed you to overwrite the contents, please request an overide request.")
            elif (isDuplicate == "Global") and override_count:
                fsnData["Rewrite Ticket"] = override_count
                MOSES.addToPiggyBank(fsnData, self.userID, self.password)
                self.alertMessage("Success","Successfully added an FSN to the Piggy Bank.")
                self.populateTable()
                completion = True
            else:
                MOSES.addToPiggyBank(fsnData, self.userID, self.password)
                self.alertMessage("Success","Successfully added an FSN to the Piggy Bank.")

                completion = True
        elif mode == "Modification":
            fsnData = self.getFSNDataDict()
            #print "Trying to modify an entry."
            MOSES.updatePiggyBankEntry(fsnData, self.userID, self.password, )
            self.alertMessage("Success", "Successfully modified an entry in the Piggy Bank.")
            #print "Modified!"
            completion = True
        if completion:
            #FSN = fsnData["FSN"]
            #clar_code = str(self.lineEditClarification.text()).strip()
            #clarification_status = MOSES.checkIfClarificationPosted(self.userID, self.password, FSN, clar_code)
            #do I need a comment box? Not yet, maybe after I figure how to make a combocheckbox.
            #if type(clarification_status) == type(selected_date):
            #    MOSES.updateClarification(self.userID, self.password, FSN, self.userID, clar_code)
            #else:
            #    MOSES.addClarification(self.userID, self.password, FSN, selected_date, clar_code)
            #self.populateTable()
            #self.displayEfficiency()
            self.resetForm()
            self.piggybanker_thread.getPiggyBank()
            self.porker_thread.getEfficiency()

    def alertMessage(self, title, message):
        """PORK Window."""
        QtGui.QMessageBox.about(self, title, message)

    def getMode(self):
        """PORK Window."""
        mode = None
        if self.buttonModifyFSN.isChecked():
            mode = "Modification"
        elif self.buttonAddFSN.isChecked():
            mode = "Addition"
        return mode

    def resetForm(self):
        """PORK Window."""
        self.lineEditFSN.setText("")
        self.spinBoxWordCount.setValue(0)
        self.lineEditRefLink.setText("NA")
        self.lineEditUploadLink.setText("")
        self.lineEditClarification.setText("NA")
        self.buttonAddFSN.setChecked(True)

    def cellSelected(self, row, column):
        """Triggered when a cell is clicked.
        If the current mode is set to modification, it will copy the fields in the selected row to the form.
"""
        self.selected_row = row
        self.selected_column = column
        mode = self.getMode()
        if mode == "Modification":
            self.askToOverwrite = QtGui.QMessageBox.question(self, 'Overwrite data?', """Do you want to overwrite
the existing data in the form with the data in the cell and modify that cell?""",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
            if self.askToOverwrite == QtGui.QMessageBox.Yes:
                self.fetchDataToForm(self.selected_row, self.selected_column,"All")

        #if the audit form isn't already cleared,
        #ask for a confirmation about clearing it, clear it and then call this function once again.

    def fetchDataToForm(self, row, column, fields="Recent"):
        """PORK Window."""
        """Fills the form with all/some of the fields."""
        columns = self.piggybank.columnCount()

        for columnCounter in range(columns):

            self.columnHeaderLabel = str(self.piggybank.horizontalHeaderItem(columnCounter).text())
            self.cellValue = str(self.piggybank.item(row, columnCounter).text())

            if self.columnHeaderLabel == "Description Type":
                self.typeIndex = self.comboBoxType.findText(self.cellValue)
                self.comboBoxType.setCurrentIndex(self.typeIndex)

            elif self.columnHeaderLabel == "Priority":
                self.priorityIndex = self.comboBoxPriority.findText(self.cellValue)
                self.comboBoxPriority.setCurrentIndex(self.priorityIndex)

            elif self.columnHeaderLabel == "Source":
                self.sourceIndex = self.comboBoxSource.findText(self.cellValue)
                self.comboBoxSource.setCurrentIndex(self.sourceIndex)

            elif self.columnHeaderLabel == "BU":
                self.BUIndex = self.comboBoxBU.findText(self.cellValue)
                self.comboBoxBU.setCurrentIndex(self.BUIndex)
                self.populateSuperCategory()

            elif self.columnHeaderLabel == "Super-Category":
                self.superIndex = self.comboBoxSuperCategory.findText(self.cellValue)
                self.comboBoxSuperCategory.setCurrentIndex(self.superIndex)
                self.populateCategory()

            elif self.columnHeaderLabel == "Category":
                self.categoryIndex = self.comboBoxCategory.findText(self.cellValue)
                self.comboBoxCategory.setCurrentIndex(self.categoryIndex)
                self.populateSubCategory()

            elif self.columnHeaderLabel == "Sub-Category":
                self.subCatIndex = self.comboBoxSubCategory.findText(self.cellValue)
                self.comboBoxSubCategory.setCurrentIndex(self.subCatIndex)
                self.populateBrandVertical()

            elif self.columnHeaderLabel == "Vertical":
                self.verticalIndex = self.comboBoxVertical.findText(self.cellValue)
                self.comboBoxVertical.setCurrentIndex(self.verticalIndex)

            elif self.columnHeaderLabel == "Brand":
                self.lineEditBrand.setText(self.cellValue)

            elif fields == "All":
                if self.columnHeaderLabel == "FSN":
                    self.lineEditFSN.setText(self.cellValue)
                elif self.columnHeaderLabel == "Upload Link":
                    self.lineEditUploadLink.setText(self.cellValue)
                elif self.columnHeaderLabel == "Reference Link":
                    self.lineEditRefLink.setText(self.cellValue)
                elif self.columnHeaderLabel == "Clarification":
                    self.lineEditClarification.setText(self.cellValue)
                elif self.columnHeaderLabel == "Word Count":
                    self.spinBoxWordCount.setValue(int(self.cellValue))

    def copyCommonFields(self):
        """PORK Window Method to copy common fields over to the next entry."""
        self.fetchDataToForm(self.selected_row, self.selected_column, fields = "Recent")

    def clearAll(self):
        """PORK Window."""
        """Clears all the fields of the form."""
        self.lineEditFSN.setText("")
        self.comboBoxType.setCurrentIndex(-1)
#        self.comboBoxPriority.setCurrentIndex(-1)
        self.comboBoxSource.setCurrentIndex(-1)
        self.comboBoxBU.setCurrentIndex(-1)
        self.comboBoxSuperCategory.setCurrentIndex(-1)
        self.comboBoxCategory.setCurrentIndex(-1)
        self.comboBoxSubCategory.setCurrentIndex(-1)
        self.comboBoxVertical.setCurrentIndex(-1)
        self.spinBoxWordCount.setValue(0)
        self.lineEditBrand.setText("")
        self.lineEditRefLink.setText("")
        self.lineEditUploadLink.setText("")
        self.lineEditClarification.setText("")
        self.buttonAddFSN.setChecked(True)

    def getFSNDataDict(self):
        """This method gets all the relevant data from the form and returns a dictionary."""
        """Checks all the FSN details and returns a dictionary which can be added to the Piggy bank."""
        self.fsnDataList = []
        self.valid = True
        try:
            self.fsn = str(self.lineEditFSN.text()).replace(",",";").replace("'","").strip()
            if len(self.fsn) == 0:
                self.valid = False
                self.alertMessage("User Error","Please enter the FSN.")
                return []
        except:
            self.alertMessage("Runtime Error","Please enter the FSN.")
            self.lineEditFSN.setFocus()
            self.valid = False
            return []
        try:
            self.type = str(self.comboBoxType.currentText()).replace(",",";").replace("'","").strip()
            if len(self.type) == 0:
                self.valid = False
                self.alertMessage("User Error","Please select a type.")
                return []
        except:
            self.alertMessage("Runtime Error","Please select a type.")
            self.comboBoxType.setFocus()
            self.valid = False
            return []
        try:
            self.source = str(self.comboBoxSource.currentText()).replace(",",";").replace("'","").strip()
            if len(self.source) == 0:
                self.valid = False
                self.alertMessage("User Error","Please select a type.")
                return []
        except:
            self.alertMessage("Runtime Error","Please select a source.")
            self.comboBoxSource.setFocus()
            self.valid = False
            return []
        try:
            self.bu = str(self.comboBoxBU.currentText()).replace(",",";").replace("'","").strip()
            if len(self.bu) == 0:
                self.valid = False
                self.alertMessage("User Error","Please select the BU.")
                return []
        except:
            self.alertMessage("Runtime Error","Please select the BU.")
            self.comboBoxBU.setFocus()
            return []
        try:
            self.supercategory = str(self.comboBoxSuperCategory.currentText()).replace(",",";").replace("'","").strip()
            if len(self.supercategory) == 0:
                self.valid = False
                self.alertMessage("User Error","Please select the super-category.")
                return []
        except:
            self.alertMessage("Runtime Error","Please select the super-category.")
            self.comboBoxSuperCategory.setFocus()
            return []
        try:
            self.category = str(self.comboBoxCategory.currentText()).replace(",",";").replace("'","").strip()
            if len(self.category) == 0:
                self.valid = False
                self.alertMessage("User Error","Please select the category.")
                return []
        except:
            self.alertMessage("Runtime Error","Please select the category.")
            self.comboBoxCategory.setFocus()
            self.valid = False
            return []
        try:
            self.subcategory = str(self.comboBoxSubCategory.currentText()).replace(",",";").replace("'","").strip()
            if len(self.subcategory) == 0:
                self.valid = False
                self.alertMessage("User Error","Please select the sub-category.")
                return []
        except:
            self.alertMessage("Runtime Error","Please select the sub-category.")
            self.comboBoxSubCategory.setFocus()
            self.valid = False
            return []
        try:
            self.vertical = str(self.comboBoxVertical.currentText()).replace(",",";").replace("'","").strip()
            if len(self.vertical) == 0:
                self.valid = False
                self.alertMessage("User Error","Please select the vertical.")
                return []
        except:
            self.alertMessage("Runtime Error","Please select the vertical.")
            self.comboBoxVertical.setFocus()
            self.valid = False
            return []
        try:
            self.brand = str(self.lineEditBrand.text()).replace(",",";").replace("'","").strip()
            if len(self.brand) == 0:
                self.valid = False
                self.alertMessage("User Error","Please enter the brand.")
                return []
        except:
            self.alertMessage("Runtime Error","Please enter the brand.")
            self.lineEditBrand.setFocus()
            self.valid = False
            return []
        try:
            self.wordcount = int(self.spinBoxWordCount.value())
            if self.wordcount <= 50:
                answer = QtGui.QMessageBox.question(self, """Are you sure that's the right word count?""", """Are you sure you'd like to report only %d words for this article?""" % self.wordcount, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if answer == QtGui.QMessageBox.No:
                    self.valid = False
        except:
            self.alertMessage("Runtime Error","Please enter the word count. Word count must be an integer.")
            self.spinBoxWordCount.setFocus()
            self.valid = False
            return []
        try:
            self.uploadlink = str(self.lineEditUploadLink.text()).replace(",",";").replace("'","").strip()
            if len(self.uploadlink) == 0:
                self.valid = False
                self.alertMessage("User Error","Please enter the upload link.")
                return []
        except:
            self.alertMessage("Runtime Error","Please enter the upload link.")
            self.lineEditUploadLink.setFocus()
            self.valid = False
            return []
        try:
            self.referencelink = str(self.lineEditRefLink.text()).replace(",",";").replace("'","").strip()
            if len(self.referencelink) == 0:
                self.valid = False
                self.alertMessage("User Error","Please enter the reference link.")
                return []
        except:
            self.alertMessage("Runtime Error","Please enter the reference link.")
            self.lineEditRefLink.setFocus()
            self.valid = False
            return []
        try:
            self.clarification = str(self.lineEditClarification.text()).replace(",",";").replace("'","").strip()
            if len(self.clarification) == 0:
                self.valid = False
                self.alertMessage("User Error","Clarification cell cannot be empty.")
                return []
        except:
            self.alertMessage("Runtime Error","Clarification cell cannot be empty.")
            self.lineEditClarification.setFocus()
            self.valid = False
            return []
        #Success!
        if self.valid:
            writer_name = MOSES.getEmpName(self.userID)
            writer_email = MOSES.getEmpEmailID(self.userID)
            active_date = self.getActiveDate()
            self.fsnDataList = {
                "Article Date": active_date,
                "WriterID": self.userID,
                "Writer Name": writer_name,
                "Writer Email ID": writer_email,
                "FSN": self.fsn,
                "Description Type": self.type,
                "Source": self.source,
                "BU" : self.bu,
                "Super-Category": self.supercategory,
                "Category": self.category,
                "Sub-Category": self.subcategory,
                "Vertical": self.vertical,
                "Brand": self.brand,
                "Word Count": self.wordcount,
                "Upload Link": self.uploadlink,
                "Reference Link": self.referencelink,
                "Rewrite Ticket": 0,
                "End Time": datetime.datetime.now(),
                "PC User Name": getpass.getuser(),
                "Job Ticket": self.getJobTicket(active_date, self.userID, self.fsn)
            }
            query_dict = {
                "Source":self.source,
                "Description Type":self.type,
                "BU":self.bu,
                "Super-Category":self.supercategory,
                "Category": self.category,
                "Sub-Category": self.subcategory,
                "Vertical": self.vertical
            }
            target = MOSES.getTargetFor(self.userID, self.password, query_dict, self.getActiveDate())
            self.fsnDataList.update({"Target": target})
        return self.fsnDataList

    def getJobTicket(self, given_date, given_id, given_fsn):
        import codecs
        ticket_decrypted = "%d%d%d%s%s" %(given_date.year, given_date.month, given_date.day, given_id, given_fsn)
        return str(codecs.encode(ticket_decrypted,"rot_13"))

    def updateStatusBar(self, message):
        #print "Received ", message
        self.status_bar.showMessage(message)

    def mapThreads(self):
        init_date = datetime.date.today()
        self.piggybanker_thread = PiggyBanker(self.userID, self.password, init_date)
        self.piggybanker_thread.piggybankChanged.connect(self.populateTableThreaded)
        self.porker_thread = Porker(self.userID, self.password, init_date, mode=2)
        self.porker_thread.sendEfficiency.connect(self.displayEfficiencyThreaded)
        self.porker_thread.sendDatesData.connect(self.sendDatesDataToCalendar)
        self.porker_thread.sendStatsData.connect(self.updateStatsTable)
        self.porker_thread.sendActivity.connect(self.displayPorkerProgress)


    def calendarPageChanged(self, year, month):
        """When the calendar page is changed, this triggers the porker method which
        fetches the efficiency values for the entire month."""
        self.porker_thread.setVisibleDates(datetime.date(year, month, 15))
        self.porker_thread.sentDatesData = False

    def sendDatesDataToCalendar(self, dates_data):
        self.workCalendar.setDatesData(dates_data)

    def hide_form(self):
        piggy_is_hidden = self.hide_piggy_button.isChecked()
        form_is_hidden = self.hide_form_button.isChecked()
        if (not piggy_is_hidden):
            self.form.setVisible(not form_is_hidden)
            self.resize(200,200)
        elif form_is_hidden:
            self.form.setVisible(form_is_hidden)
            self.resize(800,600)

    def hide_piggy(self):
       #print "Hiding piggy!"
        piggy_is_hidden = self.hide_piggy_button.isChecked()
        form_is_hidden = self.hide_form_button.isChecked()
        if (not form_is_hidden):
            #print "Form isn't hidden, so I'll hide the piggy bank."
            self.piggyWidget.setVisible(not piggy_is_hidden)
        elif piggy_is_hidden:
            self.piggyWidget.setVisible(piggy_is_hidden)


        piggy_is_hidden = self.hide_piggy_button.isChecked()
        form_is_hidden = self.hide_form_button.isChecked()
        if piggy_is_hidden or form_is_hidden:
            self.contract()
        else:
            self.expand()

    def contract(self):
        self.resize(self.centralWidget().minimumSizeHint())
        self.quote_thread.setWidth(50)
        self.center()

    def expand(self):
        self.resize(self.centralWidget().minimumSizeHint())
        self.quote_thread.setWidth(100)
        self.center()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())