import os
import datetime
import MOSES
import pandas
from functools import partial
from PyQt4 import QtGui, QtCore
import numpy
from ViktorKrum import ViktorKrum

class CategoryFinder(QtGui.QHBoxLayout):
    pickRow = QtCore.pyqtSignal(dict)
    def __init__(self, category_tree, category_tree_headers=None, *args, **kwargs):
        super(CategoryFinder, self).__init__(*args, **kwargs)
        self.category_tree = category_tree
        if category_tree_headers is not None:
            self.category_tree_headers = category_tree_headers
        else:
            self.category_tree_headers = ["BU","Super-Category","Category","Sub-Category","Vertical"]
        self.category_seeker = ViktorKrum(self.category_tree, self.category_tree_headers)
        self.createUI()
        self.mapEvents()

    def mapEvents(self):
        self.find_button.clicked.connect(self.findIdentifier)
        self.category_seeker.sendResult.connect(self.useRetrievedDataFrame)

    def createUI(self):
        self.finder_label = QtGui.QLabel("Find in the Category Tree:")
        self.search_criteria_combo_box = QtGui.QComboBox()
        self.search_criteria_combo_box.setToolTip("Select which column you'd like to look in. The 'any' option looks into all of them.")
        self.search_criteria_combo_box.addItems(["Any"] + self.category_tree_headers)
        
        self.search_string_line_edit = QtGui.QLineEdit()
        self.search_string_line_edit.setToolTip("Type what you'd like to find. One query at a time.")
        self.search_string_line_edit.setMinimumWidth(150)
        suggestions = sorted(set(list(self.category_tree["Vertical"]) + list(self.category_tree["BU"]) + list(self.category_tree["Super-Category"])+ list(self.category_tree["Category"]) + list(self.category_tree["Sub-Category"])))
        completer = QtGui.QCompleter(suggestions)
        self.search_string_line_edit.setCompleter(completer)

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

        self.addWidget(self.finder_label,0, QtCore.Qt.AlignLeft)
        self.addWidget(self.search_criteria_combo_box,0)
        self.addWidget(self.search_string_line_edit,1)
        self.addWidget(self.find_button,0,)

    def alertMessage(self, title, message):
        """Vindaloo."""
        QtGui.QMessageBox.about(QtGui.QWidget(), title, message)


    def findIdentifier(self):
        """Efficiency Calculator."""
        self.find_button.setEnabled(False)
        self.search_string_line_edit.setEnabled(False)
        #functionName = sys._getframe().f_code.co_name
        search_string = str(self.search_string_line_edit.text()).strip().replace(" ","")
        search_criteria = str(self.search_criteria_combo_box.currentText())
        if search_string != "":
            self.category_seeker.startFindingIdentifier(search_string, search_criteria)

    def useRetrievedDataFrame(self, result_dataframe):
        self.result_dataframe = result_dataframe
        self.use_buttons = []
        results = self.result_dataframe.shape[0]
        if results >0:
            self.alertMessage("Done","Retrieved %d rows of data."%results)
            self.use_buttons = []

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
        else:
            self.alertMessage("No Search Results","There is no match when searching for %s in the category tree."%search_string)
        self.search_string_line_edit.setEnabled(True)
        self.find_button.setEnabled(True)


    def clickUse(self, count):
        self.pickRow.emit(self.result_dataframe.xs(count)[self.category_tree_headers].to_dict())
        self.result_table.setVisible(False)