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
        pass
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
            go_forth = False
            if go_forth:
                user_list = MOSES.getEmployeesList(user_id, password, datetime.date.today())
                access_list = list(user_list[user_list["Employee ID"] == user_id]["OINK Access Level"])[0].split(",")
                user_role = list(user_list[user_list["Employee ID"] == user_id]["Role"])[0]
                if len(access_list)>0:
                    userDict = {
                        "Copy Editor": Bacon, 
                        "Team Lead": Vindaloo,
                        "Big Brother": Vindaloo,
                        "Product Specialist": Bacon,
                        "Manager": Vindaloo, 
                        "Assistant Manager": Vindaloo,
                        "Admin": Pork,
                        "Content Writer": Pork
                        }
                    if user_role not in userDict.keys():
                        QtGui.QMessageBox.about(tempWidget,"Unauthorized User","This version of OINK is not coded for use by a %s. If you encounter this message, you're probably trying to use the compiled version of OINK that doesn't need Python. That version was developed for use by writers because it's easier to set up. If you'd like to use the source version instead, follow the initial setup chapter in the documentation."%user_role)
                    else:
                        need_waiting = True
                        splash = showSplashScreen(app, user_role)
                        if len(access_list)>1:
                            window = OINKChooser(user_id, password, access_list)
                        else:
                            window = userDict[user_role](user_id, password)
                        window.setAttribute(QtCore.Qt.WA_QuitOnClose)
                        QtGui.QApplication.processEvents()
                        splash.finish(window)
                else:
                    QtGui.QMessageBox.about(tempWidget,"No Access","You seem to have no access to the OINK Database. Contact your Reporting Manager and ask him or her to grant you access if necessary.")
                    need_waiting = False

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
        print "Looks like an app has opened. I'll wait quietly."
        sys.exit(app.exec_())
    else:
        print "You haven't asked for any app to open, or you've triggered an exit mechanism, so I'm quitting now."
        sys.exit()
    #print "Exiting now."

if __name__ == '__main__':
    main()
