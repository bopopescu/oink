from __future__ import division
import path
import os
import math

import numpy as pd
import pandas as pd
from PyQt4 import QtGui, QtCore

from CheckableComboBox import CheckableComboBox
from CopiableQTableWidget import CopiableQTableWidget
from ImageLabel import ImageLabel
from ImageButton import ImageButton
import MOSES

class UserManager(QtGui.QMainWindow):
    def __init__(self, user_id, password):
        super(UserManager, self).__init__(*args, **kwargs)
        self.user_id, self.password = user_id, password
        self.createUI()
        self.mapEvents()
        self.initialize()

    def createUI(self):
        self.users_list_label = QtGui.QLabel("Users: ")
        self.users_list = QtGui.QListView()
        #get the list of users from MOSES.
        self.reset_password_button = QtGui.QPushButton("Reset Password")
        self.add_user_button = QtGui.QAddUser("")

    def mapEvents(self):
        pass

    def initialize(self):
        pass

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