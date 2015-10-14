#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
import datetime
import re
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

        self.calcWidgets["Description Type"].setFixedWidth(140)
        self.calcWidgets["Source"].setFixedWidth(80)
        self.calcWidgets["BU"].setFixedWidth(140)
        self.calcWidgets["Super-Category"].setFixedWidth(140)
        self.calcWidgets["Category"].setFixedWidth(140)
        self.calcWidgets["Sub-Category"].setFixedWidth(140)
        self.calcWidgets["Vertical"].setFixedWidth(140)
        self.calcWidgets["Quantity"].setFixedWidth(60)
        self.calcWidgets["Efficiency"].setFixedWidth(60)
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


    def alertMessage(self, title, message):
        """Vindaloo."""
        QtGui.QMessageBox.about(self, title, message)

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

        efficiency = self.getEfficiency()
        if efficiency is None:
            efficiency_text = "No Target"
        else:
            efficiency_text = "%.2f%%" % (efficiency)
        self.calcWidgets["Efficiency"].setText(efficiency_text)
   
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
        request_date = datetime.date.today()

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
        self.calc_table = QtGui.QTableWidget()
        self.category_tree_headers = ["BU","Super-Category","Category","Sub-Category","Vertical"]
        self.headers = ["Description Type","Source"] + self.category_tree_headers + ["Quantity","Efficiency","Target"]
        self.calc_table.setColumnCount(len(self.headers))
        self.calc_table.setMinimumWidth(1200)
        self.addCalcRow()

        
        self.plusButton = QtGui.QPushButton("Add Another Type of Article")
        #self.findIdenLabel = QtGui.QLabel("Find a vertical")
        self.refreshButton = QtGui.QPushButton("Recalculate Efficiency")
        self.totEffLabel = QtGui.QLabel("<font size=3 face=Georgia><b>Total Efficiency:</b></font>")
        self.effScoreLabel = QtGui.QLabel("<font size=3 face=Georgia><b>00.00%</b></font>")
        
        #Finder
        self.finder_label = QtGui.QLabel("Search Based On:")
        
        self.search_criteria_combo_box = QtGui.QComboBox()
        self.search_criteria_combo_box.addItems(["Any"] + self.category_tree_headers)
        
        self.search_string_line_edit = QtGui.QLineEdit()

        self.find_button = QtGui.QPushButton("Find")

        self.result_table = QtGui.QTableWidget()
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(len(self.category_tree_headers))
        self.result_table.setHorizontalHeaderLabels(self.category_tree_headers)
        self.result_table.resizeColumnsToContents()

        self.find_widget_layout = QtGui.QGridLayout()

        self.find_widget_layout.addWidget(self.finder_label,0,0 )
        self.find_widget_layout.addWidget(self.search_criteria_combo_box,0, 1)
        self.find_widget_layout.addWidget(self.search_string_line_edit,0, 2, 1, 2)
        self.find_widget_layout.addWidget(self.find_button,0,4,1,1)
        self.find_widget_layout.addWidget(self.result_table,1,0,2,5)

        self.find_group = QtGui.QGroupBox("Find a Vertical")
        self.find_group.setLayout(self.find_widget_layout)

    def createLayouts(self):
        """Efficiency Calculator."""
        self.effLayout = QtGui.QHBoxLayout()
        self.effLayout.addWidget(self.plusButton)
        self.effLayout.addWidget(self.refreshButton)
        self.effLayout.addStretch(2)
        self.effLayout.addWidget(self.totEffLabel)
        self.effLayout.addWidget(self.effScoreLabel)

        self.finalLayout = QtGui.QVBoxLayout()
        self.finalLayout.addWidget(self.calc_table,1)
        self.finalLayout.addWidget(self.find_group,1)
        self.finalLayout.addLayout(self.effLayout,0)

        self.setLayout(self.finalLayout)

    def findIdentifierInCategoryTree(self, search_string, search_criteria):        
        dfs = [self.category_tree[self.category_tree[search_criteria].str.contains(search_string)]]
        dfs.append(self.category_tree[self.category_tree[search_criteria].str.contains(search_string.lower())])
        dfs.append(self.category_tree[self.category_tree[search_criteria].str.contains(search_string.capitalize())])
        dfs.append(self.category_tree[self.category_tree[search_criteria].str.contains(search_string.upper())])
        return pandas.concat(dfs)

    def findIdentifier(self):
        """Efficiency Calculator."""
        #functionName = sys._getframe().f_code.co_name
        search_string = str(self.search_string_line_edit.text()).strip()
        search_criteria = str(self.search_criteria_combo_box.currentText())
        df = None
        if search_criteria != "Any":
            if search_string != "":
                df = self.findIdentifierInCategoryTree(search_string, search_criteria)
                self.category_tree[self.category_tree[search_criteria].str.contains(search_string)]
                df.drop_duplicates(subset=self.category_tree_headers, inplace=True)
                self.alertMessage("Alert", "%d results found when searching for %s in the %s column of the category tree."%(len(df.index),search_string, search_criteria))
            else:
                self.alertMessage("Alert","Try typing a word into the search field before searching for something.")
        else:   
            dfs = []     
            for search_criteria in self.category_tree_headers:
                dfs.append(self.findIdentifierInCategoryTree(search_string, search_criteria))
            df = pandas.concat(dfs)
            df.drop_duplicates(subset=self.category_tree_headers, inplace=True)
            self.alertMessage("Alert", "%d results found when searching for %s in all columns of the category tree."%(len(df.index),search_string))

        if df is not None:
            self.result_table.setRowCount(0)
            row_counter = 0
            for row in df.iterrows():
                #print row[1]
                self.result_table.insertRow(row_counter)
                column_counter = 0
                for column_name in self.category_tree_headers:
                    string_value = str(row[1][column_name])
                    self.result_table.setItem(row_counter, column_counter, QtGui.QTableWidgetItem(string_value))
                    column_counter += 1
                row_counter += 1

            self.result_table.setHorizontalHeaderLabels(self.category_tree_headers)
            self.result_table.resizeColumnsToContents()
            self.result_table.resizeRowsToContents()


    def addCalcRow(self):
        """Efficiency Calculator."""
        #print "Entered the loop!"
        self.calcList.append(calculatorRow(self.userID, self.password, self.category_tree)) 
        #print "Printing Calc List", self.calcList
        row_count = int(self.calc_table.rowCount())
        self.calc_table.insertRow(0)
        row = row_count
        column = 0

        for widget_name in self.headers:
            self.calc_table.setCellWidget(row, column, self.calcList[-1].calcWidgets[widget_name])
            column+=1
        self.calc_table.setHorizontalHeaderLabels(self.headers)
        self.calc_table.resizeRowsToContents()
        self.calc_table.resizeColumnsToContents()

    
    def createEvents(self):
        """Efficiency Calculator."""
        self.plusButton.clicked.connect(self.plusAction)
        self.refreshButton.clicked.connect(self.displayEfficiency)
        self.connectQuantityWidgets()
        self.find_button.clicked.connect(self.findIdentifier)        


    def setVisuals(self):
        """Efficiency Calculator."""
        functionName = sys._getframe().f_code.co_name
        self.setWindowTitle("Efficiency Calculator: Driving What Drives You")
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