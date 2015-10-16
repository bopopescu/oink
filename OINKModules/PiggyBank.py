
from PyQt4 import QtGui
import MOSES

class PiggyBank(QtGui.QTableWidget):
    """Piggy Bank Class Definition."""
    def __init__(self):
        QtGui.QTableWidget.__init__(self, 0 ,0)
        self.setStyleSheet("gridline-color: rgb(0, 0, 0)")
        header_labels = MOSES.getPiggyBankKeys()
        self.setColumnCount(len(header_labels))
        self.setHorizontalHeaderLabels(header_labels)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.verticalHeader().setStretchLastSection(False)
        self.verticalHeader().setVisible(True)
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setVisible(True)       

    def setData(self, data_list, targets_data):
        self.data_list = data_list
        self.targets_data = targets_data

    def displayData(self):
        #print "Displaying piggybank data!"
        self.setSortingEnabled(False)
        self.setRowCount(0)
        row_index = 0
        header_labels = MOSES.getPiggyBankKeys()
        self.setColumnCount(len(header_labels))
        for row in self.data_list:
            #print "Printing:"
            #print row
            #print type(row)
            #print "Row %d" % row_index #debug
            if len(row) > 0:
                column_index = 0
                self.insertRow(row_index)
                #get the keys from the PiggyBank Key list.
                for key in header_labels: #each row is a dictionary.
                    cell_item = QtGui.QTableWidgetItem(str(row[key]))
                    text_color = QtGui.QColor(0, 0, 0)
                    
                    if self.targets_data[row_index] == 0:
                        cell_color = QtGui.QColor(255, 0, 0, 100) #Transparent red.
                    elif self.targets_data[row_index] == -1:
                        cell_color = QtGui.QColor(0, 0, 0, 10)
                        text_color = QtGui.QColor(255, 0, 0)
                    else:
                        cell_color = QtGui.QColor(255, 255, 255, 0) #invisible white.

                    cell_item.setBackgroundColor(cell_color)
                    cell_item.setTextColor(text_color)
                    self.setItem(row_index,column_index,cell_item)
                    column_index += 1
                row_index += 1
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setHorizontalHeaderLabels(header_labels)
        self.setSortingEnabled(True)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.verticalHeader().setStretchLastSection(False)
        self.verticalHeader().setVisible(True)
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setVisible(True)

        #QtGui.QMessageBox.about(self, "Success", "Pulled %d entries for selected date(s)." % len(self.data_list))
        
    def setDisplayLevel(self, identity=None):
        print "setting display level."