import sys
from PyQt4 import QtGui
import MOSES
class Farmer(QtGui.QWidget):
	def __init__(self, user_id, password):
		super(Farmer, self).__init__()
		self.user_id = user_id
		self.password = password
		self.createUI()
	
	def createUI(self):
		self.week_dates_label = QtGui.QLabel("Week Dates:")
		self.week_start_dateedit = QtGui.QDateTimeEdit()
		self.week_start_dateedit.setCalendarPopup(True)
		self.week_end_dateedit = QtGui.QDateTimeEdit()
		self.week_end_dateedit.setCalendarPopup(True)
		self.week_number_label = QtGui.QLabel("Week Number:")
		self.week_number_lineedit = QtGui.QLineEdit()
		self.sub_category_label = QtGui.QLabel("Sub-Category:")
		self.sub_category_combobox = QtGui.QComboBox()
		self.category_label = QtGui.QLabel("Category:")
		self.category_combobox = QtGui.QComboBox()
		self.super_category_label = QtGui.QLabel("Super-Category:")
		self.super_category_combobox = QtGui.QComboBox()
		self.bu_label = QtGui.QLabel("BU:")
		self.bu_combobox = QtGui.QComboBox()
		self.type_label = QtGui.QLabel("Description Type:")
		self.type_combobox = QtGui.QComboBox()
		self.source_label = QtGui.QLabel("Source:")
		self.source_combobox = QtGui.QComboBox()
		self.quantity = QtGui.QSpinBox()
		self.submit_button = QtGui.QPushButton("Submit")
		self.edit_button = QtGui.QPushButton("Edit")
		self.reset_button = QtGui.QPushButton("Reset")
		self.delete_button = QtGui.QPushButton("Delete")
		self.head_count_table = QtGui.QTableWidget()
		self.progress_bar = QtGui.QProgressBar()
		self.progress_label = QtGui.QLabel()

		self.form_layout = QtGui.QGridLayout()
		self.form_layout.addWidget(self.week_dates_label,0,0,1,2)
		self.form_layout.addWidget(self.week_start_dateedit,0,2)
		self.form_layout.addWidget(self.week_end_dateedit,0,3)
		self.form_layout.addWidget(self.week_number_label,1,0,1,2)
		self.form_layout.addWidget(self.week_number_lineedit,1,2,1,2)
		self.form_layout.addWidget(self.sub_category_label,2,0)
		self.form_layout.addWidget(self.sub_category_combobox,2,1)
		self.form_layout.addWidget(self.category_label,2,2)
		self.form_layout.addWidget(self.category_combobox,2,3)
		self.form_layout.addWidget(self.super_category_label,3,0)
		self.form_layout.addWidget(self.super_category_combobox,3,1)
		self.form_layout.addWidget(self.bu_label,3,2)
		self.form_layout.addWidget(self.bu_combobox,3,3)
		self.form_layout.addWidget(self.type_label,4,0)
		self.form_layout.addWidget(self.type_combobox,4,1)
		self.form_layout.addWidget(self.source_label,4,2)
		self.form_layout.addWidget(self.source_combobox,4,3)
		self.form_layout.addWidget(self.submit_button,5,0)
		self.form_layout.addWidget(self.edit_button,5,1)
		self.form_layout.addWidget(self.reset_button,5,2)
		self.form_layout.addWidget(self.delete_button,5,3)
		self.form_layout.addWidget(self.head_count_table,6,0,4,4)
		self.form_layout.addWidget(self.progress_bar,10,0,1,4)
		self.form_layout.addWidget(self.progress_label,11,0,1,4)
		self.setLayout(self.form_layout)
		self.show()
		self.setWindowTitle("Farmer")

if __name__ == "__main__":
	app = QtGui.QApplication([])
	u, p = MOSES.getbbc()
	farmer = Farmer(u,p)
	sys.exit(app.exec_())



