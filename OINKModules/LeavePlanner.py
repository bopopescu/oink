#!/usr/bin/python2
# -*- coding: utf-8 -*-
from __future__ import division
from PyQt4 import QtGui, QtCore
import OINKMethods as OINKM
import datetime
import math
from FormattedDateEdit import FormattedDateEdit
from CopiableQTableWidget import CopiableQTableWidget
import MOSES

class LeavePlanner(QtGui.QWidget):
    def __init__(self, user_id, password):
        """Leave Planner."""
        super(LeavePlanner, self).__init__()
        self.user_id = user_id
        self.password = password
        self.work_calendar = None
        self.createWidgets()
        self.mapTooltips()
        self.createEvents()
        self.createLayouts()
        self.setVisuals()
        self.start_date_edit.setDate(datetime.date.today())
 
    def createWidgets(self):
        """Leave Planner: Method to create all the necessary widgets for the leave planner class."""
        self.mainLabel = QtGui.QLabel("Apply for Leaves or Relaxation in Work")
        self.dateLabel1 = QtGui.QLabel("Start Date:")
        self.start_date_edit = FormattedDateEdit()
        self.start_date_edit.setMinimumDate(QtCore.QDate(2015,1,1))
        self.start_date_edit.setCalendarPopup(True)
        self.dateLabel2 = QtGui.QLabel("End Date:")
        self.end_date_edit = FormattedDateEdit()
        self.end_date_edit.setMinimumDate(QtCore.QDate(2015,1,1))
        self.end_date_edit.setCalendarPopup(True)
        self.statusLabel = QtGui.QLabel("Working Status:")
        self.statusComboBox = QtGui.QComboBox()
        self.statusComboBox.addItems(["Working","Leave"])
        self.relaxationLabel = QtGui.QLabel("Work Relaxation:")
        self.relaxationSpinBox = QtGui.QSpinBox()
        self.relaxationSpinBox.setRange(0,100)
        self.relaxationSpinBox.setSuffix("%")
        self.commentLabel = QtGui.QLabel("Comments:")
        self.commentLineEdit = QtGui.QLineEdit()
        self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                            QtGui.QDialogButtonBox.Cancel)
        self.work_calendar_table = CopiableQTableWidget(0,0)

    def createLayouts(self):
        """Leave Planner: Method to create layouts."""
        self.datesLayout = QtGui.QHBoxLayout()
        self.datesLayout.addWidget(self.dateLabel1)
        self.datesLayout.addWidget(self.start_date_edit)
        self.datesLayout.addWidget(self.dateLabel2)
        self.datesLayout.addWidget(self.end_date_edit)

        self.statusRelaxLayout = QtGui.QHBoxLayout()
        self.statusRelaxLayout.addWidget(self.statusLabel)
        self.statusRelaxLayout.addWidget(self.statusComboBox)
        self.statusRelaxLayout.addWidget(self.relaxationLabel)
        self.statusRelaxLayout.addWidget(self.relaxationSpinBox)

        self.commentsLayout = QtGui.QHBoxLayout()
        self.commentsLayout.addWidget(self.commentLabel,0)
        self.commentsLayout.addWidget(self.commentLineEdit,3)
        self.advice = QtGui.QTextEdit()
        self.advice.setReadOnly(True)
        self.advice.setText("This tool can be used to apply for leaves. However, once you apply for a leave, you can't change that. Your TL will have to. After applying for a leave, you'll have to inform your TL to approve them, or the leave won't be considered by the application. Same goes for relaxation, however, you can revert back to 0 with relaxation so long as your TL hasn't approved it yet. Also, if you ask for a relaxation of 10%, the server will record this as 0.1, this is normal.")
        self.advice.setMaximumHeight(100)
        self.advice.setStyleSheet("font: 12pt;")

        self.finalLayout = QtGui.QVBoxLayout()
        self.finalLayout.addWidget(self.mainLabel)
        self.finalLayout.addLayout(self.datesLayout)
        self.finalLayout.addLayout(self.statusRelaxLayout)
        self.finalLayout.addLayout(self.commentsLayout)
        self.finalLayout.addWidget(self.buttons)
        self.finalLayout.addWidget(self.work_calendar_table,3)
        self.finalLayout.addWidget(self.advice,0)
    
        self.setLayout(self.finalLayout)

    def mapTooltips(self):
        """Leave Planner: Maps the appropriate tooltips to the input widgets."""
        self.start_date_edit.setToolTip("Select the start date for applying for leaves\nor work relaxation.")
        self.end_date_edit.setToolTip("Select the end date for application.\nIf you want a leave on one day, leave this field as it is.")
        self.statusComboBox.setToolTip("Select whether you are working on this day or if you'd like a leave.")
        self.relaxationSpinBox.setToolTip("Set the box to appropriate relaxation you are awarded.\nIf your TL is allowing you to report 80%% for the day, set this box to 20%%.")
        self.commentLineEdit.setToolTip("Type a reason why you require this leave or relaxation for future record.")

    def createEvents(self):
        """Leave Planner: Method to map events."""
        self.start_date_edit.dateChanged.connect(self.limitEndDate)
        self.start_date_edit.dateChanged.connect(self.updateWorkCalendar)
        self.end_date_edit.dateChanged.connect(self.updateWorkCalendar)
        self.buttons.accepted.connect(self.submit)
        self.buttons.rejected.connect(self.reject)

    def setVisuals(self):
        """Leave Planner."""
        self.resize(300,100)
        self.center()
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.setWindowTitle("Leave and Work Relaxation")
        self.show()

    def center(self):
        """Leave Planner."""
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def limitEndDate(self):
        """Leave Planner: Method to limit the end date's minimum value to the start date."""
        self.end_date_edit.setMinimumDate(self.start_date_edit.date())

    def submit(self):
        """Leave Planner: Method to send the request to the work calendar table."""
        startDate = self.start_date_edit.date().toPyDate()
        endDate = self.end_date_edit.date().toPyDate()
        status = str(self.statusComboBox.currentText())
        relaxation = self.relaxationSpinBox.value() #Test this.
        relaxation = float(relaxation)/100.00
        comment = str(self.commentLineEdit.text())

        dates_list = [startDate, endDate]
        name = MOSES.getEmpName(self.user_id)

        self.alertMessage("Please Wait","This process could take a while, and OINK will appear like it has hung. Rest assured that it's running in the background. Please be patient, %s."%name)
        success = MOSES.askForModWorkCalendar(self.user_id, self.password, dates_list, status, relaxation, comment, name)
        if success:
            self.alertMessage("Success", "Your request has been submitted to the server. Ask your TL to approve the request.")
        else:
            self.alertMessage("Failed", "Your request could not be submitted. Ask your TL to manually mark your leaves in the server.")


    def updateWorkCalendar(self):
        self.work_calendar_table.showDataFrame(None)
        filter_dict = {
                        "Dates": [self.start_date_edit.date().toPyDate(), self.end_date_edit.date().toPyDate()],
                        "Employee IDs": [self.user_id]
                        }
        self.work_calendar = MOSES.getWorkCalendarFor(self.user_id, self.password, filter_dict)
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
        self.work_calendar_table.showDataFrame(self.work_calendar, highlight_rules)

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    def reject(self):
        """Leave Planner: Method to close the dialog box."""
        self.close()

