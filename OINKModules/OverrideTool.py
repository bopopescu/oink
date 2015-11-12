from __future__ import division
import os
import datetime
import sys

from PyQt4 import QtGui, QtCore

import MOSES
import OINKMethods as OINKM
from FSNTextEdit import FSNTextEdit
from FormattedDateEdit import FormattedDateEdit

class OverrideTool(QtGui.QWidget):
    """Opens an override dialog."""
    def __init__(self, user_id, password):
        """"""
        super(OverrideTool, self).__init__()
        self.user_id = user_id
        self.password = password
        self.override_table = MOSES.getOverrideTable(self.user_id, self.password)
        self.createUI()
        self.mapEvents()
        #self.getFSNs()

    def createUI(self):
        """"""
        self.fsn_text_edit = FSNTextEdit()
        self.override_date = FormattedDateEdit()
        self.override_button = QtGui.QPushButton("Create Overrides for selected FSNs.")
        self.data_tabulator = CopiableQTableWidget()
        self.data_tabulator.setDataFrame(self.override_table[self.override_table["Override Date"] == datetime.date.today()])

        column2 = QtGui.QVBoxLayout()
        column2.addStretch(2)
        column2.addWidget(self.override_date, 1)
        column2.addWidget(self.override_button, 1)
        column2.addStretch(2)

        options_layout = QtGui.QHBoxLayout()
        options_layout.addWidget(self.fsn_text_edit,2)
        options_layout.addLayout(column2,1)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(options_layout,1)
        layout.addWidget(self.data_tabulator,3)
       
        self.FSN_layout = QtGui.QHBoxLayout()
        self.FSN_layout.addWidget(self.FSN_Label)
        self.FSN_layout.addWidget(self.FSN_list)
        self.FSN_layout.addLayout(self.FSN_Buttons_layout)
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.FSN_layout)
        self.layout.addWidget(self.data_tabulator)
        
        self.setLayout(self.layout)

        self.FSN_list.setToolTip("Paste FSN(s) here.")
        self.check_button.setToolTip("Click to compute.")
        self.open_file.setToolTip("Click to open a file and get FSNs from it.")
        self.exportData_button.setToolTip("Click to save data to file")

        self.setWindowTitle("Kung Pao! The Override Dialog and FSN Finder.")
        self.move(350, 150)
        self.resize(300, 400)
        self.show()

    def mapEvents(self):
        """"""
        self.override_button.clicked.connect(self.create_override)
        self.check_button.clicked.connect(self.populate_result_table)

    def getFSNs(self):
        """"""
        fsns_as_a_string = str(self.FSN_list.toPlainText()).strip()
        #print fsns_as_a_string
        if "," in fsns_as_a_string:
            fsnsList = fsns_as_a_string.split(",")
        elif r"\n" in fsns_as_a_string:
            fsnsList = fsns_as_a_string.split(r"\n")
        elif " " in fsns_as_a_string:
            fsnsList = fsns_as_a_string.split(" ")
        elif r"\t" in fsns_as_a_string:
            fsnsList = fsns_as_a_string.split(r"\t")
        elif type(fsns_as_a_string) == type(""):
            fsnsList = [fsns_as_a_string]
        validated_list = filter(OINKM.checkIfFSN, fsnsList)

        return validated_list

    def populate_result_table(self):
        """"""
        fsnsList = self.getFSNs()
        #print "I got these FSNS:\n", fsnsList
        if fsnsList != None:
            for FSN in fsnsList:
                entries = MOSES.readFromPiggyBank({"FSN": FSN}, self.user_id, self.password)
                fsn_dump_entries = MOSES.readFromDump({"FSN": FSN})
                
                if (len(entries) == 0) or (len(fsn_dump_entries) == 0):
                    print "I didn't receive any entries in the piggybank table."

    def create_override(self):
        """"""
        if len(getFSNs()) > 0:
            for FSN in getFSNs():
                MOSES.addOverride(FSN, self.date_time_planner.date().toPyDate(), self.user_id, self.password)
        else:
            print "OK!" #I STOPPED CODING HERE!
        return True


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    u, p = MOSES.getBigbrotherCredentials()
    test_window = OverrideTool(u, p)
    test_window.show()
    sys.exit(app.exec_())    