#!/usr/bin/python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from PassResetDialog import PassResetDialog
from EfficiencyCalculator import EfficiencyCalculator
from FilterBox import FilterBox
from OINKMethods import version
import MOSES
from datetime import datetime

class DateSelectorWidget(QtGui.QWidget):
    def __init__(self):
        super(QtGui.QWidget , self).__init__()
        self.mode = "Normal"
        self.create_widgets()
        self.create_layout(self.mode)
        self.create_events()
        self.set_tooltips()
        self.set_date_limits()
        self.start_date_picker.setDate(QtCore.QDate(datetime.date(datetime.today())))
        self.limitEndDate()
        self.get_dates()

    def create_widgets(self):
        """date_selector_widget"""
        self.start_date_label = QtGui.QLabel("<b>Select a start date:</b>")
        self.start_date_picker = QtGui.QDateTimeEdit()
        self.start_date_picker.setMinimumWidth(100)
        self.start_date_picker.setMaximumWidth(100)

        self.start_date_picker.setCalendarPopup(True)
        self.end_date_label = QtGui.QLabel("<b>Select an end date:</b>")
        self.end_date_picker = QtGui.QDateTimeEdit()
        self.end_date_picker.setMinimumWidth(100)
        self.end_date_picker.setMaximumWidth(100)
        self.end_date_picker.setCalendarPopup(True)
        #Disable the hidden end date feature for now.
        #self.reveal_end_date_button = QtGui.QPushButton("V")

    def create_layout(self, mode = "Normal"):
        self.date_selector_layout = QtGui.QVBoxLayout()
        self.start_date_layout = QtGui.QHBoxLayout()
        self.start_date_layout.addWidget(self.start_date_label,2)
        self.start_date_layout.addWidget(self.start_date_picker,3)
        #self.start_date_layout.addWidget(self.reveal_end_date_button,1)
        self.end_date_layout = QtGui.QHBoxLayout()
        self.end_date_layout.addWidget(self.end_date_label, 1)
        self.end_date_layout.addWidget(self.end_date_picker, 2)
        #self.mode = mode
        self.date_selector_layout.addLayout(self.start_date_layout)
        self.date_selector_layout.addLayout(self.end_date_layout)
        #self.end_date_label.hide()
        #self.end_date_picker.hide()
        self.setLayout(self.date_selector_layout)

    def create_events(self):
        """date_selector_widget"""
        #self.reveal_end_date_button.clicked.connect(self.expand_dates)
        self.start_date_picker.dateChanged.connect(self.limitEndDate)

    def set_tooltips(self):
        """date_selector_widget"""
        self.start_date_picker.setToolTip("Select a starting date.")
        self.end_date_picker.setToolTip("Select an ending date.")
        #self.reveal_end_date_button.setToolTip("Click to set an ending date.")

    def get_dates(self):
        """date_selector_widget"""
        start_date = self.start_date_picker.date().toPyDate()
        end_date = self.end_date_picker.date().toPyDate()
        return start_date, end_date

    def set_date_limits(self):
        """Sets limits to the date time edits and also sets the format."""
        self.start_date_picker.setDisplayFormat("MMMM dd, yyyy")
        self.start_date_picker.setMinimumDate(QtCore.QDate(2015,1,1))
        self.end_date_picker.setDisplayFormat("MMMM dd, yyyy")

    def expand_dates(self):
        """Reveals the end date options and hides the expansion button."""
        self.reveal_end_date_button.hide()
        self.end_date_label.show()
        self.end_date_picker.show()

    def limitEndDate(self):
        """Leave Planner: Method to limit the end date's minimum value to the start date."""
        self.end_date_picker.setMinimumDate(self.start_date_picker.date())
        self.end_date_picker.setDate(self.start_date_picker.date())
