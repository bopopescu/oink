#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import datetime
from PyQt4 import QtGui, QtCore
import OINKMethods as OINKM
import MOSES
#from UsersThread import UsersThread

class LogInDialog(QtGui.QDialog):

    def __init__(self):
        """Login Dialog"""
        super(LogInDialog, self).__init__()
        self.generateWidgets()
        self.createVisuals()
        self.refresh()
        self.createLayouts()
        self.mapTooltips()
        self.createActions()


    def generateWidgets(self):
        """Login Dialog"""
        self.loginLabel = QtGui.QLabel("User ID:")
        self.loginLineEdit = QtGui.QLineEdit()
        self.loginLineEdit.setToolTip("Enter your user ID here. Your user ID is your Flipkart employee ID.")
        self.passwordLabel = QtGui.QLabel("Password:")
        self.passwordLineEdit = QtGui.QLineEdit()
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setToolTip("Enter your password here.")
        self.hostLabel = QtGui.QLabel("Host ID:")
        self.hostLineEdit = QtGui.QLineEdit()
        hostID = MOSES.getHostID()
        self.hostLineEdit.setText(hostID)
        self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                            QtGui.QDialogButtonBox.Cancel)       

    def refresh(self):
        user_ids = []
        #First attempt to get the user data from the cache.
        if not os.path.exists("cache"):
            os.makedirs("path")
        if os.path.exists(os.path.join("cache","users_list.txt")):
            user_ids = open(os.path.join("cache","users_list.txt")).read().split(",")
            file_exists = True
            cache_retrieval_success = len(user_ids)>0
        else:
            file_exists = False
            cache_retrieval_success = False
        retrieval_success = cache_retrieval_success
        #If the cache data isn't valid, or if the cache file doesnt' exist:
        if (not cache_retrieval_success) or (not file_exists):
            u, p = MOSES.getBigbrotherCredentials()
            user_ids, connection_success = MOSES.getUsersList(u, p, datetime.datetime.now())
            if connection_success:
                cached_file_handler = open(os.path.join("cache","users_list.txt"),"w")
                if not os.path.exists("cache"):
                    os.makedirs("cache")
                    users = ",".join(user_ids)
                    cached_file_handler.write(users)
                    cached_file_handler.close()
                retrieval_success = True
        if retrieval_success:
            user_completer = QtGui.QCompleter(user_ids)
            self.loginLineEdit.setCompleter(user_completer)
        else:
            if not connection_success:
                message = "Host is unreachable."
            elif not cache_retrieval_success:
                message = "The cached file doesn't have any entries, or it doesn't exist."
            else:
                message = "Unknown error"
            self.alertMessage("User List Retrieval Error","There was a problem retrieving a list of users: {0}".format(message))
    
    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    def createLayouts(self):
        """Login Dialog"""
        self.IDLayout = QtGui.QHBoxLayout()
        self.IDLayout.addWidget(self.loginLabel,1)
        self.IDLayout.addWidget(self.loginLineEdit,2)
        self.passLayout = QtGui.QHBoxLayout()
        self.passLayout.addWidget(self.passwordLabel,1)
        self.passLayout.addWidget(self.passwordLineEdit,2)
        self.hostIDLayout = QtGui.QHBoxLayout()
        self.hostIDLayout.addWidget(self.hostLabel)
        self.hostIDLayout.addWidget(self.hostLineEdit)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.IDLayout)
        self.layout.addLayout(self.passLayout)
        self.layout.addLayout(self.hostIDLayout)
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def createVisuals(self):
        """Login Dialog"""
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.move(500,200)
        self.resize(200,100)
        self.setWindowTitle("OINK Login")

    def getUserDetails(self):
        """Login Dialog"""
        userID = str(self.loginLineEdit.text()).strip()
        password = str(self.passwordLineEdit.text()).strip()
        return userID, password
        
    def createActions(self):
        """Login Dialog"""
        self.buttons.accepted.connect(self.submit)
        self.buttons.rejected.connect(self.reject)

    def mapTooltips(self):
        """Login Dialog"""
        self.loginLineEdit.setToolTip("Enter your login ID here.\nIt is your Flipkart employee ID.\nIt is not your e-mail or LDAP ID.")
        self.passwordLineEdit.setToolTip("Enter your password here. If it's your first time logging in, the password is 'password'.\nIn case you have forgotten your password, ask your TL to reset your password.")
        self.hostLineEdit.setToolTip("Do not change this field unless otherwise instructed by your TL or by the Admin.")

    def reject(self):
        """Login Dialog"""
        super(LogInDialog, self).reject()

    def closeEvent(self, e):
        super(LogInDialog, self).closeEvent(e)

    def validateUserID(self):
        """Login Dialog"""
        userID, password = self.getUserDetails()
        if userID == "bigbrother":
            self.warningMessage = QtGui.QWidget()
            continue_as_admin = QtGui.QMessageBox.question(\
                    self.warningMessage,"Use Big Brother Credentials?",\
                    "Are you sure you want to use the Bigbrother Credentials?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if continue_as_admin == QtGui.QMessageBox.Yes:
                return MOSES.checkPassword(userID,password)[0]
            else:
                return False
        else:
            return MOSES.checkPassword(userID,password)[0]

    
    def submit(self):
        """Login Dialog.
        This method first detects if the host ID has been altered.
        Then, it validates the host ID and moves on to validate the login credentials.
    """
        hostID = str(self.hostLineEdit.text())
        if MOSES.detectChangeInHost(hostID):
            MOSES.changeHostID(hostID)
        if MOSES.checkHostID(hostID):
            if self.validateUserID():
                super(LogInDialog,self).accept()
            else:
                self.warningMessage = QtGui.QWidget()
                self.warningMessage.say = QtGui.QMessageBox.question(\
                    self.warningMessage,"Login failure",\
                    "The password and user ID do not match: thou shall not pass!",QtGui.QMessageBox.Ok,QtGui.QMessageBox.Ok)
        else:
            self.warningmessage = QtGui.QWidget()
            self.warningmessage.say = QtGui.QMessageBox.question(self.warningmessage, "Error with host ID!", "The host seems to be unreachable. Please contact Admin.", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
