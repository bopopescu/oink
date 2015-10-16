import os
import datetime
import MOSES
import pandas
from functools import partial
from PyQt4 import QtGui, QtCore
import numpy

class CategoryFinder(QtGui.QHBoxLayout):
    pickRow = QtCore.pyqtSignal(dict)
    def __init__(self, category_tree, category_tree_headers, *args, **kwargs):
        super(CategoryFinder, self).__init__(*args, **kwargs)
        self.category_tree = category_tree
        self.category_tree_headers = category_tree_headers
        self.createUI()
        self.mapEvents()

    def mapEvents(self):
        self.find_button.clicked.connect(self.findIdentifier)

    def createUI(self):
        self.finder_label = QtGui.QLabel("Find in the Category Tree:")
        self.search_criteria_combo_box = QtGui.QComboBox()
        self.search_criteria_combo_box.setToolTip("Select which column you'd like to look in. The 'any' option looks into all of them.")
        self.search_criteria_combo_box.addItems(["Any"] + self.category_tree_headers)
        
        self.search_string_line_edit = QtGui.QLineEdit()
        self.search_string_line_edit.setToolTip("Type what you'd like to find. One query at a time.")
        self.search_string_line_edit.setMinimumWidth(150)

        self.find_button = QtGui.QPushButton("Find")
        self.find_button.setToolTip("This is the self destruct button. NOT! It's the search button. Watch out Google, I'm coming after you.")

        self.result_table = QtGui.QTableWidget()
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(len(self.category_tree_headers)+ 1)
        self.result_table.setHorizontalHeaderLabels(self.category_tree_headers+["Use Button"])
        self.result_table.resizeColumnsToContents()
        self.result_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.result_table.verticalHeader().setStretchLastSection(False)
        self.result_table.setVisible(False)
        self.use_buttons = []

        #self.find_widget_layout = QtGui.QHBoxLayout()

        self.addWidget(self.finder_label,0, QtCore.Qt.AlignLeft)
        self.addWidget(self.search_criteria_combo_box,0)
        self.addWidget(self.search_string_line_edit,1)
        self.addWidget(self.find_button,0,)

        #self.find_widget_layout.addWidget(self.result_table,1,0,2,7)

    def alertMessage(self, title, message):
        """Vindaloo."""
        QtGui.QMessageBox.about(QtGui.QWidget(), title, message)

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
        self.result_dataframe = None
        self.use_buttons = []
        if search_string != "":
            if search_criteria != "Any":
                self.result_dataframe = self.findIdentifierInCategoryTree(search_string, search_criteria)
                self.category_tree[self.category_tree[search_criteria].str.contains(search_string)]
                self.result_dataframe.drop_duplicates(subset=self.category_tree_headers, inplace=True)
                self.result_dataframe = self.result_dataframe.reset_index()
                self.alertMessage("Alert", "%d results found when searching for '%s' in the %s column of the category tree."%(len(self.result_dataframe.index),search_string, search_criteria))
            else:
                dfs = []     
                for search_criteria in self.category_tree_headers:
                    dfs.append(self.findIdentifierInCategoryTree(search_string, search_criteria))
                self.result_dataframe = pandas.concat(dfs)
                self.result_dataframe.drop_duplicates(subset=self.category_tree_headers, inplace=True)
                self.result_dataframe = self.result_dataframe.reset_index()

                self.alertMessage("Alert", "%d results found when searching for '%s' in all columns of the category tree."%(len(self.result_dataframe.index),search_string))

        if self.result_dataframe is not None:
            self.result_table.setRowCount(0)
            row_counter = 0
            for row in self.result_dataframe.iterrows():
                #print row[1]
                self.result_table.insertRow(row_counter)
                column_counter = 0
                for column_name in self.category_tree_headers:
                    string_value = str(row[1][column_name])
                    self.result_table.setItem(row_counter, column_counter, QtGui.QTableWidgetItem(string_value))
                    column_counter += 1
                self.use_buttons.append(QtGui.QPushButton("Use"))
                self.use_buttons[-1].setToolTip("Click to use this combination.")
                self.use_buttons[row_counter].clicked.connect(partial(self.clickUse, row_counter))
                self.result_table.setCellWidget(row_counter, column_counter, self.use_buttons[row_counter])

                row_counter += 1

            self.result_table.setHorizontalHeaderLabels(self.category_tree_headers+["Use Button"])
            self.result_table.resizeColumnsToContents()
            self.result_table.resizeRowsToContents()
            self.result_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self.result_table.horizontalHeader().setStretchLastSection(True)
            self.result_table.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self.result_table.verticalHeader().setStretchLastSection(False)
        if self.result_table.rowCount() >0:
            self.result_table.setVisible(True)
            self.result_table.show()
            self.result_table.setWindowTitle("Search Results")
            self.result_table.setMinimumWidth(600)


    def clickUse(self, count):
        self.pickRow.emit(self.result_dataframe.xs(count)[self.category_tree_headers].to_dict())
        self.result_table.setVisible(False)