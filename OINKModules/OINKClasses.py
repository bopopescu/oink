#!/usr/bin/python2
# -*- coding: utf-8 -*-

#OINKClasses
#Contains the EfficiencyCalculator, the Calculator Row, the PORKWindow, 
#VINDALOOWindow, BACONWindow classes.

__version__ = "1.0 - MOSES"
__DocString__ = """
*************************
P.O.R.K. - O.I.N.K. Report Management System
P.O.R.K. - PiggyBank Organizer and Relay Konsole
P.O.R.K. and the O.I.N.K. report management system were developed by 
Vinay Keerthi K. T. for the Flipkart Internet Private Limited Content Team.
They were developed primarily over a period of three months.

Coder Note:

Read the Change Log text file for more information.

This code is pridominantly written in accordance with PEP 8 and PEP 20 guidelines, the
guidelines otherwise known as the Zen of Python.
*************************
"""

#import required modules

import os
import sys 
import itertools
import threading
from glob import glob
from datetime import datetime

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt

import OINKMethods as OINKM
import MOSES
from FilterBox import FilterBox

def showSplashScreen(app, user_role, prank = False):
        # Create and display the splash screen
        if prank:
            image = 'Images\luuv.jpg'
        else:
            userDict = {"Content Writer": 'Images\PORK.png', "Copy Editor": 'Images\BACON.png', "Team Leader": 'Images\Vindaloo.png', "Big Brother": "Images\VINDALOO.png"}
            image = userDict[user_role]

        splash_pix = QtGui.QPixmap(image)
        splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        app.processEvents()
        time.sleep(2)

def brotherEyeOpen():
        if os.path.isfile("CSVs\BrotherEye.omacs"):
            brotherEye = file("CSVs\BrotherEye.omacs", "w")
            brotherEye.truncate()
            brotherEye.write("PORK Version: %s\nFile Open\nTime:%s"%(__version__,datetime.now()))
        else:
            brotherEye = file("CSVs\BrotherEye.omacs","w")
            brotherEye.write("PORK Version: %s\nFile Open\nTime:%s"%(__version__,datetime.now()))
        brotherEye.close()

def brotherEyeClose():
        if os.path.isfile("CSVs\BrotherEye.omacs"):
            brotherEye = file("CSVs\BrotherEye.omacs", "w")
            brotherEye.truncate()
            brotherEye.write("PORK Version: [version]%s[/version]\nFile Closed\nTime:[ctime]%s[/ctime]"%(__version__,datetime.now()))
        else:
            brotherEyeFile = file("CSVs\BrotherEye.omacs","w")
            brotherEye.write("PORK Version: %s\nFile Closed\nTime:%s"%(__version__,datetime.now()))

def brotherEyeFileModified(fsnData,date):
        if os.path.isfile("CSVs\BrotherEye.1984"):
            brotherEyeModificationTracker = file("CSVs\BrotherEye.1984","a")
            brotherEyeModificationTracker.write("\n[number]%d[/number] FSNs completed for [date]%s[/date] at [time]%s[/time]." % (fsnData,date,datetime.now()))
        else:
            brotherEyeModificationTracker = file("CSVs\BrotherEye.1984","a")
            brotherEyeModificationTracker.write("\n[number]%d[/number] FSNs completed for [date]%s[/date] at [time]%s[/time]." % (fsnData,date,datetime.now()))
        brotherEyeModificationTracker.close()

def detectFileOpen():
    if os.path.isfile("CSVs\BrotherEye.omacs"):
        brotherEyeFileContents = file("CSVs\BrotherEye.omacs","rb").read()
        #print brotherEyeFileContents.find("Open")
        if brotherEyeFileContents.find("Open") == -1:
            return False
        else:
            return True
    else:
        return False

def login():
    """Opens a login dialog and returns the username and password."""
    userID = 0
    password = 0
    success = False
    loginPrompt = LogInDialog()
    if loginPrompt.exec_():
        #print "woot!"
        userID, password2 = loginPrompt.getUserDetails()
        #print "%s, %s" %(userID,password2)
        return userID, password2
    else:
        return None

def passwordResetter(userID,password):
    """Dialog resets the password."""
    passwordReset = passResetDialog(userID,password)
    if passwordReset.exec_():
        newPassword = passwordReset.getNewPassword()
        return newPassword