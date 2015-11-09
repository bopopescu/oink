from __future__ import division
import path
import os
import math
import datetime

import numpy as pd
import pandas as pd
from PyQt4 import QtGui, QtCore

from CheckableComboBox import CheckableComboBox
from CopiableQTableWidget import CopiableQTableWidget
from ImageLabel import ImageLabel
from ImageButton import ImageButton
from ProgressBar import ProgressBar
import MOSES

class UserManager(QtGui.QMainWindow):
    def __init__(self, user_id, password,*args, **kwargs):
        super(UserManager, self).__init__(*args, **kwargs)
        self.user_id, self.password = user_id, password
        #get the list of users from MOSES.
        self.employees_data = MOSES.getEmployeesList(self.user_id, self.password)
        self.manager_mapping_data = MOSES.getManagerMappingTable(self.user_id, self.password)
        self.createUI()
        self.mapEvents()
        self.initialize()


    def createUI(self):
        self.users_list_label = QtGui.QLabel("Users: ")
        self.users_list_view = QtGui.QListWidget()


        
        self.add_employee_button = ImageButton(os.path.join("Images","add.png"),48,48,os.path.join("Images","add_mouseover.png"))
        self.remove_employee_button = ImageButton(os.path.join("Images","remove.png"),48,48,os.path.join("Images","remove_mouseover.png"))
        self.edit_employee_button = ImageButton(os.path.join("Images","modify.png"),48,48,os.path.join("Images","modify_mouseover.png"))
        
        self.add_employee_button.setFlat(True)
        self.remove_employee_button.setFlat(True)
        self.edit_employee_button.setFlat(True)


        user_list_buttons_layout = QtGui.QHBoxLayout()
        user_list_buttons_layout.addWidget(self.add_employee_button,0)
        user_list_buttons_layout.addWidget(self.remove_employee_button,0)
        user_list_buttons_layout.addWidget(self.edit_employee_button,0)

        users_list_layout = QtGui.QVBoxLayout()
        users_list_layout.addWidget(self.users_list_label,0)
        users_list_layout.addWidget(self.users_list_view,3)
        users_list_layout.addLayout(user_list_buttons_layout,1)
        users_list_layout.addStretch(1)

        self.employee_id_label = QtGui.QLabel("Employee ID")
        self.employee_id_lineedit = QtGui.QLineEdit()
        self.employee_name_label = QtGui.QLabel("Name")
        self.employee_name_lineedit = QtGui.QLineEdit()
        name_id_row = QtGui.QHBoxLayout()
        name_id_row.addWidget(self.employee_id_label,0)
        name_id_row.addWidget(self.employee_id_lineedit,2)
        name_id_row.addWidget(self.employee_name_label,0)
        name_id_row.addWidget(self.employee_name_lineedit,2)

        self.email_label = QtGui.QLabel("Email ID:")
        self.email_lineedit = QtGui.QLineEdit()
        email_row = QtGui.QHBoxLayout()
        email_row.addWidget(self.email_label,0)
        email_row.addWidget(self.email_lineedit,2)

        self.current_role_label = QtGui.QLabel("Role:")
        self.current_role_combobox = QtGui.QComboBox()
        current_role_row = QtGui.QHBoxLayout()
        current_role_row.addWidget(self.current_role_label,0)
        current_role_row.addWidget(self.current_role_combobox,1)

        self.doj_label = QtGui.QLabel("Date of Joining:")
        self.doj_dateedit = QtGui.QDateEdit()
        self.dol_checkbox = QtGui.QCheckBox("Last Working Date:")
        self.dol_checkbox.setToolTip("Check to mark the LWD of this employee.\nLeave unchecked if the employee is still in the team.")
        self.dol_dateedit = QtGui.QDateEdit()
        self.doj_dateedit.setCalendarPopup(True)
        self.dol_dateedit.setCalendarPopup(True)

        doj_dol_row = QtGui.QHBoxLayout()
        doj_dol_row.addWidget(self.doj_label, 0)
        doj_dol_row.addWidget(self.doj_dateedit, 0)
        doj_dol_row.addWidget(self.dol_checkbox, 0)
        doj_dol_row.addWidget(self.dol_dateedit, 0)

        self.former_role_label = QtGui.QLabel("Former Role:")
        self.former_role_combobox = QtGui.QComboBox()
        self.dop_checkbox = QtGui.QCheckBox("Promoted")
        self.dop_checkbox.setToolTip("Check this to record a promotion and keep details of the former role.")
        self.dop_label = QtGui.QLabel("Date of Promotion:")
        self.dop_dateedit = QtGui.QDateEdit()
        self.dop_dateedit.setCalendarPopup(True)

        promotion_row = QtGui.QHBoxLayout()
        promotion_row.addWidget(self.dop_checkbox, 0)
        promotion_row.addWidget(self.dop_label, 0)
        promotion_row.addWidget(self.dop_dateedit, 1)
        promotion_row.addWidget(self.former_role_label, 0)
        promotion_row.addWidget(self.former_role_combobox, 1)

        self.access_label = QtGui.QLabel("OINK Application Access")
        self.access_combobox = CheckableComboBox("Applications")
        self.access_combobox.addItems(["PORK","BACON","VINDALOO"])
        access_row = QtGui.QHBoxLayout()
        access_row.addWidget(self.access_label,0)
        access_row.addWidget(self.access_combobox,2)
        access_row.addStretch(1)

        self.reset_password_button = QtGui.QPushButton("Reset Password")
        self.init_work_calendar_button = QtGui.QPushButton("Initialize Calendar")
        self.save_button = QtGui.QPushButton("Save")
        self.reset_button = QtGui.QPushButton("Revert")


        form_buttons_layout = QtGui.QHBoxLayout()
        form_buttons_layout.addStretch(2)
        form_buttons_layout.addWidget(self.reset_password_button,0)
        form_buttons_layout.addWidget(self.save_button,0)
        form_buttons_layout.addWidget(self.init_work_calendar_button,0)
        form_buttons_layout.addWidget(self.reset_button,0)


        self.progress_bar = ProgressBar()
        self.status_label = QtGui.QLabel()

        self.manager_mapping = CopiableQTableWidget(0,0)

        self.manager_name_label = QtGui.QLabel("Reporting Manager:")
        self.manager_name_combobox = QtGui.QComboBox()
        self.manager_effective_date_label = QtGui.QLabel("Revision Date:")
        self.manager_effective_dateedit = QtGui.QDateEdit()
        self.manager_effective_dateedit.setDate(datetime.date.today())
        self.add_new_manager_mapping_row = QtGui.QPushButton("Add New Mapping")
        self.remove_manager_mapping_row = QtGui.QPushButton("Remove Mapping")
        self.save_manager_mapping_table = QtGui.QPushButton("Save Mapping Changes")

        manager_mapping_form = QtGui.QHBoxLayout()
        manager_mapping_form.addWidget(self.manager_name_label,0)
        manager_mapping_form.addWidget(self.manager_name_combobox,1)
        manager_mapping_form.addWidget(self.manager_effective_date_label,0)
        manager_mapping_form.addWidget(self.manager_effective_dateedit,1)
        manager_mapping_form.addWidget(self.add_new_manager_mapping_row,1)
        manager_mapping_form.addWidget(self.remove_manager_mapping_row,1)
        manager_mapping_form.addWidget(self.save_manager_mapping_table,1)
        



        user_data_form_layout = QtGui.QVBoxLayout()
        user_data_form_layout.addLayout(name_id_row,0)
        user_data_form_layout.addLayout(email_row,0)
        user_data_form_layout.addLayout(current_role_row,0)
        user_data_form_layout.addLayout(doj_dol_row,0)
        user_data_form_layout.addLayout(promotion_row,0)
        user_data_form_layout.addLayout(access_row,0)
        user_data_form_layout.addLayout(form_buttons_layout,0)
        user_data_form_layout.addWidget(self.manager_mapping,1)
        user_data_form_layout.addLayout(manager_mapping_form,0)
        user_data_form_layout.addStretch(1)
        user_data_form_layout.addWidget(self.progress_bar,0)
        user_data_form_layout.addWidget(self.status_label,0)

        user_data_form = QtGui.QGroupBox("User Information:")
        user_data_form.setLayout(user_data_form_layout)

        layout = QtGui.QHBoxLayout()
        layout.addLayout(users_list_layout,1)
        layout.addWidget(user_data_form,2)
        self.central_widget = QtGui.QWidget()
        self.central_widget.setLayout(layout)

        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("OINK User Manager")
        self.setWindowIcon(QtGui.QIcon(os.path.join('Images','PORK_Icon.png')))
        self.show()

    def mapEvents(self):
        self.users_list_view.itemSelectionChanged.connect(self.changedCurrentEmployee)
        self.dop_checkbox.toggled.connect(self.toggleDOP)
        self.dol_checkbox.toggled.connect(self.toggleDOL)
        self.reset_password_button.clicked.connect(self.resetPassword)
        self.manager_mapping.currentCellChanged.connect(self.populateManagerMappingForm)

    def populateManagerMappingForm(self, row=None, column=None):
        rows = sorted(set(index.row() for index in self.manager_mapping.selectedIndexes()))
        manager = self.manager_mapping_data.loc[row]
        name = manager["Reporting Manager Name"]
        date_ = manager["Revision Date"]
        self.manager_name_combobox.setCurrentIndex(self.manager_name_combobox.findText(name))
        self.manager_effective_dateedit.setDate(date_)


    def resetPassword(self):
        current_employee_name = str(self.users_list_view.currentItem().text())
        employee_data = self.getEmployeeData(current_employee_name)
        employee_id = employee_data["Employee ID"]
        MOSES.resetPassword(self.user_id, self.password, employee_id)
        self.alertMessage("Reset Password","Successfully reset %s's password to 'password'!"%(current_employee_name))

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    def toggleDOP(self):
        if self.dop_checkbox.isChecked():
            self.dop_dateedit.setEnabled(True)
            self.former_role_combobox.setEnabled(True)
        else:
            self.former_role_combobox.setCurrentIndex(-1)
            self.former_role_combobox.setEnabled(False)
            self.dop_dateedit.setEnabled(False)

    def toggleDOL(self):
        if self.dol_checkbox.isChecked():
            self.dol_dateedit.setEnabled(True)
        else:
            self.dol_dateedit.setEnabled(False)


    def changedCurrentEmployee(self):
        current_employee_name = str(self.users_list_view.currentItem().text())
        self.showPage(current_employee_name)

    def showPage(self, employee_name):
        employee_data = self.getEmployeeData(employee_name)
        self.employee_name_lineedit.setText(employee_data["Name"])
        self.employee_id_lineedit.setText(employee_data["Employee ID"])
        self.email_lineedit.setText(employee_data["Email ID"])
        self.doj_dateedit.setDate(employee_data["DOJ"])
        
        if employee_data["DOL"] is None:
            self.dol_checkbox.setChecked(False)
        else:
            self.dol_checkbox.setChecked(True)
            self.dol_dateedit.setDate(employee_data["DOL"])
        self.current_role_combobox.setCurrentIndex(self.current_role_combobox.findText(employee_data["Role"]))
        
        if employee_data["Date of Promotion"] is None:
            self.dop_checkbox.setChecked(False)
            self.former_role_combobox.setCurrentIndex(-1)
        else:
            self.dop_checkbox.setChecked(True)
            self.dop_dateedit.setDate(employee_data["Date of Promotion"])
            self.former_role_combobox.setCurrentIndex(self.former_role_combobox.findText(employee_data["Former Role"]))
        self.access_combobox.select(employee_data["Access Level"])

        self.toggleDOP()
        self.toggleDOL()

        self.manager_mapping_data = MOSES.getManagerMappingTable(self.user_id, self.password, employee_data["Employee ID"])
        self.manager_mapping.showDataFrame(self.manager_mapping_data)
        self.manager_name_combobox.setCurrentIndex(-1)



    def getEmployeeData(self, employee_name):
        location_match = self.employees_data["Name"] == employee_name
        employee_id = list(self.employees_data[location_match]["Employee ID"])[0]
        employee_name = list(self.employees_data[location_match]["Name"])[0]
        employee_email_id = list(self.employees_data[location_match]["Email ID"])[0]
        employee_doj = list(self.employees_data[location_match]["DOJ"])[0]
        employee_dol = list(self.employees_data[location_match]["DOL"])[0]
        employee_role = list(self.employees_data[location_match]["Role"])[0]
        employee_dop = list(self.employees_data[location_match]["Date of Promotion"])[0]
        employee_former_role = list(self.employees_data[location_match]["Former Role"])[0]
        employee_oink_access = list(self.employees_data[location_match]["OINK Access Level"])[0]

        data = {
                "Employee ID": employee_id,
                "Name": employee_name,
                "Email ID": employee_email_id,
                "DOJ": employee_doj,
                "DOL": employee_dol,
                "Role": employee_role,
                "Date of Promotion": employee_dop,
                "Former Role": employee_former_role,
                "Access Level": employee_oink_access
        }
        return data


    def initialize(self):
        employees_list = list(set(self.employees_data["Name"]))
        employees_list.sort()
        self.users_list_view.addItems(employees_list)
        self.manager_name_combobox.addItems(employees_list)
        roles = list(set(self.employees_data["Role"]))
        roles.sort()
        self.current_role_combobox.addItems(roles)
        self.former_role_combobox.addItems(roles)
        self.toggleDOL()
        self.toggleDOP()



    def populateEmployeesList(self):
        pass
    
    def addEmployee(self):
        pass

    def modifyEmployee(self):
        pass

    def resetEmployeePassword(self):
        pass

    def promoteEmployee(self):
        pass

    def populateReportingManagerList(self):
        pass