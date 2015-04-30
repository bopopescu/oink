from PyQt4 import QtGui, QtCore

import MOSES

class OverrideDialog(QtGui.QDialog):
    """Opens an override dialog."""
    def __init__(self, userID, password):
        """"""
        super(override_dialog, self).__init__()
        self.userID = userID
        self.password = password
        self.create_widgets()
        self.create_layouts()
        self.set_tooltips()
        self.create_events()
        #self.get_FSNs()
        self.create_visuals()

    def create_widgets(self):
        """"""
        self.FSN_Label = QtGui.QLabel("<b>FSN(s):<b>")
        self.FSN_list = QtGui.QTextEdit()
        self.FSN_list.setMinimumWidth(300)
        self.FSN_list.setMinimumHeight(100)
        self.check_button = QtGui.QPushButton("Fetch information")
        self.open_file = QtGui.QPushButton("Get FSNs from file")
        self.override_button = QtGui.QPushButton("Create Overrides for selected FSNs.")
        self.exportData_button = QtGui.QPushButton("Fetch data and\nexport to CSVs")
        self.data_tabulator = QtGui.QTableWidget(0, 0)
        
    def create_layouts(self):
        self.FSN_Buttons_layout = QtGui.QVBoxLayout()
        self.FSN_Buttons_layout.addWidget(self.check_button)
        self.FSN_Buttons_layout.addWidget(self.open_file)
        self.FSN_Buttons_layout.addWidget(self.exportData_button)
       
        self.FSN_layout = QtGui.QHBoxLayout()
        self.FSN_layout.addWidget(self.FSN_Label)
        self.FSN_layout.addWidget(self.FSN_list)
        self.FSN_layout.addLayout(self.FSN_Buttons_layout)
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.FSN_layout)
        self.layout.addWidget(self.data_tabulator)
        
        self.setLayout(self.layout)

    def set_tooltips(self):
        """Maps tooltips to the widgets."""
        self.FSN_list.setToolTip("Paste FSN(s) here.")
        self.check_button.setToolTip("Click to compute.")
        self.open_file.setToolTip("Click to open a file and get FSNs from it.")
        self.exportData_button.setToolTip("Click to save data to file")

    def create_visuals(self):
        """Creates all visual aspects."""
        self.setWindowTitle("Kung Pao! The Override Dialog and FSN Finder.")
        self.move(350, 150)
        self.resize(300, 400)
        self.show()

    def create_events(self):
        """"""
        self.override_button.clicked.connect(self.create_override)
        self.check_button.clicked.connect(self.populate_result_table)

    def get_FSNs(self):
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
        validated_List = filter(OINKM.check_if_FSN, fsnsList)
        """validated_List = []
        for fsn in fsnsList:
            if OINKM.check_if_FSN(fsn):
                validated_List.append(fsn)"""
        return validated_List

    def populate_result_table(self):
        """"""
        fsnsList = self.get_FSNs()
        #print "I got these FSNS:\n", fsnsList
        if fsnsList != None:
            for FSN in fsnsList:
                entries = MOSES.readFromPiggyBank({"FSN": FSN}, self.userID, self.password)
                fsn_dump_entries = MOSES.readFromDump({"FSN": FSN})
                
                if (len(entries) == 0) or (len(fsn_dump_entries) == 0):
                    print "I didn't receive any entries in the piggybank table."

    def create_override(self):
        """"""
        if len(get_FSNs()) > 0:
            for FSN in get_FSNs():
                MOSES.addOverride(FSN, self.date_time_planner.date().toPyDate(), self.userID, self.password)
        else:
            print "OK!" #I STOPPED CODING HERE!
        return True
    