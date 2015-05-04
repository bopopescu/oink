import time
import datetime
from PyQt4 import QtCore

import MOSES

class PorkKent(QtCore.QThread):
    """A thread for Vindaloo which pulls the team report given two dates.
    It emits a list of dictionaries which corresponds to the team report.
"""
    gotSummary = QtCore.pyqtSignal(list)
    processingSummary = QtCore.pyqtSignal(int, int)
    def __init__(self, user_id, password, start_date, end_date=None):
        super(PorkKent, self).__init__()
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()

        self.user_id = user_id
        self.password = password
        self.start_date = start_date
        if end_date is None:
            self.end_date = self.start_date
        else:
            self.end_date = end_date
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def __del__(self):
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def run(self):
        self.mutex.unlock()
        self.initial_dates = [self.start_date, self.end_date]
        self.current_dates = []
        while True:
            self.initial_dates = [self.start_date, self.end_date]
            if self.current_dates != self.initial_dates:
                self.summarize()
                self.current_dates = self.initial_dates
        print "I should not be here!"
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
        for writer in self.writers:
            self.writer_id = writer["Employee ID"]
            self.writer_name = writer["Name"]
            self.writer_email = writer["Email ID"]
            try:
                writer_summary = self.fetchWriterSummary()
            except Exception, err:
                print "********\nEncountered an error while trying to fetch data for the summary sheet in PorkKent.\nPrinting the error:\n%s\n********" % repr(err)
                time.sleep(5)
                try:
                    writer_summary = self.fetchWriterSummary(1)
                except Exception, err:
                    print "Encounter********\ned an error while trying to fetch data for the summary sheet in PorkKent.\nPrinting the error:\n%s\n********" % repr(err)
                    time.sleep(5)
                    try:
                        writer_summary = self.fetchWriterSummary(2)
                    except Exception, err:
                        print "Encounter********\ned an error while trying to fetch data for the summary sheet in PorkKent.\nPrinting the error:\n%s\n********" % repr(err)
                        time.sleep(5)
                        try:
                            writer_summary = self.fetchWriterSummary(3)
                        except Exception, err:
                            print "Encountered********\n an error while trying to fetch data for the summary sheet in PorkKent.\nPrinting the error:\n%s\n********" % repr(err)
                            raise
            self.summary_data.append(writer_summary)
            done = len(self.summary_data)
            self.processingSummary.emit(done,total)
            self.gotSummary.emit(self.summary_data)
            if self.break_loop:
                self.break_loop = False
                break
    def getSummary(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.break_loop = True
        #print "Successfully changed the dates."
    def fetchWriterSummary(self, retry=None):
        if retry is not None:
            print "Retrying to fetch the data. (trial#%d)" %retry 
        writer_summary = {
            "Report Date": self.end_date,
            "Writer ID": self.writer_id,
            "Writer Name": self.writer_name,
            "Writer Email ID": self.writer_email,
            "Efficiency": MOSES.getEfficiencyFor(self.user_id, self.password, self.end_date, self.writer_id),
            "Average Efficiency": MOSES.getEfficiencyForDateRange(self.user_id, self.password, self.start_date, self.end_date, self.writer_id),
            "Weekly Efficiency": MOSES.getEfficiencyForWeek(self.user_id, self.password, self.end_date, self.writer_id),
            "Monthly Efficiency": MOSES.getEfficiencyForMonth(self.user_id, self.password, self.end_date, self.writer_id),
            "Quarterly Efficiency": MOSES.getEfficiencyForQuarter(self.user_id, self.password, self.end_date, self.writer_id),
            "CFM": MOSES.getCFMFor(self.user_id, self.password, self.end_date, self.writer_id),
            "Average CFM": MOSES.getCFMBetweenDates(self.user_id, self.password, self.start_date, self.end_date, self.writer_id),
            "Weekly CFM": MOSES.getCFMForWeek(self.user_id, self.password, self.end_date, self.writer_id),
            "Monthly CFM": MOSES.getCFMForMonth(self.user_id, self.password, self.end_date, self.writer_id),
            "Quarterly CFM": MOSES.getCFMForQuarter(self.user_id, self.password, self.end_date, self.writer_id),
            "GSEO": MOSES.getGSEOFor(self.user_id, self.password, self.end_date, self.writer_id),
            "Average GSEO": MOSES.getGSEOBetweenDates(self.user_id, self.password, self.start_date, self.end_date, self.writer_id),
            "Weekly GSEO": MOSES.getGSEOForWeek(self.user_id, self.password, self.end_date, self.writer_id),
            "Monthly GSEO": MOSES.getGSEOForMonth(self.user_id, self.password, self.end_date, self.writer_id),
            "Quarterly GSEO": MOSES.getGSEOForQuarter(self.user_id, self.password, self.end_date, self.writer_id),
        }
        return writer_summary

