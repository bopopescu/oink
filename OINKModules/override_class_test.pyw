import OINKClasses as oc
import MOSES
from PyQt4 import QtGui
import sys

app = QtGui.QApplication(sys.argv)
userID, password = MOSES.getBigbrotherCredentials()
overide = oc.override_dialog(userID, password)
sys.exit(app.exec_())