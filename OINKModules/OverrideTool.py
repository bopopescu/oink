from __future__ import division
import os
import datetime
import sys

from PyQt4 import QtGui, QtCore

import MOSES
import OINKMethods as OINKM
from FSNTextEdit import FSNTextEdit
from FormattedDateEdit import FormattedDateEdit
from CopiableQTableWidget import CopiableQTableWidget

class OverrideTool(QtGui.QWidget):
    """Opens an override dialog."""
    def __init__(self, user_id, password):
        """"""
        super(OverrideTool, self).__init__()
        self.user_id = user_id
        self.password = password
        self.getOverrideTable()
        self.createUI()
        self.mapEvents()
        self.override_date.setDate(datetime.date.today())
        #self.getFSNs()

    def getOverrideTable(self):
        self.override_table = MOSES.getOverrideTable(self.user_id, self.password)

    def createUI(self):
        self.fsn_text_edit = FSNTextEdit()
        self.override_date = FormattedDateEdit()
        self.override_button = QtGui.QPushButton("Override")
        self.override_comment_label = QtGui.QLabel("Reason:")
        self.override_comment_field = QtGui.QLineEdit()
        self.override_comment_field.setToolTip("Enter a reason for the override here.")
        self.data_tabulator = CopiableQTableWidget()

        column2 = QtGui.QVBoxLayout()
        column2.addStretch(2)
        column2.addWidget(self.override_date, 1)
        column2.addWidget(self.override_button, 1)
        column2.addWidget(self.override_comment_label, 1)
        column2.addWidget(self.override_comment_field, 1)
        column2.addStretch(2)

        options_layout = QtGui.QHBoxLayout()
        options_layout.addWidget(self.fsn_text_edit,2)
        options_layout.addLayout(column2,1)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(options_layout,1)
        layout.addWidget(self.data_tabulator,3)
        
        self.setLayout(layout)

        self.setWindowTitle("Override Tool")
        self.show()

    def mapEvents(self):
        """"""
        self.override_button.clicked.connect(self.createOverride)
        self.override_date.dateChanged.connect(self.changedDate)

    def changedDate(self):
        query_date = self.override_date.date().toPyDate()
        resultant_data_frame = self.override_table[self.override_table["Override Date"] == query_date]
        self.showDataFrame(resultant_data_frame)

    def showDataFrame(self, data_frame):
        self.data_tabulator.showDataFrame(data_frame)
        self.data_tabulator.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.data_tabulator.verticalHeader().setStretchLastSection(False)
        self.data_tabulator.verticalHeader().setVisible(True)

        self.data_tabulator.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.data_tabulator.horizontalHeader().setStretchLastSection(False)
        self.data_tabulator.horizontalHeader().setVisible(True)

    def createOverride(self):
        """"""
        fsn_list = self.fsn_text_edit.getFSNs()

        if len(fsn_list) > 0:
            comment = str(self.override_comment_field.text()).strip()
            if len(comment)==0:
                self.ask_comment = QtGui.QMessageBox.question(self, 'No reason for override?', "Hi there! You seem to be trying to override an FSN without giving a reason for doing so. Are you sure you want to do that? If you don't want to type a reason, go on ahead. I suggest typing one, because you'll have a neat record of that here.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if self.ask_comment == QtGui.QMessageBox.Yes:
                    allow = True
                else:
                    allow = False
            else:
                allow = True
            if allow:
                self.override_button.setEnabled(False)
                if len(fsn_list)>1:
                    self.alertMessage("Please Wait","Looks like you're trying to override more than one FSN so this step could take a second or a minute, though definitely not more than that. Please wait, and remember, <i>Roma die uno non aedificata est</i>.")
                failures = []
                for FSN in fsn_list:
                    trial_status = MOSES.addOverride(FSN, self.override_date.date().toPyDate(), self.user_id, self.password, comment)
                    if not trial_status:
                        failures.append(FSN)
                if len(failures) == 0:
                    self.alertMessage("Success!","Successfully overrided the requested %d FSN(s)."%len(fsn_list))
                else:
                    self.alertMessage("Failed!","Failed in overriding %d of the %d FSN(s)."%(len(failures),len(fsn_list)))
                self.getOverrideTable()
                self.changedDate()
        else:
            self.alertMessage("No FSNs Provided","You don't seem to have pasted any valid FSNs. Could you try that again?")
        self.override_button.setEnabled(True)
        return True

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    u, p = MOSES.getBigbrotherCredentials()
    test_window = OverrideTool(u, p)
    test_window.show()
    sys.exit(app.exec_())    