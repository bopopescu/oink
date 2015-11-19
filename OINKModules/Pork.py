#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
import getpass
import math
import datetime
import random
import numpy
import pandas as pd
from PyQt4 import QtGui, QtCore

from EfficiencyCalculator import EfficiencyCalculator
from WeekCalendar import WeekCalendar
from LeavePlanner import LeavePlanner
from OINKUIMethods import passwordResetter
from AnimalFarm import AnimalFarm
from PiggyBanker import PiggyBanker
from Porker import Porker
from PiggyBank import PiggyBank
import OINKMethods as OINKM
from ImageButton import ImageButton
from ImageLabel import ImageLabel
from Seeker import Seeker
import MOSES
from CategoryFinder import CategoryFinder
from Player import Player
from TNAViewer import TNAViewer
from ProgressBar import ProgressBar
from SharinganButton import SharinganButton
from CopiableQTableWidget import CopiableQTableWidget
from FormattedDateEdit import FormattedDateEdit
from IconButton import IconButton
from Taunter import Taunter

class Pork(QtGui.QMainWindow):
    def __init__(self, user_id, password, category_tree=None, employees_list=None, brand_list=None):
        super(QtGui.QMainWindow, self).__init__()
        self.x_pos, self.right_pos = "center","middle"
        self.flip = random.randint(0, 1)
        
        #store the variables so they are accessible elsewhere in this class.
        self.user_id = user_id
        self.password = password
        self.brand_list = brand_list
        self.player = Player()
        MOSES.createLoginStamp(self.user_id, self.password)
        if category_tree is None:
            self.category_tree = MOSES.getCategoryTree(self.user_id, self.password)
        else:
            self.category_tree = category_tree
        self.last_working_date = MOSES.getLastWorkingDate(self.user_id, self.password)
        self.clip = QtGui.QApplication.clipboard()
        self.stats_table_headers = ["Timeframe","Efficiency", "CFM", "GSEO"]
        #Create the widgets and arrange them as needed.
        self.mainWidget = QtGui.QWidget()
        self.setCentralWidget(self.mainWidget)
        self.createUI()
        self.mapThreads()
        self.createLayouts()
        #Create all visual and usability aspects of the program.
        self.mapToolTips()
        self.mapEvents()
        self.setTabOrders()
        self.addMenus()
        self.setVisuals()
        self.refreshStatsTable()
        #Initialize the application with required details.
        self.populateBU()
        #self.populateTable()
        self.initForm()
        #self.porker_thread.getStatsData(self.getActiveDate())
        #Final set up.
        self.currentFSNDataList = []
        #Ignorance is bliss.
        #self.setFocusPolicy(QtCore.Qt.NoFocus)
        if self.brand_list is not None:
            brand_completer = QtGui.QCompleter(self.brand_list)
            self.lineEditBrand.setCompleter(brand_completer)


    def mapThreads(self):
        init_date = datetime.date.today()
        if self.user_id == "62487":
            init_date = datetime.date(2015,6,10)
            self.workCalendar.setSelectedDate(QtCore.QDate(init_date))
            self.alertMessage("Heil Vinay!", "Changing the date to %s so that you have data to look at."%init_date)
        self.piggybanker_thread = PiggyBanker(self.user_id, self.password, init_date, category_tree=self.category_tree)
        self.piggybanker_thread.piggybankChanged.connect(self.populateTable)
        #Main thread that supplies daily data based on PORK activities, such as calendar action and entering FSNs.
        self.porker_thread = Porker(self.user_id, self.password, init_date, category_tree=self.category_tree)
        self.porker_thread.sendResultDictionary.connect(self.useResultDictionary)
        self.porker_thread.sendStats.connect(self.useStatsData)

    def createUI(self):
        #creates all the widgets
        #Create the tab widget, adds tabs and creates all the related widgets and layouts.
        self.fk_icon = ImageLabel(os.path.join("Images","fk_logo_mini.png"), 64, 64)
        if self.flip == 0:
            self.bigbrother_icon = ImageButton(os.path.join("Images","bigbrother.png"), 64, 64)
        else:
            self.bigbrother_icon = SharinganButton(64, 64)

        self.bigbrother_icon.setFlat(True)
        self.pork_icon = ImageLabel(os.path.join("Images","pork_logo.png"),64, 64)
        self.v_icon = ImageButton(os.path.join("Images","v.png"),64,64)
        self.fk_icon.setToolTip("Flipkart Content Team")
        self.bigbrother_icon.setToolTip("Big Brother lied. Of course he did.")
        self.pork_icon.setToolTip("All animals are created equal, but some animals are created more equal than others.")
        self.v_icon.setToolTip("Remember, remember, the 5th of November.")
        self.logos_layout = QtGui.QVBoxLayout()
        self.logos_layout.addWidget(self.fk_icon,0)
        self.logos_layout.addWidget(self.bigbrother_icon,0)
        self.logos_layout.addWidget(self.pork_icon,0)
        self.logos_layout.addWidget(self.v_icon,0)
        self.logos_layout.addStretch(10)

        height, width = 32, 32
        self.calculator_button = IconButton("Efficiency Calculator",os.path.join("Images","calculator.png"),height, width, os.path.join("Images","calculator_mouseover.png"))
        self.calculator_button.setToolTip("Open the Efficiency calculator tool.")
        self.calculator_button.setFlat(True)
        self.tna_button = IconButton("TNA", os.path.join("Images","tna.png"),height, width, os.path.join("Images","tna_mouseover.png"))
        self.tna_button.setToolTip("Open the training needs assessment window")
        self.tna_button.setFlat(True)
        self.find_button = IconButton("Find FSNs", os.path.join("Images","find.png"),height, width,os.path.join("Images","find_mouseover.png"))
        self.find_button.setToolTip("Open Seeker to find who wrote an FSN.")
        self.find_button.setFlat(True)
        self.leave_button = IconButton("Leaves and Relaxation",os.path.join("Images","leave.png"),height, width,os.path.join("Images","leave_mouseover.png"))
        self.leave_button.setToolTip("Apply for leaves on the OINK server")
        self.leave_button.setFlat(True)
        #self.relaxation_button = ImageButton(os.path.join("Images","relaxation.png"),height, width,os.path.join("Images","relaxation_mouseover.png"))
        #self.relaxation_button.setToolTip("Apply for relaxation")
        #self.relaxation_button.setFlat(True)
        #self.project_button = ImageButton(os.path.join("Images","projects.png"),height, width, os.path.join("Images","projects_mouseover.png"))
        #self.project_button.setToolTip("Open Project Log")
        #self.project_button.setFlat(True)

        self.icon_panel = QtGui.QHBoxLayout()
        self.icon_panel.addWidget(self.calculator_button,0)
        self.icon_panel.addWidget(self.tna_button,0)
        self.icon_panel.addWidget(self.find_button,0)
        self.icon_panel.addWidget(self.leave_button,0)
        #self.icon_panel.addWidget(self.relaxation_button,0)
        #self.icon_panel.addWidget(self.project_button,0)

        self.piggybank = PiggyBank()
        #initialize Calendar
        self.workCalendar = WeekCalendar(self.user_id, self.password)

        self.workCalendar.setMinimumSize(350,350)
        self.workCalendar.setMaximumHeight(350)

        self.stats = QtGui.QGroupBox("My Performance and Tools")
        self.status_bar = Taunter()
        self.status_bar.setText("Welcome to P.O.R.K. Big Brother is watching you.")
        self.status_bar.setMaximumHeight(50)
        self.menu = self.menuBar()
        self.stats_table = CopiableQTableWidget(0, 0)

        self.stats_table.setToolTip("This report displays your statistics for the last working date.\nIf you've selected a Monday, this will show you\nyour data for last Friday, provided you weren't on leave on that day.\nIf you were, it'll search for the date\non which you last worked and show you that.")
        self.stats_table.setFixedSize(300,160)
        self.refresh_stats_button = ImageButton(os.path.join("Images","refresh.png"),24,24, os.path.join("Images","refresh_mouseover.png"))
        self.refresh_stats_button.setFlat(True)

        self.stats_progress_bar = ProgressBar()
        self.stats_progress_message = QtGui.QLabel("Awaiting signals.")
        self.stats_progress_message.setStyleSheet("QLabel { font-size: 8px }")
        self.stats_progress = QtGui.QWidget()
        self.stats_progress_layout = QtGui.QGridLayout()
        self.stats_progress_layout.addWidget(self.refresh_stats_button,0,0,1,1)
        self.stats_progress_layout.addWidget(self.stats_progress_bar,0,1,1,3)
        self.stats_progress_layout.addWidget(self.stats_progress_message,0,1,1,3)
        self.stats_progress_layout.setColumnStretch(0,0)
        self.stats_progress.setLayout(self.stats_progress_layout)
        self.stats_progress_bar.setRange(0,1)
        self.stats_layout = QtGui.QVBoxLayout()
        self.stats_layout.addLayout(self.icon_panel,0)
        self.stats_layout.addWidget(self.stats_table)
        self.stats_layout.addWidget(self.stats_progress)
        self.stats_layout.addStretch(3)
        self.stats.setLayout(self.stats_layout)


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
        self.category_tree_headers = ["BU","Super-Category","Category","Sub-Category","Vertical"]
        self.category_finder = CategoryFinder(self.category_tree, self.category_tree_headers)



        self.efficiency_progress_bar = ProgressBar()
        self.efficiency_progress_bar.setRange(0,100)
        self.efficiency_progress_bar.setMinimumWidth(200)


        self.efficiency_progress_bar.setTextVisible(True)
        #Create all the widgets associated with the form.
        self.labelFSN = QtGui.QLabel("FSN:")
        self.lineEditFSN = QtGui.QLineEdit(self)
        self.labelType = QtGui.QLabel("Description Type:")
        self.comboBoxType = QtGui.QComboBox()
        self.comboBoxType.setMaximumWidth(150)
        self.comboBoxType.addItems(sorted(set(self.category_tree["Description Type"])))
        self.comboBoxType.setToolTip("Select the description type.")

        self.labelSource = QtGui.QLabel("Source:")
        self.comboBoxSource = QtGui.QComboBox()
        self.comboBoxSource.setMaximumWidth(150)
        self.comboBoxSource.addItems(sorted(set(self.category_tree["Source"])))
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
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                            QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setMaximumWidth(300)
        self.buttonBox.setMaximumHeight(40)


    def createLayouts(self):
        #Begin the form's layout.
        form_fields_layout = QtGui.QGridLayout()
        
        form_fields_layout.addWidget(self.labelFSN,0,0)
        form_fields_layout.addWidget(self.lineEditFSN,0,1,1,3)
        form_fields_layout.addLayout(self.category_finder, 1, 0, 1, 4, QtCore.Qt.AlignLeft)
        form_fields_layout.addWidget(self.labelType,2,0)
        form_fields_layout.addWidget(self.comboBoxType,2,1)
        form_fields_layout.addWidget(self.labelSource,2,2)
        form_fields_layout.addWidget(self.comboBoxSource,2,3)
        form_fields_layout.addWidget(self.labelBU,3,0)
        form_fields_layout.addWidget(self.comboBoxBU,3,1)
        form_fields_layout.addWidget(self.labelSuperCategory,3,2)
        form_fields_layout.addWidget(self.comboBoxSuperCategory,3,3)
        form_fields_layout.addWidget(self.labelCategory,4,0)
        form_fields_layout.addWidget(self.comboBoxCategory,4,1)
        form_fields_layout.addWidget(self.labelSubCategory,4,2)
        form_fields_layout.addWidget(self.comboBoxSubCategory,4,3)
        form_fields_layout.addWidget(self.labelVertical,5,0)
        form_fields_layout.addWidget(self.comboBoxVertical,5,1)
        form_fields_layout.addWidget(self.labelBrand,5,2)
        form_fields_layout.addWidget(self.lineEditBrand,5,3)
        form_fields_layout.addWidget(self.labelWordCount,6,0)
        form_fields_layout.addWidget(self.spinBoxWordCount,6,1)
        form_fields_layout.addWidget(self.labelUploadLink,6,2)
        form_fields_layout.addWidget(self.lineEditUploadLink,6,3)
        form_fields_layout.addWidget(self.labelRefLinks,7,0)
        form_fields_layout.addWidget(self.lineEditRefLink,7,1,1,2)
        form_fields_layout.addWidget(self.buttonBox,8,2,1,2)
        ######################--------------------#################
        #Create a layout for the buttons.
        mode_control_buttons_layout = QtGui.QGridLayout()
        mode_control_buttons_layout.addWidget(self.buttonAddFSN,0,0,1,1,QtCore.Qt.AlignRight)
        mode_control_buttons_layout.addWidget(self.buttonModifyFSN,0,1,1,1,QtCore.Qt.AlignHCenter)
        mode_control_buttons_layout.addWidget(self.buttonCopyFields,0,2,1,1,QtCore.Qt.AlignLeft)

        #set the buttons above the form's layout.
        form_layout = QtGui.QVBoxLayout()
        form_layout.addLayout(mode_control_buttons_layout,1)
        form_layout.addLayout(form_fields_layout,0)
        
        self.form = QtGui.QGroupBox("Piggy Bank Form")
        self.form.setLayout(form_layout)

        calendar_and_icons = QtGui.QGroupBox("My Work Calendar")
        calendars_and_icons_layout = QtGui.QVBoxLayout()
        calendars_and_icons_layout.addWidget(self.workCalendar,3)
        calendar_and_icons.setLayout(calendars_and_icons_layout)
        #Create the piggy bank widget and layout.
        top_row = QtGui.QHBoxLayout()
        top_row.addLayout(self.logos_layout,0)
        top_row.addWidget(calendar_and_icons,0, QtCore.Qt.AlignLeft)
        top_row.addWidget(self.stats,0, QtCore.Qt.AlignHCenter)
        top_row.addWidget(self.form,1, QtCore.Qt.AlignLeft)

        self.piggy_bank_calendar_and_report_layout = QtGui.QVBoxLayout()
        self.piggy_bank_calendar_and_report_layout.addLayout(top_row,0)
        self.piggy_bank_calendar_and_report_layout.addWidget(self.piggybank,2)

        #create the final layout.
        self.finalLayout = QtGui.QVBoxLayout()
        self.finalLayout.addWidget(self.menu,0)
        self.finalLayout.addLayout(self.piggy_bank_calendar_and_report_layout,2)
        self.finalLayout.addWidget(self.efficiency_progress_bar,0)
        self.finalLayout.addWidget(self.status_bar,1)

        #self.finalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        #self.finalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        #Investigate later.
        self.mainWidget.setLayout(self.finalLayout)

    def mapToolTips(self):
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
        self.lineEditBrand.setToolTip("Type the FSN's brand here.\nFor Books, use the writer's name as the brand where appropriate. (If Flipkart ever writes on Books again). \nContact your TL for assistance.")
        self.spinBoxWordCount.setToolTip("Type the word count of the article here.")
        self.lineEditUploadLink.setToolTip("If you are not using an FSN or an ISBN, please paste the appropriate upload link here.")
        self.lineEditRefLink.setToolTip("Paste the reference link(s) here.\nMultiple links can be appended by using a comma or a semi-colon.\nAvoid spaces like the plague.")

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_S:
                self.say = QtGui.QMessageBox.question(self,"All Animals are created equal.","But some animals are <b>more</b> equal than others.", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

    def displayPorkerProgress(self, activity, eta, completed):
        if completed:
            #print "Completed one porker cycle."
            self.stats_progress_bar.setRange(0,1)
            self.stats_progress_message.setText(" Last Updated at %s" % datetime.datetime.strftime(datetime.datetime.now(),"%H:%M:%S"))
        else:
            #print "Porker at work. Message : ", activity
            self.stats_progress_bar.setRange(0,0)
            time_as_string = datetime.datetime.strftime(eta,"%H:%M:%S")
            time_diff = (eta-datetime.datetime.now()).seconds if eta>datetime.datetime.now() else -1
            self.stats_progress_message.setText(" %s\n ETA: %s (%d sec)" %(activity, time_as_string, time_diff))
            
    def setTabOrders(self):
        self.setTabOrder(self.workCalendar, self.buttonAddFSN)
        self.setTabOrder(self.buttonAddFSN, self.buttonModifyFSN)
        self.setTabOrder(self.buttonModifyFSN, self.lineEditFSN)
        self.setTabOrder(self.lineEditFSN, self.comboBoxType)
        self.setTabOrder(self.comboBoxType, self.comboBoxSource)
        self.setTabOrder(self.comboBoxSource, self.comboBoxBU)
        self.setTabOrder(self.comboBoxBU, self.comboBoxSuperCategory)
        self.setTabOrder(self.comboBoxSuperCategory, self.comboBoxCategory)
        self.setTabOrder(self.comboBoxCategory, self.comboBoxSubCategory)
        self.setTabOrder(self.comboBoxSubCategory, self.comboBoxVertical)
        self.setTabOrder(self.comboBoxVertical, self.lineEditBrand)
        self.setTabOrder(self.lineEditBrand, self.spinBoxWordCount)
        self.setTabOrder(self.spinBoxWordCount, self.lineEditUploadLink)
        self.setTabOrder(self.lineEditUploadLink,self.lineEditRefLink)
        self.setTabOrder(self.lineEditRefLink, self.buttonBox)

    def addMenus(self):
        self.fileMenu = self.menu.addMenu("&File")
        self.reset_password_action = QtGui.QAction("Reset password", self)
        self.reset_password_action.triggered.connect(self.reset_password)
        self.fileMenu.addAction(self.reset_password_action)

    def setVisuals(self):
        """PORK Window: Sets all the visual aspects of the PORK Main Window."""
        self.setWindowIcon(QtGui.QIcon(os.path.join(MOSES.getPathToImages(),"PORK_Icon.png")))
        self.setWindowTitle("P.O.R.K. v%s - Server : %s, User: %s (%s)" % (MOSES.version(), MOSES.getHostID(), self.user_id, MOSES.getEmpName(self.user_id)))
        self.center()
        self.move(0,0)
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

    def mapEvents(self):
        self.workCalendar.clicked[QtCore.QDate].connect(self.changedDate)
        self.workCalendar.currentPageChanged.connect(self.calendarPageChanged)
        self.piggybank.cellClicked.connect(self.cellSelected)
        self.piggybank.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.buttonBox.accepted.connect(self.validateAndSendToPiggy)
        self.comboBoxBU.currentIndexChanged['QString'].connect(self.populateSuperCategory)
        self.comboBoxSuperCategory.currentIndexChanged['QString'].connect(self.populateCategory)
        self.comboBoxCategory.currentIndexChanged['QString'].connect(self.populateSubCategory)
        self.comboBoxSubCategory.currentIndexChanged['QString'].connect(self.populateBrandVertical)
        #self.comboBoxVertical.currentIndexChanged['QString'].connect(self.getVerticalGuidelines)
        self.lineEditFSN.editingFinished.connect(self.FSNEditFinishTriggers)
        self.lineEditFSN.textChanged.connect(self.FSNEditFinishTriggers)
        self.comboBoxType.currentIndexChanged['QString'].connect(self.FSNEditFinishTriggers)
        self.buttonBox.rejected.connect(self.clearAll)
        #self.buttonAddClarification.clicked.connect(self.addClarification)
        self.buttonCopyFields.clicked.connect(self.copyCommonFields)
        self.refresh_stats_button.clicked.connect(self.refreshStatsTable)
        self.calculator_button.clicked.connect(self.showEfficiencyCalc)
        self.tna_button.clicked.connect(self.openTNA)
        self.find_button.clicked.connect(self.openSeeker)
        self.leave_button.clicked.connect(self.applyForLeave)
        #self.relaxation_button.clicked.connect(self.openRelaxationTool)
        #self.project_button.clicked.connect(self.openProjectManager)
        self.category_finder.pickRow.connect(self.setFormValues)
        self.v_icon.clicked.connect(self.showAbout)
        self.bigbrother_icon.clicked.connect(self.playTMNT)

    def playTMNT(self):
        self.player.allow_play = True           

    def setFormValues(self, values_dict):
        self.comboBoxBU.setCurrentIndex(self.comboBoxBU.findText(values_dict["BU"]))
        self.comboBoxSuperCategory.setCurrentIndex(self.comboBoxSuperCategory.findText(values_dict["Super-Category"]))
        self.comboBoxCategory.setCurrentIndex(self.comboBoxCategory.findText(values_dict["Category"]))
        self.comboBoxSubCategory.setCurrentIndex(self.comboBoxSubCategory.findText(values_dict["Sub-Category"]))
        self.comboBoxVertical.setCurrentIndex(self.comboBoxVertical.findText(values_dict["Vertical"]))
        self.alertMessage("Used row", "Successfully copied the fields into the Piggy Bank form.")

    def openSeeker(self):
        self.seeker = Seeker(self.user_id, self.password)
        self.seeker.show()

    def openLeaveManagementTool(self):
        self.alertMessage("Feature unavailable","The Leave Management Tool is still under development")

    def openRelaxationTool(self):
        self.alertMessage("Feature unavailable","The Relaxation tool is still under development")

    def openProjectManager(self):
        self.alertMessage("Feature unavailable","The Relaxation tool is still under development")

    def openTNA(self):
        self.tna_viewer = TNAViewer(self.user_id, self.password, self.category_tree)

    def notify(self,title,message):
        """PORK Window: Method to show a tray notification"""
        self.trayIcon.showMessage(title,message)

    def applyForLeave(self):
        """PORK Window: Method to call the leave planner dialog."""
        #print "Applying for a leave!" #debug
        leaveapp = LeavePlanner(self.user_id,self.password)
        if leaveapp.exec_():
            #print "Success!" #debug
            self.alertMessage('Success', "Successfully submitted the request.")
        return True

    def reset_password(self):
        """Opens a password reset method and allows the user to reset his/her password."""
        self.password = passwordResetter(self.user_id, self.password)

    def viewEscalations(self):
        self.featureUnavailable()

    def showEfficiencyCalc(self):
        self.calculator = EfficiencyCalculator(self.user_id, self.password, self.category_tree)
        self.calculator.show()

    def changedDate(self):
        new_date = self.getActiveDate()
        self.piggybanker_thread.setDate(new_date)
        self.piggybanker_thread.getPiggyBank()
        self.refreshStatsTable()
        self.displayEfficiencyThreaded(self.porker_thread.getEfficiencyFor(new_date))
        self.mapToolTips()
        self.FSNEditFinishTriggers()

    def refreshStatsTable(self):
        active_date = self.getActiveDate()
        self.porker_thread.updateForDate(active_date)
        self.porker_thread.getStatsFor(active_date)

    def populateTable(self, data, efficiencies):
        #print "Got %d Articles from the piggybanker_thread." %len(data)
        self.piggybank.setData(data, efficiencies)
        self.piggybank.displayData()

    def getActiveDateString(self):
        date = self.workCalendar.selectedDate()
        return str(date.toString('dddd, dd MMMM yyyy'))

    def getActiveDate(self):
        """Returns the python datetime for the selected date in the calendar."""
        dateAsQDate = self.workCalendar.selectedDate()
        dateString = str(dateAsQDate.toString('dd/MM/yyyy'))
        dateAsDateTime = OINKM.getDate(dateString)
        return dateAsDateTime

    def displayEfficiencyThreaded(self, efficiency):
        #print "Received %f efficiency." % efficiency
        #self.alertMessage("Efficiency","Efficiency is %0.2f%%" % (efficiency*100))
        self.efficiency_progress_bar.setFormat("%0.02f%%" %(efficiency*100))
        #print "Integer value of efficiency = %d" % efficiency
        if math.isnan(efficiency):
            efficiency = 0.0
        efficiency = int(efficiency*100) #this works
        if efficiency > 100:
            self.efficiency_progress_bar.setRange(0,efficiency)
            self.efficiency_progress_bar.setColor("#0088D6")
        elif 99 <= efficiency <= 100:
            self.efficiency_progress_bar.setRange(0,efficiency)
            self.efficiency_progress_bar.setColor("#008000")
        else:
            self.efficiency_progress_bar.setRange(0,100)
            self.efficiency_progress_bar.setColor("#cc0000")
        self.efficiency_progress_bar.setValue(efficiency)

    def submit(self):
        """Method to send the FSN data to SQL."""
        data = self.getFSNDataDict()
        if data != []:
            MOSES.addToPiggyBank(data, self.user_id, self.password)

    def populateBU(self):
        self.comboBoxBU.clear()
        bus = list(set(self.category_tree["BU"]))
        bus.sort()
        self.comboBoxBU.addItems(bus)
        self.comboBoxBU.setCurrentIndex(-1)

    def populateSuperCategory(self):
        self.comboBoxSuperCategory.clear()
        bu = str(self.comboBoxBU.currentText())
        filtered_category_tree = self.category_tree.loc[self.category_tree["BU"] == bu]
        super_categories = list(set(filtered_category_tree["Super-Category"]))
        super_categories.sort()
        self.comboBoxSuperCategory.addItems(super_categories)

    def populateCategory(self):
        self.comboBoxCategory.clear()
        super_category = str(self.comboBoxSuperCategory.currentText())
        filtered_category_tree = self.category_tree.loc[self.category_tree["Super-Category"] == super_category]
        categories = list(set(filtered_category_tree["Category"]))
        categories.sort()
        self.comboBoxCategory.addItems(categories)

    def populateSubCategory(self):
        self.comboBoxSubCategory.clear()
        category = str(self.comboBoxCategory.currentText())
        filtered_category_tree = self.category_tree.loc[self.category_tree["Category"] == category]
        sub_categories = list(set(filtered_category_tree["Sub-Category"]))
        sub_categories.sort()
        self.comboBoxSubCategory.addItems(sub_categories)

    def populateBrandVertical(self):
        self.comboBoxVertical.clear()
        sub_category = str(self.comboBoxSubCategory.currentText())
        filtered_category_tree = self.category_tree.loc[self.category_tree["Sub-Category"] == sub_category]
        verticals = list(set(filtered_category_tree["Vertical"]))
        verticals.sort()
        self.comboBoxVertical.addItems(verticals)

    def closeEvent(self,event):
        self.askToClose = QtGui.QMessageBox.question(self, 'Close P.O.R.K?', "Are you sure you'd like to quit?\nPlease keep this application open when you're working since it guides you through the process and helps you interact with your process suppliers and customers.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if self.askToClose == QtGui.QMessageBox.Yes:
            MOSES.createLogoutStamp(self.user_id, self.password)
            super(Pork, self).closeEvent(event)
        else:
            event.ignore()

    def FSNEditFinishTriggers(self):
        """This should run after the FSN is entered. But it needs type too."""
        self.lineEditFSN.setStyleSheet(".QLineEdit {background-color: white;}")
        fsnString = str(self.lineEditFSN.text()).strip()
        fsn_type = str(self.comboBoxType.currentText()).replace(",",";").strip()
        #print fsnString, fsn_type
        if OINKM.checkIfFSN(fsnString):
            #print "I got an FSN. I'm going to check!"
            isDuplicate = MOSES.checkDuplicacy(fsnString, fsn_type, self.getActiveDate())
            override_status, override_count = MOSES.checkForOverride(fsnString, self.getActiveDate(), self.user_id, self.password)
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
        """if (len(str(self.lineEditUploadLink.text())) == 0) and (str(self.lineEditUploadLink.text()).count(' ') <= 0):
                                    fsnString = str(self.lineEditFSN.text()).strip()
                                    if (len(fsnString) == 13) or (len(fsnString) == 16):"""
        self.lineEditUploadLink.setText("http://www.flipkart.com/search?q=" + fsnString)

    def validateForm(self):
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
        """This method checks if the given data is complete, and then if the data is for today, 
        it allows addition or modification."""
        completion = False
        allowAction = False
        mode = self.getMode()
        selected_date = self.getActiveDate()
        dates_user_is_allowed_to_manipulate = [datetime.date.today(), self.last_working_date]

        if selected_date not in dates_user_is_allowed_to_manipulate:
            allowAction = False
            self.alertMessage("Not Allowed", "You cannot make changes to dates other than your last working date and today.")
        else:
            allowAction = True
        if allowAction:
            if mode == "Addition":
                fsnData = self.getFSNDataDict()
                fsn = fsnData["FSN"]
                fsntype = fsnData["Description Type"]
                if self.isValidType(fsn, fsntype):
                    isDuplicate = MOSES.checkDuplicacy(fsn, fsntype, self.getActiveDate())
                    override_status, override_count = MOSES.checkForOverride(fsn, selected_date, self.user_id, self.password)
                    if isDuplicate == "Local":
                        self.alertMessage("Repeated FSN","You just reported that FSN today!")
                    elif (isDuplicate == "Global") and not override_status:
                        self.alertMessage("Repeated FSN","That FSN was already reported before by a writer. If your TL has instructed you to overwrite the contents, please request an overide request.")
                    elif (isDuplicate == "Global") and override_count:
                        fsnData["Rewrite Ticket"] = override_count
                        MOSES.addToPiggyBank(fsnData, self.user_id, self.password)
                        self.alertMessage("Success","Successfully added an FSN to the Piggy Bank.")
                        self.populateTable()
                        completion = True
                    else:
                        MOSES.addToPiggyBank(fsnData, self.user_id, self.password)
                        self.alertMessage("Success","Successfully added an FSN to the Piggy Bank.")
                        completion = True
            elif mode == "Modification":
                fsnData = self.getFSNDataDict()
                #print "Trying to modify an entry."
                success = MOSES.updatePiggyBankEntry(fsnData, self.user_id, self.password)
                if success:
                    self.alertMessage("Success", "Successfully modified an entry in the Piggy Bank.")
                    completion = True
                else:
                    self.alertMessage("Failure", "Sorry, that entry cannot be modified. That could be because if you make that change, this entry will conflict with another in the piggybank. Ask your TL to make the change herself.")
                    completion = False
                #print "Modified!"
            if completion:
                #Upon completion, do the following things:
                    #Reset the form
                    #Update the efficiency.
                self.resetForm()
                self.piggybanker_thread.getPiggyBank()
                self.porker_thread.updateForDate(selected_date)
                print "Asked to update for %s."%selected_date

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    def isValidType(self, fsn, fsn_type):
        """This method checks if the writer has used a valid description type in the dialog."""
        if ((OINKM.checkIfFSN(fsn)) and ("SEO" in fsn_type)) or (not(OINKM.checkIfFSN(fsn)) and ("SEO" not in fsn_type)):
            #If the value in the fsn field is an FSN and the description type is an SEO type, then it could be invalid.
            #If the value in the fsn field is not an FSN and the description type is not an SEO type, then it could be invalid.
            if "SEO" in fsn_type:
                question = "You seem to be writing an FSN article but the description type appears to be an SEO. Are you sure you want to submit that?"
            else:
                question = "You seem to be writing about something that's not an FSN. Are you sure you want to submit that?"
            change_type = QtGui.QMessageBox.question(
                                self,
                                "Possible Description Type Mismatch",
                                question,
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, 
                                QtGui.QMessageBox.No
                            )
            if change_type is not None:
                if change_type == QtGui.QMessageBox.Yes:
                    is_valid = True
                else:
                    is_valid = False
            else:
                is_valid = False
        else:
            #If the value in the FSN field is an FSN and the type is not an SEO type.
            #if the value is not an FSN and the type is one of the SEO types.
            is_valid = True
        return is_valid

    def getMode(self):
        mode = None
        if self.buttonModifyFSN.isChecked():
            mode = "Modification"
        elif self.buttonAddFSN.isChecked():
            mode = "Addition"
        return mode

    def resetForm(self):
        self.lineEditFSN.setText("")
        self.spinBoxWordCount.setValue(0)
        self.lineEditRefLink.setText("NA")
        self.lineEditUploadLink.setText("")
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
                elif self.columnHeaderLabel == "Word Count":
                    self.spinBoxWordCount.setValue(int(self.cellValue))

    def copyCommonFields(self):
        """PORK Window Method to copy common fields over to the next entry."""
        self.fetchDataToForm(self.selected_row, self.selected_column, fields = "Recent")

    def clearAll(self):
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
        #Success!
        if self.valid:
            writer_name = MOSES.getEmpName(self.user_id)
            writer_email = MOSES.getEmpEmailID(self.user_id)
            active_date = self.getActiveDate()
            self.fsnDataList = {
                "Article Date": active_date,
                "WriterID": self.user_id,
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
                "Job Ticket": self.getJobTicket(active_date, self.user_id, self.fsn)
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
            target = MOSES.getTargetFor(self.user_id, self.password, query_dict, self.getActiveDate(), self.category_tree)
            self.fsnDataList.update({"Target": target})
        return self.fsnDataList

    def getJobTicket(self, given_date, given_id, given_fsn):
        import codecs
        ticket_decrypted = "%d%d%d%s%s" %(given_date.year, given_date.month, given_date.day, given_id, given_fsn)
        return str(codecs.encode(ticket_decrypted,"rot_13"))

    def useResultDictionary(self, result_dictionary):
        current_dict = result_dictionary.get(self.getActiveDate())
        if current_dict is not None:
            self.displayEfficiencyThreaded(current_dict["Efficiency"])
        self.workCalendar.setDatesData(result_dictionary)

    def useStatsData(self, stats):
        self.stats_table.showDataFrame(stats)
        self.stats_table.adjustToColumns()

    def calendarPageChanged(self, year, month):
        """When the calendar page is changed, this triggers the porker method which
        fetches the efficiency values for the entire month."""
        success = self.porker_thread.extendDates(datetime.date(year, month, 1))
        #if not success:
        #    self.alertMessage("Failure!","Unable to extend the thread's dates for some reason.")
        #efficiency = self.porker_thread.getEfficiencyFor(self.getActiveDate())
        #self.porker_thread.sentDatesData = False

    def sendDatesDataToCalendar(self, dates_data):
        self.workCalendar.setDatesData(dates_data)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def showAbout(self):
        title = "About OINK"
        message = "OINK and all related tools were created over a period of a year, starting on the 5th of November 2014, by Vinay Keerthi. The <a href=\"https://www.github.com/vinay87/oink\">github page</a> has more details regarding development."
        QtGui.QMessageBox.about(self, title, message)


    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if event.buttons() == QtCore.Qt.NoButton:
                pos = QtGui.QCursor().pos()
                x, y = pos.x(), pos.y()
                bigbrother_pos = self.bigbrother_icon.pos()
                x_diff = (x-bigbrother_pos.x())
                width, height = 64, 64
                if x_diff>width:
                    x_pos = "right"
                elif x_diff<0:
                    x_pos = "left"
                else:
                    x_pos = "center"
                y_diff = (y - bigbrother_pos.y())
                if y_diff <0:
                    y_pos = "above"
                elif y_diff>height:
                    y_pos = "below"
                else:
                    y_pos = "middle"
                if (x_pos != self.x_pos) or (y_pos !=self.y_pos):
                    if self.flip == 0:
                        image_path = os.path.join("Images","bigbrother","sauron","%s_%s.png"%(x_pos,y_pos))
                        self.bigbrother_icon.showImage(image_path)
                    self.x_pos, self.y_pos = x_pos, y_pos
        return QtGui.QMainWindow.eventFilter(self, source, event)