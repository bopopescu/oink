#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
from datetime import datetime
import pandas
from PyQt4 import QtGui, QtCore

import MOSES

class calculatorRow:
    """Class definition for a single row of the efficiency calculator."""
    def __init__(self, userID, password, category_tree):
        """Calculator Row"""
        self.userID = userID
        self.password = password
        self.category_tree = category_tree
        self.efficiency = 0.0
        self.createWidgets()
        self.populateTypeSource()
        self.mapToolTips()
        self.populateBU()
        self.createEvents()

    def createWidgets(self):
        """Calculator Row: Method to create widgets for a single calculator Row."""
        #startTime = datetime.now()        
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
        self.calcWidgets.update({"Target": QtGui.QLabel("-")})

        self.calcWidgets["Description Type"].setFixedWidth(180)
        self.calcWidgets["Source"].setFixedWidth(105)
        self.calcWidgets["BU"].setFixedWidth(150)
        self.calcWidgets["Super-Category"].setFixedWidth(150)
        self.calcWidgets["Category"].setFixedWidth(150)
        self.calcWidgets["Sub-Category"].setFixedWidth(150)
        self.calcWidgets["Vertical"].setFixedWidth(150)
        self.calcWidgets["Quantity"].setFixedWidth(60)
        self.calcWidgets["Efficiency"].setFixedWidth(60)
        self.calcWidgets["Target"].setFixedWidth(60)

        #functionName = sys._getframe().f_code.co_name
        #endTime = datetime.now()
        #timeSpent = endTime - startTime
        #print "Spent %s in %s." % (timeSpent, functionName)

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

    def createEvents(self):
        """Calculator Row"""
        self.calcWidgets["BU"].currentIndexChanged.connect(self.populateSupC)
        self.calcWidgets["Super-Category"].currentIndexChanged.connect(self.populateC)
        self.calcWidgets["Category"].currentIndexChanged.connect(self.populateSubC)
        self.calcWidgets["Sub-Category"].currentIndexChanged.connect(self.populateVert)
        
        self.calcWidgets["Vertical"].currentIndexChanged.connect(self.updateEfficiency)
        self.calcWidgets["Quantity"].valueChanged.connect(self.updateEfficiency)
        self.calcWidgets["Description Type"].currentIndexChanged.connect(self.updateEfficiency)
        self.calcWidgets["Source"].currentIndexChanged.connect(self.updateEfficiency)


    def updateEfficiency(self):
        """Calculator Row"""
        #startTime = datetime.now()
        efficiency = self.getEfficiency()
        if efficiency is None:
            efficiency_text = "No Target"
        else:
            efficiency_text = "%.2f%%" % (efficiency)
        self.calcWidgets["Efficiency"].setText(efficiency_text)
        functionName = sys._getframe().f_code.co_name
        #endTime = datetime.now()
        #timeSpent = endTime - startTime
        #print "Spent %s in %s." % (timeSpent, functionName)
   
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
        bus = list(set(self.category_tree["BU"]))
        bus.sort()
        self.calcWidgets["BU"].clear()
        self.calcWidgets["BU"].addItems(bus)
        self.calcWidgets["BU"].setCurrentIndex(-1)


    def populateSupC(self):
        """Calculator Row"""
        bu = str(self.calcWidgets["BU"].currentText())
        filtered_category_tree = self.category_tree.loc[self.category_tree["BU"] == bu]
        super_categories = list(set(filtered_category_tree["Super-Category"]))
        super_categories.sort()
        self.calcWidgets["Super-Category"].clear()
        self.calcWidgets["Super-Category"].addItems(super_categories)
        self.calcWidgets["Super-Category"].setCurrentIndex(-1)

    def populateC(self):
        """Calculator Row"""
        super_category = str(self.calcWidgets["Super-Category"].currentText())
        self.calcWidgets["Category"].clear()
        filtered_category_tree = self.category_tree.loc[self.category_tree["Super-Category"] == super_category]
        categories = list(set(filtered_category_tree["Category"]))
        categories.sort()
        self.calcWidgets["Category"].addItems(categories)
        self.calcWidgets["Category"].setCurrentIndex(-1)

    def populateSubC(self):
        """Calculator Row"""
        category = str(self.calcWidgets["Category"].currentText())
        self.calcWidgets["Sub-Category"].clear()
        filtered_category_tree = self.category_tree.loc[self.category_tree["Category"] == category]
        sub_categories = list(set(filtered_category_tree["Sub-Category"]))
        sub_categories.sort()

        self.calcWidgets["Sub-Category"].addItems(sub_categories)
        self.calcWidgets["Sub-Category"].setCurrentIndex(-1)

    def populateVert(self):
        """Calculator Row"""
        sub_category = self.calcWidgets["Sub-Category"].currentText()
        filtered_category_tree = self.category_tree.loc[self.category_tree["Sub-Category"] == sub_category]
        verticals = list(set(filtered_category_tree["Vertical"]))
        verticals.sort()
        self.calcWidgets["Vertical"].clear()
        self.calcWidgets["Vertical"].addItems(verticals)
        self.calcWidgets["Vertical"].setCurrentIndex(-1)

    def getEfficiency(self):
        """Calculator Row"""
        row = {
            "Description Type": str(self.calcWidgets["Description Type"].currentText()),
            "Source": str(self.calcWidgets["Source"].currentText()),
            "BU": str(self.calcWidgets["BU"].currentText()),
            "Super-Category": str(self.calcWidgets["Super-Category"].currentText()),
            "Category": str(self.calcWidgets["Category"].currentText()),
            "Sub-Category": str(self.calcWidgets["Sub-Category"].currentText()),
            "Vertical": str(self.calcWidgets["Vertical"].currentText())
        }
        request_date = datetime.date(startTime)

        target = float(MOSES.getTargetFor(self.userID, self.password, row, request_date))

        self.calcWidgets["Target"].setText("%s"%target)

        quantity = float(self.calcWidgets["Quantity"].value())
        self.efficiency = (quantity*100.00/target) if target >0 else None
        return self.efficiency

class EfficiencyCalculator(QtGui.QDialog):
    """Class definition for the efficiency calculator."""
    def __init__(self, userID, password, category_tree=None):
        """Efficiency Calculator Initializer function."""
        self.userID = userID
        self.password = password
        if category_tree is None:
            self.category_tree = MOSES.getCategoryTree(self.userID, self.password)
        else:
            self.category_tree = category_tree 
        super(QtGui.QDialog, self).__init__()
        self.calcList = []
        self.createWidgets()
        self.createLayouts()
        self.createEvents()
        self.setVisuals()

    def createWidgets(self):
        """Efficiency Calculator: Creates widgets."""
        #startTime = datetime.now()
        #functionName = sys._getframe().f_code.co_name
        self.calc_table = QtGui.QTableWidget()
        self.headers = ["Description Type","Source","BU","Super-Category","Category","Sub-Category","Vertical","Quantity","Efficiency","Target"]
        self.calc_table.setColumnCount(len(self.headers))
        self.addCalcRow()

        
        self.plusButton = QtGui.QPushButton("Add Another Type of Article")
        #self.findIdenLabel = QtGui.QLabel("Find a vertical")
        self.refreshButton = QtGui.QPushButton("Recalculate Efficiency")
        self.totEffLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Total Efficiency:</b></font>")
        self.effScoreLabel = QtGui.QLabel("<font size=3 face=Georgia><b>00.00%</b></font>")
        #endTime = datetime.now()
        #timeSpent = endTime - startTime
        #print "Spent %s in %s." % (timeSpent, functionName)

    def createLayouts(self):
        """Efficiency Calculator."""
        #startTime = datetime.now()
        #functionName = sys._getframe().f_code.co_name
        
        self.effLayout = QtGui.QHBoxLayout()
        self.effLayout.addWidget(self.plusButton)
        self.effLayout.addWidget(self.refreshButton)
        self.effLayout.addStretch(2)
        self.effLayout.addWidget(self.totEffLabel)
        self.effLayout.addWidget(self.effScoreLabel)
        
        self.finalLayout = QtGui.QVBoxLayout()

        self.finalLayout.addWidget(self.calc_table,3)
        self.finalLayout.addStretch(1)
        self.finalLayout.addLayout(self.effLayout)

        self.setLayout(self.finalLayout)

        #endTime = datetime.now()
        #timeSpent = endTime - startTime
        #print "Spent %s in %s." % (timeSpent, functionName)

    def addCalcRow(self):
        """Efficiency Calculator."""
        #print "Entered the loop!"
        self.calcList.append(calculatorRow(self.userID, self.password, self.category_tree)) 
        #print "Printing Calc List", self.calcList
        row_count = int(self.calc_table.rowCount())
        self.calc_table.insertRow(row_count)
        row = row_count
        column = 0

        for widget_name in self.headers:
            self.calc_table.setCellWidget(row, column, self.calcList[-1].calcWidgets[widget_name])
            column+=1
        self.calc_table.setHorizontalHeaderLabels(self.headers)
        self.calc_table.resizeColumnsToContents()

    
    def createEvents(self):
        """Efficiency Calculator."""
        #startTime = datetime.now()
        self.plusButton.clicked.connect(self.plusAction)
        self.refreshButton.clicked.connect(self.displayEfficiency)
        self.connectQuantityWidgets()
        functionName = sys._getframe().f_code.co_name
        #endTime = datetime.now()
        #timeSpent = endTime - startTime
        #print "Spent %s in %s." % (timeSpent, functionName)

    def setVisuals(self):
        """Efficiency Calculator."""
        #startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name
        self.setWindowTitle("Efficiency Calculator: Driving What Drives You")
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.show()
        #endTime = datetime.now()
        #timeSpent = endTime - startTime
        #print "Spent %s in %s." % (timeSpent, functionName)

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
        #startTime = datetime.now()
        totalEfficiency = 0.0
        for calc_row in self.calcList:
            calc_row.updateEfficiency()
            efficiency = calc_row.efficiency if calc_row.efficiency is not None else 0
            totalEfficiency += efficiency
        self.effScoreLabel.setText("%.2f%%"%totalEfficiency)
        functionName = sys._getframe().f_code.co_name
        #endTime = datetime.now()
        #timeSpent = endTime - startTime
        #print "Spent %s in %s." % (timeSpent, functionName)

    def findIdentifier(self):
        """Efficiency Calculator."""
        startTime = datetime.now()
        functionName = sys._getframe().f_code.co_name
        endTime = datetime.now()
        timeSpent = endTime - startTime
        print "Spent %s in %s." % (timeSpent, functionName)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    u, p = MOSES.getBigbrotherCredentials()
    calc = EfficiencyCalculator(u,p)
    calc.show()
    sys.exit(app.exec_())