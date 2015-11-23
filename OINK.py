#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
import datetime
import time
import ctypes

from PyQt4 import QtGui, QtCore
#Pyinstaller troubleshooting imports.
import pandas
import matplotlib
import PIL
import pygame
import os
import six
import Tkinter
import FixTk
#essentials.
from OINKModules.Pork import Pork
from OINKModules.Vindaloo import Vindaloo
from OINKModules.Bacon import Bacon
from OINKModules.OINKUIMethods import detectFileOpen, login, showSplashScreen, passwordResetter
from OINKModules import MOSES
from OINKModules.OINKChooser import OINKChooser
from OINKModules.OINKLoader import OINKLoader

def main():
    try:
        from OINKModules.Registron import Registron
        registron = Registron()
    except Exception, e:
        print repr(e)
        pass
    app = QtGui.QApplication(sys.argv)
    QtGui.qApp.setStyle(QtCore.QString(u'Plastique'))
    #Check if the program is already active or if it wasn't closed properly.
    tempWidget = QtGui.QWidget()
    tempWidget.setAttribute(QtCore.Qt.WA_QuitOnClose)
    need_waiting = False
    try:
        login_details = login()
        if login_details is not None:
            user_id, password = login_details[0], login_details[1] 
            if password == "password":
                tempWidget = QtGui.QWidget()
                tempWidget.setAttribute(QtCore.Qt.WA_QuitOnClose)
                QtGui.QMessageBox.about(tempWidget,"Please Change Your Password","Your TL appears to have reset your password. Please change it.")
                password = passwordResetter(user_id, password)
            oink_loader = OINKLoader(user_id, password)
            app.installEventFilter(oink_loader)
            oink_loader.setAttribute(QtCore.Qt.WA_QuitOnClose)
            need_waiting = True
        else:
            QtGui.QMessageBox.about(tempWidget,"Bye","Thats all, folks!")

    except Exception, e:
        error = repr(e)
        timestamp = str(datetime.datetime.now())
        print "Time: %s, Error: %s" %(timestamp, error)
        tempWidget = QtGui.QWidget()
        QtGui.QMessageBox.about(tempWidget,"Error","There has been an error. Please contact BigBrother.\nError:%s" % error)
        raise
    if need_waiting:
        sys.exit(app.exec_())
    else:
        sys.exit()
    #print "Exiting now."

if __name__ == '__main__':
    main()
