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
    def __init__(self,userid, password):
        """Leave Planner."""
        super(LeavePlanner, self).__init__()
        self.userID = userid
        self.password = password
        self.createWidgets()
        self.mapTooltips()
        self.createEvents()
        self.createLayouts()
        self.setVisuals()
        self.dateLineEdit1.setDate(datetime.date.today())
 
    def createWidgets(self):
        """Leave Planner: Method to create all the necessary widgets for the leave planner class."""
        self.mainLabel = QtGui.QLabel("Apply for Leaves or Relaxation in Work")
        self.dateLabel1 = QtGui.QLabel("Start Date:")
        self.dateLineEdit1 = FormattedDateEdit()
        self.dateLineEdit1.setMinimumDate(QtCore.QDate(2015,1,1))
        self.dateLineEdit1.setCalendarPopup(True)
        self.dateLabel2 = QtGui.QLabel("End Date:")
        self.dateLineEdit2 = FormattedDateEdit()
        self.dateLineEdit2.setMinimumDate(QtCore.QDate(2015,1,1))
        self.dateLineEdit2.setCalendarPopup(True)
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
        self.work_calendar = CopiableQTableWidget(0,0)

    def createLayouts(self):
        """Leave Planner: Method to create layouts."""

        self.datesLayout = QtGui.QHBoxLayout()
        self.datesLayout.addWidget(self.dateLabel1)
        self.datesLayout.addWidget(self.dateLineEdit1)
        self.datesLayout.addWidget(self.dateLabel2)
        self.datesLayout.addWidget(self.dateLineEdit2)

        self.statusRelaxLayout = QtGui.QHBoxLayout()
        self.statusRelaxLayout.addWidget(self.statusLabel)
        self.statusRelaxLayout.addWidget(self.statusComboBox)
        self.statusRelaxLayout.addWidget(self.relaxationLabel)
        self.statusRelaxLayout.addWidget(self.relaxationSpinBox)

        self.commentsLayout = QtGui.QHBoxLayout()
        self.commentsLayout.addWidget(self.commentLabel,0)
        self.commentsLayout.addWidget(self.commentLineEdit,3)

        self.finalLayout = QtGui.QVBoxLayout()
        self.finalLayout.addWidget(self.mainLabel)
        self.finalLayout.addLayout(self.datesLayout)
        self.finalLayout.addLayout(self.statusRelaxLayout)
        self.finalLayout.addLayout(self.commentsLayout)
        self.finalLayout.addWidget(self.buttons)
        self.finalLayout.addWidget(self.work_calendar)
    
        self.setLayout(self.finalLayout)

    def mapTooltips(self):
        """Leave Planner: Maps the appropriate tooltips to the input widgets."""
        self.dateLineEdit1.setToolTip("Select the start date for applying for leaves\nor work relaxation.")
        self.dateLineEdit2.setToolTip("Select the end date for application.\nIf you want a leave on one day, leave this field as it is.")
        self.statusComboBox.setToolTip("Select whether you are working on this day or if you'd like a leave.")
        self.relaxationSpinBox.setToolTip("Set the box to appropriate relaxation you are awarded.\nIf your TL is allowing you to report 80%% for the day, set this box to 20%%.")
        self.commentLineEdit.setToolTip("Type a reason why you require this leave or relaxation for future record.")

    def createEvents(self):
        """Leave Planner: Method to map events."""
        self.dateLineEdit1.dateChanged.connect(self.limitEndDate)
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
        self.dateLineEdit2.setMinimumDate(self.dateLineEdit1.date())

    def submit(self):
        """Leave Planner: Method to send the request to the work calendar table."""
        startDate = self.dateLineEdit1.date().toPyDate()
        endDate = self.dateLineEdit2.date().toPyDate()
        status = str(self.statusComboBox.currentText())
        relaxation = self.relaxationSpinBox.value() #Test this.
        relaxation = float(relaxation)/100.00
        comment = str(self.commentLineEdit.text())

        datesList = OINKM.getDatesBetween(startDate,endDate)
        successes = []
        for each_date in datesList:
            successes.append(MOSES.modWorkingStatus(self.userID, self.password, each_date, status, relaxation, comment))

        if successes.count(False) == 0:
            self.alertMessage("Success", "Your request has been submitted to the server. Ask your TL to approve the request.")
        elif successes.count(True) == 0:
            self.alertMessage("Failed", "Your request could not be submitted. Ask your TL to manually mark your leaves in the server.")
        else:
            self.alertMessage("Partial Success","The server modified the entries for %d dates. It failed for %d dates. Ask your TL to check the Work Calendar on the server."%(successes.count(True),successes.count(False)))


            
    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    def reject(self):
        """Leave Planner: Method to close the dialog box."""
        self.close()

