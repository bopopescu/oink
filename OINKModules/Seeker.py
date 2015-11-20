import sys
import os
import datetime
from PyQt4 import QtGui, QtCore
from Peeves import Peeves
from ProgressBar import ProgressBar
from CopiableQTableWidget import CopiableQTableWidget
from ImageButton import ImageButton

class Seeker(QtGui.QWidget):
    """Seeker class to find FSNs or Item_IDs 
    and filter out those which have not been written before.
    """
    def __init__(self, user_id, password):
        super(Seeker, self).__init__()
        self.user_id = user_id
        self.password = password
        self.mode = 0
        self.clip = QtGui.QApplication.clipboard()
        self.peeves = Peeves(user_id, password)
        self.createUI()
        self.createEvents()

    def createUI(self):
        self.fsns_label = QtGui.QLabel("FSNs\Item IDs:")
        self.fsns_text_edit = QtGui.QTextEdit()
        self.fsns_text_edit.setToolTip("Paste a list of FSNs or Item IDs here,\nseparated either by a new line or a comma.")
        self.type_selector = QtGui.QComboBox()
        self.type_selector.addItems(["FSN(s)", "Item ID(s)"])
        self.type_selector.setToolTip("Select the list type. Are you searching by FSNs or Item IDs?")
        self.type_selector.setCurrentIndex(0)
        self.output_table = CopiableQTableWidget(0, 0)
        self.progress_bar = ProgressBar()
        self.fetch_data_button = ImageButton(os.path.join("Images","find.png"),64,64,os.path.join("Images","find_mouseover.png"))
        self.fetch_data_button.setFlat(True)
        form_searcher_layout = QtGui.QVBoxLayout()
        form_searcher_layout.addWidget(self.fsns_label, 0)
        form_searcher_layout.addWidget(self.fsns_text_edit, 2)

        self.seeker_button = ImageButton(os.path.join("Images","seeker.png"),100,100,os.path.join("Images","seeker_mouseover.png"))
        self.seeker_button.setFlat(True)
        self.seeker_button.setToolTip("You're a Wizard, Harry.")
        
        form_options_layout = QtGui.QVBoxLayout()
        form_options_layout.addStretch(1)
        form_options_layout.addWidget(self.seeker_button,1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        form_options_layout.addStretch(2)
        form_options_layout.addWidget(self.type_selector, 0)
        form_options_layout.addWidget(self.fetch_data_button, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)

        form_layout = QtGui.QHBoxLayout()
        form_layout.addLayout(form_searcher_layout, 3)
        form_layout.addLayout(form_options_layout, 0)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(form_layout, 0)
        layout.addWidget(self.output_table, 3)
        layout.addWidget(self.progress_bar, 0)

        self.setLayout(layout)
        self.setWindowTitle("Seeker: The FSN Finding Tool")
        self.setWindowIcon(QtGui.QIcon(os.path.join('Images','PORK_Icon.png')))
        self.show()

    def createEvents(self):
        """"""
        self.fetch_data_button.clicked.connect(self.fetchData)
        self.peeves.sendProgress.connect(self.displayProgress)
        #self.peeves.sendRow.connect(self.displayFSNs)
        self.peeves.sendData.connect(self.populateTable)
    
    def fetchData(self):
        text_edit_contents = str(self.fsns_text_edit.toPlainText()).strip()
        if '"' in text_edit_contents:
            text_edit_contents.replace('"',"")
        if " " in text_edit_contents:
            text_edit_contents.replace(' ', "")
        search_items = list(set(text_edit_contents.split("\n")))
        self.search_type = self.type_selector.currentIndex()
        self.peeves.fetchData(search_items, self.search_type)

    def populateTable(self, fsn_data):
        #print "Populating the table!"
        self.output_table.setSortingEnabled(False)

        table_headers = [
            "FSN",
            "Status",
            "Item ID",
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
            "Brand"
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
        progress = float(done)/float(total)
        if done < total:
            time_string = datetime.datetime.strftime(eta, "%d %B, %H:%M:%S")
            self.progress_bar.setFormat("Getting FSN Data. Finished %d of %d. ETA: %s" %(done, total, time_string))
        else:
            self.progress_bar.setFormat("Completed fetching FSN Data")
        self.progress_bar.setValue(int(progress*100))
    
if __name__ == "__main__":
    import MOSES
    class SoleSeeker(Seeker):
        def __init__(self, user_id, password):
            super(SoleSeeker, self).__init__(user_id, password)
            self.user_id = user_id
            self.password = password

        def keyPressEvent(self, e):
            if (e.modifiers() & QtCore.Qt.ControlModifier):
                if e.key() == QtCore.Qt.Key_C: #copy
                    table_to_copy = self.output_table
                    selected = table_to_copy.selectedRanges()
                    s = '\t'+"\t".join([str(table_to_copy.horizontalHeaderItem(i).text()) for i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1)])
                    s = s + '\n'

                    for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
                        s += str(r+1) + '\t' 
                        for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                            try:
                                s += str(table_to_copy.item(r,c).text()) + "\t"
                            except AttributeError:
                                s += "\t"
                        s = s[:-1] + "\n" #eliminate last '\t'
                    self.clip.setText(s)
    app = QtGui.QApplication([])
    u, p = MOSES.getBigbrotherCredentials()
    seeker = SoleSeeker(u, p)
    sys.exit(app.exec_())
