import sys
import datetime
from PyQt4 import QtGui, QtCore
from Peeves import Peeves


class Seeker(QtGui.QWidget):
    """Seeker class to find FSNs and filter out those which have not been written before.
    """
    def __init__(self, user_id, password):
        super(Seeker, self).__init__()
        self.user_id = user_id
        self.password = password
        self.mode = 1
        self.clip = QtGui.QApplication.clipboard()
        self.peeves = Peeves(user_id, password)
        self.createUI()
        self.createEvents()

    def createUI(self):
        self.fsns_label = QtGui.QLabel("FSNs:")
        self.fsns_text_edit = QtGui.QTextEdit()
        self.fsns_text_edit.setToolTip("Paste a list of FSNs here. The FSNs can be separated by a comma or a new line.")
        self.mode_label = QtGui.QLabel("Mode")
        self.mode_combo_box = QtGui.QComboBox()
        self.mode_combo_box.addItems(["Show All Data", "Show Only Unreported FSNs"])
        self.output_table = QtGui.QTableWidget(0,0)
        self.progress_bar = QtGui.QProgressBar()
        progress_bar_style = """
            .QProgressBar {
                 text-align: center;
             }"""
        self.progress_bar.setStyleSheet(progress_bar_style)
        #self.processing_information = QtGui.QLabel("")
        self.fetch_data_button = QtGui.QPushButton("Fetch Data")
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.fsns_label, 0, 0, 2, 1)
        self.layout.addWidget(self.fsns_text_edit, 0, 1, 2, 2)
        self.layout.addWidget(self.mode_label, 2, 0)
        self.layout.addWidget(self.mode_combo_box, 2, 1)
        self.layout.addWidget(self.fetch_data_button, 2, 2)
        self.layout.addWidget(self.output_table, 3, 0, 3, 3)
        self.layout.addWidget(self.progress_bar, 6, 0, 1, 3)
        #self.layout.addWidget(self.processing_information, 7, 0, 3, 1)
        self.setLayout(self.layout)
        self.setWindowTitle("Seeker: Lardo Suilla Pervia Faciunt.")
        self.show()

    def createEvents(self):
        """"""
        self.mode_combo_box.currentIndexChanged.connect(self.changeMode)
        self.fetch_data_button.clicked.connect(self.fetchData)
        self.peeves.sendProgress.connect(self.displayProgress)
        #self.peeves.sendRow.connect(self.displayFSNs)
        self.peeves.sendData.connect(self.populateTable)
    
    def fetchData(self):
        fsns = str(self.fsns_text_edit.toPlainText()).strip().split("\n")
        fsns = ",".join(fsns)
        fsns.replace('"',"")
        self.fsns_text_edit.setText(fsns)
        fsns = str(self.fsns_text_edit.toPlainText()).strip().split(",")
        self.peeves.fetchData(fsns, self.mode)
        #print len(fsns)

    def populateTable(self, fsn_data):
        #print "Populating the table!"
        self.output_table.setSortingEnabled(False)
        table_headers = [
            "FSN",
            "Status",
            "Description Type",
            "Writer ID",
            "Writer Name",
            "Article Date",
            "Database table",
            "BU",
            "Super-Category",
            "Category",
            "Sub-Category",
            "Vertical",
            "Brand",
            "Item ID"
            ]
        #print table_headers
        rows = len(fsn_data)
        columns = len(table_headers)
        self.output_table.setRowCount(rows)
        self.output_table.setColumnCount(columns)
        row_counter = 0

        for each_fsn in fsn_data:
            column_counter = 0
#            self.output_table.addRow(row_counter)
            for key in table_headers:
                item = QtGui.QTableWidgetItem(str(each_fsn[key]))
                self.output_table.setItem(row_counter, column_counter, item)
                column_counter += 1
            row_counter += 1
        self.output_table.setHorizontalHeaderLabels(table_headers)
        self.output_table.setSortingEnabled(True)
        self.output_table.sortItems(1)
        self.output_table.resizeColumnsToContents()
        self.output_table.resizeRowsToContents()
        #print fsn_data
    
    def displayProgress(self, done, total, eta):
        done, total, eta
        progress = float(done)/float(total)
        if done < total:
            self.progress_bar.setFormat("Getting FSN Data. Finished %d of %d. ETA: %s" %(done, total, eta))
        else:
            self.progress_bar.setFormat("Completed fetching FSN Data")
        self.progress_bar.setValue(int(progress*100))
    
    def changeMode(self):
        self.mode = self.mode_combo_box.currentIndex() + 1
        #print self.mode

if __name__ == "__main__":
    import MOSES
    app = QtGui.QApplication([])
    u, p = MOSES.getBigbrotherCredentials()
    seeker = Seeker(u, p)
    sys.exit(app.exec_())
