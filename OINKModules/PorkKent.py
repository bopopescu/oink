from __future__ import division
import time
import datetime
import math
from PyQt4 import QtCore

import MOSES

class PorkKent(QtCore.QThread):
    """A thread for Vindaloo which pulls the team report given two dates.
    It emits a list of dictionaries which corresponds to the team report.
"""
    gotSummary = QtCore.pyqtSignal(list)
    processingSummary = QtCore.pyqtSignal(int, int, datetime.datetime)
    processingStep = QtCore.pyqtSignal(str)
    completedSummary = QtCore.pyqtSignal(bool)
    readyForTeamReport = QtCore.pyqtSignal(list)
    
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
        finished_all_writers = False
        start_time = datetime.datetime.now()
        for writer in self.writers:
            self.writer_id = writer["Employee ID"]
            self.writer_name = writer["Name"]
            self.writer_email = writer["Email ID"]
            try:
                writer_summary = self.fetchWriterSummary()
            except Exception, err:
                print "********\nEncountered an error while trying to fetch data for the summary sheet in PorkKent.\nPrinting the error:\n%s\n********" % repr(err)
                pass
                time.sleep(5)
                try:
                    writer_summary = self.fetchWriterSummary(1)
                except Exception, err:
                    print "********\nEncountered an error while trying to fetch data for the summary sheet in PorkKent.\nPrinting the error:\n%s\n********" % repr(err)
                    pass
                    time.sleep(5)
                    try:
                        writer_summary = self.fetchWriterSummary(2)
                    except Exception, err:
                        print "********\nEncountered an error while trying to fetch data for the summary sheet in PorkKent.\nPrinting the error:\n%s\n********" % repr(err)
                        pass
                        time.sleep(5)
                        try:
                            writer_summary = self.fetchWriterSummary(3)
                        except Exception, err:
                            print "********\nEncountered an error while trying to fetch data for the summary sheet in PorkKent.\nPrinting the error:\n%s\n********" % repr(err)
                            raise
            self.summary_data.append(writer_summary)
            done = len(self.summary_data)
            self.processingSummary.emit(done,total, MOSES.getETA(start_time, done, total))
            self.gotSummary.emit(self.summary_data)
            self.completedSummary.emit(False)
            if self.break_loop:
                self.processingStep.emit("Breaking the loop!")
                break
        if not self.break_loop:
            self.completedSummary.emit(True)
            self.readyForTeamReport.emit(self.summary_data)
            finished_all_writers = True
            self.processingStep.emit("Finished processing data for all writers between %s and %s." % (self.start_date, self.end_date))
        else:
            self.break_loop = False
        #After looping, once the writers' data is done, emit the team summary data.
        #if finished_all_writers:
        #    team_report = self.getTeamReport(self.summary_data)

    def getTeamReport(self, summary_data):
        """Build team report."""
        teams = ["Amrita", "Sherin", "RPD", "Overall"]


    def getSummary(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.break_loop = True
        #print "Successfully changed the dates."

    def fetchWriterSummary(self, retry=None):
        if retry is not None:
            print "Retrying to fetch the data. (trial#%d)" %retry
        self.processingStep.emit("Getting article count for %s for %s." % (self.writer_name, self.end_date))
        article_count = MOSES.getArticleCount(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting average article count for %s between %s and %s." % (self.writer_name, self.start_date, self.end_date))
        a_article_count = MOSES.getArticleCountBetween(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
        self.processingStep.emit("Getting weekly article count for %s for %s." % (self.writer_name, self.end_date))
        w_article_count = MOSES.getArticleCountForWeek(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting monthly article count for %s for %s." % (self.writer_name, self.end_date))
        m_article_count = MOSES.getArticleCountForMonth(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting quarterly article count for %s for %s." % (self.writer_name, self.end_date))
        q_article_count = MOSES.getArticleCountForQuarter(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting quarterly article count for %s for %s." % (self.writer_name, self.end_date))
        hy_article_count = MOSES.getArticleCountForHalfYear(self.user_id, self.password, self.end_date, self.writer_id)
        
        self.processingStep.emit("Getting efficiency for %s for %s." % (self.writer_name, self.end_date))
        efficiency = MOSES.getEfficiencyFor(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting average efficiency for %s between %s and %s." % (self.writer_name, self.start_date, self.end_date))
        a_efficiency = MOSES.getEfficiencyForDateRange(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
        self.processingStep.emit("Getting weekly efficiency for %s for %s." % (self.writer_name, self.end_date))
        w_efficiency = MOSES.getEfficiencyForWeek(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting monthly efficiency for %s for %s." % (self.writer_name, self.end_date))
        m_efficiency = MOSES.getEfficiencyForMonth(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting quarterly efficiency for %s for %s." % (self.writer_name, self.end_date))
        q_efficiency = MOSES.getEfficiencyForQuarter(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting half-yearly efficiency for %s for %s." % (self.writer_name, self.end_date))
        hy_efficiency = MOSES.getEfficiencyForHalfYear(self.user_id, self.password, self.end_date, self.writer_id)
        
        self.processingStep.emit("Getting audit count for %s for %s." % (self.writer_name, self.end_date))
        audit_count = MOSES.getAuditCount(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting average audit count for %s between %s and %s." % (self.writer_name, self.start_date, self.end_date))
        a_audit_count = MOSES.getAuditCountBetween(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
        self.processingStep.emit("Getting weekly audit count for %s for %s." % (self.writer_name, self.end_date))
        w_audit_count = MOSES.getAuditCountForWeek(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting monthly audit count for %s for %s." % (self.writer_name, self.end_date))
        m_audit_count = MOSES.getAuditCountForMonth(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting quarterly audit count for %s for %s." % (self.writer_name, self.end_date))
        q_audit_count = MOSES.getAuditCountForQuarter(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting quarterly audit count for %s for %s." % (self.writer_name, self.end_date))
        hy_audit_count = MOSES.getAuditCountForHalfYear(self.user_id, self.password, self.end_date, self.writer_id)
        
        self.processingStep.emit("Getting CFM for %s for %s." % (self.writer_name, self.end_date))
        cfm = MOSES.getCFMFor(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting average CFM for %s between %s and %s." % (self.writer_name, self.start_date, self.end_date))
        a_cfm = MOSES.getCFMBetweenDates(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
        self.processingStep.emit("Getting weekly CFM for %s for %s." % (self.writer_name, self.end_date))
        w_cfm = MOSES.getCFMForWeek(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting monthly CFM for %s for %s." % (self.writer_name, self.end_date))
        m_cfm = MOSES.getCFMForMonth(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting quarterly CFM for %s for %s." % (self.writer_name, self.end_date))
        q_cfm = MOSES.getCFMForQuarter(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting quarterly CFM for %s for %s." % (self.writer_name, self.end_date))
        hy_cfm = MOSES.getCFMForHalfYear(self.user_id, self.password, self.end_date, self.writer_id)
        
        self.processingStep.emit("Getting GSEO for %s for %s." % (self.writer_name, self.end_date))
        gseo = MOSES.getGSEOFor(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting GSEO for %s between %s and %s." % (self.writer_name, self.start_date, self.end_date))
        a_gseo = MOSES.getGSEOBetweenDates(self.user_id, self.password, self.start_date, self.end_date, self.writer_id)
        self.processingStep.emit("Getting weekly GSEO for %s for %s." % (self.writer_name, self.end_date))
        w_gseo = MOSES.getGSEOForWeek(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting average GSEO for %s between %s and %s." % (self.writer_name, self.start_date, self.end_date))
        m_gseo = MOSES.getGSEOForMonth(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting quarterly GSEO for %s for %s." % (self.writer_name, self.end_date))
        q_gseo = MOSES.getGSEOForQuarter(self.user_id, self.password, self.end_date, self.writer_id)
        self.processingStep.emit("Getting half-yearly GSEO for %s for %s." % (self.writer_name, self.end_date))
        hy_gseo = MOSES.getGSEOForHalfYear(self.user_id, self.password, self.end_date, self.writer_id)
        
        self.processingStep.emit("Getting Team Leader Name for %s for %s." % (self.writer_name, self.end_date))
        writer_tl = MOSES.getReportingManager(self.user_id, self.password, query_user=self.writer_id, query_date=self.end_date)["Reporting Manager Name"]
        self.processingStep.emit("Getting Stack Rank Indices for %s for %s." % (self.writer_name, self.end_date))
        stack_rank_index = self.getStackRankIndex(efficiency, cfm, gseo)
        a_stack_rank_index = self.getStackRankIndex(a_efficiency, a_cfm, a_gseo)
        w_stack_rank_index = self.getStackRankIndex(w_efficiency, w_cfm, w_gseo)
        m_stack_rank_index = self.getStackRankIndex(m_efficiency, m_cfm, m_gseo)
        q_stack_rank_index = self.getStackRankIndex(q_efficiency, q_cfm, q_gseo)
        hy_stack_rank_index = self.getStackRankIndex(hy_efficiency, hy_cfm, hy_gseo)
        self.processingStep.emit("Building final writer stats data for %s for %s." % (self.writer_name, self.end_date))
        
        writer_summary = {
            "Report Date": self.end_date,
            "Writer ID": self.writer_id,
            "Writer Name": self.writer_name,
            "Writer Email ID": self.writer_email,
            "Reporting Manager": writer_tl,
            "Article Count": article_count,
            "Weekly Article Count": w_article_count,
            "Monthly Article Count": m_article_count,
            "Quarterly Article Count": q_article_count,
            "Half-Yearly Article Count": hy_article_count,
            "Average Article Count": a_article_count,
            "Efficiency": efficiency,
            "Weekly Efficiency": w_efficiency,
            "Monthly Efficiency": m_efficiency,
            "Quarterly Efficiency": q_efficiency,
            "Half-Yearly Efficiency": hy_efficiency,
            "Average Efficiency": a_efficiency,
            "Audit Count": audit_count,
            "Weekly Audit Count": w_audit_count,
            "Monthly Audit Count": m_audit_count,
            "Quarterly Audit Count": q_audit_count,
            "Half-Yearly Audit Count": hy_audit_count,
            "Average Audit Count": a_audit_count,
            "CFM": cfm,
            "Weekly CFM": w_cfm,
            "Monthly CFM": m_cfm,
            "Quarterly CFM": q_cfm,
            "Half-Yearly CFM": hy_cfm,
            "Average CFM": a_cfm,
            "GSEO": gseo,
            "Weekly GSEO": w_gseo,
            "Monthly GSEO": m_gseo,
            "Quarterly GSEO": q_gseo,
            "Half-Yearly GSEO": hy_gseo,
            "Average GSEO": a_gseo,
            "Stack Rank Index": stack_rank_index,
            "Weekly Stack Rank Index": w_stack_rank_index,
            "Monthly Stack Rank Index": m_stack_rank_index,
            "Quarterly Stack Rank Index": q_stack_rank_index,
            "Half-Yearly Stack Rank Index": hy_stack_rank_index,
            "Average Stack Rank Index": a_stack_rank_index
        }
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


