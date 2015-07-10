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
        self.writers_list = MOSES.getWritersList(self.user_id, self.password)
        self.brands = MOSES.getBrandValues(self.user_id, self.password)
        self.mapEvents()
        self.populateBrand()
        self.populateWriters()
        self.populateCategoryFilters()

    def createUI(self):
        self.instruction_label = QtGui.QLabel("<b>Select filters from the following:</b>")
        self.filter_text_edit = QtGui.QTextEdit()
        self.writers_filter_box = CheckableComboBox("Writers")
        self.description_types_box = CheckableComboBox("Description Types")
        self.source_types_box = CheckableComboBox("Source")
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
        self.end_date_edit.setMaximumDate(datetime.date.today())
        self.all_time_dates = QtGui.QCheckBox("Pull All Time Data")
        self.all_time_dates.setToolTip("Check this box to pull data for the selected filter from all available data.")
        self.piggybank = QtGui.QTableWidget(0,0)
        self.piggybank_summary = QtGui.QTableWidget(0,0)

        self.piggybank_tabs = QtGui.QTabWidget()
        self.piggybank_tabs.addTab(self.piggybank,"Piggy Bank")
        self.piggybank_tabs.addTab(self.piggybank_summary,"Piggy Bank Summary")
        self.reset_button = QtGui.QPushButton("Reset Visible Data")
        self.reset_button.setMinimumWidth(120)
        self.reset_button.setMinimumHeight(20)
        reset_style_string = """
        .QPushButton {
            background-color: red;
            color: white;
            font: 8pt;
        }
        .QPushButton:hover {
            background-color: black;
            color: red;
            font: bold 8pt;
        
        }
        """
        self.reset_button.setStyleSheet(reset_style_string)
        self.pull_button = QtGui.QPushButton("Pull Data")
        self.pull_button.setToolTip("Click here to extract data from the OINK server for the selected filters.")
        self.pull_button.setMinimumWidth(150)
        self.pull_button.setMinimumHeight(30)
        style_string = """
        .QPushButton {
            background-color: #0088D6;
            color: #FDDE2E;
            font: 12pt;
        }
        .QPushButton:hover {
            background-color: #FDDE2E;
            color: #0088D6;
            font: bold 12pt;
        
        }
        """
        self.pull_button.setStyleSheet(style_string)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.instruction_label)
        filters_sub_layouts = [QtGui.QHBoxLayout() for i in range(4)]
        filters_sub_layouts[0].addWidget(self.all_time_dates,0)
        filters_sub_layouts[0].addWidget(self.start_date_edit,0)
        filters_sub_layouts[0].addWidget(self.end_date_edit,0)
        filters_sub_layouts[0].addWidget(self.writers_filter_box,0)
        filters_sub_layouts[1].addWidget(self.description_types_box,0)
        filters_sub_layouts[1].addWidget(self.source_types_box,0)
        filters_sub_layouts[1].addWidget(self.super_categories_filter_box,0)
        filters_sub_layouts[2].addWidget(self.categories_filter_box,0)
        filters_sub_layouts[2].addWidget(self.sub_categories_filter_box,0)
        filters_sub_layouts[2].addWidget(self.verticals_filter_box,0)
        filters_sub_layouts[3].addWidget(self.brands_filter_box,0)
        filters_sub_layouts[3].addWidget(self.reset_button,1)
        filters_sub_layouts[3].addWidget(self.pull_button,2)
        for layout in filters_sub_layouts:
            self.layout.addLayout(layout)
        self.layout.addWidget(self.piggybank_tabs)
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
        self.all_time_dates.stateChanged.connect(self.toggleDates)

    def limitEndDate(self):
        self.end_date_edit.setMinimumDate(self.start_date_edit.date())
        self.end_date_edit.setDate(self.start_date_edit.date())

    def toggleDates(self,state):
        if state == 0:
            self.start_date_edit.setEnabled(True)
            self.end_date_edit.setEnabled(True)
        else:
            self.start_date_edit.setEnabled(False)
            self.end_date_edit.setEnabled(False)

    def populateCategoryFilters(self):
        """This method:
        1. First checks the current filters in the following order BU> Super-Category > Category > Sub-Category > Vertical
        2. If a BU is selected:
            1. It'll populate the Super-Category with the corresponding value(s).

        It should go on and do this for all selected parameters."""
        self.populateBU()
        self.populateSuperCategory()
        self.populateCategory()
        self.populateSubCategory()
        self.populateVertical()


    def populateBU(self):
        self.BUs_filter_box.clear()
        bus = list(set(self.category_tree["BU"]))
        bus.sort()
        self.BUs_filter_box.addItems(bus)

    def populateWriters(self):
        self.writers_filter_box.addItems([writer["Name"] for writer in self.writers_list])

    def populateBrand(self):
        self.brands_filter_box.clear()
        self.brands_filter_box.addItems(self.brands)


    def populateSuperCategory(self):
        self.super_categories_filter_box.clear()
        super_categories = list(set(self.category_tree["Super-Category"]))
        super_categories.sort()
        self.super_categories_filter_box.addItems(super_categories)


    def populateSubCategory(self):
        self.sub_categories_filter_box.clear()
        sub_categories = list(set(self.category_tree["Sub-Category"]))
        sub_categories.sort()
        self.sub_categories_filter_box.addItems(sub_categories)

    def populateCategory(self):
        self.categories_filter_box.clear()
        categories = list(set(self.category_tree["Category"]))
        categories.sort()
        self.categories_filter_box.addItems(categories)
    
    def populateVertical(self):
        self.verticals_filter_box.clear()
        verticals = list(set(self.category_tree["Vertical"]))
        verticals.sort()
        self.verticals_filter_box.addItems(verticals)



if __name__ == "__main__":
    app = QtGui.QApplication([])
    u, p = MOSES.getBigbrotherCredentials()
    piggybank = PiggyBankWithFilter(u,p)
    piggybank.show()
    sys.exit(app.exec_())