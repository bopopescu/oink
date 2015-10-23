import time
import calendar
import datetime

from PyQt4 import QtCore

import OINKMethods as OINKM
import MOSES

class Porker(QtCore.QThread):
    """This class emits the work status and efficiency for a user for a specific date."""
    sendEfficiency = QtCore.pyqtSignal(float)
    sendEfficiencyNonContinous = QtCore.pyqtSignal(float)
    sendDatesData = QtCore.pyqtSignal(dict)
    sendStatsData = QtCore.pyqtSignal(dict)
    sendActivity = QtCore.pyqtSignal(str, datetime.datetime, bool)

    def __init__(self, userID, password, start_date, end_date=None, query_user=None, mode=None, category_tree=None, parent=None):
        """Modes :
            0. Default, this emits sendEfficiency.
            1. Used with WeekCalendar. This emits a dictionary with dates for keys 
               and a list of [workstatus, relaxation, efficiency] for values.
            2. Emits both sendEfficiency and sendDatesData. Used in Pork to get the information a single thread.
        """
        super(Porker, self).__init__(parent)
        self.userID = userID
        self.password = password
        self.start_date = start_date
        if end_date is None:
            self.end_date = self.start_date
        else:
            self.end_date = end_date

        if mode is None:
            self.mode = 0
        elif mode in [0, 1, 2, 3]:
            self.mode = mode
        else:
            self.mode = 0
            print "Error with the Porker Mode."
        if category_tree is not None:
            self.category_tree=category_tree
        else:
            self.category_tree = MOSES.getCategoryTree(self.userID, self.password)

        self.process_date = self.start_date
        self.stats_date = self.start_date
        if query_user is None:
            self.query_user = self.userID
        else:
            self.query_user = query_user
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
        """As soon as this loads, emit everything."""
        self.mutex.unlock()
        #Find out if the person/company is working on the given date.
        self.modes = [self.broadcastEfficiency, self.broadcastDatesData, self.dualMode]
        self.old_efficiency = 0.0
        self.current_datesData = {}
        self.old_datesData = {}
        self.sentDatesData = False #Allow emitting this.
        self.sentStatsData = False #Allow emitting this.
        while True:
            self.start_time = datetime.datetime.now()
            #print "Running mode:", self.mode
            if self.mode in [0, 1, 2]:
                self.modes[self.mode]()
                self.sendActivity.emit("Completed",datetime.datetime.now(), True)
            else:
                self.dualMode()
                if not self.sentStatsData:
                    self.getStatsData()
                    self.sendActivity.emit("Completed",datetime.datetime.now(), True)
            #time.sleep(1)
        self.mutex.lock()

    def dualMode(self):
        self.broadcastEfficiency()
        if not self.sentDatesData:
            self.broadcastDatesData()

    def broadcastEfficiency(self):
        #print "I'm in broadcastEfficiency"
        if self.start_date == self.end_date:
            if self.start_date in self.current_datesData.keys():
                #If this has been already calculated, why bother?
                self.current_efficiency = self.current_datesData[self.start_date][2]
            else:
                #print "Here0"
                self.current_efficiency = MOSES.getEfficiencyForDateRange(self.userID, self.password, self.start_date, self.end_date, self.query_user, category_tree=self.category_tree)
                #print "Here00"
        #print "Here"
        self.current_efficiency = MOSES.getEfficiencyForDateRange(self.userID, self.password, self.start_date, self.end_date, self.query_user, category_tree=self.category_tree)
        #print "Here2"
        if self.old_efficiency != self.current_efficiency:
            #Since the efficiency seems to have changed, resend all.
            #print "Here3"
            self.sentDatesData = False
            self.sentStatsData = False
            self.sendEfficiency.emit(self.current_efficiency)
            self.old_efficiency = self.current_efficiency
            #print "Here4"
            self.sendActivity.emit("Refreshed efficiency. Moving on to next process.", MOSES.getETA(self.start_time, 2, 3), False)
        #print "I'm leaving broadcastEfficiency"

            
    def broadcastDatesData(self):
        #print "Running mode 1"
        self.process_month = self.process_date.month
        self.process_year = self.process_date.year
        self.process_month_first = 1
        self.process_month_last = calendar.monthrange(self.process_year, self.process_month)[1]
#        self.month_first = datetime.date(self.process_year, 1, 30)
#        self.month_last = datetime.date(self.process_year, 12, 31)
        self.month_first = OINKM.getMonday(datetime.date(self.process_year, self.process_month, self.process_month_first))

        self.month_last = self.month_first + datetime.timedelta(40)
        #datetime.date(self.process_year, self.process_month, self.process_month_last)

        self.dates_list = OINKM.getDatesBetween(self.month_first, self.month_last)
        start_time = datetime.datetime.now()
        total = len(self.dates_list)
        counter = 0
        #print self.dates_list
        for each_date in self.dates_list:
            if MOSES.isWorkingDay(self.userID, self.password, each_date):
                status, relaxation = MOSES.getWorkingStatus(self.userID, self.password, each_date)
                if status == "Working" and relaxation >= 0.0:
                    efficiency = MOSES.getEfficiencyFor(self.userID, self.password, each_date, category_tree=self.category_tree)
                else:
                    efficiency = 0.0
            else:
                status = "Holiday"
                relaxation = "NA"
                efficiency = 0.0
            counter += 1
            eta = MOSES.getETA(start_time, counter, total)
            cfm = MOSES.getCFMFor(self.userID, self.password, each_date)
            gseo = MOSES.getGSEOFor(self.userID, self.password, each_date)
            #print cfm, gseo
            self.sendActivity.emit("Refreshing Current Calendar Page (%d/%d)."%(counter,total), eta, False)
            self.current_datesData.update({each_date:[status, relaxation, efficiency, cfm, gseo]})
        if self.current_datesData != self.old_datesData:
            self.sendDatesData.emit(self.current_datesData)
            self.sendActivity.emit("Compiled Calendar Dates Data. Moving on to next process.", MOSES.getETA(self.start_time,1,3), False)
        self.sentDatesData = True
        if self.sentStatsData == True:
            self.sendActivity.emit("Completed",datetime.datetime.now(), True)

    def getStatsData(self):
        """This method is used with the Writer Statistics table. It takes a date and emits a dictionary containing all the data for
        the last working date for the given user."""
        start_time = datetime.datetime.now()
        self.sendActivity.emit("Refreshing stats table.", MOSES.getETA(self.start_time,2,3), False)
        no_of_steps = 30 #There are ~17 steps in this function, but some of the later steps will take doubly as long. Hence the increased step count.
        last_working_date = MOSES.getLastWorkingDate(self.userID, self.password, self.stats_date)
        self.sendActivity.emit("Calculated last working date.", MOSES.getETA(start_time, 1, no_of_steps), False)
        current_week = OINKM.getWeekNum(last_working_date)
        current_month = OINKM.getMonth(last_working_date)
        current_quarter = OINKM.getQuarter(last_working_date)
        current_half_year = OINKM.getHalfYear(last_working_date)
        
        if last_working_date in  self.current_datesData.keys():
            #If this is already calculated, why bother recalculating, right?
            lwd_efficiency = self.current_datesData[last_working_date][2]
            #print "Found %f for %s." %(lwd_efficiency, last_working_date)
        else:
            lwd_efficiency = MOSES.getEfficiencyFor(self.userID, self.password, last_working_date, category_tree=self.category_tree)
        self.sendActivity.emit("Got the efficiency for the last working date.", MOSES.getETA(start_time, 2, no_of_steps), False)
        if lwd_efficiency is None:
            lwd_efficiency = "-"
        else:
            lwd_efficiency *= 100.00
        lwd_gseo = MOSES.getGSEOFor(self.userID, self.password, last_working_date)
        self.sendActivity.emit("Got the GSEO for the last working date.", MOSES.getETA(start_time, 3, no_of_steps), False)

        if lwd_gseo is None:
            lwd_gseo = "-"
        else:
            lwd_gseo *= 100.00

        lwd_cfm = MOSES.getCFMFor(self.userID, self.password, last_working_date)
        self.sendActivity.emit("Got the CFM for the last working date.", MOSES.getETA(start_time, 4, no_of_steps), False)
        if lwd_cfm is None:
            lwd_cfm = "-"
        else:
            lwd_cfm *= 100.00

        cw_efficiency = MOSES.getEfficiencyForWeek(self.userID, self.password, last_working_date, category_tree=self.category_tree)
        self.sendActivity.emit("Got the efficiency for the week.", MOSES.getETA(start_time, 5, no_of_steps), False)
        if cw_efficiency is None:
            cw_efficiency = "-"
        else:
            cw_efficiency *= 100.00
        
        cw_gseo = MOSES.getGSEOForWeek(self.userID, self.password, last_working_date)
        self.sendActivity.emit("Got the GSEO for the week.", MOSES.getETA(start_time, 6, no_of_steps), False)
        if cw_gseo is None:
            cw_gseo = "-"
        else:
            cw_gseo *= 100.00
        
        cw_cfm = MOSES.getCFMForWeek(self.userID, self.password, last_working_date)
        self.sendActivity.emit("Got the CFM for the week.", MOSES.getETA(start_time, 7, no_of_steps), False)

        if cw_cfm is None:
            cw_cfm = "-"
        else:
            cw_cfm *= 100.00

        cm_efficiency = MOSES.getEfficiencyForMonth(self.userID, self.password, last_working_date, category_tree=self.category_tree)
        #This is where the lag starts, so increasing the counter in steps of 2
        self.sendActivity.emit("Got the efficiency for the month.", MOSES.getETA(start_time, 9, no_of_steps), False)
        
        if cm_efficiency is None:
            cm_efficiency = "-"
        else:
            cm_efficiency *= 100.00

        cm_gseo = MOSES.getGSEOForMonth(self.userID, self.password, last_working_date)
        self.sendActivity.emit("Got the GSEO for the month.", MOSES.getETA(start_time, 11, no_of_steps), False)
        if cm_gseo is None:
            cm_gseo = "-"
        else:
            cm_gseo *= 100.00

        cm_cfm = MOSES.getCFMForMonth(self.userID, self.password, last_working_date)
        self.sendActivity.emit("Got the CFM for the month.", MOSES.getETA(start_time, 13, no_of_steps), False)

        if cm_cfm is None:
            cm_cfm = "-"
        else:
            cm_cfm *= 100.00

        cq_efficiency = MOSES.getEfficiencyForQuarter(self.userID, self.password, last_working_date, category_tree=self.category_tree)
        self.sendActivity.emit("Got the efficiency for the quarter.", MOSES.getETA(start_time, 15, no_of_steps), False)
        if cq_efficiency is None:
            cq_efficiency = "-"
        else:
            cq_efficiency *= 100.00

        cq_gseo = MOSES.getGSEOForQuarter(self.userID, self.password, last_working_date)
        self.sendActivity.emit("Got the GSEO for the quarter.", MOSES.getETA(start_time, 15, no_of_steps), False)
        if cq_gseo is None:
            cq_gseo = "-"
        else:
            cq_gseo *= 100.00

        cq_cfm = MOSES.getCFMForQuarter(self.userID, self.password, last_working_date)
        self.sendActivity.emit("Got the CFM for the quarter.", MOSES.getETA(start_time, 17, no_of_steps), False)
        if cq_cfm is None:
            cq_cfm = "-"
        else:
            cq_cfm *= 100.00

        chy_efficiency = MOSES.getEfficiencyForHalfYear(self.userID, self.password, last_working_date, category_tree=self.category_tree)
        self.sendActivity.emit("Got the Efficiency for the half-year.", MOSES.getETA(start_time, 22, no_of_steps), False)
        if chy_efficiency is None:
            chy_efficiency = "-"
        else:
            chy_efficiency *= 100.00

        chy_gseo = MOSES.getGSEOForHalfYear(self.userID, self.password, last_working_date)
        self.sendActivity.emit("Got the GSEO for the half-year.", MOSES.getETA(start_time, 26, no_of_steps), False)
        if chy_gseo is None:
            chy_gseo = "-"
        else:
            chy_gseo *= 100.00

        chy_cfm = MOSES.getCFMForHalfYear(self.userID, self.password, last_working_date)
        self.sendActivity.emit("Got the GSEO for the half-year.", MOSES.getETA(start_time, 30, no_of_steps), False)
        if chy_cfm is None:
            chy_cfm = "-"
        else:
            chy_cfm *= 100.00


        stats_data = {
        "LWD": last_working_date,
        "Current Week": current_week,
        "Current Month": current_month,
        "Current Quarter": current_quarter,
        "Current Half Year": current_half_year,
        "LWD Efficiency": lwd_efficiency,
        "LWD GSEO": lwd_gseo,
        "LWD CFM": lwd_cfm,
        "CW Efficiency": cw_efficiency,
        "CW GSEO": cw_gseo,
        "CW CFM": cw_cfm,
        "CM Efficiency": cm_efficiency,
        "CM GSEO": cm_gseo,
        "CM CFM": cm_cfm,
        "CQ Efficiency": cq_efficiency,
        "CQ GSEO": cq_gseo,
        "CQ CFM": cq_cfm,
        "CHY Efficiency": chy_efficiency,
        "CHY GSEO": chy_gseo,
        "CHY CFM": chy_cfm
        }
        self.sendStatsData.emit(stats_data)
        self.sendActivity.emit("Refreshed stats data.", MOSES.getETA(self.start_time, 3, 3), False)
        self.sentStatsData = True

    def getEfficiency(self):
        #work_status = MOSES.getWorkStatus() #Find out if the person/company is working on the given date.
        current_efficiency = MOSES.getEfficiencyForDateRange(self.userID, self.password, self.start_date, self.end_date, self.query_user, category_tree=self.category_tree)
        self.sendEfficiency.emit(current_efficiency)

    def setDate(self, new_date):
        self.start_date = new_date
        self.end_date = new_date
    
    def setVisibleDates(self, new_date):
        self.process_date = new_date
        #self.broadcastDatesData()

    def setStartDate(self, new_date):
        self.start_date = new_date

    def setEndDate(self, new_date):
        self.end_date = new_date

    def setQueryUser(self, new_user):
        self.query_user = new_user
    