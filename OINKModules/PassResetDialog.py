#!/usr/bin/python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

import MOSES

class PassResetDialog(QtGui.QDialog):
    def __init__(self, userID, password):
        """Password Reset Dialog."""
        super(PassResetDialog,self).__init__()
        self.userID = userID
        self.password = password
        self.generateWidgets()
        self.createLayouts()
        self.setVisuals()
        self.createEvents()
    
    def generateWidgets(self):
        """Password Reset Dialog."""
        """Method to create the password reset box widgets."""
        self.userIDLabel = QtGui.QLabel("User ID & Name:")
        self.userIDPrintLabel = QtGui.QLabel("%s - %s" %(self.userID,MOSES.getEmpName(self.userID)))
        self.passwordLabel1 = QtGui.QLabel("Enter new password:")
        self.passwordLineEdit1 = QtGui.QLineEdit()
        self.passwordLineEdit1.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLabel2 = QtGui.QLabel("Repeat the password:")
        self.passwordLineEdit2 = QtGui.QLineEdit()
        self.passwordLineEdit2.setEchoMode(QtGui.QLineEdit.Password)
        self.statusLabel = QtGui.QLabel("")
        self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                            QtGui.QDialogButtonBox.Cancel)

    def createLayouts(self):
        """Password Reset Dialog."""
        """Method to set the layout of the password reset box."""
        self.userIDLayout = QtGui.QHBoxLayout()
        self.userIDLayout.addWidget(self.userIDLabel,0)
        self.userIDLayout.addWidget(self.userIDPrintLabel,2)
        self.passwordLayout1 = QtGui.QHBoxLayout()
        self.passwordLayout1.addWidget(self.passwordLabel1,0)
        self.passwordLayout1.addWidget(self.passwordLineEdit1,2)
        self.passwordLayout2 = QtGui.QHBoxLayout()
        self.passwordLayout2.addWidget(self.passwordLabel2,0)
        self.passwordLayout2.addWidget(self.passwordLineEdit2,2)
        self.finalLayout = QtGui.QVBoxLayout()
        self.finalLayout.addLayout(self.userIDLayout)
        self.finalLayout.addLayout(self.passwordLayout1)
        self.finalLayout.addLayout(self.passwordLayout2)
        self.finalLayout.addWidget(self.statusLabel)
        self.finalLayout.addWidget(self.buttons)
        self.setLayout(self.finalLayout)
    
    def setVisuals(self):
        """Password Reset Dialog."""
        """Method to set the visual aspects of the password reset box."""
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.move(500,200)
        self.resize(400,100)
        self.setWindowTitle("OINK Password Reset")
    
    def createEvents(self):
        """Password Reset Dialog."""
        """Method to set the events of the password reset box."""
        self.passwordLineEdit1.textChanged.connect(self.passwordsMatch)
        self.passwordLineEdit2.textChanged.connect(self.passwordsMatch)
        self.buttons.accepted.connect(self.submit)
        self.buttons.rejected.connect(self.reject)
    
    def submit(self):
        """Password Reset Dialog."""
        """Sumbmits the form."""
        if self.resetPassword():
            super(PassResetDialog,self).accept()
    
    def reject(self):
        """Password Reset Dialog."""
        super(PassResetDialog,self).reject()

    def getNewPassword(self):
        """Password Reset Dialog."""
        #print "Trying to return new password %s" %self.newPassword
        return self.newPassword
    
    def passwordsMatch(self):
        """Password Reset Dialog."""
        password1 = str(self.passwordLineEdit1.text())
        password2 = str(self.passwordLineEdit2.text())
        if password1 != password2:
            self.statusLabel.setText("<font color=Red>Passwords do not match!</font>")
            return False
        else:
            self.statusLabel.setText("<font color=Green>Passwords match!</font>")
            self.newPassword = password1
            return True
    
    def resetPassword(self):
        """Password Reset Dialog."""
        if self.passwordsMatch():
            self.newPassword = str(self.passwordLineEdit1.text())
            MOSES.resetOwnPassword(self.userID, self.password, self.newPassword)
            return True
        else:
            self.warningMessage = QtGui.QWidget()
            self.warningMessage.say = QtGui.QMessageBox.question(\
                self.warningMessage,"Password reset failure",\
                "Passwords do not match!",QtGui.QMessageBox.Ok,QtGui.QMessageBox.Ok)
            return False #print error message.
