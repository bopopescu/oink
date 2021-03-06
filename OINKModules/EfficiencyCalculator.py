#!/usr/bin/python2
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import datetime
import re
import pandas
import math
from PyQt4 import QtGui, QtCore

import MOSES
from CategoryFinder import CategoryFinder
class calculatorRow:
    """Class definition for a single row of the efficiency calculator."""
    
    def __init__(self, userID, password, category_tree, target_date):
        """Calculator Row"""
        self.userID = userID
        self.password = password
        self.category_tree = category_tree
        self.target_date = target_date
        self.efficiency = 0.0
        self.createWidgets()
        self.populateTypeSource()
        self.mapToolTips()
        self.populateBU()
        self.createEvents()

        self.calcWidgets["Source"].setCurrentIndex(self.calcWidgets["Source"].findText("Inhouse"))

    def createWidgets(self):
        """Calculator Row: Method to create widgets for a single calculator Row."""
        self.calcWidgets = {}
        self.calcWidgets.update({"Description Type": QtGui.QComboBox()})
        self.calcWidgets.update({"Source": QtGui.QComboBox()})
        self.calcWidgets.update({"BU": QtGui.QComboBox()})
        self.calcWidgets.update({"Super-Category": QtGui.QComboBox()})
        self.calcWidgets.update({"Category": QtGui.QComboBox()})
        self.calcWidgets.update({"Sub-Category": QtGui.QComboBox()})
        self.calcWidgets.update({"Vertical": QtGui.QComboBox()})
        self.calcWidgets.update({"Quantity": QtGui.QSpinBox()})
        self.calcWidgets.update({"Efficiency": QtGui.QDoubleSpinBox()})
        self.calcWidgets.update({"Target": QtGui.QLabel("-")})

        self.calcWidgets["Quantity"].setRange(0,100000000)
        self.calcWidgets["Efficiency"].setRange(0,100000000)
        self.calcWidgets["Efficiency"].setSuffix("%")
        self.calcWidgets["Efficiency"].setSingleStep(0.5)


        self.calcWidgets["Description Type"].setFixedWidth(140)
        self.calcWidgets["Source"].setFixedWidth(80)
        self.calcWidgets["BU"].setFixedWidth(140)
        self.calcWidgets["Super-Category"].setFixedWidth(140)
        self.calcWidgets["Category"].setFixedWidth(140)
        self.calcWidgets["Sub-Category"].setFixedWidth(140)
        self.calcWidgets["Vertical"].setFixedWidth(140)
        self.calcWidgets["Quantity"].setFixedWidth(80)
        self.calcWidgets["Efficiency"].setFixedWidth(80)
        self.calcWidgets["Target"].setFixedWidth(60)

        self.calcWidgets["Description Type"].setFixedHeight(20)
        self.calcWidgets["Source"].setFixedHeight(20)
        self.calcWidgets["BU"].setFixedHeight(20)
        self.calcWidgets["Super-Category"].setFixedHeight(20)
        self.calcWidgets["Category"].setFixedHeight(20)
        self.calcWidgets["Sub-Category"].setFixedHeight(20)
        self.calcWidgets["Vertical"].setFixedHeight(20)
        self.calcWidgets["Quantity"].setFixedHeight(20)
        self.calcWidgets["Efficiency"].setFixedHeight(20)
        self.calcWidgets["Target"].setFixedHeight(20)


        style_sheet = """
                .QLabel, .QComboBox, .QSpinBox {
                    font: 11px;
                }
        """
        for widget_label in self.calcWidgets.keys():
            self.calcWidgets[widget_label].setStyleSheet(style_sheet)

    def setValues(self, values_dict):
        bu_index = self.calcWidgets["BU"].findText(values_dict["BU"])
        self.calcWidgets["BU"].setCurrentIndex(bu_index)
        
        supercategory_index = self.calcWidgets["Super-Category"].findText(values_dict["Super-Category"])
        self.calcWidgets["Super-Category"].setCurrentIndex(supercategory_index)
        
        category_index = self.calcWidgets["Category"].findText(values_dict["Category"])
        self.calcWidgets["Category"].setCurrentIndex(category_index)
        
        subcategory_index = self.calcWidgets["Sub-Category"].findText(values_dict["Sub-Category"])
        self.calcWidgets["Sub-Category"].setCurrentIndex(subcategory_index)

        vertical_index = self.calcWidgets["Vertical"].findText(values_dict["Vertical"])
        self.calcWidgets["Vertical"].setCurrentIndex(vertical_index)

    def alertMessage(self, title, message):
        """Vindaloo."""
        QtGui.QMessageBox.about(QtGui.QWidget(), title, message)

    def mapToolTips(self):
        """Calculator Row"""
        self.calcWidgets["Description Type"].setToolTip("Choose the type of the description.")
        self.calcWidgets["Source"].setToolTip("Choose the article source.")
        self.calcWidgets["BU"].setToolTip("Select the BU")
        self.calcWidgets["Super-Category"].setToolTip("Select the Super-Category")
        self.calcWidgets["Category"].setToolTip("Select the Category")
        self.calcWidgets["Sub-Category"].setToolTip("Select the Sub-Category")
        self.calcWidgets["Vertical"].setToolTip("Select the Vertical")
        self.calcWidgets["Quantity"].setToolTip("Set the number of articles article.")
        self.calcWidgets["Efficiency"].setToolTip("Change this and press the tab key to increase the number of articles appropriately.")
        self.calcWidgets["Target"].setToolTip("This is the appropriate target for today's date.")


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

        self.calcWidgets["Efficiency"].editingFinished.connect(self.updateQuantity)

    def updateQuantity(self):
        minimum_efficiency = float(self.calcWidgets["Efficiency"].value())
        if self.target >0:
            if minimum_efficiency >=self.efficiency:
                required_articles = int(math.ceil(self.target*minimum_efficiency/100))
            else:
                required_articles = int(math.floor(self.target*minimum_efficiency/100))

            self.calcWidgets["Quantity"].setValue(required_articles)
        else:
            self.alertMessage("No target!","That row doesn't have a target. It could be that you've not filled all the options, or there's no target defined in the category tree on the server.")

    def updateEfficiency(self):
        """Calculator Row"""
        efficiency = self.getEfficiency()
        if efficiency is None:
            efficiency = 0
            self.calcWidgets["Efficiency"].setStyleSheet("QDoubleSpinBox {background-color: #FF0000}")
            self.calcWidgets["Efficiency"].setToolTip("This row has no defined efficiency!")
        else:
            self.calcWidgets["Efficiency"].setStyleSheet("")    
            self.calcWidgets["Efficiency"].setToolTip("Change this to increase the number of articles appropriately.")
        self.calcWidgets["Efficiency"].setValue(efficiency)
   
    def populateTypeSource(self):
        """Calculator Row"""
        self.types = sorted(set(self.category_tree["Description Type"]))
        self.sources = sorted(set(self.category_tree["Source"]))
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
        target = float(MOSES.getTargetFor(self.userID, self.password, row, self.target_date, self.category_tree))
        self.target = target

        self.calcWidgets["Target"].setText("%s"%target)

        quantity = float(self.calcWidgets["Quantity"].value())
        self.efficiency = (quantity*100.00/target) if target > 0 else None
        return self.efficiency

class EfficiencyCalculator(QtGui.QDialog):
    """Class definition for the efficiency calculator."""
    def __init__(self, userID, password, category_tree=None, *args, **kwargs):
        """Efficiency Calculator Initializer function."""
        super(QtGui.QDialog, self).__init__()
        self.userID = userID
        self.password = password
        if category_tree is None:
            self.category_tree = MOSES.getCategoryTree(self.userID, self.password)
        else:
            self.category_tree = category_tree 
        self.target_date = datetime.date.today()
        self.retrieved_data = None
        self.allow_paste = False
        self.calcList = []
        self.createWidgets()
        self.createLayouts()
        self.createEvents()
        self.setVisuals()

    def createWidgets(self):
        """Efficiency Calculator: Creates widgets."""
        self.calc_table = QtGui.QTableWidget()
        self.category_tree_headers = ["BU","Super-Category","Category","Sub-Category","Vertical"]
        self.headers = ["Description Type","Source"] + self.category_tree_headers + ["Quantity","Efficiency","Target"]
        self.calc_table.setColumnCount(len(self.headers))
        self.calc_table.setMinimumWidth(1200)
        self.date_label = QtGui.QLabel("Target Date:")
        self.date_picker = QtGui.QDateEdit()
        self.date_picker.setMinimumDate(QtCore.QDate(datetime.date(2015,1,1)))
        self.date_picker.setDate(QtCore.QDate(datetime.date.today()))
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDisplayFormat('MMM d yyyy')
        self.addCalcRow()
        self.plusButton = QtGui.QPushButton("Add Another Type of Article")
        #self.findIdenLabel = QtGui.QLabel("Find a vertical")
        self.refreshButton = QtGui.QPushButton("Recalculate Efficiency")
        self.totEffLabel = QtGui.QLabel("Total Efficiency:")
        self.effScoreLabel = QtGui.QLabel("00.00%")
        label_style_sheet = """
            QLabel {
                    font: 16px;
                    font-weight: bold;
            }"""
        self.totEffLabel.setStyleSheet(label_style_sheet)
        self.effScoreLabel.setStyleSheet(label_style_sheet)

        self.finder_widget = CategoryFinder(self.category_tree, self.category_tree_headers)
        #Finder
        

    def createLayouts(self):
        """Efficiency Calculator."""
        efficiency_and_date_layout = QtGui.QHBoxLayout()
        efficiency_and_date_layout.addWidget(self.date_label,0,QtCore.Qt.AlignLeft)
        efficiency_and_date_layout.addWidget(self.date_picker,0,QtCore.Qt.AlignLeft)
        efficiency_and_date_layout.addWidget(self.plusButton,0)
        efficiency_and_date_layout.addWidget(self.refreshButton,0)
        efficiency_and_date_layout.addStretch(2)
        efficiency_and_date_layout.addWidget(self.totEffLabel, 0, QtCore.Qt.AlignRight)
        efficiency_and_date_layout.addWidget(self.effScoreLabel, 0, QtCore.Qt.AlignRight)
        self.finalLayout = QtGui.QVBoxLayout()
        self.finalLayout.addLayout(self.finder_widget,0)
        self.finalLayout.addWidget(self.calc_table,1)
        self.finalLayout.addLayout(efficiency_and_date_layout,0)
        self.setLayout(self.finalLayout)

    def addCalcRow(self):
        """Efficiency Calculator."""
        #print "Entered the loop!"
        self.calcList.append(calculatorRow(self.userID, self.password, self.category_tree, self.target_date)) 
        if self.allow_paste:
            if self.retrieved_data is not None:
                self.calcList[-1].setValues(self.retrieved_data)
                self.retrieved_data = None
                self.allow_paste = False
            else:
                self.alertMessage("Error", "There's no retrieved data.")
        #print "Printing Calc List", self.calcList
        row_count = int(self.calc_table.rowCount())
        self.calc_table.insertRow(0)
        row = 0
        column = 0
        for widget_name in self.headers:
            self.calc_table.setCellWidget(row, column, self.calcList[-1].calcWidgets[widget_name])
            column+=1
        self.calc_table.setHorizontalHeaderLabels(self.headers)
        self.calc_table.resizeRowsToContents()
        self.calc_table.resizeColumnsToContents()
        self.calc_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.calc_table.horizontalHeader().setStretchLastSection(True)
        self.calc_table.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    
    def createEvents(self):
        """Efficiency Calculator."""
        self.plusButton.clicked.connect(self.plusAction)
        self.refreshButton.clicked.connect(self.displayEfficiency)
        self.connectQuantityWidgets()
        self.finder_widget.pickRow.connect(self.useRow)
        self.calc_table.cellClicked.connect(self.tryPasting)
        self.date_picker.dateChanged.connect(self.changeDate)

    def changeDate(self):
        self.target_date = self.date_picker.date().toPyDate()
        for calc_row in self.calcList:
            calc_row.target_date = self.target_date
        self.displayEfficiency()

    def useRow(self, row_dict):
        self.alertMessage("Select Row","Click on any cell in a row to use the chosen attributes, or, if you like, you can add a new row that'll be populated with that category combination right away.")
        self.retrieved_data = row_dict
        self.allow_paste = True

    def tryPasting(self, row, column):
        if self.allow_paste:
            if self.retrieved_data is not None:
                self.calcList[(self.calc_table.rowCount()-1) - row].setValues(self.retrieved_data)
                self.retrieved_data = None
                self.allow_paste = False
            else:
                self.alertMessage("Error", "No retrieved data!")


    def setVisuals(self):
        """Efficiency Calculator."""
        functionName = sys._getframe().f_code.co_name
        self.setWindowTitle("Efficiency Calculator: Ignorance is Knowledge")
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.show()


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
        totalEfficiency = 0.0
        for calc_row in self.calcList:
            calc_row.updateEfficiency()
            efficiency = calc_row.efficiency if calc_row.efficiency is not None else 0
            totalEfficiency += efficiency
        self.effScoreLabel.setText("%.2f%%"%totalEfficiency)

    def alertMessage(self, title, message):
        """Vindaloo."""
        QtGui.QMessageBox.about(self, title, message)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    u, p = MOSES.getBigbrotherCredentials()
    calc = EfficiencyCalculator(u,p)
    calc.show()
    sys.exit(app.exec_())
