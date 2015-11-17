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
		self.createUI()
		self.mapEvents()
		self.initiate()
	def createUI(self):
		self.date_label = QtGui.QLabel("Date(s):")
		self.start_date = FormattedDateEdit()
		self.end_date = FormattedDateEdit()

		self.employees_label = QtGui.QLabel("Employees:")
		self.employees_selection_box = CheckableComboBox("Employees")
		self.clear_button = QtGui.QPushButton("Clear")

		self.refresh_table_button = QtGui.QPushButton("Refresh Table")
		self.approve_selected_button = QtGui.QPushButton("Approve Selected")
		self.reject_selected_button = QtGui.QPushButton("Reject Selected")

		self.comment_label = QtGui.QLabel("Approval\\Rejection Comment:")
		self.comment_box = QtGui.QLineEdit()

		self.leave_table = CopiableQTableWidget(0, 0)

		row_1 = QtGui.QHBoxLayout()
		row_1.addWidget(self.date_label,0)
		row_1.addWidget(self.start_date,0)
		row_1.addWidget(self.end_date,0)
		row_1.addWidget(self.employees_label,0)
		row_1.addWidget(self.employees_selection_box,0)
		row_1.addWidget(self.clear_button,0)

		row_2 = QtGui.QHBoxLayout()
		row_2.addWidget(self.comment_label,0)
		row_2.addWidget(self.comment_box,0)
		row_2.addWidget(self.approve_selected_button,0)
		row_2.addWidget(self.reject_selected_button,0)
		row_2.addWidget(self.refresh_table_button,0)

		layout = QtGui.QVBoxLayout()
		layout.addLayout(row_1)
		layout.addLayout(row_2)
		layout.addWidget(self.leave_table)

		self.setLayout(layout)
		self.setWindowTitle("Leaves Manager")
		self.show()

	def mapEvents(self):
		self.start_date.dateChanged.connect(self.startDateChanged)
		self.refresh_table_button.clicked.connect(self.applyFilters)
		self.clear_button.clicked.connect(self.employees_selection_box.clearSelection)

	def initiate(self):
		self.start_date.setDate(datetime.date.today())
		self.employees_list = MOSES.getEmployeesList(self.user_id, self.password, self.end_date.date().toPyDate())
		self.employees_selection_box.clear()
		self.employees_selection_box.addItems(sorted(list(self.employees_list["Name"])))
		self.employees_selection_box.selectAll()
		self.applyFilters()

	def applyFilters(self):
		selected_employee_ids = [list(self.employees_list[self.employees_list["Name"] == x]["Employee ID"])[0] for x in self.employees_selection_box.getCheckedItems()]
		if len(selected_employee_ids)<=0:
			self.employees_selection_box.selectAll()
			selected_employee_ids = [list(self.employees_list[self.employees_list["Name"] == x]["Employee ID"])[0] for x in self.employees_selection_box.getCheckedItems()]
		filter_dict = {
						"Dates": [self.start_date.date().toPyDate(), self.end_date.date().toPyDate()],
						"Employee IDs": selected_employee_ids
					}
		self.work_calendar = MOSES.getWorkCalendarFor(self.user_id, self.password, filter_dict)
		self.leave_table.showDataFrame(self.work_calendar)
		self.leave_table.setSortingEnabled(True)


	def startDateChanged(self):
		self.end_date.setDate(self.start_date.date())
		self.end_date.setMinimumDate(self.start_date.date())
