from __future__ import division
import sys
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
from FormattedDateEdit import FormattedDateEdit
import MOSES

class UserManager(QtGui.QMainWindow):
    def __init__(self, user_id, password,*args, **kwargs):
        super(UserManager, self).__init__(*args, **kwargs)
        self.user_id, self.password = user_id, password
        #get the list of users from MOSES.
        self.refreshData()
        self.createUI()
        self.mapEvents()
        self.initialize()

    def refreshData(self):
        self.employees_data = MOSES.getEmployeesList(self.user_id, self.password)
        self.manager_mapping_data = MOSES.getManagerMappingTable(self.user_id, self.password)

    def createUI(self):
        self.users_list_label = QtGui.QLabel("Users: ")
        self.users_list_view = QtGui.QListWidget()

        self.add_employee_button = ImageButton(
                                        os.path.join("Images","add.png"),
                                            48,
                                            48,
                                            os.path.join("Images","add_mouseover.png")
                                        )
        self.edit_employee_button = ImageButton(
                                            os.path.join("Images","modify.png"),
                                            48,
                                            48,
                                            os.path.join("Images","modify_mouseover.png")
                                        )

        self.edit_employee_button.setCheckable(True)
        self.add_employee_button.setCheckable(True)
        self.button_group = QtGui.QButtonGroup()
        self.button_group.addButton(self.edit_employee_button)
        self.button_group.addButton(self.add_employee_button)
        self.button_group.setExclusive(True)


        user_list_buttons_layout = QtGui.QHBoxLayout()
        user_list_buttons_layout.addWidget(self.add_employee_button,0)
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
        self.doj_dateedit = FormattedDateEdit()
        self.dol_checkbox = QtGui.QCheckBox("Last Working Date:")
        self.dol_checkbox.setToolTip("Check to mark the LWD of this employee.\nLeave unchecked if the employee is still in the team.")
        self.dol_dateedit = FormattedDateEdit()
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
        self.dop_dateedit = FormattedDateEdit()
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
        self.save_button = QtGui.QPushButton("Save")
        self.reset_button = QtGui.QPushButton("Revert")

        form_buttons_layout = QtGui.QHBoxLayout()
        form_buttons_layout.addStretch(2)
        form_buttons_layout.addWidget(self.reset_password_button,0)
        form_buttons_layout.addWidget(self.save_button,0)
        form_buttons_layout.addWidget(self.reset_button,0)

        self.progress_bar = ProgressBar()
        self.status_label = QtGui.QLabel()

        self.manager_mapping = CopiableQTableWidget(0,0)

        self.manager_name_label = QtGui.QLabel("Reporting Manager:")
        self.manager_name_combobox = QtGui.QComboBox()
        self.manager_effective_date_label = QtGui.QLabel("Revision Date:")
        self.manager_effective_dateedit = FormattedDateEdit()
        self.manager_effective_dateedit.setDate(datetime.date.today())
        self.manager_effective_dateedit.setCalendarPopup(True)
        self.add_new_manager_mapping_row = QtGui.QPushButton("Add or Update")
        self.remove_manager_mapping_row = QtGui.QPushButton("Remove")

        manager_mapping_form = QtGui.QHBoxLayout()
        manager_mapping_form.addWidget(self.manager_name_label,0)
        manager_mapping_form.addWidget(self.manager_name_combobox,2)
        manager_mapping_form.addWidget(self.manager_effective_date_label,0)
        manager_mapping_form.addWidget(self.manager_effective_dateedit,1)
        manager_mapping_form.addWidget(self.add_new_manager_mapping_row,0)
        manager_mapping_form.addWidget(self.remove_manager_mapping_row,0)

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
        self.add_new_manager_mapping_row.clicked.connect(self.addUpdateManagerMapping)
        self.remove_manager_mapping_row.clicked.connect(self.removeManagerMapping)
        self.save_button.clicked.connect(self.saveSelectedEmployee)
        self.reset_button.clicked.connect(self.changedCurrentEmployee)
        self.add_employee_button.clicked.connect(self.changeMode)
        self.edit_employee_button.clicked.connect(self.changeMode)


    def saveSelectedEmployee(self):
        #First, build a dictionary with the former values.
        #Then, build a dictionary with the new values.
        #pass these dictionaries to a MOSES function.
        employee_id = str(self.employee_id_lineedit.text()).strip()
        employee_name = str(self.employee_name_lineedit.text()).strip()
        employee_email_id = str(self.email_lineedit.text()).strip()
        employee_role = str(self.current_role_combobox.currentText()).strip()
        employee_doj = self.doj_dateedit.date().toPyDate()
        employee_dol = self.dol_dateedit.date().toPyDate() if self.dol_checkbox.isChecked() else "NULL"
        employee_dop = self.dop_dateedit.date().toPyDate() if self.dop_checkbox.isChecked() else "NULL"
        employee_former_role = str(self.former_role_combobox.currentText()).strip() if self.dop_checkbox.isChecked() else "NULL"
        employee_oink_access = str(",".join(self.access_combobox.getCheckedItems())) if len(self.access_combobox.getCheckedItems())>0 else "Pork"

        if self.add_employee_button.isChecked():
            mode = 1
        else:
            mode = 0

        if (employee_id in list(self.employees_data["Employee ID"])) and (mode == 1):
            self.alertMessage("Conflicting User ID","The User ID %s already exists in the system. You can't add another user with that Employee ID."%employee_id)
        else:
            print employee_id, list(self.employees_data["Employee ID"])
            employee_dict = {
                            "Employee ID": employee_id,
                            "Name": employee_name,
                            "Email ID": employee_email_id,
                            "Role": employee_role,
                            "DOJ": employee_doj,
                            "DOL": employee_dol,
                            "Date of Promotion": employee_dop,
                            "Former Role": employee_former_role,
                            "OINK Access Level": ",".join(employee_oink_access) if type(employee_oink_access) == list else employee_oink_access
                        }
            success = MOSES.createOrModifyEmployeeDetails(self.user_id, self.password, employee_dict, mode)
            if success:
                self.refreshData()
                self.initialize()
                self.populateEmployeesList()
                self.alertMessage("Success","Successfully completed the operation")
            else:
                self.alertMessage("Failure","Revenge is just the beginning.")


    def changeMode(self):
        if self.add_employee_button.isChecked():
            self.employee_id_lineedit.setEnabled(True)
        elif self.edit_employee_button.isChecked():
            self.employee_id_lineedit.setEnabled(False)


    def removeManagerMapping(self):
        failure = True
        employee_data = self.getEmployeeData(self.getSelectedEmployee())
        if employee_data is not None:
            employee_id = employee_data["Employee ID"]
            reporting_manager_name = str(self.manager_name_combobox.currentText())
            reporting_manager_data = self.getEmployeeData(reporting_manager_name)
            if reporting_manager_data is not None:
                reporting_manager_id = reporting_manager_data["Employee ID"]
                revision_date = self.manager_effective_dateedit.date().toPyDate()
                MOSES.removeFromManagerMapping(self.user_id, self.password, employee_id, reporting_manager_id, revision_date)
                self.changedCurrentEmployee()
                failure = False
            else:
                failure = True
        else:
            failure = True

        if failure:
            self.alertMessage("Failure","Please select a row that you'd like to delete. If you're having problems, select a cell in another row, then select a cell in the row you'd like to delete.")
        else:
            self.alertMessage("Success","Successfully removed a row from the Manager Mapping Table with the selected parameters.")

    def addUpdateManagerMapping(self):
        employee_id = self.getEmployeeData(self.getSelectedEmployee())["Employee ID"]
        reporting_manager_name = str(self.manager_name_combobox.currentText())
        reporting_manager_id = self.getEmployeeData(reporting_manager_name)["Employee ID"]
        revision_date = self.manager_effective_dateedit.date().toPyDate()
        MOSES.addUpdateManagerMapping(self.user_id, self.password, employee_id, reporting_manager_id, revision_date)
        self.changedCurrentEmployee()
        self.alertMessage("Success","Successfully added a row into the Manager Mapping Table with the selected parameters.")


    def populateManagerMappingForm(self, row=None, column=None):
        rows = sorted(set(index.row() for index in self.manager_mapping.selectedIndexes()))
        manager = self.manager_mapping_data.loc[row]
        name = manager["Reporting Manager Name"]
        date_ = manager["Revision Date"]
        if name is not None:
            self.manager_name_combobox.setCurrentIndex(self.manager_name_combobox.findText(name))
        else:
            self.manager_name_combobox.setCurrentIndex(-1)

        if date_ is not None:
            self.manager_effective_dateedit.setDate(date_)
        else:
            self.manager_effective_dateedit.setDate(datetime.date.today())

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
        self.showPage(self.getSelectedEmployee())

    def showPage(self, employee_name):
        employee_data = self.getEmployeeData(employee_name)
        if employee_data is not None:
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
            self.access_combobox.clearSelection()
            access_level = employee_data["Access Level"] if "," not in employee_data["Access Level"] else employee_data["Access Level"].split(",")
            self.access_combobox.select(access_level)

            self.toggleDOP()
            self.toggleDOL()

            self.manager_mapping_data = MOSES.getManagerMappingTable(self.user_id, self.password, employee_data["Employee ID"])
            self.manager_mapping.showDataFrame(self.manager_mapping_data)
            self.manager_mapping.verticalHeader().setStretchLastSection(False)
            self.manager_mapping.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self.manager_mapping.verticalHeader().setVisible(True)

            self.manager_mapping.horizontalHeader().setStretchLastSection(True)
            self.manager_mapping.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self.manager_mapping.horizontalHeader().setResizeMode(QtGui.QHeaderView.Interactive)
            self.manager_mapping.horizontalHeader().setVisible(True)
            self.manager_mapping.horizontalHeader().setStretchLastSection(False)
            self.manager_name_combobox.setCurrentIndex(-1)

    def getSelectedEmployee(self):
        return str(self.users_list_view.currentItem().text())

    def getEmployeeData(self, employee_name):
        location_match = self.employees_data["Name"] == employee_name
        if True in set(location_match):
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
        else:
            data = None
        return data


    def initialize(self):
        employees_list = list(set(self.employees_data["Name"]))
        employees_list.sort()
        self.users_list_view.clear()
        self.users_list_view.addItems(employees_list)
        self.manager_name_combobox.clear()
        self.manager_name_combobox.addItems(employees_list)
        roles = list(set(self.employees_data["Role"]))
        roles.sort()
        self.current_role_combobox.addItems(roles)
        self.former_role_combobox.addItems(roles)
        self.toggleDOL()
        self.toggleDOP()
        self.manager_name_combobox.setCurrentIndex(-1)
        self.manager_effective_dateedit.setDate(datetime.date.today())
        self.edit_employee_button.setChecked(True)
        self.employee_id_lineedit.setEnabled(False)
        self.users_list_view.setCurrentRow(0)


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
