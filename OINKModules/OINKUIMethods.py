#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
import sys 
import time
import itertools
import threading
from glob import glob
from datetime import datetime

from PyQt4 import QtCore, QtGui, Qt
from PassResetDialog import PassResetDialog
from LogInDialog import LogInDialog
from FilterBox import FilterBox

import OINKMethods as OINKM
import MOSES

def showSplashScreen(app, user_role, prank = False):
        # Create and display the splash screen
        
        userDict = {"Content Writer": 'Images\PORK.png', "Copy Editor": 'Images\Vindaloo.png', "Team Lead": 'Images\Vindaloo.png', "Manager":'Images\Vindaloo.png', "Assistant Manager": 'Images\Vindaloo.png',  "Big Brother": "Images\VINDALOO.png"}
        image = userDict[user_role]
        
        #image = "Images\OINK.png"
        splash_pix = QtGui.QPixmap(image)
        splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        #splash.showMessage("OINK: In Pigs We Trust")
        splash.setMask(splash_pix.mask())
        splash.show()
        time.sleep(1)
        return splash

def brotherEyeOpen():
        if os.path.isfile("CSVs\BrotherEye.omacs"):
            brotherEye = file("CSVs\BrotherEye.omacs", "w")
            brotherEye.truncate()
            brotherEye.write("PORK Version: %s\nFile Open\nTime:%s"%(OINKM.version(),datetime.now()))
        else:
            brotherEye = file("CSVs\BrotherEye.omacs","w")
            brotherEye.write("PORK Version: %s\nFile Open\nTime:%s"%(OINKM.version(),datetime.now()))
        brotherEye.close()

def brotherEyeClose():
        if os.path.isfile("CSVs\BrotherEye.omacs"):
            brotherEye = file("CSVs\BrotherEye.omacs", "w")
            brotherEye.truncate()
            brotherEye.write("PORK Version: [version]%s[/version]\nFile Closed\nTime:[ctime]%s[/ctime]"%(OINKM.version(),datetime.now()))
        else:
            brotherEyeFile = file("CSVs\BrotherEye.omacs","w")
            brotherEye.write("PORK Version: %s\nFile Closed\nTime:%s"%(OINKM.version(),datetime.now()))

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

def passwordResetter(userID, password):
    """Dialog resets the password."""
    passwordReset = PassResetDialog(userID,password)
    if passwordReset.exec_():
        newPassword = passwordReset.getNewPassword()
        return newPassword