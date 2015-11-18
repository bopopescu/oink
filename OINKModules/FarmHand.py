from __future__ import division
import os
import sys
import datetime

from PyQt4 import QtGui, QtCore

import MOSES
from CheckableComboBox import CheckableComboBox

class FarmHand(QtGui.QWidget):
    def __init__(self, user_id, password):
        super(FarmHand,self).__init__()
        self.user_id, self.password = user_id, password
        self.createUI()
        self.mapEvents()
        self.clip = QtGui.QApplication.clipboard()
        self.show()
        
    
    def createUI(self):
        self.start_date_edit = QtGui.QDateEdit()
        self.start_date_edit.setMinimumDate(datetime.date(2015,1,1))
        self.start_date_edit.setToolTip("Select a start date.")
        self.start_date_edit.setMaximumDate(datetime.date.today())
        self.end_date_edit = QtGui.QDateEdit()
        self.end_date_edit.setToolTip("Select an end date.")
        self.end_date_edit.setMinimumDate(datetime.date(2015,1,1))
        self.end_date_edit.setMaximumDate(datetime.date.today())
        self.start_date_edit.setCalendarPopup(True)
        self.end_date_edit.setCalendarPopup(True)
        self.start_date_label = QtGui.QLabel("Select a start date:")
        self.end_date_label = QtGui.QLabel("Select an end date:")
        self.type_combo_box = CheckableComboBox("Article Type")
        self.type_combo_box.setToolTip("Select what article types you want to check the helpfulness data metrics for.\nLeave as is to pull the overall metrics.")
        self.type_combo_box.setMinimumWidth(210)

        self.type_combo_box.addItems(["PD","RPD","BG"])
        self.pull_button = QtGui.QPushButton("Pull Helpfulness Data")
        self.helpfulness_report_table = QtGui.QTableWidget(0,0)
        self.helpfulness_data_table = QtGui.QTableWidget(0,0)
        style_string = """
        .QTableWidget {
            gridline-color: rgb(0, 0, 0);
        }
        """
        self.setStyleSheet(style_string)
        self.reports_tab = QtGui.QTabWidget()
        self.reports_tab.addTab(self.helpfulness_report_table,"Report")
        self.reports_tab.addTab(self.helpfulness_data_table,"Data")
        self.layout = QtGui.QVBoxLayout()
        self.form_layout = QtGui.QHBoxLayout()
        self.form_layout.addWidget(self.start_date_label,0)
        self.form_layout.addWidget(self.start_date_edit,0)
        self.form_layout.addWidget(self.end_date_label,0)
        self.form_layout.addWidget(self.end_date_edit,0)
        self.form_layout.addWidget(self.type_combo_box,2)
        self.form_layout.addWidget(self.pull_button,0)
        self.layout.addLayout(self.form_layout,0)
        self.layout.addWidget(self.reports_tab,1)
        self.setLayout(self.layout)
        self.setWindowTitle("Farm Hand")
        if "OINKModules" in os.getcwd():
            icon_file_name_path = os.path.join(os.path.join('..',"Images"),'PORK_Icon.png')
        else:
            icon_file_name_path = os.path.join('Images','PORK_Icon.png')
        self.setWindowIcon(QtGui.QIcon(icon_file_name_path))

    def mapEvents(self):
        self.start_date_edit.dateChanged.connect(self.limitEndDate)
        self.pull_button.clicked.connect(self.populateReport)

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_C:
                current_tab = self.reports_tab.currentIndex()

                if current_tab == 0:
                    table_to_copy = self.helpfulness_report_table
                else:
                    table_to_copy = self.helpfulness_data_table

                selected = table_to_copy.selectedRanges()
                s = '\t'+"\t".join([str(table_to_copy.horizontalHeaderItem(i).text()) for i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1)])
                s = s + '\n'
                for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
                    s += str(r+1) + '\t' 
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(table_to_copy.item(r,c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)

    def populateReport(self):
#        print "Populating report"
        entity_types = self.type_combo_box.getCheckedItems()
        if len(entity_types) == 0:
            entity_types = None
        data = MOSES.getFeedbackBetweenDates(self.user_id, self.password, self.start_date_edit.date().toPyDate(), self.end_date_edit.date().toPyDate(), entity_types)
        if data["total"] != 0: 
            self.helpfulness_report_table.setRowCount(1)
            self.helpfulness_report_table.setColumnCount(4)
            self.helpfulness_report_table.setHorizontalHeaderLabels(["Yes","No","Total","Helpfulness%"])
            self.helpfulness_report_table.setItem(0,0,QtGui.QTableWidgetItem(str(data["yes"])))
            self.helpfulness_report_table.setItem(0,1,QtGui.QTableWidgetItem(str(data["total"]-data["yes"])))
            self.helpfulness_report_table.setItem(0,2,QtGui.QTableWidgetItem(str(data["total"])))
            self.helpfulness_report_table.setItem(0,3,QtGui.QTableWidgetItem("%.2f%%"%(100*data["yes"]/data["total"])))
            #print data["data"][0].keys()
            data_headers = ["Time Stamp","Article Type","Item ID","FSN","Feedback","Feedback Comment"]
            table_rows = len(data["data"])
            self.helpfulness_data_table.setSortingEnabled(False)
            self.helpfulness_data_table.setRowCount(table_rows)
            self.helpfulness_data_table.setColumnCount(len(data_headers))
            self.helpfulness_data_table.setHorizontalHeaderLabels(data_headers)
            for row_index in range(table_rows):
                self.helpfulness_data_table.setItem(row_index,0,QtGui.QTableWidgetItem(str(data["data"][row_index]["create_stamp"])))
                self.helpfulness_data_table.setItem(row_index,1,QtGui.QTableWidgetItem(str(data["data"][row_index]["entity_type"])))
                self.helpfulness_data_table.setItem(row_index,2,QtGui.QTableWidgetItem(str(data["data"][row_index]["entity_id"])))
                self.helpfulness_data_table.setItem(row_index,3,QtGui.QTableWidgetItem(str(data["data"][row_index]["FSN"])))
                self.helpfulness_data_table.setItem(row_index,4,QtGui.QTableWidgetItem(str(data["data"][row_index]["feedback"])))
                self.helpfulness_data_table.setItem(row_index,5,QtGui.QTableWidgetItem(str(data["data"][row_index]["metadata"])))
            self.helpfulness_data_table.setSortingEnabled(True)
            self.helpfulness_data_table.resizeColumnsToContents()
            self.helpfulness_data_table.setColumnWidth(5,200)
            self.helpfulness_data_table.setWordWrap(True)
            self.helpfulness_data_table.resizeRowsToContents()
            self.alertMessage("Completed!","Finished summarizing feedback data for the selected entity types between %s and %s" %(self.start_date_edit.date().toPyDate(), self.end_date_edit.date().toPyDate()))
        else:
            self.alertMessage("No Data Available!","There is no feedback available for the selected entity types between %s and %s" %(self.start_date_edit.date().toPyDate(), self.end_date_edit.date().toPyDate()))

    def limitEndDate(self):
        self.end_date_edit.setMinimumDate(self.start_date_edit.date().toPyDate())

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    u, p = MOSES.getBigbrotherCredentials()
    farm_hand = FarmHand(u,p)
    farm_hand.show()
    sys.exit(app.exec_())