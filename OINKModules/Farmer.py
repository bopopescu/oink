import sys
import datetime
import pandas
from PyQt4 import QtGui, QtCore
import MOSES
import OINKMethods as OINKM
class Farmer(QtGui.QWidget):
    def __init__(self, user_id, password):
        super(Farmer, self).__init__()
        self.user_id = user_id
        self.password = password
        self.createUI()
        self.createEvents()
        self.category_tree = MOSES.getCategoryTree(self.user_id, self.password)
        self.populateCategory()
        self.populateTypeSource()
        self.populateHeadCountTable()

    def createUI(self):
        minimum_width = 200
        self.week_dates_label = QtGui.QLabel("Week Dates:")
        self.week_start_dateedit = QtGui.QDateTimeEdit()
        self.week_start_dateedit.setMinimumDate(QtCore.QDate(2015,1,1))
        self.week_start_dateedit.setMinimumWidth(minimum_width)
        self.week_start_dateedit.setDate(datetime.date.today())
        self.week_start_dateedit.setCalendarPopup(True)
        self.week_start_dateedit.setDisplayFormat("MMMM dd, yyyy")
        self.week_end_dateedit = QtGui.QDateTimeEdit()
        self.week_end_dateedit.setMinimumWidth(minimum_width)
        self.start_date = self.week_start_dateedit.date().toPyDate()
        self.end_date = MOSES.getLastWorkingDayOfWeek(self.start_date)
        self.week_end_dateedit.setMinimumDate(self.end_date)
        self.week_end_dateedit.setMaximumDate(self.end_date)
        self.week_end_dateedit.setCalendarPopup(True)
        self.week_end_dateedit.setDisplayFormat("MMMM dd, yyyy")
        self.week_number = OINKM.getWeekNum(self.start_date)
        self.week_number_label = QtGui.QLabel("Week Number:")
        self.week_number_lineedit = QtGui.QLineEdit()
        self.week_number_lineedit.setMinimumWidth(minimum_width)
        self.week_number_lineedit.setText("Week #%d" %self.week_number)
        self.category_label = QtGui.QLabel("Category:")
        self.category_combobox = QtGui.QComboBox()
        self.category_combobox.setMinimumWidth(minimum_width)
        self.super_category_label = QtGui.QLabel("Super-Category:")
        self.super_category_combobox = QtGui.QComboBox()
        self.super_category_combobox.setMinimumWidth(minimum_width)
        self.bu_label = QtGui.QLabel("BU:")
        self.bu_combobox = QtGui.QComboBox()
        self.bu_combobox.setMinimumWidth(minimum_width)
        self.type_label = QtGui.QLabel("Description Type:")
        self.type_combobox = QtGui.QComboBox()
        self.type_combobox.setMinimumWidth(minimum_width)
        self.source_label = QtGui.QLabel("Source:")
        self.source_combobox = QtGui.QComboBox()
        self.source_combobox.setMinimumWidth(minimum_width)
        self.quantity_label = QtGui.QLabel("Quantity:")
        self.quantity_box = QtGui.QSpinBox()
        self.quantity_box.setMinimumWidth(minimum_width)
        self.submit_button = QtGui.QPushButton("Submit")
        self.edit_button = QtGui.QPushButton("Edit")
        self.reset_button = QtGui.QPushButton("Reset")
        self.delete_button = QtGui.QPushButton("Delete")
        self.head_count_table = QtGui.QTableWidget()
        self.progress_bar = QtGui.QProgressBar()
        self.progress_label = QtGui.QLabel()

        self.form_layout = QtGui.QGridLayout()
        self.form_layout.addWidget(self.week_dates_label,0,0)
        self.form_layout.addWidget(self.week_start_dateedit,0,1)
        self.form_layout.addWidget(self.week_end_dateedit,0,2)
        self.form_layout.addWidget(self.week_number_lineedit,0,3)
        self.form_layout.addWidget(self.category_label,1,0)
        self.form_layout.addWidget(self.category_combobox,1,1)
        self.form_layout.addWidget(self.super_category_label,1,2)
        self.form_layout.addWidget(self.super_category_combobox,1,3)
        self.form_layout.addWidget(self.bu_label,2,0)
        self.form_layout.addWidget(self.bu_combobox,2,1)
        self.form_layout.addWidget(self.type_label,2,2)
        self.form_layout.addWidget(self.type_combobox,2,3)
        self.form_layout.addWidget(self.source_label,3,0)
        self.form_layout.addWidget(self.source_combobox,3,1)
        self.form_layout.addWidget(self.quantity_label, 3, 2)
        self.form_layout.addWidget(self.quantity_box, 3, 3)
        self.form_layout.addWidget(self.submit_button,4,0)
        self.form_layout.addWidget(self.edit_button,4,1)
        self.form_layout.addWidget(self.reset_button,4,2)
        self.form_layout.addWidget(self.delete_button,4,3)
        self.form_layout.addWidget(self.head_count_table,5,0,4,4)
        self.form_layout.addWidget(self.progress_bar,9,0,1,4)
        self.form_layout.addWidget(self.progress_label,10,0,1,4)
        self.setLayout(self.form_layout)
        self.show()
        self.setWindowTitle("Farmer: Two legs good, four legs bad.")
    
    def createEvents(self):
        self.week_start_dateedit.dateChanged.connect(self.limitEndDate)
        self.week_start_dateedit.dateChanged.connect(self.putWeekNumber)
        self.reset_button.clicked.connect(self.reset)
        self.submit_button.clicked.connect(self.submit)
        self.delete_button.clicked.connect(self.delete)
        self.edit_button.clicked.connect(self.edit)
        #self.sub_category_combobox.currentIndexChanged.connect(self.populateCategory)
        self.category_combobox.currentIndexChanged.connect(self.populateSuperCategory)
        self.super_category_combobox.currentIndexChanged.connect(self.populateBU)
    
    def limitEndDate(self):
        self.start_date = self.week_start_dateedit.date().toPyDate()
        self.end_date = MOSES.getLastWorkingDayOfWeek(self.start_date)
        self.week_end_dateedit.setMinimumDate(self.end_date)
        self.week_end_dateedit.setMaximumDate(self.end_date)
        
    def putWeekNumber(self):
        self.week_number = OINKM.getWeekNum(self.start_date)
        self.week_number_lineedit.setText("Week #%d" %self.week_number)

    def submit():
        print "Event triggered successfully."
    def reset():
        print "Event triggered successfully."
    def edit():
        print "Event triggered successfully."
    def delete():
        print "Event triggered successfully."
    def populateHeadCountTable(self):
        print "Event triggered successfully."
    def displayProgress(self):
        print "Event triggered successfully."
    def displayMessage(self):
        print "Event triggered successfully."
    def getDataDict(self):
        print "Event triggered successfully."
    def populateCategory(self):
        self.category_combobox.clear()
        self.categories = list(set(self.category_tree["Category"]))
        self.categories.sort()
        self.category_combobox.addItems(self.categories)
    
    def populateSuperCategory(self):
        self.super_category_combobox.clear()
        self.category = str(self.category_combobox.currentText())
        filtered_category_tree = self.category_tree.loc[self.category_tree['Category'] == self.category]
        self.super_categories = list(set(filtered_category_tree["Super-Category"]))
        self.super_categories.sort()
        self.super_category_combobox.addItems(self.super_categories)
    
    def populateBU(self):
        self.bu_combobox.clear()
        self.super_category = str(self.super_category_combobox.currentText())
        filtered_category_tree = self.category_tree.loc[self.category_tree['Super-Category'] == self.super_category]
        self.bus = list(set(filtered_category_tree["BU"]))
        self.bus.sort()
        self.bu_combobox.addItems(self.bus)
    
    def populateTypeSource(self):
        self.type_combobox.clear()
        self.type_combobox.addItems(["Regular Description","SEO","Rich Product Description"])
        self.source_combobox.clear()
        self.source_combobox.addItems(["Inhouse","Outsourced"])


if __name__ == "__main__":
    app = QtGui.QApplication([])
    u, p = MOSES.getbbc()
    farmer = Farmer(u,p)
    sys.exit(app.exec_())



