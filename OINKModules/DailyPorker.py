from __future__ import division

import sys
import math
import datetime

from PyQt4 import QtGui, QtCore

import MOSES

class PorkLane(QtCore.QThread):
    """
    This threaded class emits the daily report data to DailyPorker.
    It works thus:
    1. DailyPorker creates an instance of this thread without a mode.
    2. When the user clicks the Build Report button, Daily Porker sets the mode to the 
        selected parameters and allows PorkLane to run.
    3. PorkLane then sends the built report back to DailyPorker, which displays it.
    """
    sendProgress = QtCore.pyqtSignal(str, datetime.datetime, int, bool)
    sendReport = QtCore.pyqtSignal(list)

    def __init__(self, user_id, password, mode=None):
        super(PorkLane, self).__init__()
        self.user_id = user_id
        self.password = password
        if mode is None:
            self.allowRun = False
            self.mode = []
        else:
            self.allowRun = True
            self.mode = mode
        self.start_date = datetime.date.today()
        self.end_date = datetime.date.today()
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def __del__(self):
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def run(self):
        self.mutex.unlock()
        while True:
            if self.allowRun:
                print """Pork Lane allowed to run!"""
                self.summarize()
        self.mutex.lock()

    def summarize(self):
        """
        1. Get the list of all writers working on the start_date.
        
        2. For each writer, 
            2.1 If the dates are different, get the average efficiency between the two dates.
            2.2 get the efficiency on the end_date.
            2.4 get the efficiency on the week of the end_date.
            2.5 get the effiency on the month of the end_date.
            2.6 get the efficiency on the quarter.
            2.7 get the effiency on the half-year.
        3. Build all this information into a dictionary.
        4. Compile all dictionaries into a list.
        5. Emit the list.
        """
        self.writers = MOSES.getWritersList(self.user_id, self.password, self.start_date)
        self.summary_data = []
        done = 0
        total = len(self.writers)
        self.break_loop = False
        start_time = datetime.datetime.now()
        for writer in self.writers:
            self.writer_id = writer["Employee ID"]
            self.writer_name = writer["Name"]
            self.writer_email = writer["Email ID"]
            success = False
            retry = 0
            while not success:
                try:
                    writer_summary = self.fetchWriterSummary()
                    success = True
                except:
                    retry += 1
                    if retry >5:
                        raise
                    else:
                        pass
            self.summary_data.append(writer_summary)
            done = len(self.summary_data)
            self.sendProgress.emit("Processed data for %s for %s."%(self.writer_name, self.start_date), MOSES.getETA(start_time, done, total), int(done/total), False)
            if self.break_loop:
                break
            else:
                self.sendReport.emit(self.summary_data)

        if not self.break_loop:
            self.sendReport.emit(self.summary_data)
            self.allowRun = False
            self.sendProgress.emit("Finished processing data for all writers for %s." % self.start_date, datetime.datetime.now(),100,True)
        else:
            self.break_loop = False

    def fetchWriterSummary(self, retry=None):
        """
        This method checks the mode.
        """
        if retry is not None:
            #put a notification or signal here.
            print "Retrying to fetch the data. (Trial#%d)" %retry
        
        keys_list = ["Report Date", "Writer ID", "Writer Name", "Writer Email ID", "Reporting Manager",
                "Article Count", "Weekly Article Count", "Monthly Article Count", 
                "Quarterly Article Count", "Half-Yearly Article Count", "Average Article Count", "Efficiency",
                "Weekly Efficiency", "Monthly Efficiency", "Quarterly Efficiency", "Half-Yearly Efficiency",
                "Average Efficiency", "Audit Count", "Weekly Audit Count","Monthly Audit Count",
                "Quarterly Audit Count", "Half-Yearly Audit Count", "Average Audit Count",
                "CFM", "Weekly CFM", "Monthly CFM", "Quarterly CFM", "Half-Yearly CFM",
                "Average CFM", "GSEO", "Weekly GSEO", "Monthly GSEO",
                "Quarterly GSEO", "Half-Yearly GSEO", "Average GSEO", "Stack Rank Index",
                "Weekly Stack Rank Index", "Monthly Stack Rank Index",
                "Quarterly Stack Rank Index", "Half-Yearly Stack Rank Index", "Average Stack Rank Index"
                ]
        writer_summary = dict((key,"-") for key in keys_list)
        writer_summary["Report Date"] = self.start_date
        writer_summary["Writer ID"] = self.writer_id
        writer_summary["Writer Name"] = self.writer_name
        writer_summary["Writer Email ID"] = self.writer_email

        writer_summary["Reporting Manager"] = MOSES.getReportingManager(self.user_id, self.password, query_user=self.writer_id, query_date=self.end_date)["Reporting Manager Name"]
        
        if "Daily" in self.mode:
            writer_summary["Article Count"] = MOSES.getArticleCount(self.user_id, self.password, self.start_date, self.writer_id)
            writer_summary["Efficiency"] = MOSES.getEfficiencyFor(self.user_id, self.password, self.start_date, self.writer_id)
            writer_summary["Audit Count"] = MOSES.getAuditCount(self.user_id, self.password, self.start_date, self.writer_id)
            if writer_summary["Audit Count"] > 0:
                writer_summary["CFM"] = MOSES.getCFMFor(self.user_id, self.password, self.start_date, self.writer_id)
                writer_summary["GSEO"] = MOSES.getGSEOFor(self.user_id, self.password, self.start_date, self.writer_id)
                writer_summary["Stack Rank Index"] = self.getStackRankIndex(writer_summary["Efficiency"], writer_summary["CFM"], writer_summary["GSEO"])
        
        if "Average" in self.mode:
            writer_summary["Average Article Count"] = MOSES.getArticleCountBetween(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
            writer_summary["Average Efficiency"] = MOSES.getEfficiencyForDateRange(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
            writer_summary["Average Audit Count"] = MOSES.getAuditCountBetween(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
            if writer_summary["Average Audit Count"] > 0:
                writer_summary["Average CFM"] = MOSES.getCFMBetweenDates(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
                writer_summary["Average GSEO"] = MOSES.getGSEOBetweenDates(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
                writer_summary["Average Stack Rank Index"] = self.getStackRankIndex(writer_summary["Average Efficiency"], writer_summary["Average CFM"], writer_summary["Average GSEO"])
        
        if "Weekly" in self.mode:
            writer_summary["Weekly Article Count"] = MOSES.getArticleCountForWeek(self.user_id, self.password, self.start_date, self.writer_id)
            writer_summary["Weekly Efficiency"] = MOSES.getEfficiencyForWeek(self.user_id, self.password, self.start_date, self.writer_id)
            writer_summary["Weekly Audit Count"] = MOSES.getAuditCountForWeek(self.user_id, self.password, self.start_date, self.writer_id)
            if writer_summary["Weekly Audit Count"] > 0:
                writer_summary["Weekly CFM"] = MOSES.getCFMForWeek(self.user_id, self.password, self.start_date, self.writer_id)
                writer_summary["Weekly GSEO"] = MOSES.getGSEOForWeek(self.user_id, self.password, self.start_date, self.writer_id)
                writer_summary["Weekly Stack Rank Index"] = self.getStackRankIndex(writer_summary["Weekly Efficiency"], writer_summary["Weekly CFM"], writer_summary["Weekly GSEO"])

        if "Monthly" in self.mode:
            writer_summary["Monthly Article Count"] = MOSES.getArticleCountForMonth(self.user_id, self.password, self.start_date, self.writer_id)
            writer_summary["Monthly Efficiency"] = MOSES.getEfficiencyForMonth(self.user_id, self.password, self.start_date, self.writer_id)
            writer_summary["Monthly Audit Count"] = MOSES.getAuditCountForMonth(self.user_id, self.password, self.start_date, self.writer_id)
            if writer_summary["Monthly Audit Count"] > 0:
                writer_summary["Monthly CFM"] = MOSES.getCFMForMonth(self.user_id, self.password, self.start_date, self.writer_id)
                writer_summary["Monthly GSEO"] = MOSES.getGSEOForMonth(self.user_id, self.password, self.start_date, self.writer_id)
                writer_summary["Monthly Stack Rank Index"] = self.getStackRankIndex(writer_summary["Monthly Efficiency"], writer_summary["Monthly CFM"], writer_summary["Monthly GSEO"])

        if "Quarterly" in self.mode:
            writer_summary["Quarterly Article Count"] = MOSES.getArticleCountForQuarter(self.user_id, self.password, self.start_date, self.writer_id)
            writer_summary["Quarterly Efficiency"] = MOSES.getEfficiencyForQuarter(self.user_id, self.password, self.start_date, self.writer_id)
            writer_summary["Quarterly Audit Count"] = MOSES.getAuditCountForQuarter(self.user_id, self.password, self.start_date, self.writer_id)
            if writer_summary["Quarterly Audit Count"] > 0:
                writer_summary["Quarterly CFM"] = MOSES.getCFMForQuarter(self.user_id, self.password, self.start_date, self.writer_id)
                writer_summary["Quarterly GSEO"] = MOSES.getGSEOForQuarter(self.user_id, self.password, self.start_date, self.writer_id)
                writer_summary["Quarterly Stack Rank Index"] = self.getStackRankIndex(writer_summary["Quarterly Efficiency"], writer_summary["Quarterly CFM"], writer_summary["Quarterly GSEO"])
        
        if "Half-Yearly" in self.mode:
            writer_summary["Half-Yearly Article Count"] = MOSES.getArticleCountForHalfYear(self.user_id, self.password, self.start_date, self.writer_id)
            writer_summary["Half-Yearly Efficiency"] = MOSES.getEfficiencyForHalfYear(self.user_id, self.password, self.start_date, self.writer_id)
            writer_summary["Half-Yearly Audit Count"] = MOSES.getAuditCountForHalfYear(self.user_id, self.password, self.start_date, self.writer_id)
            if writer_summary["Half-Yearly Audit Count"] > 0:
                writer_summary["Half-Yearly CFM"] = MOSES.getCFMForHalfYear(self.user_id, self.password, self.start_date, self.writer_id)
                writer_summary["Half-Yearly GSEO"] = MOSES.getGSEOForHalfYear(self.user_id, self.password, self.start_date, self.writer_id)
                writer_summary["Half-Yearly Stack Rank Index"] = self.getStackRankIndex(writer_summary["Half-Yearly Efficiency"], writer_summary["Half-Yearly CFM"], writer_summary["Half-Yearly GSEO"])
        return writer_summary

    def getStackRankIndex(self, eff, cfm, gseo):
        parameters_are_not_valid = eff is None or cfm is None or gseo is None
        if parameters_are_not_valid:
            stack_rank_index = "NA"
        elif not(math.isnan(eff) or math.isnan(cfm) or math.isnan(gseo)):
            quality_average = (self.getQKRA(cfm)*3 + self.getQKRA(gseo))/4
            stack_rank_index = (self.getEffKRA(eff) + quality_average*2)/3
        else:
            #print (eff, cfm, gseo)
            stack_rank_index = "NA"
        if stack_rank_index is None:
            #print "Error?"
            #print (eff, cfm, gseo)
            stack_rank_index = "NA"
        return stack_rank_index

    def getEffKRA(self, eff):
        if eff < 0.95:
            kra = 1
        elif 0.95 <= eff < 1.0:
            kra = 2
        elif 1.0 <= eff < 1.05:
            kra = 3
        elif 1.05 <= eff < 1.1:
            kra = 4
        elif eff >= 1.1:
            kra = 5
        return kra

    def getQKRA(self, q):
        if q < 0.9:
            kra = 1
        elif 0.9 <= q < 0.95:
            kra = 2
        elif 0.95 <= q <= 0.97:
            kra = 3
        elif 0.97 < q <= 0.99:
            kra = 4
        elif q > 0.99:
            kra = 5
        return kra

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

        self.report = QtGui.QTableWidget(0, 0)
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
        self.build_stop_button.clicked.connect(self.buildStop)
        self.end_date_check_box.stateChanged.connect(self.toggleEndDate)
        self.start_date_edit.dateChanged.connect(self.limitEndDate)
        self.pork_lane = PorkLane(self.user_id, self.password)
        self.pork_lane.sendReport.connect(self.populateReport)
        self.pork_lane.sendProgress.connect(self.displayProgress)

    def buildStop(self):
        if self.build_stop_button.isChecked():
            report_types = self.getRequiredReportTypes()
            if len(report_types) > 0:
                self.build = True
                self.build_stop_button.setText("Stop Building Report")
                self.build_stop_button.setToolTip("Uncheck this button to stop building the report.")
                self.pork_lane.mode = report_types #set pork lane report types.
                self.pork_lane.start_date = self.start_date_edit.date().toPyDate()
                self.pork_lane.end_date = self.end_date_edit.date().toPyDate()
                self.pork_lane.allowRun = True #allow building.
            else:
                self.build = False
                self.alertMessage("Error","Please select at least one parameter in the checklist before attempting to build the report.")
                self.build_stop_button.setChecked(False)
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
        return [key for key in self.report_selection_dict.keys() if self.report_selection_dict[key]]

    def populateReport(self, report):
        mode = self.pork_lane.mode
        columns = ["Report Date", "Writer ID", "Writer Name", "Writer Email ID", "Reporting Manager"]
        if "Daily" in mode:
            columns += ["Article Count", "Efficiency", "Audit Count", "CFM", "GSEO", "Stack Rank Index"]
        if "Weekly" in mode:
            columns += ["Weekly Article Count", "Weekly Efficiency", "Weekly Audit Count", "Weekly CFM", "Weekly GSEO", "Weekly Stack Rank Index"]
        if "Monthly" in mode:
            columns += ["Monthly Article Count", "Monthly Efficiency", "Monthly Audit Count", "Monthly CFM", "Monthly GSEO", "Monthly Stack Rank Index"]
        if "Quarterly" in mode:
            columns += ["Quarterly Article Count", "Quarterly Efficiency", "Quarterly Audit Count", "Quarterly CFM", "Quarterly GSEO", "Quarterly Stack Rank Index"]
        if "Half-Yearly" in mode:
            columns += ["Half-Yearly Article Count", "Half-Yearly Efficiency", "Half-Yearly Audit Count", "Half-Yearly CFM", "Half-Yearly GSEO", "Half-Yearly Stack Rank Index"]
        if "Average" in mode:
            columns += ["Average Article Count", "Average Efficiency", "Average Audit Count", "Average CFM", "Average GSEO", "Average Stack Rank Index"]
        self.report.setRowCount(0)
        row_counter = 0

        self.report.setColumnCount(len(columns))
        self.report.setHorizontalHeaderLabels(columns)
        self.report.setSortingEnabled(False)
        red = QtGui.QColor(231, 90, 83)
        green = QtGui.QColor(60, 179, 113)
        blue = QtGui.QColor(23, 136, 216)

        for writer_row in report:
            self.report.insertRow(row_counter)
            column_counter = 0
            for column_name in columns:
                if "Efficiency" in column_name:
                    steps = [100.00, 105.00, 110.00]
                elif ("CFM" in column_name) or ("GSEO" in column_name):
                    steps = [95.00, 97.00]
                else:
                    steps = []
                parameter = writer_row[column_name]

                if (type(parameter) == str):
                    parameter_is_valid = False
                elif (parameter is None):
                    parameter_is_valid = False
                elif type(parameter) == float:
                    if math.isnan(parameter):
                        parameter_is_valid = False
                    else:
                        parameter_is_valid = True
                elif type(parameter) == datetime.date:
                    parameter_is_valid = False    
                else:
                    parameter_is_valid = True
                
                if parameter_is_valid:
                     parameter_as_string = "%02.2f" %parameter
                elif column_name in ["Report Date", "Writer ID", "Writer Name", "Writer Email ID", "Reporting Manager"]:
                    parameter_as_string = str(parameter)
                else:
                    parameter_as_string = "-"


                writer_cell_item = QtGui.QTableWidgetItem(parameter_as_string)
                if parameter_is_valid:
                    if steps != []:                    
                        if parameter < steps[0]:
                            writer_cell_item.setBackgroundColor(red)
                        elif steps[0] <= parameter <= steps[1]:
                            writer_cell_item.setBackgroundColor(green)
                        elif parameter > steps[1]:
                            writer_cell_item.setBackgroundColor(blue)
                self.report.setItem(row_counter, column_counter, writer_cell_item)
                column_counter += 1
            row_counter += 1 
        self.report.setSortingEnabled(True)



    def displayProgress(self, progress_text, eta, progress, state):
        if state:
            self.pork_lane.allowRun = False
            self.build_stop_button.setText("Build Report")
            self.build_stop_button.setToolTip("Click this button to start building the report")
        print progress_text
        print "Displaying progress."

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)