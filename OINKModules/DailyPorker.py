from __future__ import division

import sys
import math
import datetime
import os

from PyQt4 import QtGui, QtCore
import numpy
import MOSES
from DailyGraphView import DailyGraphView
import Graphinator
from ProgressBar import ProgressBar

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
    sendGraphs = QtCore.pyqtSignal(bool)
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
        self.enablePlotting = False
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
                #print """Pork Lane allowed to run!"""
                self.summarize()
                if self.enablePlotting:
                    self.sendGraphs.emit(False)
                    Graphinator.generateDailyGraphs(self.start_date)
                    self.sendGraphs.emit(True)

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
            self.sendProgress.emit("Processed data for %s for %s."%(self.writer_name, self.start_date), MOSES.getETA(start_time, done, total), int(done*100/total), False)
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
                "Daily Article Count", "Weekly Article Count", "Monthly Article Count", 
                "Quarterly Article Count", "Half-Yearly Article Count", "Average Article Count", 
                "Daily Efficiency",
                "Weekly Efficiency", "Monthly Efficiency", "Quarterly Efficiency", "Half-Yearly Efficiency",
                "Average Efficiency", 
                "Daily Audit Count", "Weekly Audit Count","Monthly Audit Count",
                "Quarterly Audit Count", "Half-Yearly Audit Count", "Average Audit Count",
                "Daily CFM", "Weekly CFM", "Monthly CFM", "Quarterly CFM", "Half-Yearly CFM",
                "Average CFM", 
                "Daily GSEO", "Weekly GSEO", "Monthly GSEO",
                "Quarterly GSEO", "Half-Yearly GSEO", "Average GSEO", 
                "Daily Efficiency KRA", "Weekly Efficiency KRA", "Average Efficiency KRA", 
                "Monthly Efficiency KRA", "Quarterly Efficiency KRA", "Half-Yearly Efficiency KRA",
                "Daily CFM KRA", "Weekly CFM KRA", "Average CFM KRA", 
                "Monthly CFM KRA", "Quarterly CFM KRA", "Half-Yearly CFM KRA",
                "Daily GSEO KRA", "Weekly GSEO KRA", "Average GSEO KRA", 
                "Monthly GSEO KRA", "Quarterly GSEO KRA", "Half-Yearly GSEO KRA",
                "Daily Stack Rank Index",
                "Weekly Stack Rank Index", "Monthly Stack Rank Index",
                "Quarterly Stack Rank Index", "Half-Yearly Stack Rank Index", "Average Stack Rank Index"
                ]
        writer_summary = dict((key,"-") for key in keys_list)
        writer_summary["Report Date"] = self.start_date
        writer_summary["Writer ID"] = self.writer_id
        writer_summary["Writer Name"] = self.writer_name
        writer_summary["Writer Email ID"] = self.writer_email

        writer_summary["Reporting Manager"] = MOSES.getReportingManager(self.user_id, self.password, query_user=self.writer_id, query_date=self.end_date)["Reporting Manager Name"]
        
        if "Daily Article Count" in self.mode:
            writer_summary["Daily Article Count"] = MOSES.getArticleCount(self.user_id, self.password, self.start_date, self.writer_id)
        if ("Daily Efficiency" in self.mode) or ("Daily Stack Rank Index" in self.mode) or ("Daily Efficiency KRA"):
            writer_summary["Daily Efficiency"] = MOSES.getEfficiencyFor(self.user_id, self.password, self.start_date, self.writer_id)
            if (type(writer_summary["Daily Efficiency"]) != str) and (not math.isnan(writer_summary["Daily Efficiency"])):
                try:
                    writer_summary["Daily Efficiency KRA"] = self.getEffKRA(writer_summary["Daily Efficiency"])
                except:
                    print writer_summary["Daily Efficiency"]
        if ("Daily Audit Count" in self.mode) or ("Daily CFM" in self.mode) or ("Daily GSEO" in self.mode) or ("Daily Stack Rank Index" in self.mode) or ("Daily CFM KRA") or ("Daily GSEO KRA"):
            writer_summary["Daily Audit Count"] = MOSES.getAuditCount(self.user_id, self.password, self.start_date, self.writer_id)
            if writer_summary["Daily Audit Count"] > 0:
                if ("Daily CFM" in self.mode) or ("Daily Stack Rank Index" in self.mode) or ("Daily CFM KRA"):
                    writer_summary["Daily CFM"] = MOSES.getCFMFor(self.user_id, self.password, self.start_date, self.writer_id)
                    if type(writer_summary["Daily CFM"]) != str:
                        writer_summary["Daily CFM KRA"] = self.getQKRA(writer_summary["Daily CFM"])

                if( "Daily GSEO" in self.mode) or ("Daily Stack Rank Index" in self.mode) or ("Daily GSEO KRA"):
                    writer_summary["Daily GSEO"] = MOSES.getGSEOFor(self.user_id, self.password, self.start_date, self.writer_id)
                    if type(writer_summary["Daily GSEO"])!= str:
                        writer_summary["Daily GSEO KRA"] = self.getQKRA(writer_summary["Daily GSEO"])

                if "Daily Stack Rank Index" in self.mode:
                    writer_summary["Daily Stack Rank Index"] = self.getStackRankIndex(writer_summary["Daily Efficiency"], writer_summary["Daily CFM"], writer_summary["Daily GSEO"])        

        if "Average Article Count" in self.mode:
            writer_summary["Average Article Count"] = MOSES.getArticleCountBetween(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
        if ("Average Efficiency" in self.mode) or ("Average Stack Rank Index" in self.mode) or ("Average Efficiency KRA" in self.mode):
            writer_summary["Average Efficiency"] = MOSES.getEfficiencyForDateRange(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
            if (type(writer_summary["Average Efficiency"]) != str) and (not math.isnan(writer_summary["Average Efficiency"])):
                try:
                    writer_summary["Average Efficiency KRA"] = self.getEffKRA(writer_summary["Average Efficiency"])
                except:
                    print writer_summary["Average Efficiency"]
        if ("Average Audit Count" in self.mode) or ("Average CFM" in self.mode) or ("Average GSEO" in self.mode) or ("Average Stack Rank Index" in self.mode) or ("Average CFM KRA" in self.mode) or ("Average GSEO KRA" in self.mode):
            writer_summary["Average Audit Count"] = MOSES.getAuditCountBetween(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
            if writer_summary["Average Audit Count"] > 0:
                if ("Average CFM" in self.mode) or ("Average Stack Rank Index" in self.mode) or ("Average CFM KRA" in self.mode):
                    writer_summary["Average CFM"] = MOSES.getCFMBetweenDates(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
                    if type(writer_summary["Average CFM"])!= str:
                        writer_summary["Average CFM KRA"] = MOSES.getQKRA(writer_summary["Average CFM"])
                if ("Average GSEO" in self.mode) or ("Average Stack Rank Index" in self.mode)  or ("Average GSEO KRA" in self.mode):
                    writer_summary["Average GSEO"] = MOSES.getGSEOBetweenDates(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
                    if type(writer_summary["Average GSEO"])!= str:
                        writer_summary["Average GSEO KRA"] = MOSES.getQKRA(writer_summary["Average GSEO"])
                if ("Average Stack Rank Index" in self.mode):
                    writer_summary["Average Stack Rank Index"] = self.getStackRankIndex(writer_summary["Average Efficiency"], writer_summary["Average CFM"], writer_summary["Average GSEO"])
        
        if "Weekly Article Count" in self.mode:
            writer_summary["Weekly Article Count"] = MOSES.getArticleCountForWeek(self.user_id, self.password, self.start_date, self.writer_id)
        if ("Weekly Efficiency" in self.mode) or ("Weekly Stack Rank Index" in self.mode) or ("Weekly Efficiency KRA" in self.mode):
            writer_summary["Weekly Efficiency"] = MOSES.getEfficiencyForWeek(self.user_id, self.password, self.start_date, self.writer_id)
            if (type(writer_summary["Weekly Efficiency"]) != str) and (not math.isnan(writer_summary["Weekly Efficiency"])):
                try:
                    writer_summary["Weekly Efficiency KRA"] = self.getEffKRA(writer_summary["Weekly Efficiency"])
                except:
                    print writer_summary["Weekly Efficiency"]
        if ("Weekly Audit Count" in self.mode) or ("Weekly CFM" in self.mode) or ("Weekly GSEO" in self.mode) or ("Weekly Stack Rank Index" in self.mode) or ("Weekly CFM KRA" in self.mode) or ("Weekly GSEO KRA" in self.mode):
            writer_summary["Weekly Audit Count"] = MOSES.getAuditCountForWeek(self.user_id, self.password, self.start_date, self.writer_id)
            if writer_summary["Weekly Audit Count"] > 0:
                if ("Weekly CFM" in self.mode) or ("Weekly Stack Rank Index" in self.mode) or ("Weekly CFM KRA" in self.mode):
                    writer_summary["Weekly CFM"] = MOSES.getCFMForWeek(self.user_id, self.password, self.start_date, self.writer_id)
                    if type(writer_summary["Weekly CFM"])!= str:
                        writer_summary["Weekly CFM KRA"] = self.getQKRA(writer_summary["Weekly CFM"])
                if ("Weekly GSEO" in self.mode) or ("Weekly Stack Rank Index" in self.mode) or ("Weekly GSEO KRA" in self.mode):
                    writer_summary["Weekly GSEO"] = MOSES.getGSEOForWeek(self.user_id, self.password, self.start_date, self.writer_id)
                    if type(writer_summary["Weekly GSEO"])!= str:
                        writer_summary["Weekly GSEO KRA"] = self.getQKRA(writer_summary["Weekly GSEO"])
                if ("Weekly Stack Rank Index" in self.mode):
                    writer_summary["Weekly Stack Rank Index"] = self.getStackRankIndex(writer_summary["Weekly Efficiency"], writer_summary["Weekly CFM"], writer_summary["Weekly GSEO"])

        if "Monthly Article Count" in self.mode:
            writer_summary["Monthly Article Count"] = MOSES.getArticleCountForMonth(self.user_id, self.password, self.start_date, self.writer_id)
        if ("Monthly Efficiency" in self.mode) or ("Monthly Stack Rank Index" in self.mode) or ("Monthly Efficiency KRA" in self.mode):
            writer_summary["Monthly Efficiency"] = MOSES.getEfficiencyForMonth(self.user_id, self.password, self.start_date, self.writer_id)
            if (type(writer_summary["Monthly Efficiency"]) != str) and (not math.isnan(writer_summary["Monthly Efficiency"])):
                try:
                    writer_summary["Monthly Efficiency KRA"] = self.getEffKRA(writer_summary["Monthly Efficiency"])
                except:
                    print writer_summary["Monthly Efficiency"]
        if ("Monthly Audit Count" in self.mode) or ("Monthly CFM" in self.mode) or ("Monthly GSEO" in self.mode) or ("Monthly Stack Rank Index" in self.mode) or ("Monthly CFM KRA" in self.mode) or ("Monthly GSEO KRA" in self.mode):
            writer_summary["Monthly Audit Count"] = MOSES.getAuditCountForMonth(self.user_id, self.password, self.start_date, self.writer_id)
            if writer_summary["Monthly Audit Count"] > 0:
                if ("Monthly CFM" in self.mode) or ("Monthly Stack Rank Index" in self.mode) or ("Monthly CFM KRA" in self.mode):
                    writer_summary["Monthly CFM"] = MOSES.getCFMForMonth(self.user_id, self.password, self.start_date, self.writer_id)
                    if type(writer_summary["Monthly CFM"])!= str:
                        writer_summary["Monthly CFM KRA"] = self.getQKRA(writer_summary["Monthly CFM"])
                if ("Monthly GSEO" in self.mode) or ("Monthly Stack Rank Index" in self.mode) or ("Monthly CFM KRA" in self.mode):
                    writer_summary["Monthly GSEO"] = MOSES.getGSEOForMonth(self.user_id, self.password, self.start_date, self.writer_id)
                    if type(writer_summary["Monthly GSEO"])!= str:
                        writer_summary["Monthly GSEO KRA"] = self.getQKRA(writer_summary["Monthly GSEO"])

                if ("Monthly Stack Rank Index" in self.mode):
                    writer_summary["Monthly Stack Rank Index"] = self.getStackRankIndex(writer_summary["Monthly Efficiency"], writer_summary["Monthly CFM"], writer_summary["Monthly GSEO"])
        
        if "Quarterly Article Count" in self.mode:
            writer_summary["Quarterly Article Count"] = MOSES.getArticleCountForQuarter(self.user_id, self.password, self.start_date, self.writer_id)
        if ("Quarterly Efficiency" in self.mode) or ("Quarterly Stack Rank Index" in self.mode) or ("Quarterly Efficiency KRA" in self.mode):
            writer_summary["Quarterly Efficiency"] = MOSES.getEfficiencyForQuarter(self.user_id, self.password, self.start_date, self.writer_id)
            if (type(writer_summary["Quarterly Efficiency"]) != str) and (not math.isnan(writer_summary["Quarterly Efficiency"])):
                try:
                    writer_summary["Quarterly Efficiency KRA"] = self.getEffKRA(writer_summary["Quarterly Efficiency"])
                except:
                    print writer_summary["Quarterly Efficiency"]
        if ("Quarterly Audit Count" in self.mode) or ("Quarterly CFM" in self.mode) or ("Quarterly GSEO" in self.mode) or ("Quarterly Stack Rank Index" in self.mode) or ("Quarterly CFM KRA" in self.mode) or ("Quarterly GSEO KRA" in self.mode):
            writer_summary["Quarterly Audit Count"] = MOSES.getAuditCountForQuarter(self.user_id, self.password, self.start_date, self.writer_id)
            if writer_summary["Quarterly Audit Count"] > 0:
                if ("Quarterly CFM" in self.mode) or ("Quarterly Stack Rank Index" in self.mode) or ("Quarterly CFM KRA" in self.mode):
                    writer_summary["Quarterly CFM"] = MOSES.getCFMForQuarter(self.user_id, self.password, self.start_date, self.writer_id)
                    if type(writer_summary["Quarterly CFM"])!= str:
                        writer_summary["Quarterly CFM KRA"] = self.getQKRA(writer_summary["Quarterly CFM"])
                if ("Quarterly GSEO" in self.mode) or ("Quarterly Stack Rank Index" in self.mode) or ("Quarterly GSEO KRA" in self.mode):
                    writer_summary["Quarterly GSEO"] = MOSES.getGSEOForQuarter(self.user_id, self.password, self.start_date, self.writer_id)
                    if type(writer_summary["Quarterly GSEO"])!= str:
                        writer_summary["Quarterly GSEO KRA"] = self.getQKRA(writer_summary["Quarterly GSEO"])
                if ("Quarterly Stack Rank Index" in self.mode):
                    writer_summary["Quarterly Stack Rank Index"] = self.getStackRankIndex(writer_summary["Quarterly Efficiency"], writer_summary["Quarterly CFM"], writer_summary["Quarterly GSEO"])
        
        if "Half-Yearly Article Count" in self.mode:
            writer_summary["Half-Yearly Article Count"] = MOSES.getArticleCountForHalfYear(self.user_id, self.password, self.start_date, self.writer_id)
        if ("Half-Yearly Efficiency" in self.mode) or ("Half-Yearly Stack Rank Index" in self.mode) or ("Half-Yearly Efficiency KRA" in self.mode):
            writer_summary["Half-Yearly Efficiency"] = MOSES.getEfficiencyForHalfYear(self.user_id, self.password, self.start_date, self.writer_id)
            if (type(writer_summary["Half-Yearly Efficiency"]) != str) and (not math.isnan(writer_summary["Half-Yearly Efficiency"])):
                try:
                    writer_summary["Half-Yearly Efficiency KRA"] = self.getEffKRA(writer_summary["Half-Yearly Efficiency"])
                except:
                    print writer_summary["Half-Yearly Efficiency"]
        if ("Half-Yearly Audit Count Count" in self.mode) or ("Half-Yearly CFM" in self.mode) or ("Half-Yearly GSEO" in self.mode) or ("Half-Yearly Stack Rank Index" in self.mode) or ("Half-Yearly CFM KRA" in self.mode) or ("Half-Yearly GSEO KRA" in self.mode):
            writer_summary["Half-Yearly Audit Count"] = MOSES.getAuditCountForHalfYear(self.user_id, self.password, self.start_date, self.writer_id)
            if writer_summary["Half-Yearly Audit Count"] > 0:
                if ("Half-Yearly CFM" in self.mode) or ("Half-Yearly Stack Rank Index" in self.mode) or ("Half-Yearly CFM KRA" in self.mode):
                    writer_summary["Half-Yearly CFM"] = MOSES.getCFMForHalfYear(self.user_id, self.password, self.start_date, self.writer_id)
                    print type(writer_summary["Half-Yearly CFM"])
                    if type(writer_summary["Half-Yearly CFM"])!= str:
                        writer_summary["Half-Yearly CFM KRA"] = self.getQKRA(writer_summary["Half-Yearly CFM"])
                        print writer_summary["Half-Yearly CFM KRA"]
                if ("Half-Yearly GSEO" in self.mode) or ("Half-Yearly Stack Rank Index" in self.mode) or ("Half-Yearly GSEO KRA" in self.mode):
                    writer_summary["Half-Yearly GSEO"] = MOSES.getGSEOForHalfYear(self.user_id, self.password, self.start_date, self.writer_id)
                    if type(writer_summary["Half-Yearly GSEO"])!= str:
                        writer_summary["Half-Yearly GSEO KRA"] = self.getQKRA(writer_summary["Half-Yearly GSEO"])
                if ("Half-Yearly Stack Rank Index" in self.mode):
                    writer_summary["Half-Yearly Stack Rank Index"] = self.getStackRankIndex(writer_summary["Half-Yearly Efficiency"], writer_summary["Half-Yearly CFM"], writer_summary["Half-Yearly GSEO"])
        return writer_summary

    def getStackRankIndex(self, eff, cfm, gseo):
        parameters_are_not_valid = (eff is None) or (cfm is None) or (gseo is None) or (type(eff) == str) or (type(cfm) == str) or (type(gseo) == str) 
        try:
            if parameters_are_not_valid:
                stack_rank_index = "NA"
            elif not(math.isnan(eff) or math.isnan(cfm) or math.isnan(gseo)):
                quality_average = (self.getQKRA(cfm)*3 + self.getQKRA(gseo))/4
                stack_rank_index = (self.getEffKRA(eff) + quality_average*2)/3
            else:
                #print (eff, cfm, gseo)
                stack_rank_index = "NA"
        except:
            print eff, cfm, gseo
            raise
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
        .QTableWidget {
            gridline-color: rgb(0, 0, 0);
        }
        """
        self.setStyleSheet(style_string)
        self.clip = QtGui.QApplication.clipboard()
        self.createUI()
        self.center()
        self.setAutoFillBackground(True)
        self.mapEvents()

    def center(self):
        #frameGm = self.frameGeometry()
        #screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        #centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        #frameGm.moveCenter(centerPoint)
        #self.move(frameGm.topLeft())
        self.move(70,50)

    def createUI(self):
        self.reports_list = QtGui.QListWidget()
        self.reports_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.reports_list.setMinimumSize(120,80)
        self.reports_list.setMaximumSize(120,80)
        report_names = ["Article Count","Efficiency","Audit Count","CFM","GSEO","Stack Rank Index","Efficiency KRA","CFM KRA","GSEO KRA"]#,"Audit Percentage"]
        for report_name in report_names:
            self.reports_list.addItem(report_name)
        list_box_style = """
            QListWidget::item:selected {
                background-color: #0088d6; /*Blue*/
                color: #fdde2e; /*Yellow*/
            }
            QListWidget::item:hover {
                color: #0088d6; /*Blue*/
                background-color: #fdde2e; /*Yellow*/
            }
            QListWidget::item {
                color: black;
                background-color: white;
            }

            """
        self.reports_list.setStyleSheet(list_box_style)
        for item_index in range(self.reports_list.count()):
            item = self.reports_list.item(item_index)
            #print item.text()
            if item.text() in ["Efficiency","CFM","GSEO", "Stack Rank Index"]:
                self.reports_list.setItemSelected(item, True)

        self.start_date_label = QtGui.QLabel("<b>Select a report date:</b>")
        self.start_date_edit = QtGui.QDateTimeEdit()
        self.start_date_edit.setToolTip("Set the date for which you want to generate the report.")
        self.start_date_edit.setDate(MOSES.getLastWorkingDate(self.user_id, self.password, queryUser="All"))
        self.start_date_edit.setDisplayFormat("MMMM dd, yyyy")
        self.start_date_edit.setMinimumDate(QtCore.QDate(2015,1,1))
        self.start_date_edit.setCalendarPopup(True)
        self.instruction_label = QtGui.QLabel("<b>Select the parameters which need to be pulled:</b>")
        self.daily_check_box = QtGui.QCheckBox("Daily")
        self.daily_check_box.setToolTip("Check this to include the daily metrics in the compiled report.")
        self.weekly_check_box = QtGui.QCheckBox("Weekly")
        self.weekly_check_box.setToolTip("Check this to include the weekly metrics in the compiled report.")
        self.monthly_check_box = QtGui.QCheckBox("Monthly")
        self.monthly_check_box.setToolTip("Check this to include the monthly metrics in the compiled report.")
        self.quarterly_check_box = QtGui.QCheckBox("Quarterly")
        self.quarterly_check_box.setToolTip("Check this to include the quarterly metrics in the compiled report.")
        self.half_yearly_check_box = QtGui.QCheckBox("Half-Yearly")
        self.half_yearly_check_box.setToolTip("Check this to include the half-yearly metrics in the compiled report.")
        self.end_date_check_box = QtGui.QCheckBox("Until End Date")
        self.end_date_check_box.setToolTip("Check this to include the average metrics\nbetween the first date and the end date in the compiled report.")
        self.end_date_edit = QtGui.QDateTimeEdit()
        self.end_date_edit.setToolTip("Select an end date. Only working days will be considered for the calculation.\nThis field will be disabled if the checkbox isn't marked to calculate the average statistics between dates.")
        self.end_date_edit.setDate(QtCore.QDate(datetime.date.today()))
        self.end_date_edit.setDisplayFormat("MMMM dd, yyyy")
        self.end_date_edit.setMinimumDate(QtCore.QDate(datetime.date.today()))
        self.end_date_edit.setCalendarPopup(True)

        self.sorting_filter_label = QtGui.QLabel("<b>Sort Report By:</b>")
        self.sorting_filter_combobox = QtGui.QComboBox()
        self.sorting_filter_combobox.setToolTip("Select the parameter you want to sort the generated reports by.")

        self.graphs_check_box = QtGui.QCheckBox("Plot Required Graphs")
        self.graphs_check_box.setToolTip("Check this if you want to automatically plot the graphs.")
        self.graphs_check_box.setEnabled(False)
        self.writer_report_check_box = QtGui.QCheckBox("Build Writer(s) Report")
        self.writer_report_check_box.setToolTip("Check this if you want to build the report for all the writers' data.")
        self.writer_report_check_box.setEnabled(False)
        self.team_report_check_box = QtGui.QCheckBox("Build Team Report")
        self.team_report_check_box.setToolTip("Check this if you want to build the report segregated by the reporting manager.")
        self.team_report_check_box.setEnabled(False)
        
        self.report = QtGui.QTableWidget(0, 0)
        #self.t_report = QtGui.QTableWidget(0, 0)
        self.graphs = DailyGraphView()
        #self.t_graphs = QtGui.QWidget()
        
        self.progress_bar = ProgressBar()
        self.build_stop_button = QtGui.QPushButton("Build Report")
        self.build_stop_button.setToolTip("Click this button to start building the report")
        self.build_stop_button.setCheckable(True)

        self.export_graphs_button = QtGui.QPushButton("Export Graphs")
        self.export_graphs_button.setToolTip("Click this button to save the generated graphs in a desired location.")
        self.export_graphs_button.setEnabled(False)
        self.export_report_button = QtGui.QPushButton("Export Report To CSV")
        self.export_report_button.setToolTip("Click this button to save the generated report in a desired location.")
        self.export_report_button.setEnabled(False)


        self.reports_tab = QtGui.QTabWidget()
        self.reports_tab.addTab(self.report,"Writers' Report")
        self.reports_tab.addTab(self.graphs, "Writers' Graphs")
        #self.reports_tab.addTab(self.t_report,"Team Report")
        #self.reports_tab.addTab(self.t_graphs, "Team Graphs")
        self.status = QtGui.QLabel("I'm a Porkitzer Prize Winning Reporter.")

        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.start_date_label,0,0)
        self.layout.addWidget(self.start_date_edit,0,1,1,1)
        self.layout.addWidget(self.instruction_label,1,0,1,2)
        self.layout.addWidget(self.daily_check_box, 2, 0)
        self.layout.addWidget(self.weekly_check_box, 2, 1)
        self.layout.addWidget(self.monthly_check_box, 2, 2)
        self.layout.addWidget(self.quarterly_check_box, 2, 3)
        self.layout.addWidget(self.half_yearly_check_box, 2, 4)
        self.layout.addWidget(self.end_date_check_box, 2, 6)
        self.layout.addWidget(self.end_date_edit, 2, 7)
        self.layout.addWidget(self.reports_list,2, 8, 2, 1)
        self.layout.addWidget(self.graphs_check_box, 3, 0)
        self.layout.addWidget(self.writer_report_check_box, 3, 1)
        self.layout.addWidget(self.team_report_check_box,3,2)
        self.layout.addWidget(self.sorting_filter_label,3,3)
        self.layout.addWidget(self.sorting_filter_combobox,3,4)
        self.layout.addWidget(self.build_stop_button, 3, 5)
        self.layout.addWidget(self.export_report_button,3,6)
        self.layout.addWidget(self.export_graphs_button,3,7)
        self.layout.addWidget(self.reports_tab, 4, 0, 1, 10)
        self.layout.addWidget(self.progress_bar, 5, 0, 1, 10)
        self.layout.addWidget(self.status,6, 0, 1, 10)
        self.resetReportSelection()
        #Set stretch factors to rows.
        for row_number in range(10):
            self.layout.setRowStretch(row_number,0)

        for column_number in range(10):
            self.layout.setColumnStretch(column_number,0)
       
        self.setLayout(self.layout)
        self.resize(800, 600)
        self.setWindowTitle("The Daily Porker: Straight from the Pigs")
        if "OINKModules" in os.getcwd():
            icon_file_name_path = os.path.join(os.path.join('..',"Images"),'PORK_Icon.png')
        else:
            icon_file_name_path = os.path.join('Images','PORK_Icon.png')
        self.setWindowIcon(QtGui.QIcon(icon_file_name_path))

    def mapEvents(self):
        self.build_stop_button.clicked.connect(self.buildStop)
        self.end_date_check_box.stateChanged.connect(self.toggleEndDate)
        self.start_date_edit.dateChanged.connect(self.limitEndDate)
        self.pork_lane = PorkLane(self.user_id, self.password)
        self.pork_lane.sendReport.connect(self.populateReport)
        self.pork_lane.sendProgress.connect(self.displayProgress)
        self.pork_lane.sendGraphs.connect(self.displayGraphs)
        self.daily_check_box.stateChanged.connect(self.refreshSortFilter)
        self.weekly_check_box.stateChanged.connect(self.refreshSortFilter)
        self.monthly_check_box.stateChanged.connect(self.refreshSortFilter)
        self.quarterly_check_box.stateChanged.connect(self.refreshSortFilter)
        self.half_yearly_check_box.stateChanged.connect(self.refreshSortFilter)
        self.end_date_check_box.stateChanged.connect(self.refreshSortFilter)
        self.reports_list.itemSelectionChanged.connect(self.refreshSortFilter)

    def displayGraphs(self,handle):
        if handle:
            self.graphs.graph_date = self.pork_lane.start_date
            self.graphs.enable_plotting = True
            self.graphs.plotGraph()
            self.progress_bar.setRange(0,100)
            self.progress_bar.setFormat("Completed at %s." %(datetime.datetime.strftime(datetime.datetime.now(),"%H:%M:%S")))
            self.status.setText("Beware the alien, the mutant, the heretic.")  
            self.progress_bar.setValue(100)
            #self.export_graphs_button.setEnabled(True)
        else:
            self.export_graphs_button.setEnabled(False)
            self.status.setText("Creating Graphs...")        
            self.progress_bar.setValue(0)
            self.progress_bar.setRange(0,0)


    def refreshSortFilter(self):
        report_types = self.getRequiredReportTypes()
        self.sorting_filter_combobox.clear()
        if len(report_types) > 0:
            self.sorting_filter_combobox.setEnabled(True)
            self.sorting_filter_combobox.addItems(report_types)
        else:
            self.sorting_filter_combobox.setEnabled(False)
        self.sorting_filter_combobox.setCurrentIndex(-1)


    def buildStop(self):
        if self.build_stop_button.isChecked():
            report_types = self.getRequiredReportTypes()
            if len(report_types) > 0:
                self.build = True
                self.build_stop_button.setText("Stop Building Report")
                self.build_stop_button.setToolTip("Uncheck this button to stop building the report.")
                self.pork_lane.mode = report_types #set pork lane report types.
                self.pork_lane.enablePlotting = self.graphs_check_box.isChecked()
                self.pork_lane.start_date = self.start_date_edit.date().toPyDate()
                self.pork_lane.end_date = self.end_date_edit.date().toPyDate()
                self.pork_lane.allowRun = True #allow building.
            else:
                self.build = False
                self.alertMessage("Error","Please select at least one parameter in the checklist before attempting to build the report.")
                self.build_stop_button.setChecked(False)
        else:
            self.build = False
            self.pork_lane.allowRun = False #stop building.
            self.build_stop_button.setText("Build Report")
            self.build_stop_button.setToolTip("Click this button to start building the report")
            

    def toggleEndDate(self, state):
        if state == 2:
            self.end_date_edit.setEnabled(True)
        else:
            self.end_date_edit.setEnabled(False)

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
        time_frame_list = [key for key in self.report_selection_dict.keys() if self.report_selection_dict[key]]
        report_type_list = [item.text() for item in self.reports_list.selectedItems()]
        reports_list = []
        for time_frame in time_frame_list:
            reports_list += ["%s %s"%(time_frame, report_type) for report_type in report_type_list]
        return reports_list

    def populateReport(self, report):
        mode = self.pork_lane.mode
        columns = ["Report Date", "Writer ID", "Writer Email ID", "Writer Name", "Reporting Manager"]
        columns += mode
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
                if ("Efficiency" in column_name) and ("KRA" not in column_name):
                    steps = [1.00, 1.05, 1.10]
                elif (("CFM" in column_name) or ("GSEO" in column_name)) and ("KRA" not in column_name):
                    steps = [0.95, 0.97]
                elif ("KRA" in column_name) or ("Index" in column_name):
                    steps = [3.0,4.0,5.0]
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
                    if "Count" in column_name:
                        parameter_as_string = "%03d" % parameter
                    elif ("Stack Rank Index" in column_name) or ("KRA" in column_name):
                        parameter_as_string = "%01.2f" % parameter
                    else:
                        if math.isnan(parameter):
                            parameter_as_string = "-"
                        else:
                            parameter_as_string = "%06.2f%%" %(round(parameter*100,4))
                elif column_name in ["Report Date", "Writer ID", "Writer Name", "Writer Email ID", "Reporting Manager"]:
                    parameter_as_string = str(parameter)
                else:
                    parameter_as_string = "-"

                writer_cell_item = QtGui.QTableWidgetItem(parameter_as_string)
                writer_cell_item.setTextAlignment(QtCore.Qt.AlignCenter)
                if parameter_is_valid:
                    if steps != []:
                        if round(parameter,4) < steps[0]:
                            writer_cell_item.setBackgroundColor(red)
                        elif steps[0] <= (round(parameter,4)) <= steps[1]:
                            writer_cell_item.setBackgroundColor(green)
                        elif (round(parameter,4)) > steps[1]:
                            writer_cell_item.setBackgroundColor(blue)
                self.report.setItem(row_counter, column_counter, writer_cell_item)
                column_counter += 1
            row_counter += 1 
        self.report.setSortingEnabled(True)
        self.report.resizeColumnsToContents()
        self.report.resizeRowsToContents()
        sorting_factor = self.getSortColumn()
        if sorting_factor is not "NA":
            sort_index = mode.index(sorting_factor) + 5
            self.report.sortItems(sort_index,QtCore.Qt.DescendingOrder)

    def getSortColumn(self):
        if self.sorting_filter_combobox.currentIndex() != -1:
            return str(self.sorting_filter_combobox.currentText())
        else:
            return "NA"
    def displayProgress(self, progress_text, eta, progress, state):
        if state:
            self.pork_lane.allowRun = False
            self.build_stop_button.setChecked(False)
            self.build_stop_button.setText("Build Report")
            self.build_stop_button.setToolTip("Click this button to start building the report")
            self.progress_bar.setFormat("Completed at %s." %(datetime.datetime.strftime(eta,"%H:%M:%S")))        
            self.progress_bar.setValue(progress)
        else:
            self.progress_bar.setFormat("%s ETA: %s" %(progress_text, datetime.datetime.strftime(eta,"%H:%M:%S")))
            self.progress_bar.setValue(progress)

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_C:
                table_to_copy = self.report
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
            elif e.key() == QtCore.Qt.Key_R:
                #print "Trying to reset?"
                self.resetReportSelection()
    
    def resetReportSelection(self):
        self.daily_check_box.setChecked(True)
        self.weekly_check_box.setChecked(True)
        self.monthly_check_box.setChecked(False)
        self.quarterly_check_box.setChecked(False)
        self.half_yearly_check_box.setChecked(False)
        self.end_date_check_box.setChecked(False)
        self.end_date_edit.setEnabled(False)
        self.sorting_filter_combobox.setEnabled(True)
        self.graphs_check_box.setChecked(True)
        self.writer_report_check_box.setChecked(True)
        self.team_report_check_box.setChecked(False)
        for item_index in range(self.reports_list.count()):
            item = self.reports_list.item(item_index)
            if item.text() in ["Efficiency","CFM","GSEO", "Stack Rank Index", "Article Count", "Audit Count"]:
                self.reports_list.setItemSelected(item, True)
            else:
                self.reports_list.setItemSelected(item, False)
        self.refreshSortFilter()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([])
    u, p = MOSES.getBigbrotherCredentials()
    dailyporker = DailyPorker(u,p)
    dailyporker.show()
    sys.exit(app.exec_())