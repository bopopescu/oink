from __future__ import division
import os
import datetime

from PyQt4 import QtGui, QtCore
import pandas as pd

from CheckableComboBox import CheckableComboBox
from CopiableQTableWidget import CopiableQTableWidget
from FormattedDateEdit import FormattedDateEdit
import MOSES

class LeaveApproval(QtGui.QWidget):
    def __init__(self, user_id, password, *args, **kwargs):
        super(LeaveApproval, self).__init__(*args, **kwargs)
        self.user_id, self.password = user_id, password
        self.work_calendar = None
        self.selected_name = False
        self.createUI()
        self.initiate()
        self.mapEvents()
        self.applyFilters()


    def createUI(self):
        self.date_label = QtGui.QLabel("Date(s):")
        self.start_date = FormattedDateEdit()
        self.end_date = FormattedDateEdit()

        self.employees_label = QtGui.QLabel("Employees:")
        self.employees_selection_box = CheckableComboBox("Employees")
        self.all_button = QtGui.QPushButton("Select All")
        self.clear_button = QtGui.QPushButton("Clear")

        self.refresh_table_button = QtGui.QPushButton("Refresh Table")
        self.approve_selected_button = QtGui.QPushButton("Approved")
        self.approve_selected_button.setCheckable(True)
        self.reject_selected_button = QtGui.QPushButton("Rejected")
        self.reject_selected_button.setCheckable(True)
        self.pending_selected_button = QtGui.QPushButton("Pending")
        self.pending_selected_button.setCheckable(True)

        self.button_group = QtGui.QButtonGroup()
        self.button_group.addButton(self.approve_selected_button)
        self.button_group.addButton(self.reject_selected_button)
        self.button_group.addButton(self.pending_selected_button)
        self.button_group.setExclusive(True)

        self.approval_comment_label = QtGui.QLabel("Approval\\Rejection Comment:")
        self.rejection_comment_lineedit = QtGui.QLineEdit()

        self.leave_table = CopiableQTableWidget(0, 0)

        self.status_label = QtGui.QLabel("Status")
        self.status_combobox = QtGui.QComboBox()
        self.status_combobox.addItems(["Working","Leave"])
        self.comment_label = QtGui.QLabel("Comment")
        self.comment_lineedit = QtGui.QLineEdit()
        self.save_selected_button = QtGui.QPushButton("Save")
        self.save_selected_button.setEnabled(False)
        self.save_all_button = QtGui.QPushButton("Save All")

        row_1 = QtGui.QHBoxLayout()
        row_1.addWidget(self.date_label,0)
        row_1.addWidget(self.start_date,0)
        row_1.addWidget(self.end_date,0)
        row_1.addWidget(self.employees_label,0)
        row_1.addWidget(self.employees_selection_box,0)
        row_1.addWidget(self.all_button,0)
        row_1.addWidget(self.clear_button,0)

        self.relaxation_label = QtGui.QLabel("Relaxation")
        self.relaxation_spinbox = QtGui.QDoubleSpinBox()
        self.relaxation_spinbox.setSuffix("%")

        row_2 = QtGui.QHBoxLayout()
        row_2.addWidget(self.status_label, 0)
        row_2.addWidget(self.status_combobox, 0)
        row_2.addWidget(self.relaxation_label, 0)
        row_2.addWidget(self.relaxation_spinbox, 0)
        row_2.addWidget(self.comment_label, 0)
        row_2.addWidget(self.comment_lineedit, 0)

        row_3 = QtGui.QHBoxLayout()
        row_3.addWidget(self.approval_comment_label,0)
        row_3.addWidget(self.rejection_comment_lineedit,0)
        row_3.addWidget(self.approve_selected_button,0)
        row_3.addWidget(self.reject_selected_button,0)
        row_3.addWidget(self.pending_selected_button,0)
        row_3.addWidget(self.save_selected_button,0)
        row_3.addWidget(self.save_all_button,0)
        row_3.addWidget(self.refresh_table_button,0)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(row_1)
        layout.addLayout(row_2)
        layout.addLayout(row_3)
        layout.addWidget(self.leave_table)

        self.setLayout(layout)
        self.setWindowTitle("Leaves Manager")
        self.setWindowIcon(QtGui.QIcon(os.path.join(MOSES.getPathToImages(),"PORK_Icon.png")))
        self.show()

    def mapEvents(self):
        self.start_date.dateChanged.connect(self.startDateChanged)
        self.end_date.dateChanged.connect(self.applyFilters)
        self.refresh_table_button.clicked.connect(self.applyFilters)
        self.clear_button.clicked.connect(self.employees_selection_box.clearSelection)
        self.leave_table.currentCellChanged.connect(self.populateForm)
        self.employees_selection_box.changedSelection.connect(self.applyFilters)
        self.save_selected_button.clicked.connect(self.saveSelected)
        self.save_all_button.clicked.connect(self.saveAll)
        self.all_button.clicked.connect(self.employees_selection_box.selectAll)

    def saveSelected(self):
        if self.selected_name:
            self.saveThese([self.selected_name])
        else:
            self.alertMessage("Select a row","Select a row in the work calendar and then try again.")
            self.save_selected_button.setEnabled(False)

    def saveAll(self):
        self.saveThese(self.employees_selection_box.getCheckedItems())


    def saveThese(self, selected_names):
        selected_employee_ids = [list(self.employees_list[self.employees_list["Name"] == x]["Employee ID"])[0] for x in selected_names]
        dates = [self.start_date.date().toPyDate(), self.end_date.date().toPyDate()]
        allow_continue = False
        if (len(selected_employee_ids)>1) and (dates[0] == dates[1]):
            ask = QtGui.QMessageBox.question(self, 'Multiple Employees Selected!', "You appear to have chosen the ids of several employees. Click yes if you'd like to continue modifying the work calendar for all their names. If not, click no and select only one employee's name.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if ask == QtGui.QMessageBox.Yes:
                allow_continue = True
        elif (len(selected_employee_ids) > 1) and (dates[0] < dates[1]):
            ask = QtGui.QMessageBox.question(self, 'Multiple Dates and Employees Selected!', "You appear to have chosen the ids of several employees and an entire date range. Are you sure that you want to apply the settings for all of them for all these dates? I'd recommend changing the status of one employee for one date at a time. Click yes if you'd like to continue modifying the work calendar for all their names for those dates. If not, click no and select only one employee's name and one date.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if ask == QtGui.QMessageBox.Yes:
                allow_continue = True
        elif (len(selected_employee_ids) == 1) and (dates[0] < dates[1]):
            ask = QtGui.QMessageBox.question(self, 'Multiple Dates Selected!', "You appear to have chosen an entire date range. Are you sure that you want to apply the settings for the selected employee all these dates? I'd recommend changing the status of one employee for one date at a time. Click yes if you'd like to continue modifying the work calendar for all their names for those dates. If not, click no and select only one date.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if ask == QtGui.QMessageBox.Yes:
                allow_continue = True
        elif (len(selected_employee_ids) <= 0):
            self.alertMessage('No Employees Selected!', "Please select an employee in order to process the work status and relaxation.")
        else:
            allow_continue = True

        if allow_continue:
            status = str(self.status_combobox.currentText())
            relaxation = self.relaxation_spinbox.value()/100
            comment = str(self.comment_lineedit.text())
            if self.approve_selected_button.isChecked():
                approval = "Approved"
            elif self.reject_selected_button.isChecked():
                approval = "Rejected"
            else:
                approval = "Pending"
            approval_comment = str(self.rejection_comment_lineedit.text())
            self.alertMessage("Please Wait","This could take a while. Click OK and hold on to your horses.")
            update = MOSES.updateWorkCalendarFor(self.user_id, self.password, status, relaxation, comment, approval, approval_comment, dates, selected_employee_ids)
            if update:
                self.alertMessage("Success","Successfully updated the Work Calendar")
                self.applyFilters()
            else:
                self.alertMessage("Failure","Failed in updating the Work Calendar")

        else:
            print "Not allowed to continue"

    def initiate(self):
        self.start_date.setDate(datetime.date.today())
        self.start_date.setMinimumDate(datetime.date(2015,1,1))
        self.end_date.setDate(self.start_date.date())
        self.end_date.setMinimumDate(self.start_date.date())
        self.employees_list = MOSES.getEmployeesList(self.user_id, self.password, self.end_date.date().toPyDate())
        self.employees_selection_box.clear()
        self.employees_selection_box.addItems(sorted(list(self.employees_list["Name"])))
        self.employees_selection_box.selectAll()

    def applyFilters(self):
        self.leave_table.showDataFrame(None)
        selected_employee_ids = [list(self.employees_list[self.employees_list["Name"] == x]["Employee ID"])[0] for x in self.employees_selection_box.getCheckedItems()]
        if len(selected_employee_ids)<=0:
            self.alertMessage("No Employees Selected","Select at least one employee!")
        else:
            filter_dict = {
                            "Dates": [self.start_date.date().toPyDate(), self.end_date.date().toPyDate()],
                            "Employee IDs": selected_employee_ids
                        }
            time_diff = (filter_dict["Dates"][1] - filter_dict["Dates"][0])
            if datetime.timedelta(days=5) < time_diff < datetime.timedelta(days=30):
                self.alertMessage("Please Wait","The work calendar is being refreshed. This may take a while since you've selected over a week's worth of data.")
            elif time_diff >= datetime.timedelta(days=30):
                self.alertMessage("Please Wait","The work calendar is being refreshed. This will take quite some time longer than usual since you've selected a date range wider than or equal to 30 days.")

            
            self.work_calendar = MOSES.getWorkCalendarFor(self.user_id, self.password, filter_dict)
            self.alertMessage("Success","Retrieved the Work Calendar")
            yellow = QtGui.QColor(200,200,0)
            green = QtGui.QColor(0,153,0)
            red = QtGui.QColor(170,0,0)

            highlight_rules = [
                                {
                                    "Columns": ["Status","Approval"],
                                    "Values": ["Leave","Approved"],
                                    "Color":green
                                },
                                {
                                    "Columns": ["Status","Approval"],
                                    "Values": ["Leave","Pending"],
                                    "Color":  yellow
                                },
                                {
                                    "Columns": ["Status","Approval"],
                                    "Values": ["Leave","Rejected"],
                                    "Color": red
                                },
                                {
                                    "Columns": ["Relaxation","Approval"],
                                    "Values": [[0.01,1.00],"Approved"],
                                    "Color": green
                                },
                                {
                                    "Columns": ["Relaxation","Approval"],
                                    "Values": [[0.01,1.00],"Pending"],
                                    "Color":  yellow
                                },
                                {
                                    "Columns": ["Relaxation","Approval"],
                                    "Values": [[0.01,1.00],"Rejected"],
                                    "Color": red
                                }
                                ]
            self.leave_table.showDataFrame(self.work_calendar,highlight_rules)
            self.leave_table.setSortingEnabled(False)

    def startDateChanged(self):
        self.end_date.setDate(self.start_date.date())
        self.end_date.setMinimumDate(self.start_date.date())
        self.applyFilters()

    def populateForm(self, row=None, column=None):
        if self.work_calendar is not None:
            #rows = sorted(set(index.row() for index in self.leave_table.selectedIndexes()))
            try:
                selected_row = self.work_calendar.loc[row]
                self.selected_name = selected_row["Employee Name"]
                status = selected_row["Status"]
                relaxation = selected_row["Relaxation"]
                comment = selected_row["Comment"]
                approval = selected_row["Approval"]
                rejection_comment = selected_row["Rejection Comment"]
                date_ = selected_row["Date"]
                self.save_selected_button.setText("Save %s's entry"%self.selected_name)
                self.save_selected_button.setEnabled(True)
            except:
                self.selected_name = None
                self.save_selected_button.setText("Save Selected")
                self.save_selected_button.setEnabled(False)
                comment = ""
                relaxation = 0.0
                rejection_comment = ""
                status = "Working"
                approval = "Pending"

            self.comment_lineedit.setText(comment if comment is not None else "")
            self.status_combobox.setCurrentIndex(self.status_combobox.findText(status))
            self.rejection_comment_lineedit.setText(rejection_comment if rejection_comment is not None else "")
            self.relaxation_spinbox.setValue((relaxation*100))
            if approval is not None:
                if approval == "Approved":
                    self.approve_selected_button.setChecked(True)
                elif approval == "Rejected":
                    self.reject_selected_button.setChecked(True)
                else:
                    self.pending_selected_button.setChecked(True)
            else:
                print "Approval is None!"

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)