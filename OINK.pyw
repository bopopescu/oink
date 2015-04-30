#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
import datetime

from PyQt4 import QtGui, QtCore
from OINKModules.Pork import Pork
from OINKModules.Vindaloo import Vindaloo
from OINKModules.Bacon import Bacon
from OINKModules.Napoleon import Napoleon

from OINKModules.OINKUIMethods import detectFileOpen, login, showSplashScreen, passwordResetter
from OINKModules import MOSES

def main():
    app = QtGui.QApplication(sys.argv)
    QtGui.qApp.setStyle(QtCore.QString(u'Cleanlooks'))
    #Check if the program is already active or if it wasn't closed properly.
    if not detectFileOpen(): #FIX Use some other method to detect if the process is currently active.
        try:
            login_details = login()
            if login_details is not None:
                userID, password = login_details[0], login_details[1] 
                if password == "password":
                    password = passwordResetter(userID, password)
                user_role = MOSES.getUserRole(userID, password)
                userDict = {
                    "Content Writer": Pork, "Copy Editor": Vindaloo, 
                    "Team Lead": Vindaloo, "Big Brother": Vindaloo, 
                    "Manager": Vindaloo, "Assistant Manager": Vindaloo
                    }
                
                #print "Ok, %s mode" % user_role
                showSplashScreen(app, user_role)

                window = userDict[user_role](userID, password)
                window.setAttribute(QtCore.Qt.WA_QuitOnClose)
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
    else:
        warningMessage = QtGui.QWidget()
        warningMessage.say = QtGui.QMessageBox.question(\
            warningMessage,"Multiple Instances detected.",\
            "Another instance of OINK seems to be open right now. If you're certain that it is not, please contact Admin.",\
            QtGui.QMessageBox.Ok,QtGui.QMessageBox.Ok)
    sys.exit(app.exec_())
    app.exit()

if __name__ == '__main__':
    main()