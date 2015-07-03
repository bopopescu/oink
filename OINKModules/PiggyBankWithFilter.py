import datetime, os, sys
from PyQt4 import QtGui, QtCore
import MOSES
from CheckableComboBox import CheckableComboBox

class PiggyBankWithFilter(QtGui.QWidget):
    def __init__(self, user_id, password):
        super(PiggyBankWithFilter, self).__init__()
        self.createUI()
        self.user_id, self.password = user_id, password
        self.category_tree = MOSES.getCategoryTree(self.user_id, self.password)
        self.mapEvents()
        self.populateBU()

    def createUI(self):
        self.instruction_label = QtGui.QLabel("Select filters from the following:")
        self.filter_text_edit = QtGui.QTextEdit()
        self.writers_filter_box = CheckableComboBox("Writers")
        self.BUs_filter_box = CheckableComboBox("BUs")
        self.super_categories_filter_box = CheckableComboBox("Super-Categories")
        self.categories_filter_box = CheckableComboBox("Categories")
        self.sub_categories_filter_box = CheckableComboBox("Sub-Categories")
        self.verticals_filter_box = CheckableComboBox("Verticals")
        self.brands_filter_box = CheckableComboBox("Brands")
        self.start_date_edit = QtGui.QDateTimeEdit()
        self.start_date_edit.setDate(QtCore.QDate(datetime.date.today()))
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("MMMM dd, yyyy")
        self.start_date_edit.setMinimumDate(QtCore.QDate(2015,1,1))
        self.end_date_edit = QtGui.QDateTimeEdit()
        self.end_date_edit.setDate(QtCore.QDate(datetime.date.today()))
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("MMMM dd, yyyy")
        self.end_date_edit.setMinimumDate(self.start_date_edit.date().toPyDate())
        
        self.piggybank = QtGui.QTableWidget(0,0)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.instruction_label)
        self.filters_layout = QtGui.QHBoxLayout()
        self.filters_layout.addWidget(self.start_date_edit)
        self.filters_layout.addWidget(self.end_date_edit)
        self.filters_layout.addWidget(self.writers_filter_box)
        self.filters_layout.addWidget(self.BUs_filter_box)
        self.filters_layout.addWidget(self.super_categories_filter_box)
        self.filters_layout.addWidget(self.categories_filter_box)
        self.filters_layout.addWidget(self.sub_categories_filter_box)
        self.filters_layout.addWidget(self.verticals_filter_box)
        self.filters_layout.addWidget(self.brands_filter_box)
        self.layout.addLayout(self.filters_layout)
        self.layout.addWidget(self.piggybank)
        self.setLayout(self.layout)
        self.setWindowTitle("Piggy Bank")
        if "OINKModules" in os.getcwd():
            icon_file_name_path = os.path.join(os.path.join('..',"Images"),'PORK_Icon.png')
        else:
            icon_file_name_path = os.path.join('Images','PORK_Icon.png')
        self.setWindowIcon(QtGui.QIcon(icon_file_name_path))
        self.move(120,100)

    def mapEvents(self):
        self.start_date_edit.dateChanged.connect(self.limitEndDate)

    def limitEndDate(self):
        self.end_date_edit.setMinimumDate(self.start_date_edit.date())
        self.end_date_edit.setDate(self.start_date_edit.date())

    def populateBU(self):
        self.BUs_filter_box.clear()
        bus = list(set(self.category_tree["BU"]))
        bus.sort()
        self.BUs_filter_box.addItems(bus)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    u, p = MOSES.getBigbrotherCredentials()
    piggybank = PiggyBankWithFilter(u,p)
    piggybank.show()
    sys.exit(app.exec_())