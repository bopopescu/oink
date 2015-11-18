from __future__ import division
import math
import os
import sys
import datetime
import time
import random

from PyQt4 import QtGui, QtCore
from ProgressBar import ProgressBar
from Pork import Pork
from Vindaloo import Vindaloo
from Bacon import Bacon
from IncredibleBulk import IncredibleBulk

import MOSES

class OINKChooser(QtGui.QWidget):
    def __init__(self, user_id, password, oink_widget_list, category_tree, employees_list, brands_list):
        super(OINKChooser, self).__init__()
        self.user_id, self.password = user_id, password
        self.category_tree = category_tree
        self.employees_list = employees_list
        self.brands_list = brands_list
        self.createUI(oink_widget_list)
        self.mapEvents()

    def createUI(self, oink_widget_list):
        self.label = QtGui.QLabel("Choose A Widget:")
        self.combo_box_widgets = QtGui.QComboBox()
        self.combo_box_widgets.addItems(oink_widget_list)
        self.button = QtGui.QPushButton("Launch")

        final_layout = QtGui.QHBoxLayout()
        final_layout.addWidget(self.label)
        final_layout.addWidget(self.combo_box_widgets)
        final_layout.addWidget(self.button)
        final_page = QtGui.QWidget()
        final_page.setLayout(final_layout)

        self.progress_bar = ProgressBar()
        self.message = QtGui.QLabel("Loading.....")
        loading_layout = QtGui.QVBoxLayout()
        loading_layout.addWidget(self.progress_bar)
        loading_layout.addWidget(self.message)
        loading_page = QtGui.QWidget()
        loading_page.setLayout(loading_layout)

        self.stacked_widget = QtGui.QStackedWidget()
        self.stacked_widget.addWidget(final_page)
        self.stacked_widget.addWidget(loading_page)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)
        self.setWindowTitle("OINK Widget Chooser")
        self.show()

    def mapEvents(self):
        self.button.clicked.connect(self.launchChosenWidget)

    def launchChosenWidget(self):
        chosen_widget = str(self.combo_box_widgets.currentText())
        if chosen_widget.upper() == "PORK":
            self.pork_window = Pork(self.user_id, self.password, self.category_tree, self.brands_list)
        elif chosen_widget.upper() == "VINDALOO":
            self.vindaloo_window = Vindaloo(self.user_id, self.password, self.category_tree, self.employees_list, self.brands_list)
        elif chosen_widget.upper() == "BACON":
            self.bacon_window = Bacon(self.user_id, self.password, self.category_tree)
        else:
            self.alertMessage("Error","%s is not a valid option."%chosen_widget)

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(title, message)

    def showProgress(self, progress, message):
        self.progress_bar.setValue(progress)
        self.message.setText(message)

    def turnPage(self, category_tree):
        self.category_tree = category_tree
        self.stacked_widget.setCurrentIndex(1)