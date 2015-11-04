from __future__ import division

import sys
import math
import datetime
import os
from PyQt4 import QtGui, QtCore
import numpy
import pandas as pd

import MOSES
from DailyGraphView import DailyGraphView
import Graphinator
from ProgressBar import ProgressBar
from CopiableQTableWidget import CopiableQTableWidget
from CheckableComboBox import CheckableComboBox

def getReportTypes():
    report_types = ["Article Count", "Efficiency","Audit Count", "CFM", "GSEO","Efficiency KRA","CFM KRA","GSEO KRA", "Stack Rank Index"]
    time_frames = ["Daily","Weekly","Monthly","Half-Yearly"]
    time_frame_based_report_types = ["%s %s"%(time_frame, report_type) for time_frame in time_frames for report_type in report_types]
    return ["Report Date", "Writer ID", "Writer Name", "Writer Email ID", "Reporting Manager"] + time_frame_based_report_types


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
    def __init__(self, user_id, password, category_tree, mode=None):
        super(PorkLane, self).__init__()
        self.user_id = user_id
        self.password = password
        if mode is None:
            self.allowRun = False
            self.mode = []
        else:
            self.allowRun = True
            self.mode = mode
        self.category_tree = category_tree
        self.start_date = datetime.date.today()
        self.end_date = datetime.date.today()
        self.writers_list = []
        self.time_frame_list = []
        self.parameter_list = []
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
        self.summary_data = []
        done = 0
        total = len(self.writers_list)
        start_time = datetime.datetime.now()
        self.mode = self.getMode()
        for writer_name in self.writers_list:
            writer_summary = self.fetchWriterSummary(writer_name)
            self.summary_data.append(writer_summary)
            done = len(self.summary_data)
            self.sendProgress.emit("Processed data for %s for %s."%(writer_name, self.start_date), MOSES.getETA(start_time, done, total), int(done*100/total), False)
            self.sendReport.emit(self.summary_data)

        self.sendReport.emit(self.summary_data)
        self.allowRun = False
        self.sendProgress.emit("Finished processing data for all writers for %s." % self.start_date, datetime.datetime.now(),100,True)

    def getMode(self):
        reports_list = ["%s %s"%(time_frame, parameter_type) for time_frame in self.time_frame_list for parameter_type in self.parameter_list]
        return reports_list

    def fetchWriterSummary(self, writer_name):
        """
        This method checks the mode.
        """
        keys_list = getReportTypes()
        writer_id = str(list(self.writers_data_frame[self.writers_data_frame["Name"] == writer_name]["Employee ID"])[0])
        writer_email = str(list(self.writers_data_frame[self.writers_data_frame["Name"] == writer_name]["Email ID"])[0])

        writer_summary = dict((key,"-") for key in keys_list)
        writer_summary["Report Date"] = self.start_date
        writer_summary["Writer ID"] = writer_id
        writer_summary["Writer Name"] = writer_name
        writer_summary["Writer Email ID"] = writer_email

        writer_summary["Reporting Manager"] = MOSES.getReportingManager(self.user_id, self.password, query_user=writer_id, query_date=self.end_date)
        
        if "Daily Article Count" in self.mode:
            writer_summary["Daily Article Count"] = MOSES.getArticleCount(self.user_id, self.password, self.start_date, writer_id)
        if ("Daily Efficiency" in self.mode) or ("Daily Stack Rank Index" in self.mode) or ("Daily Efficiency KRA"):
            writer_summary["Daily Efficiency"] = MOSES.getEfficiencyFor(self.user_id, self.password, self.start_date, writer_id, self.category_tree)
            if (type(writer_summary["Daily Efficiency"]) != str) and (not math.isnan(writer_summary["Daily Efficiency"])):
                try:
                    writer_summary["Daily Efficiency KRA"] = self.getEffKRA(writer_summary["Daily Efficiency"])
                except:
                    print writer_summary["Daily Efficiency"]
        if ("Daily Audit Count" in self.mode) or ("Daily CFM" in self.mode) or ("Daily GSEO" in self.mode) or ("Daily Stack Rank Index" in self.mode) or ("Daily CFM KRA") or ("Daily GSEO KRA"):
            writer_summary["Daily Audit Count"] = MOSES.getAuditCount(self.user_id, self.password, self.start_date, writer_id)
            if writer_summary["Daily Audit Count"] > 0:
                if ("Daily CFM" in self.mode) or ("Daily Stack Rank Index" in self.mode) or ("Daily CFM KRA") or ("Daily GSEO" in self.mode) or ("Daily Stack Rank Index" in self.mode) or ("Daily GSEO KRA"):
                    writer_summary["Daily CFM"], writer_summary["Daily GSEO"], fatals = MOSES.getCFMGSEOFor(self.user_id, self.password, self.start_date, writer_id)
                    if type(writer_summary["Daily CFM"]) != str:
                        writer_summary["Daily CFM KRA"] = self.getQKRA(writer_summary["Daily CFM"])
                    if type(writer_summary["Daily GSEO"])!= str:
                        writer_summary["Daily GSEO KRA"] = self.getQKRA(writer_summary["Daily GSEO"])

                if "Daily Stack Rank Index" in self.mode:
                    writer_summary["Daily Stack Rank Index"] = self.getStackRankIndex(writer_summary["Daily Efficiency"], writer_summary["Daily CFM"], writer_summary["Daily GSEO"])        


        if "Average Article Count" in self.mode:
            writer_summary["Average Article Count"] = MOSES.getArticleCountBetween(self.user_id, self.password, self.start_date, self.end_date, writer_id)
        if ("Average Efficiency" in self.mode) or ("Average Stack Rank Index" in self.mode) or ("Average Efficiency KRA" in self.mode):
            writer_summary["Average Efficiency"] = MOSES.getEfficiencyForDateRange(self.user_id, self.password, self.start_date, self.end_date, writer_id, self.category_tree)
            if (type(writer_summary["Average Efficiency"]) != str) and (not math.isnan(writer_summary["Average Efficiency"])):
                try:
                    writer_summary["Average Efficiency KRA"] = self.getEffKRA(writer_summary["Average Efficiency"])
                except:
                    print writer_summary["Average Efficiency"]
        if ("Average Audit Count" in self.mode) or ("Average CFM" in self.mode) or ("Average GSEO" in self.mode) or ("Average Stack Rank Index" in self.mode) or ("Average CFM KRA" in self.mode) or ("Average GSEO KRA" in self.mode):
            writer_summary["Average Audit Count"] = MOSES.getAuditCountBetween(self.user_id, self.password, self.start_date, self.end_date, writer_id)
            if writer_summary["Average Audit Count"] > 0:
                if ("Average CFM" in self.mode) or ("Average Stack Rank Index" in self.mode) or ("Average CFM KRA" in self.mode) or ("Average GSEO" in self.mode) or ("Average Stack Rank Index" in self.mode)  or ("Average GSEO KRA" in self.mode):
                    writer_summary["Average CFM"], writer_summary["Average GSEO"], fatals = MOSES.getCFMGSEOBetweenDates(self.user_id, self.password, self.start_date, self.end_date, writer_id)
                    if type(writer_summary["Average CFM"])!= str:
                        writer_summary["Average CFM KRA"] = MOSES.getQKRA(writer_summary["Average CFM"])
                    if type(writer_summary["Average GSEO"])!= str:
                        writer_summary["Average GSEO KRA"] = MOSES.getQKRA(writer_summary["Average GSEO"])
                if ("Average Stack Rank Index" in self.mode):
                    writer_summary["Average Stack Rank Index"] = self.getStackRankIndex(writer_summary["Average Efficiency"], writer_summary["Average CFM"], writer_summary["Average GSEO"])
        
        if "Weekly Article Count" in self.mode:
            writer_summary["Weekly Article Count"] = MOSES.getArticleCountForWeek(self.user_id, self.password, self.start_date, writer_id)
        if ("Weekly Efficiency" in self.mode) or ("Weekly Stack Rank Index" in self.mode) or ("Weekly Efficiency KRA" in self.mode):
            writer_summary["Weekly Efficiency"] = MOSES.getEfficiencyForWeek(self.user_id, self.password, self.start_date, writer_id, self.category_tree)
            if (type(writer_summary["Weekly Efficiency"]) != str) and (not math.isnan(writer_summary["Weekly Efficiency"])):
                try:
                    writer_summary["Weekly Efficiency KRA"] = self.getEffKRA(writer_summary["Weekly Efficiency"])
                except:
                    print writer_summary["Weekly Efficiency"]
        if ("Weekly Audit Count" in self.mode) or ("Weekly CFM" in self.mode) or ("Weekly GSEO" in self.mode) or ("Weekly Stack Rank Index" in self.mode) or ("Weekly CFM KRA" in self.mode) or ("Weekly GSEO KRA" in self.mode):
            writer_summary["Weekly Audit Count"] = MOSES.getAuditCountForWeek(self.user_id, self.password, self.start_date, writer_id)
            if writer_summary["Weekly Audit Count"] > 0:
                if ("Weekly CFM" in self.mode) or ("Weekly Stack Rank Index" in self.mode) or ("Weekly CFM KRA" in self.mode) or ("Weekly GSEO" in self.mode) or ("Weekly Stack Rank Index" in self.mode) or ("Weekly GSEO KRA" in self.mode):
                    writer_summary["Weekly CFM"], writer_summary["Weekly GSEO"], fatals = MOSES.getCFMGSEOForWeek(self.user_id, self.password, self.start_date, writer_id)
                    if type(writer_summary["Weekly CFM"])!= str:
                        writer_summary["Weekly CFM KRA"] = self.getQKRA(writer_summary["Weekly CFM"])
                    if type(writer_summary["Weekly GSEO"])!= str:
                        writer_summary["Weekly GSEO KRA"] = self.getQKRA(writer_summary["Weekly GSEO"])
                if ("Weekly Stack Rank Index" in self.mode):
                    writer_summary["Weekly Stack Rank Index"] = self.getStackRankIndex(writer_summary["Weekly Efficiency"], writer_summary["Weekly CFM"], writer_summary["Weekly GSEO"])

        if "Monthly Article Count" in self.mode:
            writer_summary["Monthly Article Count"] = MOSES.getArticleCountForMonth(self.user_id, self.password, self.start_date, writer_id)
        if ("Monthly Efficiency" in self.mode) or ("Monthly Stack Rank Index" in self.mode) or ("Monthly Efficiency KRA" in self.mode):
            writer_summary["Monthly Efficiency"] = MOSES.getEfficiencyForMonth(self.user_id, self.password, self.start_date, writer_id, self.category_tree)
            if (type(writer_summary["Monthly Efficiency"]) != str) and (not math.isnan(writer_summary["Monthly Efficiency"])):
                try:
                    writer_summary["Monthly Efficiency KRA"] = self.getEffKRA(writer_summary["Monthly Efficiency"])
                except:
                    print writer_summary["Monthly Efficiency"]
        if ("Monthly Audit Count" in self.mode) or ("Monthly CFM" in self.mode) or ("Monthly GSEO" in self.mode) or ("Monthly Stack Rank Index" in self.mode) or ("Monthly CFM KRA" in self.mode) or ("Monthly GSEO KRA" in self.mode):
            writer_summary["Monthly Audit Count"] = MOSES.getAuditCountForMonth(self.user_id, self.password, self.start_date, writer_id)
            if writer_summary["Monthly Audit Count"] > 0:
                if ("Monthly CFM" in self.mode) or ("Monthly Stack Rank Index" in self.mode) or ("Monthly CFM KRA" in self.mode) or ("Monthly GSEO" in self.mode) or ("Monthly Stack Rank Index" in self.mode) or ("Monthly CFM KRA" in self.mode):
                    writer_summary["Monthly CFM"], writer_summary["Monthly GSEO"], fatals = MOSES.getCFMGSEOForMonth(self.user_id, self.password, self.start_date, writer_id)
                    if type(writer_summary["Monthly CFM"])!= str:
                        writer_summary["Monthly CFM KRA"] = self.getQKRA(writer_summary["Monthly CFM"])
                    if type(writer_summary["Monthly GSEO"])!= str:
                        writer_summary["Monthly GSEO KRA"] = self.getQKRA(writer_summary["Monthly GSEO"])

                if ("Monthly Stack Rank Index" in self.mode):
                    writer_summary["Monthly Stack Rank Index"] = self.getStackRankIndex(writer_summary["Monthly Efficiency"], writer_summary["Monthly CFM"], writer_summary["Monthly GSEO"])
        
        if "Quarterly Article Count" in self.mode:
            writer_summary["Quarterly Article Count"] = MOSES.getArticleCountForQuarter(self.user_id, self.password, self.start_date, writer_id)
        if ("Quarterly Efficiency" in self.mode) or ("Quarterly Stack Rank Index" in self.mode) or ("Quarterly Efficiency KRA" in self.mode):
            writer_summary["Quarterly Efficiency"] = MOSES.getEfficiencyForQuarter(self.user_id, self.password, self.start_date, writer_id, self.category_tree)
            if (type(writer_summary["Quarterly Efficiency"]) != str) and (not math.isnan(writer_summary["Quarterly Efficiency"])):
                try:
                    writer_summary["Quarterly Efficiency KRA"] = self.getEffKRA(writer_summary["Quarterly Efficiency"])
                except:
                    print writer_summary["Quarterly Efficiency"]
        if ("Quarterly Audit Count" in self.mode) or ("Quarterly CFM" in self.mode) or ("Quarterly GSEO" in self.mode) or ("Quarterly Stack Rank Index" in self.mode) or ("Quarterly CFM KRA" in self.mode) or ("Quarterly GSEO KRA" in self.mode):
            writer_summary["Quarterly Audit Count"] = MOSES.getAuditCountForQuarter(self.user_id, self.password, self.start_date, writer_id)
            if writer_summary["Quarterly Audit Count"] > 0:
                if ("Quarterly CFM" in self.mode) or ("Quarterly Stack Rank Index" in self.mode) or ("Quarterly CFM KRA" in self.mode) or ("Quarterly GSEO" in self.mode) or ("Quarterly Stack Rank Index" in self.mode) or ("Quarterly GSEO KRA" in self.mode):
                    writer_summary["Quarterly CFM"], writer_summary["Quarterly GSEO"], fatals = MOSES.getCFMGSEOForQuarter(self.user_id, self.password, self.start_date, writer_id)
                    if type(writer_summary["Quarterly CFM"])!= str:
                        writer_summary["Quarterly CFM KRA"] = self.getQKRA(writer_summary["Quarterly CFM"])
                    if type(writer_summary["Quarterly GSEO"])!= str:
                        writer_summary["Quarterly GSEO KRA"] = self.getQKRA(writer_summary["Quarterly GSEO"])
                if ("Quarterly Stack Rank Index" in self.mode):
                    writer_summary["Quarterly Stack Rank Index"] = self.getStackRankIndex(writer_summary["Quarterly Efficiency"], writer_summary["Quarterly CFM"], writer_summary["Quarterly GSEO"])
        
        if "Half-Yearly Article Count" in self.mode:
            writer_summary["Half-Yearly Article Count"] = MOSES.getArticleCountForHalfYear(self.user_id, self.password, self.start_date, writer_id)
        if ("Half-Yearly Efficiency" in self.mode) or ("Half-Yearly Stack Rank Index" in self.mode) or ("Half-Yearly Efficiency KRA" in self.mode):
            writer_summary["Half-Yearly Efficiency"] = MOSES.getEfficiencyForHalfYear(self.user_id, self.password, self.start_date, writer_id, self.category_tree)
            if (type(writer_summary["Half-Yearly Efficiency"]) != str) and (not math.isnan(writer_summary["Half-Yearly Efficiency"])):
                try:
                    writer_summary["Half-Yearly Efficiency KRA"] = self.getEffKRA(writer_summary["Half-Yearly Efficiency"])
                except:
                    print writer_summary["Half-Yearly Efficiency"]
        if ("Half-Yearly Audit Count Count" in self.mode) or ("Half-Yearly CFM" in self.mode) or ("Half-Yearly GSEO" in self.mode) or ("Half-Yearly Stack Rank Index" in self.mode) or ("Half-Yearly CFM KRA" in self.mode) or ("Half-Yearly GSEO KRA" in self.mode):
            writer_summary["Half-Yearly Audit Count"] = MOSES.getAuditCountForHalfYear(self.user_id, self.password, self.start_date, writer_id)
            if writer_summary["Half-Yearly Audit Count"] > 0:
                if ("Half-Yearly CFM" in self.mode) or ("Half-Yearly Stack Rank Index" in self.mode) or ("Half-Yearly CFM KRA" in self.mode):
                    writer_summary["Half-Yearly CFM"], writer_summary["Half-Yearly GSEO"], fatals = MOSES.getCFMGSEOForHalfYear(self.user_id, self.password, self.start_date, writer_id)
                    if type(writer_summary["Half-Yearly CFM"])!= str:
                        writer_summary["Half-Yearly CFM KRA"] = self.getQKRA(writer_summary["Half-Yearly CFM"])
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
