from PyQt4 import QtGui, QtCore
import sys
import datetime
from PorkKent import PorkKent

class DailyPorker(QtGui.QWidget):
    def __init__(self, user_id, password):
        super(DailyPorker, self).__init__()
        self.user_id, self.password = user_id, password
        self.report_selection_dict = {
                    "Daily": False,
                    "Weekly": False,
                    "Monthly": False,
                    "Quarterly": False,
                    "Half-Yearly": False,
                    "Average": False
        }
        #self.pork_kent = PorkKent(self.user_id, self.password)
        style_string = """
        .QGridLayout, QWidget, .QPushButton, .QLabel, .QCheckBox, .QDateTimeEdit{
            background-color: #0088D6;
            color: white;
            font: 8pt;
        }
        QWidget
        {
            background-color: #0088D6;
            color: black;
            font: 8pt;
        }
        .QPushButton:hover, .QCheckBox:hover {
            background-color: #FDDE2E;
            color: black;
        }

        .QWidget, .QPushButton{
            font: 14pt;    
        }
        """
        #self.setStyleSheet(style_string)
        self.createUI()
        self.center()
        self.setAutoFillBackground(True)
        self.mapEvents()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def createUI(self):
        self.start_date_label = QtGui.QLabel("Select a report date:")
        self.start_date_edit = QtGui.QDateTimeEdit()
        self.start_date_edit.setToolTip("Set the date for which you want to generate the report.")
        self.start_date_edit.setDate(QtCore.QDate(datetime.date.today()))
        self.start_date_edit.setDisplayFormat("MMMM dd, yyyy")
        self.start_date_edit.setMinimumDate(QtCore.QDate(2015,1,1))
        self.start_date_edit.setCalendarPopup(True)
        self.instruction_label = QtGui.QLabel("Select the parameters which need to be pulled:")
        self.daily_check_box = QtGui.QCheckBox("Daily")
        self.daily_check_box.setToolTip("Check this to include the daily efficiency, CFM, GSEO and Stack Rank Index in the compiled report.")
        self.weekly_check_box = QtGui.QCheckBox("Weekly")
        self.weekly_check_box.setToolTip("Check this to include the weekly efficiency, CFM, GSEO and Stack Rank Index in the compiled report.")
        self.monthly_check_box = QtGui.QCheckBox("Monthly")
        self.monthly_check_box.setToolTip("Check this to include the monthly efficiency, CFM, GSEO and Stack Rank Index in the compiled report.")
        self.quarterly_check_box = QtGui.QCheckBox("Quarterly")
        self.quarterly_check_box.setToolTip("Check this to include the Quarterly efficiency, CFM, GSEO and Stack Rank Index in the compiled report.")
        self.half_yearly_check_box = QtGui.QCheckBox("Half-Yearly")
        self.half_yearly_check_box.setToolTip("Check this to include the Half-Yearly efficiency, CFM, GSEO and Stack Rank Index in the compiled report.")
        self.end_date_check_box = QtGui.QCheckBox("Until End Date")
        self.end_date_check_box.setToolTip("Check this to include the average efficiency, CFM, GSEO and Stack Rank Index\nbetween the first date and the end date in the compiled report.")
        self.end_date_edit = QtGui.QDateTimeEdit()
        self.end_date_edit.setToolTip("Select an end date. Only working days will be considered for the calculation.\nThis field will be disabled if the checkbox isn't marked to calculate the average statistics between dates.")
        self.end_date_edit.setDate(QtCore.QDate(datetime.date.today()))
        self.end_date_edit.setDisplayFormat("MMMM dd, yyyy")
        self.end_date_edit.setMinimumDate(QtCore.QDate(datetime.date.today()))
        self.end_date_edit.setReadOnly(True)
        self.end_date_edit.setCalendarPopup(False)

        self.report = QtGui.QTableWidget()
        self.progress_bar = QtGui.QProgressBar()
        self.build_stop_button = QtGui.QPushButton("Build Report")
        self.build_stop_button.setToolTip("Click this button to start building the report")
        self.build_stop_button.setCheckable(True)
        self.status = QtGui.QLabel("I'm a Porkitzer Prize Winning Reporter.")

        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.start_date_label,0,0)
        self.layout.addWidget(self.start_date_edit,0,1)
        self.layout.addWidget(self.instruction_label,1,0,1,3)
        self.layout.addWidget(self.daily_check_box, 2, 0)
        self.layout.addWidget(self.weekly_check_box, 2, 1)
        self.layout.addWidget(self.monthly_check_box,2,2)
        self.layout.addWidget(self.quarterly_check_box, 2, 3)
        self.layout.addWidget(self.half_yearly_check_box, 3, 0)
        self.layout.addWidget(self.end_date_check_box, 3, 1)
        self.layout.addWidget(self.end_date_edit, 3, 2, 1, 2)
        self.layout.addWidget(self.build_stop_button, 4, 1, 1, 2)
        self.layout.addWidget(self.report, 5, 0, 4, 4)
        self.layout.addWidget(self.progress_bar, 10, 0, 1, 4)
        self.layout.addWidget(self.status, 11, 0, 1, 4)
        self.setLayout(self.layout)

    def mapEvents(self):
        print "mapping"
        self.build_stop_button.clicked.connect(self.buildStop)
        self.end_date_check_box.stateChanged.connect(self.toggleEndDate)
        self.start_date_edit.dateChanged.connect(self.limitEndDate)
   
    def buildStop(self):
        if self.build_stop_button.isChecked():
            self.build = True
            self.build_stop_button.setText("Stop Building Report")
            self.build_stop_button.setToolTip("Uncheck this button to stop building the report.")
            report_types = self.getRequiredReportTypes()
        else:
            self.build = False
            self.build_stop_button.setText("Build Report")
            self.build_stop_button.setToolTip("Click this button to start building the report")

    def toggleEndDate(self, state):
        if state == 2:
            self.end_date_edit.setReadOnly(False)
            self.end_date_edit.setCalendarPopup(True)
        else:
            self.end_date_edit.setReadOnly(True)
            self.end_date_edit.setCalendarPopup(False)

    def limitEndDate(self):
        self.end_date_edit.setMinimumDate(self.start_date_edit.date())
        self.end_date_edit.setDate(self.start_date_edit.date())

    def getRequiredReportTypes(self):

        self.report_selection_dict = {
                    "Daily": self.daily_check_box.checkState() == QtCore.Qt.Checked,
                    "Weekly": self.weekly_check_box.checkState() == QtCore.Qt.Checked,
                    "Monthly": self.monthly_check_box.checkState() == QtCore.Qt.Checked,
                    "Quarterly": self.quarterly_check_box.checkState() == QtCore.Qt.Checked,
                    "Half-Yearly": self.half_yearly_check_box.checkState() == QtCore.Qt.Checked,
                    "Average": self.end_date_check_box.checkState() == QtCore.Qt.Checked
        }
        return self.report_selection_dict