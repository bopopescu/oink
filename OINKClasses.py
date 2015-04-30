#!/usr/bin/python2
# -*- coding: utf-8 -*-

#OINKClasses
#Contains the EfficiencyCalculator, the Calculator Row, the PORKWindow, 
#VINDALOOWindow, BACONWindow classes.

__version__ = "1.0 - MOSES"
__DocString__ = """
*************************
P.O.R.K. - O.I.N.K. Report Management System
P.O.R.K. - PiggyBank Organizer and Relay Konsole
P.O.R.K. and the O.I.N.K. report management system were developed by 
Vinay Keerthi K. T. for the Flipkart Internet Private Limited Content Team.
They were developed primarily over a period of three months.

Coder Note:

Read the Change Log text file for more information.

This code is pridominantly written in accordance with PEP 8 and PEP 20 guidelines, the
guidelines otherwise known as the Zen of Python.
*************************
"""

#import required modules

import os
import time
import csv
import sys 
import math
from glob import glob
from datetime import datetime

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt

import OINKMethods as OINKM
import MOSES

#########################################################################
#################Efficiency Calculator class definition##################
#########################################################################

class calculatorRow(QtGui.QWidget):
    """Class definition for a single row of the efficiency calculator."""
    def __init__(self, userID, password):
        """Calculator Row"""
        super(calculatorRow, self).__init__()
        self.userID = userID
        self.password = password
        self.createWidgets()
        self.createLayouts()
        self.populateTypeSource()
        self.mapToolTips()
        self.populateBU()
        self.createEvents()

    def createWidgets(self):
        """Calculator Row: Method to create widgets for a single calculator Row."""
        startTime = datetime.now()        
        self.calcWidgets = {}
        self.calcWidgets.update({"Description Type": QtGui.QComboBox()})
        self.calcWidgets.update({"Source": QtGui.QComboBox()})
        self.calcWidgets.update({"BU": QtGui.QComboBox()})
        self.calcWidgets.update({"Super-Category": QtGui.QComboBox()})
        self.calcWidgets.update({"Category": QtGui.QComboBox()})
        self.calcWidgets.update({"Sub-Category": QtGui.QComboBox()})
        self.calcWidgets.update({"Vertical": QtGui.QComboBox()})
        self.calcWidgets.update({"Quantity": QtGui.QSpinBox()})
        self.calcWidgets.update({"Efficiency": QtGui.QLabel("00.00%")})
        
        functionName = sys._getframe().f_code.co_name
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def mapToolTips(self):
        """Calculator Row"""
        self.calcWidgets["Description Type"].setToolTip("Choose the type of the description.")
        self.calcWidgets["Source"].setToolTip("Choose the article source.")
        self.calcWidgets["BU"].setToolTip("Select the BU")
        self.calcWidgets["Super-Category"].setToolTip("Select the Super-Category")
        self.calcWidgets["Category"].setToolTip("Select the Category")
        self.calcWidgets["Sub-Category"].setToolTip("Select the Sub-Category")
        self.calcWidgets["Vertical"].setToolTip("Select the Vertical")
        self.calcWidgets["Quantity"].setToolTip("Select the Quantity of the article.")
        self.calcWidgets["Efficiency"].setToolTip("This is the efficiency one receives for the selected FSN type.")

    def createLayouts(self):
        """Calculator Row"""
        startTime = datetime.now()
        self.calcLayout = QtGui.QHBoxLayout()
        self.calcLayout.addWidget(self.calcWidgets["Description Type"])
        self.calcLayout.addWidget(self.calcWidgets["Source"])
        self.calcLayout.addWidget(self.calcWidgets["BU"])
        self.calcLayout.addWidget(self.calcWidgets["Super-Category"])
        self.calcLayout.addWidget(self.calcWidgets["Category"])
        self.calcLayout.addWidget(self.calcWidgets["Sub-Category"])
        self.calcLayout.addWidget(self.calcWidgets["Vertical"])
        self.calcLayout.addWidget(self.calcWidgets["Quantity"])
        self.calcLayout.addWidget(self.calcWidgets["Efficiency"])
        self.setLayout(self.calcLayout)

        functionName = sys._getframe().f_code.co_name
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def createEvents(self):
        """Calculator Row"""
        startTime = datetime.now()
        self.calcWidgets["BU"].currentIndexChanged.connect(self.populateSupC)
        self.calcWidgets["Super-Category"].currentIndexChanged.connect(self.populateC)
        self.calcWidgets["Category"].currentIndexChanged.connect(self.populateSubC)
        self.calcWidgets["Sub-Category"].currentIndexChanged.connect(self.populateVert)
        self.calcWidgets["Quantity"].valueChanged.connect(self.updateEfficiency)
        functionName = sys._getframe().f_code.co_name
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def updateEfficiency(self):
        """Calculator Row"""
        startTime = datetime.now()
        self.calcWidgets["Efficiency"].setText("%.2f%%" % (self.getEfficiency()))
        functionName = sys._getframe().f_code.co_name
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)
   
    def populateTypeSource(self):
        """Calculator Row"""
        self.types = MOSES.getDescriptionTypes(self.userID,self.password)
        self.sources = MOSES.getSources(self.userID,self.password)
        self.calcWidgets["Description Type"].clear()
        self.calcWidgets["Description Type"].addItems(self.types)
        self.calcWidgets["Source"].clear()
        self.calcWidgets["Source"].addItems(self.sources)
        self.calcWidgets["Description Type"].setCurrentIndex(-1)
        self.calcWidgets["Source"].setCurrentIndex(-1)

    def populateBU(self):
        """Calculator Row"""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name
        BUValues = MOSES.getBUValues(self.userID,self.password)
        self.calcWidgets["BU"].clear()
        self.calcWidgets["BU"].addItems(BUValues)
        self.calcWidgets["BU"].setCurrentIndex(-1)

        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def populateSupC(self):
        """Calculator Row"""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name
        selectedBU = self.calcWidgets["BU"].currentText()
        self.calcWidgets["Super-Category"].clear()
        SupCValues = MOSES.getSuperCategoryValues(self.userID, self.password, BU=selectedBU)
        self.calcWidgets["Super-Category"].addItems(SupCValues)
        self.calcWidgets["Super-Category"].setCurrentIndex(-1)

        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def populateC(self):
        """Calculator Row"""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name
        selectedSupC = self.calcWidgets["Super-Category"].currentText()
        self.calcWidgets["Category"].clear()
        CatValues = MOSES.getCategoryValues(self.userID, self.password, SupC = selectedSupC)
        self.calcWidgets["Category"].addItems(CatValues)
        self.calcWidgets["Category"].setCurrentIndex(-1)
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def populateSubC(self):
        """Calculator Row"""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name
        selectedC = self.calcWidgets["Category"].currentText()
        self.calcWidgets["Sub-Category"].clear()
        SubCValues = MOSES.getSubCategoryValues(self.userID,self.password,Cat=selectedC)
        self.calcWidgets["Sub-Category"].addItems(SubCValues)
        self.calcWidgets["Sub-Category"].setCurrentIndex(-1)
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def populateVert(self):
        """Calculator Row"""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name
        selectedSubC = self.calcWidgets["Sub-Category"].currentText()
        self.calcWidgets["Vertical"].clear()
        VertValues = MOSES.getVerticalValues(self.userID, self.password, SubC = selectedSubC)
        self.calcWidgets["Vertical"].addItems(VertValues)
        self.calcWidgets["Vertical"].setCurrentIndex(-1)
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def getEfficiency(self):
        """Calculator Row"""
        startTime = datetime.now()        
        target = float(MOSES.getTargetFor(self.userID, self.password, DescriptionType = self.calcWidgets["Description Type"].currentText(), Source = self.calcWidgets["Source"].currentText(), BU = self.calcWidgets["BU"].currentText(), SuperCategory = self.calcWidgets["Super-Category"].currentText(), Category = self.calcWidgets["Category"].currentText(), SubCategory = self.calcWidgets["Sub-Category"].currentText(), Vertical = self.calcWidgets["Vertical"].currentText()))
        quantity = float(self.calcWidgets["Quantity"].value())
        functionName = sys._getframe().f_code.co_name
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)
        
        return (quantity*100.00/target)



class efficiencyCalculator(QtGui.QDialog):
    """Class definition for the efficiency calculator."""
    def __init__(self, userID, password):
        """Efficiency Calculator Initializer function."""
        self.userID = userID
        self.password = password
        super(efficiencyCalculator,self).__init__()
        self.calcList = []
        self.createWidgets()
        self.createLayouts()
        self.createEvents()
        #self.populateBU()
        #self.rebuildCalcRow(1)
        self.setVisuals()

    def createWidgets(self):
        """Efficiency Calculator: Creates widgets."""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name

        self.typeLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Description Type</b></font>")
        self.SourceLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Source</b></font>")
        self.BULabel = QtGui.QLabel("<font size=3 face=Georgia><b>BU</b></font>")
        self.SupCLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Super-Category</b></font>")
        self.CatLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Category</b></font>")
        self.SubCLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Sub-Category</b></font>")
        self.VertLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Vertical</b></font>")
        self.QtyLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Quantity</b></font>")
        self.EffLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Efficiency</b></font>")
        
        self.calcLayout  = QtGui.QVBoxLayout()
        self.addCalcRow()

        self.plusButton = QtGui.QPushButton("Add Another Type of Article")
        #self.findIdenLabel = QtGui.QLabel("Find a vertical")
        self.refreshButton = QtGui.QPushButton("Recalculate Efficiency")
        self.totEffLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Total Efficiency:</b></font>")
        self.effScoreLabel = QtGui.QLabel("<font size=3 face=Georgia><b>00.00%</b></font>")
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def createLayouts(self):
        """Efficiency Calculator."""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name

        self.labelsLayout = QtGui.QHBoxLayout()
        self.labelsLayout.addWidget(self.typeLabel)
        self.labelsLayout.addStretch(1)
        self.labelsLayout.addWidget(self.SourceLabel)
        self.labelsLayout.addStretch(1)
        self.labelsLayout.addWidget(self.BULabel)
        self.labelsLayout.addStretch(1)
        self.labelsLayout.addWidget(self.SupCLabel)
        self.labelsLayout.addStretch(1)
        self.labelsLayout.addWidget(self.CatLabel)
        self.labelsLayout.addStretch(1)
        self.labelsLayout.addWidget(self.SubCLabel)
        self.labelsLayout.addStretch(1)
        self.labelsLayout.addWidget(self.VertLabel)
        self.labelsLayout.addStretch(1)
        self.labelsLayout.addWidget(self.QtyLabel)
        self.labelsLayout.addStretch(1)
        self.labelsLayout.addWidget(self.EffLabel)
        
        self.effLayout = QtGui.QHBoxLayout()
        self.effLayout.addWidget(self.plusButton)
        self.effLayout.addWidget(self.refreshButton)
        self.effLayout.addStretch(2)
        self.effLayout.addWidget(self.totEffLabel)
        self.effLayout.addWidget(self.effScoreLabel)
        
        self.finalLayout = QtGui.QVBoxLayout()

        self.finalLayout.addLayout(self.labelsLayout)
        self.finalLayout.addLayout(self.calcLayout)
        self.finalLayout.addStretch(1)
        self.finalLayout.addLayout(self.effLayout)

        self.setLayout(self.finalLayout)

        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def addCalcRow(self):
        """Efficiency Calculator."""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name
        #print "Entered the loop!"
        self.calcList.append(calculatorRow(self.userID, self.password)) 
        #print "Printing Calc List", self.calcList
        self.calcLayout.addWidget(self.calcList[-1])
        #print "There are %d rows in the calcList" % len(self.calcList)
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)
    
    def createEvents(self):
        """Efficiency Calculator."""
        startTime = datetime.now()
        self.plusButton.clicked.connect(self.plusAction)
        self.refreshButton.clicked.connect(self.displayEfficiency)
        self.connectQuantityWidgets()
        functionName = sys._getframe().f_code.co_name
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def setVisuals(self):
        """Efficiency Calculator."""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name
        self.setWindowTitle("Efficiency Calculator")
        self.resize(800,100)
        self.show()
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def plusAction(self):
        """Efficiency Calculator."""
        self.addCalcRow()
        self.connectQuantityWidgets()

    def connectQuantityWidgets(self):
        """Efficiency Calculator."""
        for calc_row in self.calcList:
            calc_row.calcWidgets["Quantity"].valueChanged.connect(self.displayEfficiency)
        
    def displayEfficiency(self):
        """Efficiency Calculator."""
        startTime = datetime.now()
        totalEfficiency = 0.0
        for calc_row in self.calcList:
            calc_row.updateEfficiency()
            totalEfficiency += calc_row.getEfficiency()
        self.effScoreLabel.setText("%.2f%%"%totalEfficiency)
        functionName = sys._getframe().f_code.co_name
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

    def findIdentifier(self):
        """Efficiency Calculator."""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

#I still don't know how to import modules from another folder.
class WeekCalendar(QtGui.QCalendarWidget):
    def __init__(self, userid, password):
        """WeekCalendar"""
        self.UID = userid
        self.pwd = password
        QtGui.QCalendarWidget.__init__(self)
        self.color = QtGui.QColor(self.palette().color(QtGui.QPalette.Highlight))
        self.color.setAlpha(16)
        self.selectionChanged.connect(self.updateCells)
    
    def paintCell(self, painter, rect, date):
        """WeekCalendar"""
        QtGui.QCalendarWidget.paintCell(self, painter, rect, date)
        first_day = self.firstDayOfWeek()
        last_day = first_day + 6
        current_date = self.selectedDate()
        current_day = current_date.dayOfWeek()       
        if first_day <= current_day:
            first_date = current_date.addDays(first_day - current_day)
        else:
            first_date = current_date.addDays(first_day - 7 - current_day)
        last_date = first_date.addDays(6)        
        if first_date <= date <= last_date:
            painter.fillRect(rect, self.color)
        #try this!
        status, relaxation = MOSES.getWorkingStatus(self.UID,self.pwd,date.toPyDate())
        if status == "Working" and relaxation == 0.0 :
            painter.drawText(rect.bottomLeft(),"W")
        elif status == "Working" and relaxation > 0.0:
            painter.drawText(rect.bottomLeft(),"R%0.2f%%" % (relaxation*100))
        else:
            painter.drawText(rect.bottomLeft(),"L") 


class leavePlanner(QtGui.QDialog):
    def __init__(self,userid,password):
        """Leave Planner."""
        super(leavePlanner,self).__init__()
        self.userID = userid
        self.password = password
        self.createWidgets()
        self.mapTooltips()
        self.createEvents()
        self.createLayouts()
        self.setVisuals()
 
    def createWidgets(self):
        """Leave Planner: Method to create all the necessary widgets for the leave planner class."""
        self.mainLabel = QtGui.QLabel("Apply for Leaves or Relaxation in Work")
        self.dateLabel1 = QtGui.QLabel("Start Date:")
        self.dateLineEdit1 = QtGui.QDateTimeEdit()
        self.dateLineEdit1.setDisplayFormat("MMMM dd, yyyy")
        self.dateLineEdit1.setMinimumDate(QtCore.QDate(2015,1,1))
        self.dateLineEdit1.setCalendarPopup(True)
        self.dateLabel2 = QtGui.QLabel("End Date:")
        self.dateLineEdit2 = QtGui.QDateTimeEdit()
        self.dateLineEdit2.setDisplayFormat("MMMM dd, yyyy")
        self.dateLineEdit2.setMinimumDate(QtCore.QDate(2015,1,1))
        self.dateLineEdit2.setCalendarPopup(True)
        self.statusLabel = QtGui.QLabel("Working Status:")
        self.statusComboBox = QtGui.QComboBox()
        self.statusComboBox.addItems(["Working","Leave","Holiday"])
        self.relaxationLabel = QtGui.QLabel("Work Relaxation:")
        self.relaxationSpinBox = QtGui.QSpinBox()
        self.relaxationSpinBox.setRange(0,100)
        self.commentLabel = QtGui.QLabel("Comments:")
        self.commentLineEdit = QtGui.QLineEdit()
        self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                            QtGui.QDialogButtonBox.Cancel)

    def createLayouts(self):
        """Leave Planner: Method to create layouts."""

        self.datesLayout = QtGui.QHBoxLayout()
        self.datesLayout.addWidget(self.dateLabel1)
        self.datesLayout.addWidget(self.dateLineEdit1)
        self.datesLayout.addWidget(self.dateLabel2)
        self.datesLayout.addWidget(self.dateLineEdit2)

        self.statusRelaxLayout = QtGui.QHBoxLayout()
        self.statusRelaxLayout.addWidget(self.statusLabel)
        self.statusRelaxLayout.addWidget(self.statusComboBox)
        self.statusRelaxLayout.addWidget(self.relaxationLabel)
        self.statusRelaxLayout.addWidget(self.relaxationSpinBox)

        self.commentsLayout = QtGui.QHBoxLayout()
        self.commentsLayout.addWidget(self.commentLabel,0)
        self.commentsLayout.addWidget(self.commentLineEdit,3)

        self.finalLayout = QtGui.QVBoxLayout()
        self.finalLayout.addWidget(self.mainLabel)
        self.finalLayout.addLayout(self.datesLayout)
        self.finalLayout.addLayout(self.statusRelaxLayout)
        self.finalLayout.addLayout(self.commentsLayout)
        self.finalLayout.addWidget(self.buttons)
    
        self.setLayout(self.finalLayout)

    def mapTooltips(self):
        """Leave Planner: Maps the appropriate tooltips to the input widgets."""
        self.dateLineEdit1.setToolTip("Select the start date for applying for leaves\nor work relaxation.")
        self.dateLineEdit2.setToolTip("Select the end date for application.\nIf you want a leave on one day, leave this field as it is.")
        self.statusComboBox.setToolTip("Select whether you are working on this day or if you'd like a leave.")
        self.relaxationSpinBox.setToolTip("Set the box to appropriate relaxation you are awarded.\nIf your TL is allowing you to report 80%% for the day, set this box to 20%%.")
        self.commentLineEdit.setToolTip("Type a reason why you require this leave or relaxation for future record.")

    def createEvents(self):
        """Leave Planner: Method to map events."""
        self.dateLineEdit1.dateChanged.connect(self.limitEndDate)
        self.buttons.accepted.connect(self.submit)
        self.buttons.rejected.connect(self.reject)

    def setVisuals(self):
        """Leave Planner."""
        self.resize(300,100)
        self.center()
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.setWindowTitle("Leave and Work Relaxation")

    def center(self):
        """Leave Planner."""
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def limitEndDate(self):
        """Leave Planner: Method to limit the end date's minimum value to the start date."""
        self.dateLineEdit2.setMinimumDate(self.dateLineEdit1.date())

    def submit(self):
        """Leave Planner: Method to send the request to the work calendar table."""
        startDate = self.dateLineEdit1.date().toPyDate()
        endDate = self.dateLineEdit2.date().toPyDate()
        status = str(self.statusComboBox.currentText())
        relaxation = self.relaxationSpinBox.value() #Test this.
        relaxation = float(relaxation)/100.00
        comment = str(self.commentLineEdit.text())

        datesList = OINKM.getDatesBetween(startDate,endDate)
        for oneDate in datesList:
            MOSES.modWorkingStatus(self.userID,self.password,oneDate,status,relaxation,comment)
        super(leavePlanner,self).accept()

    def reject(self):
        """Leave Planner: Method to close the dialog box."""
        super(leavePlanner,self).reject()


##########################################################
##############PORKWindow Class Definition#################
##########################################################
 
class PORKWindow(QtGui.QMainWindow):
    def __init__(self, userID, password):
        """PORK Window."""
        super(QtGui.QMainWindow, self).__init__()
        #store the variables so they are accessible elsewhere in this class.
        self.userID = userID
        self.password = password
        #Create the widgets and arrange them as needed.
        self.mainWidget = QtGui.QWidget()
        self.setCentralWidget(self.mainWidget)
        self.widgetGenerator()
        self.widgetLayout()
        #Create all visual and usability aspects of the program.
        self.mapToolTips()
        self.setEvents()
        self.createActions()
        self.createTabOrder()
        self.addMenus()
        self.setVisuals()
        #Initialize the application with required details.
        self.populateBU()       
        self.populateTable()
        self.populateClarification()
        self.initForm()
        #Final set up.
        self.currentFSNDataList = []
        self.displayEfficiency()
        self.clip = QtGui.QApplication.clipboard()
        #Ignorance is bliss.
        brotherEyeOpen()    
        self.statusBar().showMessage("Welcome to P.O.R.K. All animals are created equal, but some animals are more equal than others.")

    def widgetGenerator(self):
        """PORK Window."""
        #creates all the widgets
        #Create the tab widget, adds tabs and creates all the related widgets and layouts.
        self.table = QtGui.QTableWidget(0, 0, self)
        self.tabs = QtGui.QTabWidget()
        self.stats = QtGui.QWidget()
        self.stats_layout = QtGui.QVBoxLayout()
        #yesterday means the last working day.       
        yesterday = MOSES.getLastWorkingDate(self.userID, self.password)
        self.yest_label = QtGui.QLabel("<b><u>Highlights for %s</b></u>" % yesterday)
        self.yest_efficiency_label = QtGui.QLabel("<b>Efficiency:</b>")
        #yest_efficiency = MOSES.getEfficiencyFor(self.userID, self.password, yesterday)*100
        yest_efficiency = 100.00
        self.yest_efficiency_score = QtGui.QLabel("%.2f %%" % yest_efficiency)
        self.yest_quality_label = QtGui.QLabel("<b>Quality:</b>")
        #disabled for now.
        #yest_Quality = MOSES.getQualityFor(self.userID, self.password, yesterday) #multiply 100!
        yest_Quality = {"CFM": 96.00, "GSEO": 100.00}
        self.yest_quality_score = QtGui.QLabel("%.2f%% <i>(CFM)</i>, %.2f%% <i>(GSEO)</i>." % (yest_Quality["CFM"], yest_Quality["GSEO"]))
        self.WTD_label = QtGui.QLabel("<b><u>Weekly Total Deliverables</u></b>")
        self.WTD_quality_label = QtGui.QLabel("<b>Quality:</b>")
        #disabled for now.
        #WTD_Quality = MOSES.getWTDQuality(self.userID, self.password, yesterday)
        WTD_Quality = {"CFM": 96.00, "GSEO": 100.00}
        self.WTD_quality_score = QtGui.QLabel("%.2f%% <i>(CFM)</i>, %.2f%% <i>(GSEO)</i>." % (WTD_Quality["CFM"], WTD_Quality["GSEO"]))
        self.WTD_efficiency_label = QtGui.QLabel("<b>Efficiency:</b>")
        #WTD_Efficiency = MOSES.getWTDEfficiency(self.userID, self.password, yesterday)
        WTD_Efficiency = 100.00
        self.WTD_efficiency_score = QtGui.QLabel("%.2f%%" % WTD_Efficiency)
        self.MTD_label = QtGui.QLabel("<b><u>Monthly Total Deliverables</u></b>")
        self.MTD_quality_label = QtGui.QLabel("<b>Quality:</b>")
        
        #MTD_Quality = MOSES.getMTDQuality(self.userID, self.password, yesterday)
        MTD_Quality = {"CFM": 96.00, "GSEO": 100.00}
        self.MTD_quality_score = QtGui.QLabel("%.2f%% <i>(CFM)</i>, %.2f%% <i>(GSEO)</i>."%(MTD_Quality["CFM"], MTD_Quality["GSEO"]))
        self.MTD_efficiency_label = QtGui.QLabel("<b>Efficiency:</b>")
        #MTD_efficiency = MOSES.getMTDEfficiency(self.userID, self.password, yesterday)
        MTD_efficiency = 100.00
        self.MTD_efficiency_score = QtGui.QLabel("%.2f%%" % MTD_efficiency)
        self.refresh_stats_button = QtGui.QPushButton("Refresh Statistics")
        self.stats_layout.addWidget(self.yest_label)
        self.yest_stats = QtGui.QHBoxLayout()
        self.yest_stats.addWidget(self.yest_efficiency_label)
        self.yest_stats.addWidget(self.yest_efficiency_score,2)
        self.yest_stats.addWidget(self.yest_quality_label)
        self.yest_stats.addWidget(self.yest_quality_score,2)
        self.stats_layout.addLayout(self.yest_stats)
        self.stats_layout.addWidget(self.WTD_label)
        self.WTD_stats = QtGui.QHBoxLayout()
        self.WTD_stats.addWidget(self.WTD_efficiency_label)
        self.WTD_stats.addWidget(self.WTD_efficiency_score)
        self.WTD_stats.addWidget(self.WTD_quality_label)
        self.WTD_stats.addWidget(self.WTD_quality_score)
        self.stats_layout.addLayout(self.WTD_stats)
        self.stats_layout.addWidget(self.MTD_label)
        self.MTD_stats = QtGui.QHBoxLayout()
        self.MTD_stats.addWidget(self.MTD_efficiency_label)
        self.MTD_stats.addWidget(self.MTD_efficiency_score)
        self.MTD_stats.addWidget(self.MTD_quality_label)
        self.MTD_stats.addWidget(self.MTD_quality_score)
        self.stats_layout.addLayout(self.MTD_stats)
        self.stats_layout.addWidget(self.refresh_stats_button)
        self.stats.setLayout(self.stats_layout)
        self.tabs.addTab(self.stats,"Writer Statistics")
        self.tabs.addTab(self.table,"Piggy Bank")

        #initialize Calendar
        self.workCalendar = WeekCalendar(self.userID, self.password)
        self.workCalendar.setGridVisible(True)
        #initialize buttons to modify values
        self.buttonAddFSN = QtGui.QPushButton('Add an FSN', self)
        self.buttonAddFSN.setCheckable(True)
        self.buttonModifyFSN = QtGui.QPushButton('Modify FSN', self)
        self.buttonModifyFSN.setCheckable(True)
        self.formModifierButtons = QtGui.QButtonGroup()
        self.formModifierButtons.addButton(self.buttonAddFSN)
        self.formModifierButtons.addButton(self.buttonModifyFSN)
        self.efficiencyProgress = QtGui.QProgressBar()
        self.efficiencyProgress.setRange(0,100)
        self.efficiencyProgress.setFormat("%v%")
        self.efficiencyProgress.setTextVisible(True)
        #Create all the widgets associated with the form.
        self.labelFSN = QtGui.QLabel("FSN:")
        self.lineEditFSN = QtGui.QLineEdit(self)
        self.labelType = QtGui.QLabel("Description Type:")
        self.comboBoxType = QtGui.QComboBox()
        self.comboBoxType.addItems(MOSES.getDescriptionTypes(self.userID,self.password))
        self.comboBoxType.setToolTip("Select the description type.")
        self.labelSource = QtGui.QLabel("Source:")
        self.comboBoxSource = QtGui.QComboBox()
        self.comboBoxSource.addItems(MOSES.getSources(self.userID,self.password))
        self.labelPriority = QtGui.QLabel("Priority:")
        #self.comboBoxPriority = QtGui.QComboBox()
        #self.priorityList = ["Normal","High"]
        #self.comboBoxPriority.addItems(self.priorityList)
        self.labelBU = QtGui.QLabel("Business Unit:")
        self.comboBoxBU = QtGui.QComboBox(self)
        self.labelSuperCategory = QtGui.QLabel("Super Category:")
        self.comboBoxSuperCategory = QtGui.QComboBox(self)
        self.labelCategory = QtGui.QLabel("Category:")
        self.comboBoxCategory = QtGui.QComboBox(self)
        self.labelSubCategory = QtGui.QLabel("Sub-Category:")
        self.comboBoxSubCategory = QtGui.QComboBox(self)
        self.labelBrand = QtGui.QLabel("Brand:")
        self.lineEditBrand = QtGui.QLineEdit(self)
        self.labelVertical = QtGui.QLabel("Vertical:")
        self.comboBoxVertical = QtGui.QComboBox(self)
        self.labelWordCount = QtGui.QLabel("Word Count:")
        self.lineEditWordCount = QtGui.QLineEdit(self)
        self.labelUploadLink = QtGui.QLabel("Upload Link:")
        self.lineEditUploadLink = QtGui.QLineEdit(self)
        self.labelRefLinks = QtGui.QLabel("Reference Links:")
        self.lineEditRefLink = QtGui.QLineEdit(self)
        self.labelGuidelines = QtGui.QLabel("Guidelines:")
        self.textEditGuidelines = QtGui.QTextEdit(self)
        self.textEditGuidelines.isReadOnly()
        self.labelClarifications = QtGui.QLabel("Clarifications:")
        self.lineEditClarification = QtGui.QLineEdit(self)
        self.comboBoxClarification = QtGui.QComboBox(self)
        self.buttonAddClarification = QtGui.QPushButton("+")
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                            QtGui.QDialogButtonBox.Cancel)
        self.buttonCopyFields = QtGui.QPushButton("Copy Common Fields from Selected Row")

    def widgetLayout(self):
        """PORK Window."""
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.addWidget(self.workCalendar,2)
        #self.horizontalLayout.addWidget(self.queue,1)
        #End main widgets.
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
        self.formLayout.addWidget(self.lineEditWordCount,10,1)
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
        ###Set the form's layout adjacent to the QTableWidget.
        self.piggyLayout = QtGui.QVBoxLayout()
        self.piggyLayout.addLayout(self.horizontalLayout,2)
        self.piggyLayout.addWidget(self.tabs,3)
        #create the penultimate layout.
        self.penultimateLayout = QtGui.QHBoxLayout()
        self.penultimateLayout.addLayout(self.piggyLayout,4)
        self.penultimateLayout.addLayout(self.finalFormLayout,1)
        #create the final layout.
        self.finalLayout = QtGui.QVBoxLayout()
        self.finalLayout.addLayout(self.penultimateLayout,4)
        self.finalLayout.addWidget(self.efficiencyProgress,1)
        #Investigate later.
        self.mainWidget.setLayout(self.finalLayout)

    def mapToolTips(self):
        """PORK Window."""
        self.table.setToolTip("Piggy Bank for %s" % self.getActiveDateString())
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
        self.lineEditWordCount.setToolTip("Type the word count of the article here.")
        self.lineEditUploadLink.setToolTip("If you are not using an FSN or an ISBN, please paste the appropriate upload link here.")
        self.lineEditRefLink.setToolTip("Paste the reference link(s) here.\nMultiple links can be appended by using a comma or a semi-colon.\nAvoid spaces like the plague.")
        self.lineEditClarification.setToolTip("Use the drop down menu adjacent to this box to append clarifications.\nIf a clarification is unavailable, please append it to this list by using a comma.")

    def keyPressEvent(self, e):
        """PORK Window: Found this code online. Go through it and try to improve it."""
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            selected = self.table.selectedRanges()
            if e.key() == QtCore.Qt.Key_S:
                self.say = QtGui.QMessageBox.question(self,"All Animals are created equal.","But some animals are <b>more</b> equal than others.", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if e.key() == QtCore.Qt.Key_C: #copy
                s = '\t'+"\t".join([str(self.table.horizontalHeaderItem(i).text()) for i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1)])
                s = s + '\n'
                for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
                    s += str(r+1) + '\t' 
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(self.table.item(r,c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)

    def createTabOrder(self):
        """PORK Window."""
        self.setTabOrder(self.workCalendar, self.buttonAddFSN)
        #self.setTabOrder(self.table,self.buttonAddFSN)
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
        self.setTabOrder(self.lineEditBrand, self.lineEditWordCount)
        self.setTabOrder(self.lineEditWordCount, self.lineEditUploadLink)
        self.setTabOrder(self.lineEditUploadLink,self.lineEditRefLink)
        self.setTabOrder(self.lineEditRefLink, self.comboBoxClarification)
        self.setTabOrder(self.comboBoxClarification, self.buttonAddClarification)
        self.setTabOrder(self.buttonAddClarification, self.buttonBox)
        #self.setTabOrder(self.buttonBox,self.lineEditFSN)

    def addMenus(self):
        """PORK Window."""
        self.menu = self.menuBar()
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
        self.viewStyleSheet =self.toolsMenu.addAction(self.callStyleSheet)
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
        self.setWindowTitle("P.O.R.K. %s - A Part of the O.I.N.K. Report Management System" % __version__)
        self.move(250,40)
        self.resize(800, 700)
        self.show()
        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('Images\Pork_Icon.png'),self)
        self.trayIcon.show()
        
    def initForm(self):
        """PORK Window: Method to initialize the form."""
        self.lineEditRefLink.setText("NA")
        self.lineEditClarification.setText("NA")
        self.comboBoxClarification.setCurrentIndex(-1)
        self.comboBoxSuperCategory.setCurrentIndex(-1)
        self.comboBoxSubCategory.setCurrentIndex(-1)
        self.comboBoxCategory.setCurrentIndex(-1)
        self.comboBoxVertical.setCurrentIndex(-1)
        self.lineEditBrand.setText("")
        self.comboBoxType.setCurrentIndex(-1)
        self.comboBoxSource.setCurrentIndex(-1)
        #self.comboBoxPriority.setCurrentIndex(-1)
        self.buttonAddFSN.setChecked(True)

    def setEvents(self):
        """PORK Window."""
        self.workCalendar.clicked[QtCore.QDate].connect(self.changedDate)
        self.table.cellClicked.connect(self.cellSelected)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.buttonBox.accepted.connect(self.validateAndSendToPiggy)
        self.comboBoxBU.currentIndexChanged['QString'].connect(self.populateSuperCategory)
        self.comboBoxSuperCategory.currentIndexChanged['QString'].connect(self.populateCategory)
        self.comboBoxCategory.currentIndexChanged['QString'].connect(self.populateSubCategory)
        self.comboBoxSubCategory.currentIndexChanged['QString'].connect(self.populateBrandVertical)
        self.comboBoxVertical.currentIndexChanged['QString'].connect(self.getVerticalGuidelines)
        self.lineEditFSN.editingFinished.connect(self.generateUploadLink)
        self.buttonBox.rejected.connect(self.clearAll)
        self.buttonAddClarification.clicked.connect(self.addClarification)
        self.buttonCopyFields.clicked.connect(self.copyCommonFields)

    def notify(self,title,message):
        """PORK Window: Method to show a tray notification"""
        self.trayIcon.showMessage(title,message)

    def applyForLeave(self):
        """PORK Window: Method to call the leave planner dialog."""
        #print "Applying for a leave!" #debug
        leaveapp = leavePlanner(self.userID,self.password)
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
        calculator = efficiencyCalculator(self.userID,self.password)
        if calculator.exec_():
            print "Calculator has successfully executed.!"
    
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

    def openChat(self):
        """PORK Window."""
        self.featureUnavailable()

    def changedDate(self):
        """PORK Window."""
        self.populateTable()
        self.displayEfficiency()
        self.mapToolTips()

    def populateTable(self):
        """PORK Window."""
        #print "Trying to populate the Piggy Bank Table." #debug
        data = MOSES.getUserPiggyBankData(self.getActiveDate(),self.userID,self.password)
        #print "Received %d entries." % len(data) #debug
        #print data #debug
        self.table.setRowCount(0)
        row_index = 0
        for row in data: 
            #print "Printing:"
            #print row
            #print "Row %d" % row_index #debug
            if len(row) > 0:
                self.table.setColumnCount(len(row))             
                headerLabels=[]
                column_index = 0
                self.table.insertRow(row_index)
                #get the keys from the PiggyBank Key list.
                for key in MOSES.getPiggyBankKeysInOrder(): #each row is a dictionary.
                    #print "Column %d" % column_index #debug
                    headerLabels.append(key)
                    self.table.setItem(row_index,column_index,QtGui.QTableWidgetItem(str(row[key])))
                    column_index += 1
                row_index += 1
            self.table.setHorizontalHeaderLabels(headerLabels)
        #print data

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
    
    def displayEfficiency(self):
        """PORK Window."""
        #print "Trying to display efficiency"
        queryDate = self.getActiveDate()
        efficiency = MOSES.getEfficiencyFor(self.userID,self.password,queryDate)
        #print "Received %f efficiency." % efficiency
        #self.alertMessage("Efficiency","Efficiency is %0.2f%%" % (efficiency*100))
        self.efficiencyProgress.setFormat("%0.02f%%" %(efficiency*100))
        #print "Integer value of efficiency = %d" % efficiency
        efficiency = int(efficiency*100) #this works
        if efficiency > 100:
            self.efficiencyProgress.setRange(0,efficiency)
        else:
            self.efficiencyProgress.setRange(0,100)
        self.efficiencyProgress.setValue(efficiency)
        return None

    def submit(self):
        """PORK Window."""
        """Method to send the FSN data to SQL."""
        #print "Sending data to MOSES."
        data = self.getFSNDataDict()
        if data != []:
            MOSES.addToPiggyBank(data,self.userID,self.password)
            self.populateTable() 
            self.displayEfficiency()
        else:
            print "I got nothing!"
        
    def populateBU(self):
        """PORK Window."""
        self.comboBoxBU.clear()
        BUValues = MOSES.getBUValues(self.userID,self.password)
        #print len(BUValues)
        self.comboBoxBU.addItems(BUValues)
        self.comboBoxBU.setCurrentIndex(-1)

    def populateSuperCategory(self):
        """PORK Window."""
        self.comboBoxSuperCategory.clear()
        self.selectedBU = str(self.comboBoxBU.currentText())
        try:
            self.comboBoxSuperCategory.addItems(MOSES.getSuperCategoryValues(self.userID,self.password,BU=self.selectedBU))
        except:
            self.notify("Error","Error trying to populate the Super-Category combo box with values for " + self.selectedBU + " BU. Check if there are predefined values.")

    def populateCategory(self):
        """PORK Window."""
        self.comboBoxCategory.clear()   
        self.selectedSuperCategory = str(self.comboBoxSuperCategory.currentText())
        try: 
            self.comboBoxCategory.addItems(MOSES.getCategoryValues(self.userID,self.password,SupC=self.selectedSuperCategory))
        except:
            self.notify("Error.","Error trying to populate Category combo Box with values for " + self.selectedSuperCategory + " super category. Check if there are predefined values.")
        try:
            if self.selectedSuperCategory != "BGM":
                self.textEditGuidelines.clear()
                self.textEditGuidelines.append("There seem to be no preset guidelines for the %s articles. Ask your TL if there's something you need to remember while writing articles." % self.selectedSuperCategory)
            else:
                self.textEditGuidelines.clear()
                self.textEditGuidelines.append("There are guidelines for at least one Category in %s." % self.selectedSuperCategory)
        except:
            self.notify("Error","No super category has been selected.")

    def populateSubCategory(self):
        """PORK Window."""
        self.comboBoxSubCategory.clear()
        self.selectedCategory = str(self.comboBoxCategory.currentText())
        SubCatList = MOSES.getSubCategoryValues(self.userID,self.password,Cat=self.selectedCategory)
        try: 
            self.comboBoxSubCategory.addItems(SubCatList)
        except:
            self.notify("Error","Error trying to populate Sub-Category combo-box with values for " + self.selectedCategory + " category. Check if there are predefined values.")
        try:
            if self.selectedCategory != "Toy":
                self.textEditGuidelines.clear()
                self.textEditGuidelines.append("There seem to be no preset guidelines for the %s articles. Ask your TL if there's something you need to remember while writing articles." % self.selectedCategory)
            else:
                self.textEditGuidelines.clear()
                self.textEditGuidelines.append("There are guidelines for at least one sub-category in %s." % self.selectedCategory)
        except:
            self.notify("Error","No category has been selected.")
    
    def populateBrandVertical(self):
        """PORK Window."""
        self.comboBoxVertical.clear()
        self.selectedSubCategory = str(self.comboBoxSubCategory.currentText())
        Verts = MOSES.getVerticalValues(self.userID,self.password,self.selectedSubCategory)
        try: 
            self.comboBoxVertical.addItems(Verts)
        except:
            self.notify("Error","Error trying to populate vertical combo-box with values for " + self.selectedCategory + " category. Check if there are predefined values.")
        try:
            if self.selectedCategory == "RolePlayToy":
                self.textEditGuidelines.clear()
                self.textEditGuidelines.append("Role-play toys help a child with their creative skills, imagination, leadership skills, etc.")
            elif self.selectedCategory == "EducationalToy":
                self.textEditGuidelines.clear()
                self.textEditGuidelines.append("When writing about educational toys, be sure to specify how they can improve a child's motor skills, hand-eye coordination and memory. Parents will appreciate knowing they're buying instructive toys for their kids.")    
            else:
                self.textEditGuidelines.clear()
                self.textEditGuidelines.append("There are no guidelines available for %s verticals. Please ask your TL for advice." % self.selectedVertical)    
        except:
            self.notify("Error","No sub-category has been selected.")

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
            brotherEyeClose()
            super(PORKWindow, self).closeEvent(event)
        else:
            event.ignore()

    def generateUploadLink(self):
        """PORK Window."""
        if (len(str(self.lineEditUploadLink.text())) == 0) and (str(self.lineEditUploadLink.text()).count(' ') <= 0):
            fsnString = str(self.lineEditFSN.text()).strip()    
            if (len(fsnString) == 13) or (len(fsnString) == 16):
                self.lineEditUploadLink.setText("http://www.flipkart.com/search?q=" + fsnString)

    def validateForm(self):
        """PORK Window."""
        self.listData = self.fsnData()
        self.done = 0
        for value in listData:
            if len(value) == 0:
                self.done = self.done + 1
        if (self.done==0):
            return True
        else:
            return False

    def validateAndSendToPiggy(self):
        """PORK Window."""
        #FIX
        """This method checks if the given data is complete, and then if the data is for today, it allows addition or modification."""
        completion = False
        allowAddition = False
        mode = self.getMode()
        dates_user_is_allowed_to_manipulate = [datetime.date(datetime.today()), MOSES.getLastWorkingDate(self.userID, self.password)]
        if self.getActiveDate() not in dates_user_is_allowed_to_manipulate:
            allowAddition = False
            self.alertMessage('Not Allowed', "You cannot make changes to dates other than your last working date and today.")
        elif mode == "Addition":
            fsnData = self.getFSNDataDict()
            fsn = fsnData["FSN"]
            fsntype = fsnData["Description Type"]
            isDuplicate = MOSES.checkDuplicacy(fsn, fsntype, self.getActiveDate())
            if isDuplicate == "Local":
                self.alertMessage("Repeated FSN","You just reported that FSN today!")
            elif (isDuplicate == "Global") and not (MOSES.checkForOveride(fsn, self.getActiveDate(), self.userID, self.password)):
                self.alertMessage("Repeated FSN","That FSN was already reported before by a writer. If your TL has instructed you to overwrite the contents, please request an overide request.")
            elif (isDuplicate == "Global") and (MOSES.checkForOveride(fsn, self.getActiveDate(), self.userID, self.password)):
                fsnData["Rewrite Ticket"] = "First Instance"
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
            MOSES.updatePiggyBankEntry(fsnData, self.userID, self.password)
            self.alertMessage("Success","Successfully modified an entry in the Piggy Bank.")
            #print "Modified!"
            completion = True
        if completion:
            self.resetForm()
            self.populateTable()
            self.displayEfficiency()

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
        self.lineEditWordCount.setText("")      
        self.lineEditRefLink.setText("NA")          
        self.lineEditUploadLink.setText("")         
        self.lineEditClarification.setText("NA")
        self.buttonAddFSN.setChecked(True)
    
    def cellSelected(self, row, column):
        """PORK Window Method.
        Triggered when a cell is clicked. If the current mode is set to modification, it will copy the fields in the selected row to the form.
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
        columns = self.table.columnCount()
        
        for columnCounter in range(columns):

            self.columnHeaderLabel = str(self.table.horizontalHeaderItem(columnCounter).text()) 
            self.cellValue = str(self.table.item(row, columnCounter).text())
            
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
                    self.lineEditWordCount.setText(self.cellValue)

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
        self.lineEditWordCount.setText("")
        self.lineEditBrand.setText("")          
        self.lineEditRefLink.setText("")            
        self.lineEditUploadLink.setText("")         
        self.lineEditClarification.setText("")
        self.buttonAddFSN.setChecked(True)

    def getFSNDataDict(self):
        """PORK Window."""
        """Checks all the FSN details and returns a dictionary which can be added to the Piggy bank."""
        self.fsnDataList = []
        self.valid = True
        try:
            self.fsn = str(self.lineEditFSN.text()).replace(",",";").strip()
            if len(self.fsn) == 0:
                self.valid = False
                self.alertMessage("Error","Please enter the FSN.")
                return []
        except:
            self.alertMessage("Runtime Error","Please enter the FSN.")
            self.lineEditFSN.setFocus()
            self.valid = False
            return []
        try:
            self.type = str(self.comboBoxType.currentText()).replace(",",";").strip()
            if len(self.type) == 0:
                self.valid = False
                self.alertMessage("Runtime Error","Please select a type.")
                return []
        except:
            self.alertMessage("Error","Please select a type.")
            self.comboBoxType.setFocus()
            self.valid = False
            return []
        try:
            self.source = str(self.comboBoxSource.currentText()).replace(",",";").strip()
            if len(self.source) == 0:
                self.valid = False
                self.alertMessage("Error","Please select a source.")
                return []           
        except:
            self.alertMessage("Runtime Error","Please select a source.")
            self.comboBoxSource.setFocus()
            self.valid = False
            return []
        try:
            self.bu = str(self.comboBoxBU.currentText()).replace(",",";").strip()
            if len(self.bu) == 0:
                self.valid = False
                self.alertMessage("Error","Please select the BU.")
                return []
        except:
            self.alertMessage("Error","Please select the BU.")
            self.comboBoxBU.setFocus()
            return []
        try:
            self.supercategory = str(self.comboBoxSuperCategory.currentText()).replace(",",";").strip()
            if len(self.supercategory) == 0:
                self.valid = False
                self.alertMessage("Error","Please select the super-category.")
                return []
        except:
            self.alertMessage("Runtime Error","Please select the super-category.")
            self.comboBoxSuperCategory.setFocus()
            return []
        try:
            self.category = str(self.comboBoxCategory.currentText()).replace(",",";").strip()
            if len(self.category) == 0:
                self.valid = False
                self.alertMessage("Error","Please select the category.")
                return []           
        except:
            self.alertMessage("Runtime Error","Please select the category.")
            self.comboBoxCategory.setFocus()
            self.valid = False
            return []
        try:
            self.subcategory = str(self.comboBoxSubCategory.currentText()).replace(",",";").strip()
            if len(self.subcategory) == 0:
                self.valid = False
                self.alertMessage("Error","Please select the sub-category.")
                return []
        except:
            self.alertMessage("Runtime Error","Please select the sub-category.")
            self.comboBoxSubCategory.setFocus()
            self.valid = False
            return []
        try:
            self.vertical = str(self.comboBoxVertical.currentText()).replace(",",";").strip()
            if len(self.vertical) == 0:
                self.valid = False
                self.alertMessage("Error","Please select the vertical.")
                return []
        except:
            self.alertMessage("Runtime Error","Please select the vertical.")
            self.comboBoxVertical.setFocus()
            self.valid = False
            return []
        try:
            self.brand = str(self.lineEditBrand.text()).replace(",",";").strip()
            if len(self.brand) == 0:
                self.valid = False
                self.alertMessage("Error","Please enter the brand.")
                return []
        except:
            self.alertMessage("Runtime Error","Please enter the brand.")
            self.lineEditBrand.setFocus()
            self.valid = False
            return []
        try:
            self.wordcount = int(float(str(self.lineEditWordCount.text()).strip()))

        except:
            self.alertMessage("Runtime Error","Please enter the word count. Word count must be an integer.")
            self.lineEditWordCount.setFocus()
            self.valid = False
            return []
        try:
            self.uploadlink = str(self.lineEditUploadLink.text()).replace(",",";").strip()
            if len(self.uploadlink) == 0:
                self.valid = False
                self.alertMessage("Error","Please enter the upload link.")
                return []
        except:
            self.alertMessage("Runtime Error","Please enter the upload link.")
            self.lineEditUploadLink.setFocus()
            self.valid = False
            return []
        try:
            self.referencelink = str(self.lineEditRefLink.text()).replace(",",";").strip()
            if len(self.referencelink) == 0:
                self.valid = False
                self.alertMessage("Error","Please enter the reference link.")
                return []
        except:
            self.alertMessage("Runtime Error","Please enter the reference link.")
            self.lineEditRefLink.setFocus()
            self.valid = False
            return []
        try:
            self.clarification = str(self.lineEditClarification.text()).replace(",",";").strip()
            if len(self.clarification) == 0:
                self.valid = False
                self.alertMessage("Error","Clarification cell cannot be empty.")
                return []
        except:
            self.alertMessage("Runtime Error","Clarification cell cannot be empty.")
            self.lineEditClarification.setFocus()
            self.valid = False
            return []
        #Success!
        if self.valid:
            self.fsnDataList = {
                "Article Date": self.getActiveDate(),
                "WriterID": self.userID,
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
                #"Clarification": self.clarification,
                "Rewrite Ticket": "No"
            }
        return self.fsnDataList

####################################################################
####################Login Dialog Class Definition###################
####################################################################

class LogInDialog(QtGui.QDialog):

    def __init__(self):
        """Login Dialog"""
        super(QtGui.QDialog,self).__init__()
        self.generateWidgets()
        self.createVisuals()
        self.createLayouts()
        self.mapTooltips()
        self.createActions()

    def generateWidgets(self):
        """Login Dialog"""
        self.loginLabel = QtGui.QLabel("User ID:")
        self.loginLineEdit = QtGui.QLineEdit()
        self.loginLineEdit.setToolTip("Enter your user ID here. Your user ID is your employee ID.")
        self.passwordLabel = QtGui.QLabel("Password:")
        self.passwordLineEdit = QtGui.QLineEdit()
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setToolTip("Enter your password here.")
        self.hostLabel = QtGui.QLabel("Host ID:")
        self.hostLineEdit = QtGui.QLineEdit()
        hostID = MOSES.getHostID()
        self.hostLineEdit.setText(hostID)
        self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                            QtGui.QDialogButtonBox.Cancel)       

    def createLayouts(self):
        """Login Dialog"""
        self.IDLayout = QtGui.QHBoxLayout()
        self.IDLayout.addWidget(self.loginLabel,1)
        self.IDLayout.addWidget(self.loginLineEdit,2)
        self.passLayout = QtGui.QHBoxLayout()
        self.passLayout.addWidget(self.passwordLabel,1)
        self.passLayout.addWidget(self.passwordLineEdit,2)
        self.hostIDLayout = QtGui.QHBoxLayout()
        self.hostIDLayout.addWidget(self.hostLabel)
        self.hostIDLayout.addWidget(self.hostLineEdit)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.IDLayout)
        self.layout.addLayout(self.passLayout)
        self.layout.addLayout(self.hostIDLayout)
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def createVisuals(self):
        """Login Dialog"""
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.setWindowTitle("P.O.R.K. %s - A Part of the O.I.N.K. Report Management System" % __version__)
        self.move(500,200)
        self.resize(200,100)
        self.setWindowTitle("OINK Login")

    def getUserDetails(self):
        """Login Dialog"""
        userID = str(self.loginLineEdit.text()).strip()
        password = str(self.passwordLineEdit.text()).strip()
        return userID, password
        
    def createActions(self):
        """Login Dialog"""
        self.buttons.accepted.connect(self.submit)
        self.buttons.rejected.connect(self.reject)

    def mapTooltips(self):
        """Login Dialog"""
        self.loginLineEdit.setToolTip("Enter your login ID here.\nIt is your Flipkart employee ID.\nIt is not your e-mail or LDAP ID.")
        self.passwordLineEdit.setToolTip("Enter your password here. If it's your first time logging in, the password is 'password'.\nIn case you have forgotten your password, ask your TL to reset your password.")
        self.hostLineEdit.setToolTip("Do not change this field unless otherwise instructed by your TL or by the Admin.")

    def reject(self):
        """Login Dialog"""
        super(LogInDialog,self).reject()

    def validateUserID(self):
        """Login Dialog"""
        userID, password = self.getUserDetails()
        return MOSES.checkPassword(userID,password)[0]
    
    def submit(self):
        """Login Dialog.
        This method first detects if the host ID has been altered.
        Then, it validates the host ID and moves on to validate the login credentials.
    """
        hostID = str(self.hostLineEdit.text())
        if MOSES.detectChangeInHost(hostID):
            MOSES.changeHostID(hostID)
        if MOSES.checkHostID(hostID):
            if self.validateUserID():
                super(LogInDialog,self).accept()
            else:
                self.warningMessage = QtGui.QWidget()
                self.warningMessage.say = QtGui.QMessageBox.question(\
                    self.warningMessage,"Login failure",\
                    "Stand back, Flame of Udun! Thou shalt not pass!",QtGui.QMessageBox.Ok,QtGui.QMessageBox.Ok)
        else:
            self.warningmessage = QtGui.QWidget()
            self.warningmessage.say = QtGui.QMessageBox.question(self.warningmessage, "Error with host ID!", "The host seems to be unreachable. Please contact Admin.", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

####################################################################
###############Password Reset Dialog Class Definition###############
####################################################################
class passResetDialog(QtGui.QDialog):
    def __init__(self, userID, password):
        """Password Reset Dialog."""
        super(passResetDialog,self).__init__()
        self.userID = userID
        self.password = password
        self.generateWidgets()
        self.createLayouts()
        self.setVisuals()
        self.createEvents()
    
    def generateWidgets(self):
        """Password Reset Dialog."""
        """Method to create the password reset box widgets."""
        self.userIDLabel = QtGui.QLabel("User ID & Name:")
        self.userIDPrintLabel = QtGui.QLabel("%s - %s" %(self.userID,MOSES.getEmpName(self.userID)))
        self.passwordLabel1 = QtGui.QLabel("Enter new password:")
        self.passwordLineEdit1 = QtGui.QLineEdit()
        self.passwordLineEdit1.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLabel2 = QtGui.QLabel("Repeat the password:")
        self.passwordLineEdit2 = QtGui.QLineEdit()
        self.passwordLineEdit2.setEchoMode(QtGui.QLineEdit.Password)
        self.statusLabel = QtGui.QLabel("")
        self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                            QtGui.QDialogButtonBox.Cancel)

    def createLayouts(self):
        """Password Reset Dialog."""
        """Method to set the layout of the password reset box."""
        self.userIDLayout = QtGui.QHBoxLayout()
        self.userIDLayout.addWidget(self.userIDLabel,0)
        self.userIDLayout.addWidget(self.userIDPrintLabel,2)
        self.passwordLayout1 = QtGui.QHBoxLayout()
        self.passwordLayout1.addWidget(self.passwordLabel1,0)
        self.passwordLayout1.addWidget(self.passwordLineEdit1,2)
        self.passwordLayout2 = QtGui.QHBoxLayout()
        self.passwordLayout2.addWidget(self.passwordLabel2,0)
        self.passwordLayout2.addWidget(self.passwordLineEdit2,2)
        self.finalLayout = QtGui.QVBoxLayout()
        self.finalLayout.addLayout(self.userIDLayout)
        self.finalLayout.addLayout(self.passwordLayout1)
        self.finalLayout.addLayout(self.passwordLayout2)
        self.finalLayout.addWidget(self.statusLabel)
        self.finalLayout.addWidget(self.buttons)
        self.setLayout(self.finalLayout)
    
    def setVisuals(self):
        """Password Reset Dialog."""
        """Method to set the visual aspects of the password reset box."""
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.move(500,200)
        self.resize(400,100)
        self.setWindowTitle("OINK Password Reset")
    
    def createEvents(self):
        """Password Reset Dialog."""
        """Method to set the events of the password reset box."""
        self.passwordLineEdit1.textChanged.connect(self.passwordsMatch)
        self.passwordLineEdit2.textChanged.connect(self.passwordsMatch)
        self.buttons.accepted.connect(self.submit)
        self.buttons.rejected.connect(self.reject)
    
    def submit(self):
        """Password Reset Dialog."""
        """Sumbmits the form."""
        if self.resetPassword():
            super(passResetDialog,self).accept()
    
    def reject(self):
        """Password Reset Dialog."""
        super(passResetDialog,self).reject()

    def getNewPassword(self):
        """Password Reset Dialog."""
        #print "Trying to return new password %s" %self.newPassword
        return self.newPassword
    
    def passwordsMatch(self):
        """Password Reset Dialog."""
        password1 = str(self.passwordLineEdit1.text())
        password2 = str(self.passwordLineEdit2.text())
        if password1 != password2:
            self.statusLabel.setText("<font color=Red>Passwords do not match!</font>")
            return False
        else:
            self.statusLabel.setText("<font color=Green>Passwords match!</font>")
            self.newPassword = password1
            return True
    
    def resetPassword(self):
        """Password Reset Dialog."""
        if self.passwordsMatch():
            self.newPassword = str(self.passwordLineEdit1.text())
            MOSES.resetOwnPassword(self.userID, self.password, self.newPassword)
            return True
        else:
            self.warningMessage = QtGui.QWidget()
            self.warningMessage.say = QtGui.QMessageBox.question(\
                self.warningMessage,"Password reset failure",\
                "Passwords do not match!",QtGui.QMessageBox.Ok,QtGui.QMessageBox.Ok)
            return False #print error message.

###########################################################
#############VINDALOO WINDOW CLASS DEFINITION##############
###########################################################

class VINDALOOWindow(QtGui.QMainWindow):
    def __init__(self, user_id, password):
        """Vindaloo initializer"""
        super(QtGui.QMainWindow,self).__init__()
        self.user_ID = user_id
        self.password = password
        self.generateUI()
        self.create_layout()
        self.createEvents()
        self.setVisuals()
        self.createActions()
        self.addMenus()
        #self.displayPiggyBank()
        #self.displayPiggyBankSummary()
        self.clip = QtGui.QApplication.clipboard()
    
    def generateUI(self):
        """Vindaloo UI Initializer"""
        self.mainWidget = QtGui.QWidget()
        self.setCentralWidget(self.mainWidget)
        self.dates_picker = date_selector_widget()
        self.team_report = QtGui.QTableWidget(0, 0)
        self.pullDataButton = QtGui.QPushButton("Pull Data")
        self.filtersButton = QtGui.QPushButton("Select Advanced Filters")
        self.exportButton = QtGui.QPushButton("Export Data and Reports")
        self.statusLog = QtGui.QTextEdit()
        self.piggyBank = QtGui.QTableWidget()
        self.team_report_graphs = QtGui.QWidget()
        self.rawdata = QtGui.QWidget()

    def create_layout(self):
        """Vindaloo."""
        self.tools_layout = QtGui.QVBoxLayout()
        self.tools_layout.addWidget(self.dates_picker,1)
        self.tools_layout.addWidget(self.pullDataButton,1)
        self.tools_layout.addWidget(self.filtersButton,1)
        self.tools_layout.addWidget(self.exportButton,1)
        self.tools_layout.addStretch(3)

        self.stats_tabs = QtGui.QTabWidget()
        self.stats_tabs.addTab(self.team_report, "Team Report")
        self.stats_tabs.addTab(self.team_report_graphs, "Graphs")
        self.stats_tabs.addTab(self.piggyBank, "Piggy Bank")
        self.stats_tabs.addTab(self.rawdata, "Quality Raw Data")
        self.stats_tabs.addTab(self.statusLog, "Log")

        self.finalLayout = QtGui.QHBoxLayout()
        self.finalLayout.addLayout(self.tools_layout,1)
        self.finalLayout.addWidget(self.stats_tabs,4)
        
        self.mainWidget.setLayout(self.finalLayout)
    
    def createEvents(self):
        """Vindaloo."""
        self.pullDataButton.clicked.connect(self.compileData)
        self.filtersButton.clicked.connect(self.applyFilters)
        self.exportButton.clicked.connect(self.exportData)

    def addMenus(self):
        """Vindaloo menus."""
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("&File")
        self.exportMenu = self.fileMenu.addMenu("E&xport")
        self.toolsMenu = self.menu.addMenu("&Tools")
        self.reportMenu = self.toolsMenu.addMenu("Reports")
        self.qualityMenu = self.reportMenu.addMenu("Quality Reports")
        self.teamQualityReportOption = self.qualityMenu.addAction(self.teamQualityReport)
        self.categoryQualityReportOption = self.qualityMenu.addAction(self.categoryQualityReport)
        self.productivityMenu = self.reportMenu.addMenu(\
            "Productivity Reports")
        self.wordCountTrendsOption = self.productivityMenu.addAction(\
            self.wordCountTrends)
        self.effiencyTrendsOption = self.productivityMenu.addAction(\
            self.efficiencyTrends)
        self.WBRReportOption = self.reportMenu.addAction(self.WBRReport)
        self.dailyReportOption = self.reportMenu.addAction(self.dailyReport)
        self.weeklyReportOption = self.reportMenu.addAction(self.weeklyReport)

        self.catTreeMenu = self.toolsMenu.addMenu("Category &Tree and Targets")
        self.targetRevOption = self.catTreeMenu.addAction(self.targetRev)
        self.changeCatTreeOption = self.catTreeMenu.addAction(self.changeCatTree)
        self.openEffCalcOption = self.catTreeMenu.addAction(self.openEffCalc)

        self.commMenu = self.menu.addMenu("Co&mmunication")
        self.leaveMenu = self.commMenu.addMenu("Leave Management")
        self.leaveApprovalOption = self.leaveMenu.addAction(self.leaveApproval)
        self.leaveTrackerOption = self.leaveMenu.addAction(self.leaveTracker)
        self.workforceLossOption = self.leaveMenu.addAction(self.workforceLoss)
        
        self.KRAMenu = self.toolsMenu.addMenu("&KRA Tools")
        self.askEditor = self.commMenu.addAction(self.callAskAnEditor)
        self.reviseAudit = self.commMenu.addAction(\
            self.raiseAuditRevisionTicket)
        self.chatmessenger = self.commMenu.addAction(self.callOpenChat) 
        self.helpMenu = self.menu.addMenu("&Help")

    def createActions(self):
        """Vindaloo."""
        self.dailyReport = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Daily Report",self)
        self.weeklyReport = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Weekly Report",self)
        self.teamQualityReport = QtGui.QAction(\
            QtGui.QIcon("Images\_Icon.png"),"Team Quality Report",self) 
        self.categoryQualityReport = QtGui.QAction(\
            QtGui.QIcon("Images\_Icon.png"),"Category Quality Report",self) 
        self.WBRReport = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Generate WBR Report",self)
        self.wordCountTrends = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "View Trends in Word Count",self)
        self.efficiencyTrends = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "View Trends in Efficiency Spikes",self)
        self.leaveApproval = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Leave Approval",self)
        self.leaveTracker = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Leave Tracker",self)
        self.workforceLoss = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Calculate Work Force Loss Due to Leaves",self)
        self.targetRev = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Revise Targets",self)
        self.raiseAuditRevisionTicket = QtGui.QAction(\
                        QtGui.QIcon("Images\_Icon.png"),\
                        "Raise a Revision Ticket for an Audit",self)
        self.callAskAnEditor = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Ask an Editor",self)
        self.openEffCalc = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Efficiency Calculator",self)
        self.callOpenChat = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Open Chat",self)
        self.changeCatTree = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Change Category Tree",self)

    def compileData(self):
        """Vindaloo: Pulls all data for a start and end date"""
        
    def applyFilters(self):
        """Applying filters."""

    def exportData(self):
        """Opens a dialog, asking for an output folder.
        If cancelled, it selects the default output folder 
        within the current working director.
        Then, it takes the data presented in the statistics 
        and builds a complete report."""

    def getDumpHeaders(self):
        """Vindaloo."""
        #Read the list of writers' names and Email IDs.
        self.writerInfoFile = open("Lists\writerList.csv", "rt")
        self.writerInfo = csv.reader(self.writerInfoFile)
        #Read the list of labels in PORK files.
        self.labelsInPork= open("Lists\columnLabels.csv","rt").read().split("\n")
        #create a list containing the labels in the Piggy Bank Dump.
        self.labelsInPiggyBankDump = ["Name","Email ID"]
        for label in self.labelsInPork:
                self.labelsInPiggyBankDump.append(label)
        return self.labelsInPiggyBankDump

    def getActiveDateForSQL(self):
        """Vindaloo."""
        date = self.dateCalendar.selectedDate()
        return str(date.toString('yyyy-MM-dd'))

    def getActiveDateString(self):
        """Vindaloo."""
        date = self.dateCalendar.selectedDate()
        return str(date.toString('dddd, dd MMMM yyyy'))
    
    def getActiveDate(self):
        """Vindaloo."""
        dateAsQDate = self.dateCalendar.selectedDate()
        dateString = str(dateAsQDate.toString('dd/MM/yyyy'))    
        dateAsDateTime = OINK3.getDate(dateString)
        return dateAsDateTime

    def updateTables(self):
        """Vindaloo."""
        self.displayPiggyBank()
        self.displayPiggyBankSummary()

    def displayPiggyBank(self):
        """Vindaloo: Populates the Piggy Bank display table with values for a date."""
        #print "Running displayPiggyBank."
        #get the data.
        data = MOSES.getPiggyBankDataForDate(self.getActiveDate(), self.user_ID , self.password)
        row_index = 0
        #print "There are %d entries for that date." % len(data[0])
        self.piggyBank.setRowCount(0)
        for row in data[0]: #Data is a tuple of length 2. Without the index, it'd contain an additional and annoying empty tuple.
            #print "Printing:"
            #print row
            #print "Row %d" % row_index
            if len(row) > 0:
                self.piggyBank.setColumnCount(len(row))             
                headerLabels=[]
                column_index = 0
                self.piggyBank.insertRow(row_index)
                for key in row: #each row is a dictionary.
                    #print "Column %d" % column_index
                    headerLabels.append(key)
                    self.piggyBank.setItem(row_index, column_index, QtGui.QTableWidgetItem(str(row[key])))
                    column_index += 1
                row_index += 1
            self.piggyBank.setHorizontalHeaderLabels(headerLabels)
        #print data

    def displayPiggyBankSummary(self):
        """Vindaloo: Methods to display the efficiency and quality."""

        print "Running displayPiggyBankSummary."


    def keyPressEvent(self, e):
        """Vindaloo: Found this code online. Go through it and try to improve it."""
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            selected = self.piggyBank.selectedRanges()

            if e.key() == QtCore.Qt.Key_C: #copy
                s = '\t'+"\t".join([str(self.piggyBank.horizontalHeaderItem(i).text()) for i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1)])
                s = s + '\n'

                for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
                    s += str(r+1) + '\t' 
                    #Puts 1,2,3, in the row number column instead of the vertical header text, since there is none.
                    #s += self.piggyBank.verticalHeaderItem(r).text() + '\t'
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(self.piggyBank.item(r,c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)

    def log(self, message):
        """Vindaloo."""
        with open("CSVs\Log.txt", "a") as logFile: logFile.write("\n@%s: %s" %(datetime.datetime.now(),message))
        self.statusLog.append(message)

    def notify(self,title,message):
        """Vindaloo."""
        self.trayIcon.showMessage(title,message)

    def displayStatus(self,message):
        """Vindaloo."""
        self.statusBar().showMessage(message)

    def setVisuals(self):
        """Vindaloo."""
        self.setWindowTitle("V.I.N.D.A.L.O.O. - A Part of the O.I.N.K. Report Management System")
        self.resize(800, 600)
        self.move(250,80)
        self.show()
        self.setWindowIcon(QtGui.QIcon('Images\VINDALOO_Icon.png'))     
        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('Images\VINDALOO_Icon.png'),self)
        self.trayIcon.show()
        self.notify("Welcome to Vindaloo", "All animals are created equal.")
        self.statusBar().showMessage("Hello")

#################################################################
###############BACON MAIN WINDOW CLASS DEFINITION################
#################################################################

class BACONWindow(QtGui.QMainWindow):
    def __init__(self, userID, password):
        """BACON"""
        super(BACONMainWindow,self).__init__()
        self.userID = userID
        self.password = password
        self.createWidgets()
        self.createLayouts()
        self.createEvents()
        self.createActions()
        self.refreshGraphs()
        self.setVisuals()
    def createWidgets(self):
        """BACON"""

    def createLayouts(self):
        """BACON"""

    def createEvents(self):
        """BACON"""

    def createActions(self):
        """BACON"""

    def fetchAuditQueue(self):
        """BACON"""

    def refreshGraphs(self):
        """BACON"""

    def plotCoverageChart(self):
        """BACON"""

    def plotPolarScatter(self):
        """BACON"""

    def fetchRawData(self):
        """BACON"""

    def openAuditForm(self):
        """BACON"""


########################################################################
#################BACON Audit Form Class Definition######################
########################################################################

class BACONAuditForm(QtGui.QDialog):
    def __init__(self, userID, password):
        """BACON Form"""
        super(BACONAuditForm, self).__init__()
        self.userID = userID
        self.password = password
        self.createWidgets()
        self.createLayouts()
        self.createEvents()
        self.createActions()
        self.setVisuals()

    def createWidgets(self):
        """BACON Form"""

    def createLayouts(self):
        """BACON Form"""

    def createEvents(self):
        """BACON Form"""

    def createActions(self):
        """BACON Form"""

    def fetchNextArticle(self):
        """BACON Form"""

    def fetchPreviousArticle(self):
        """BACON Form"""

    def publishAudits(self):
        """BACON Form"""

    def saveToLocal(self):
        """BACON Form"""

    def populateAuditFields(self):
        """BACON Form"""

    def addComment(self):
        """BACON Form"""

    def raiseRCA(self):
        """BACON Form"""

##############################################################
#####################Date Selector Widget#####################
##############################################################

class date_selector_widget(QtGui.QWidget):
    def __init__(self):
        super(date_selector_widget, self).__init__()
        self.mode = "Normal"
        self.create_widgets()
        self.create_layout(self.mode)
        self.create_events()
        self.set_tooltips()
        self.set_date_limits()
        self.start_date_picker.setDate(QtCore.QDate(datetime.date(datetime.today())))
        self.limitEndDate()
        self.get_dates()

    def create_widgets(self):
        """date_selector_widget"""
        self.start_date_label = QtGui.QLabel("<b>Select a start date:</b>")
        self.start_date_picker = QtGui.QDateTimeEdit()
        self.start_date_picker.setCalendarPopup(True)
        self.end_date_label = QtGui.QLabel("<b>Select an end date:</b>")
        self.end_date_picker = QtGui.QDateTimeEdit()
        self.end_date_picker.setCalendarPopup(True)
        #Disable the hidden end date feature for now.
        #self.reveal_end_date_button = QtGui.QPushButton("V")

    def create_layout(self, mode = "Normal"):
        self.date_selector_layout = QtGui.QVBoxLayout()
        self.start_date_layout = QtGui.QHBoxLayout()
        self.start_date_layout.addWidget(self.start_date_label,2)
        self.start_date_layout.addWidget(self.start_date_picker,3)
        #self.start_date_layout.addWidget(self.reveal_end_date_button,1)
        self.end_date_layout = QtGui.QHBoxLayout()
        self.end_date_layout.addWidget(self.end_date_label, 1)
        self.end_date_layout.addWidget(self.end_date_picker, 2)
        #self.mode = mode
        self.date_selector_layout.addLayout(self.start_date_layout)
        self.date_selector_layout.addLayout(self.end_date_layout)
        #self.end_date_label.hide()
        #self.end_date_picker.hide()
        self.setLayout(self.date_selector_layout)

    def create_events(self):
        """date_selector_widget"""
        #self.reveal_end_date_button.clicked.connect(self.expand_dates)
        self.start_date_picker.dateChanged.connect(self.limitEndDate)

    def set_tooltips(self):
        """date_selector_widget"""
        self.start_date_picker.setToolTip("Select a starting date.")
        self.end_date_picker.setToolTip("Select an ending date.")
        #self.reveal_end_date_button.setToolTip("Click to set an ending date.")

    def get_dates(self):
        """date_selector_widget"""
        start_date = self.start_date_picker.date().toPyDate()
        end_date = self.end_date_picker.date().toPyDate()


    def set_date_limits(self):
        """Sets limits to the date time edits and also sets the format."""
        self.start_date_picker.setDisplayFormat("MMMM dd, yyyy")
        self.start_date_picker.setMinimumDate(QtCore.QDate(2015,1,1))
        self.end_date_picker.setDisplayFormat("MMMM dd, yyyy")

    def expand_dates(self):
        """Reveals the end date options and hides the expansion button."""
        self.reveal_end_date_button.hide()
        self.end_date_label.show()
        self.end_date_picker.show()
    
    def limitEndDate(self):
        """Leave Planner: Method to limit the end date's minimum value to the start date."""
        self.end_date_picker.setMinimumDate(self.start_date_picker.date())

##############################################################
####################Duplicate FSN Overrider###################
##############################################################
class override_dialog(QtGui.QDialog):
    """Opens an override dialog."""
    def __init__(self):
        """"""
        self.create_widgets()
        self.create_layouts()
        self.create_events()

    def create_widgets(self):
        """"""
    def create_layouts(self):
        """"""
    def create_events(self):
        """"""
        self.submit_button.clicked.connect(self.create_override)
    def get_FSNs(self):
        """"""
    def create_override(self):
        """"""
        if len(get_FSNs()) > 0:
            for FSN in get_FSNs():
                MOSES.addOverride(FSN, self.date_time_planner.date().toPyDate(), self.userID, self.password)
        else:
            print "OK!" #I STOPPED CODING HERE!
        return True
    
##############################################################
#######Various methods required to run the application.#######
##############################################################

def showSplashScreen(app):
        # Create and display the splash screen
        splash_pix = QtGui.QPixmap('Images\PORK.png')
        splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        app.processEvents()
        time.sleep(2)

def brotherEyeOpen():
        if os.path.isfile("CSVs\BrotherEye.omacs"):
            brotherEye = file("CSVs\BrotherEye.omacs", "w")
            brotherEye.truncate()
            brotherEye.write("PORK Version: %s\nFile Open\nTime:%s"%(__version__,datetime.now()))
        else:
            brotherEye = file("CSVs\BrotherEye.omacs","w")
            brotherEye.write("PORK Version: %s\nFile Open\nTime:%s"%(__version__,datetime.now()))
        brotherEye.close()

def brotherEyeClose():
        if os.path.isfile("CSVs\BrotherEye.omacs"):
            brotherEye = file("CSVs\BrotherEye.omacs", "w")
            brotherEye.truncate()
            brotherEye.write("PORK Version: [version]%s[/version]\nFile Closed\nTime:[ctime]%s[/ctime]"%(__version__,datetime.now()))
        else:
            brotherEyeFile = file("CSVs\BrotherEye.omacs","w")
            brotherEye.write("PORK Version: %s\nFile Closed\nTime:%s"%(__version__,datetime.now()))

def brotherEyeFileModified(fsnData,date):
        if os.path.isfile("CSVs\BrotherEye.1984"):
            brotherEyeModificationTracker = file("CSVs\BrotherEye.1984","a")
            brotherEyeModificationTracker.write("\n[number]%d[/number] FSNs completed for [date]%s[/date] at [time]%s[/time]." % (fsnData,date,datetime.now()))
        else:
            brotherEyeModificationTracker = file("CSVs\BrotherEye.1984","a")
            brotherEyeModificationTracker.write("\n[number]%d[/number] FSNs completed for [date]%s[/date] at [time]%s[/time]." % (fsnData,date,datetime.now()))
        brotherEyeModificationTracker.close()

def detectFileOpen():
    if os.path.isfile("CSVs\BrotherEye.omacs"):
        brotherEyeFileContents = file("CSVs\BrotherEye.omacs","rb").read()
        #print brotherEyeFileContents.find("Open")
        if brotherEyeFileContents.find("Open") == -1:
            return False
        else:
            return True
    else:
        return False

def login():
    """Opens a login dialog and returns the username and password."""
    userID = 0
    password = 0
    success = False
    loginPrompt = LogInDialog()
    if loginPrompt.exec_():
        #print "woot!"
        userID, password2 = loginPrompt.getUserDetails()
        #print "%s, %s" %(userID,password2)
        return userID, password2

def passwordResetter(userID,password):
    """Dialog resets the password."""
    passwordReset = passResetDialog(userID,password)
    if passwordReset.exec_():
        newPassword = passwordReset.getNewPassword()
        return newPassword