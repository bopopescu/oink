import os
import datetime
import MOSES
import pandas
from PyQt4 import QtGui, QtCore
import numpy

class CategoryFinder(QtGui.QWidget):
	pickRow = QtCore.pyqtSignal(dict)
	def __init__(self, category_tree, category_tree_headers, *args, **kwargs):
		super(CategoryFinder, self).__init__(*args, **kwargs)
		self.category_tree = category_tree
		self.category_tree_headers = category_tree_headers
		self.createUI()
		self.mapEvents()

	def createUI(self):
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

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.find_group)
        self.setLayout(layout)

    def mapEvents(self):
        self.find_button.clicked.connect(self.findIdentifier)        

    def alertMessage(self, title, message):
        """Vindaloo."""
        QtGui.QMessageBox.about(self, title, message)

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