#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
import datetime
import time
import ctypes

from PyQt4 import QtGui, QtCore

from OINKModules.Pork import Pork
from OINKModules.Vindaloo import Vindaloo
from OINKModules.Bacon import Bacon
from OINKModules.OINKUIMethods import detectFileOpen, login, showSplashScreen, passwordResetter
from OINKModules import MOSES

def main():
    try:
        registron = MOSES.Registron()
    except Exception, e:
        pass
    app = QtGui.QApplication(sys.argv)
    QtGui.qApp.setStyle(QtCore.QString(u'Plastique'))
    #Check if the program is already active or if it wasn't closed properly.
    try:
        login_details = login()
        if login_details is not None:
            userID, password = login_details[0], login_details[1] 
            if password == "password":
                password = passwordResetter(userID, password)
            user_role = MOSES.getUserRole(userID, password)
            userDict = {
                "Content Writer": Pork, 
                "Copy Editor": Vindaloo, 
                "Team Lead": Vindaloo, 
                "Big Brother": Vindaloo,
                "Product Specialist": Vindaloo,
                "Manager": Vindaloo, 
                "Assistant Manager": Vindaloo,
                "Programmer": Pork
                }
            
            #print "Ok, %s mode" % user_role
            splash = showSplashScreen(app, user_role)
            window = userDict[user_role](userID, password)
            window.setAttribute(QtCore.Qt.WA_QuitOnClose)
            app.installEventFilter(window)
            QtGui.QApplication.processEvents()
            splash.finish(window)
        else:
            tempWidget = QtGui.QWidget()
            tempWidget.setAttribute(QtCore.Qt.WA_QuitOnClose)
            QtGui.QMessageBox.about(tempWidget,"Bye","Thats all, folks!")

    except Exception, e:
        error = repr(e)
        timestamp = str(datetime.datetime.now())
        print "Time: %s, Error: %s" %(timestamp, error)
        tempWidget = QtGui.QWidget()
        QtGui.QMessageBox.about(tempWidget,"Error","There has been an error. Please contact BigBrother.\nError:%s" % error)
        raise
    sys.exit(app.exec_())
    app.exit()

if __name__ == '__main__':
    main()