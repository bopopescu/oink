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

    def __init__(self, userID, password, start_date, end_date=None, query_user=None, mode=None, parent=None):
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
        elif mode in [0, 1, 2]:
            self.mode = mode
        else:
            self.mode = 0
            print "Error with the Porker Mode."

        self.process_date = self.start_date
        
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
        self.mutex.unlock()
        #work_status = MOSES.getWorkingStatus(self.userID, self.password, self.start_date, self.end_date, self.query_user) 
        #Find out if the person/company is working on the given date.
        self.modes = [self.broadcastEfficiency, self.broadcastDatesData, self.dualMode]
        self.old_efficiency = 0.0
        self.current_datesData = {}
        self.old_datesData = {}
        while True:
            #print "Running some mode?"
            self.modes[self.mode]()
            #time.sleep(1)
        self.mutex.lock()

    def broadcastEfficiency(self):
        #print "In mode 0"
        self.current_efficiency = MOSES.getEfficiencyForDateRange(self.userID, self.password, self.start_date, self.end_date, self.query_user)
        if self.old_efficiency != self.current_efficiency:
            #print "Sending efficiency"
            self.sendEfficiency.emit(self.current_efficiency)
            self.old_efficiency = self.current_efficiency
            
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
        for each_date in self.dates_list:
            if MOSES.isWorkingDay(self.userID, self.password, each_date):
                status, relaxation = MOSES.getWorkingStatus(self.userID, self.password, each_date)
                if status == "Working" and relaxation >= 0.0:
                    efficiency = MOSES.getEfficiencyFor(self.userID, self.password, each_date)
                else:
                    efficiency = 0.0
            else:
                status = "Holiday"
                relaxation = "NA"
                efficiency = 0.0
            self.current_datesData.update({each_date:[status, relaxation, efficiency]})
        if self.current_datesData != self.old_datesData:
            self.sendDatesData.emit(self.current_datesData)
    
    def dualMode(self):
        #print "Running mode 2"
        self.broadcastEfficiency()
        self.broadcastDatesData()

    def getEfficiency(self):
        #work_status = MOSES.getWorkStatus() #Find out if the person/company is working on the given date.
        current_efficiency = MOSES.getEfficiencyForDateRange(self.userID, self.password, self.start_date, self.end_date, self.query_user)
        self.sendEfficiency.emit(current_efficiency)

    def setDate(self, new_date):
        self.start_date = new_date
        self.end_date = new_date
    
    def setVisibleDates(self, new_date):
        self.process_date = new_date
        #self.broadcastDatesData()
    
    def getStatsData(self, new_date):
        """This method is used with the Writer Statistics table. It takes a date and emits a dictionary containing all the data for
        the last working date for the given user."""
        last_working_date = MOSES.getLastWorkingDate(self.userID, self.password, new_date)
        current_week = OINKM.getWeekNum(last_working_date)
        current_month = OINKM.getMonth(last_working_date)
        current_quarter = OINKM.getQuarter(last_working_date)
        current_half_year = OINKM.getHalfYear(last_working_date)
        
        lwd_efficiency = MOSES.getEfficiencyFor(self.userID, self.password, last_working_date)
        if lwd_efficiency is None:
            lwd_efficiency = "-"
        else:
            lwd_efficiency *= 100.00
        lwd_gseo = MOSES.getGSEOFor(self.userID, self.password, last_working_date)
        if lwd_gseo is None:
            lwd_gseo = "-"
        else:
            lwd_gseo *= 100.00

        lwd_cfm = MOSES.getCFMFor(self.userID, self.password, last_working_date)
        if lwd_cfm is None:
            lwd_cfm = "-"
        else:
            lwd_cfm *= 100.00

        cw_efficiency = MOSES.getEfficiencyForWeek(self.userID, self.password, last_working_date)
        if cw_efficiency is None:
            cw_efficiency = "-"
        else:
            cw_efficiency *= 100.00
        
        cw_gseo = MOSES.getGSEOForWeek(self.userID, self.password, last_working_date)
        if cw_gseo is None:
            cw_gseo = "-"
        else:
            cw_gseo *= 100.00
        
        cw_cfm = MOSES.getCFMForWeek(self.userID, self.password, last_working_date)
        if cw_cfm is None:
            cw_cfm = "-"
        else:
            cw_cfm *= 100.00

        cm_efficiency = MOSES.getEfficiencyForMonth(self.userID, self.password, last_working_date)
        if cm_efficiency is None:
            cm_efficiency = "-"
        else:
            cm_efficiency *= 100.00

        cm_gseo = MOSES.getGSEOForMonth(self.userID, self.password, last_working_date)
        if cm_gseo is None:
            cm_gseo = "-"
        else:
            cm_gseo *= 100.00

        cm_cfm = MOSES.getCFMForMonth(self.userID, self.password, last_working_date)
        if cm_cfm is None:
            cm_cfm = "-"
        else:
            cm_cfm *= 100.00

        cq_efficiency = MOSES.getEfficiencyForQuarter(self.userID, self.password, last_working_date)
        if cq_efficiency is None:
            cq_efficiency = "-"
        else:
            cq_efficiency *= 100.00

        cq_gseo = MOSES.getGSEOForQuarter(self.userID, self.password, last_working_date)
        if cq_gseo is None:
            cq_gseo = "-"
        else:
            cq_gseo *= 100.00

        cq_cfm = MOSES.getCFMForQuarter(self.userID, self.password, last_working_date)
        if cq_cfm is None:
            cq_cfm = "-"
        else:
            cq_cfm *= 100.00

        chy_efficiency = MOSES.getEfficiencyForHalfYear(self.userID, self.password, last_working_date)
        if chy_efficiency is None:
            chy_efficiency = "-"
        else:
            chy_efficiency *= 100.00

        chy_gseo = MOSES.getGSEOForHalfYear(self.userID, self.password, last_working_date)
        if chy_gseo is None:
            chy_gseo = "-"
        else:
            chy_gseo *= 100.00

        chy_cfm = MOSES.getCFMForHalfYear(self.userID, self.password, last_working_date)
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

    def setStartDate(self, new_date):
        self.start_date = new_date

    def setEndDate(self, new_date):
        self.end_date = new_date

    def setQueryUser(self, new_user):
        self.query_user = new_user
    