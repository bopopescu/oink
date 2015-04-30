#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
from datetime import datetime

from PyQt4 import QtGui, QtCore

import MOSES

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
        for description in self.calcWidgets:
            self.calcWidgets[description].setMinimumWidth(100)
            self.calcWidgets[description].setMaximumWidth(100)

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
        BUValues = MOSES.getBUValues(self.userID, self.password)
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

class EfficiencyCalculator(QtGui.QDialog):
    """Class definition for the efficiency calculator."""
    def __init__(self, userID, password):
        """Efficiency Calculator Initializer function."""
        self.userID = userID
        self.password = password
        super(QtGui.QDialog, self).__init__()
        self.calcList = []
        self.createWidgets()
        self.createLayouts()
        self.createEvents()
        self.setVisuals()

    def createWidgets(self):
        """Efficiency Calculator: Creates widgets."""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name

        self.typeLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Description Type</b></font>")
        self.typeLabel.setMinimumWidth(100)
        self.typeLabel.setMaximumWidth(100)

        self.SourceLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Source</b></font>")
        self.SourceLabel.setMinimumWidth(100)
        self.SourceLabel.setMaximumWidth(100)
        self.BULabel = QtGui.QLabel("<font size=3 face=Georgia><b>BU</b></font>")
        self.BULabel.setMinimumWidth(100)
        self.BULabel.setMaximumWidth(100)
         

        self.SupCLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Super-Category</b></font>")
        self.SupCLabel.setMinimumWidth(100)
        self.SupCLabel.setMaximumWidth(100)
        
        self.CatLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Category</b></font>")
        self.CatLabel.setMinimumWidth(100)
        self.CatLabel.setMaximumWidth(100)
        
        self.SubCLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Sub-Category</b></font>")
        self.SubCLabel.setMinimumWidth(100)
        self.SubCLabel.setMaximumWidth(100)
        
        self.VertLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Vertical</b></font>")
        self.VertLabel.setMinimumWidth(100)
        self.VertLabel.setMaximumWidth(100)
        self.QtyLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Quantity</b></font>")
        self.QtyLabel.setMinimumWidth(100)
        self.QtyLabel.setMaximumWidth(100)
        
        self.EffLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Efficiency</b></font>")
        self.EffLabel.setMinimumWidth(100)
        self.EffLabel.setMaximumWidth(100)
        
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
