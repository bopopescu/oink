from __future__ import division 
import time
import math
import calendar
import datetime

from PyQt4 import QtCore
import pandas as pd

import OINKMethods as OINKM
import MOSES

class Porker(QtCore.QThread):
    """This class emits the work status and efficiency for a user for a specific date."""
    #Send the result
    sendResultDictionary = QtCore.pyqtSignal(dict)
    #Send a message, alert_bool, progress_value, possible_eta
    sendActivityMessage = QtCore.pyqtSignal(str, bool, int, datetime.datetime)
    sendStats = QtCore.pyqtSignal(pd.DataFrame)

    def __init__(self, user_id, password, start_date, end_date=None, category_tree=None, *args, **kwargs):
        """New version.
        """
        super(Porker, self).__init__(*args, **kwargs)
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()

        self.user_id, self.password = user_id, password

        self.start_date = start_date
        self.stats_date = start_date
        self.stats_data = {}
        #Prepare a list of dates to process.
        l_span = 300
        r_span = 15
        self.process_dates = list(reversed(OINKM.getDatesBetween((start_date-datetime.timedelta(days=l_span)), start_date))) + OINKM.getDatesBetween((start_date+datetime.timedelta(days=1)), (start_date+datetime.timedelta(days=r_span)))

        self.queue = []
        self.force_update_dates = []
        #Preload the category_tree.
        self.result_dictionary = {}

        if category_tree is not None:
            self.category_tree = category_tree
        else:
            self.category_tree = MOSES.getCategoryTree(self.user_id, self.password)


        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def __del__(self):
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def run(self):
        """First, build a dataframe for all the dates in the calendar month. It should emit, stage by stage.
        1. Build a dictionary with dates for keys. The structure is:
            {
                datetime.date(): {
                    efficiency,
                    work_status,
                    relaxation,
                    cfm,
                    gseo,
                    fatals,
                    stats_table
                }
            }
        2. Update this dictionary for each of the dates in the process_dates list. 
        3. Keep looping through this list, removing the date once it's been processed.
        4. Whenever an action in OINK requires that a particular date's values are to be updated,
        pass that to the self.updateForDate(), and that value will be appended to the list.
        """
        while True:
            self.mutex.unlock()
            #print "Starting one set. %s."%datetime.datetime.now()
            self.computeProcessDates()
            #print "Finished one set. %s."%datetime.datetime.now()
            self.mutex.lock()

    def canSkipThisDate(self, query_date):
        #Checks if a given date needs to be processed or not, depending on if it's been previously answered, or if it's been specifically requested in the force update list.
        processed_dates = self.getProcessedDates()
        return ((query_date in processed_dates) and (query_date not in self.force_update_dates))

    def computeProcessDates(self):
        #For each index:
        for processing_date in self.process_dates:
            processed_dates = self.getProcessedDates()

            efficiency = None
            cfm = None
            gseo = None
            fatals = None
            status = None
            relaxation = None
            approval = None
            stats = None

            if self.canSkipThisDate(processing_date):
                efficiency = self.result_dictionary[processing_date].get("Efficiency")
                cfm = self.result_dictionary[processing_date].get("CFM")
                gseo = self.result_dictionary[processing_date].get("GSEO")
                fatals = self.result_dictionary[processing_date].get("Fatals")
                status = self.result_dictionary[processing_date].get("Status")
                relaxation = self.result_dictionary[processing_date].get("Relaxation")
                approval = self.result_dictionary[processing_date].get("Approval")
                
            if efficiency is None:
                efficiency = MOSES.getEfficiencyFor(self.user_id, self.password, processing_date, category_tree=self.category_tree)
            
            if (cfm is None) or (gseo is None) or (fatals is None):
                cfm, gseo, fatals = MOSES.getCFMGSEOFor(self.user_id, self.password, processing_date)
            
            if (status is None) or (relaxation is None) or (approval is None):
                status, relaxation, approval = MOSES.checkWorkStatus(self.user_id, self.password, processing_date)

            processing_dict_entry = {
                                    processing_date:
                                                {
                                                    "Efficiency": efficiency,
                                                    "Status":status,
                                                    "Relaxation": relaxation,
                                                    "Approval": approval,
                                                    "CFM": cfm,
                                                    "GSEO": gseo,
                                                    "Fatals": fatals,
                                                }
                                    }
            self.result_dictionary.update(processing_dict_entry)
            self.sendResultDictionary.emit(self.result_dictionary)
            self.sendStatsAfterUpdatingIfNecessary()

        #Flush the force_update list and the process_list.
        for each_date in self.getProcessedDates():
            if each_date in self.force_update_dates:
                self.force_update_dates.remove(each_date)
            if each_date in self.process_dates:
                self.process_dates.remove(each_date)

        self.process_dates.extend(list(reversed(sorted(set(self.queue)))))

        if len(self.process_dates)>0: 
            print self.process_dates
        self.queue = []

    def sendStatsAfterUpdatingIfNecessary(self):
        stats = self.stats_data.get(self.stats_date)
        if stats is None:
            self.updateStats()
            stats = self.stats_data[self.stats_date]
        #else:
        #    row_count = len(stats.index)
        #    if (row_count in [1,2,3,4]):
        #        self.updateStats()
        #        stats = self.stats_data[self.stats_date]     
        self.sendStats.emit(stats)

    def updateStats(self):
        self.stats_data.update({self.stats_date: self.getWriterStatsForDate(self.stats_date)})

    def getStatsFor(self, query_date):
        self.stats_date = query_date

    def updateForDate(self, queried_date):
        if queried_date not in self.process_dates: self.queue.append(queried_date)
        self.force_update_dates.append(queried_date)

    def getProcessedDates(self):
        return self.result_dictionary.keys()

    def getEfficiencyFor(self, query_date):
        efficiency = None
        if query_date in self.getProcessedDates():
            efficiency = self.result_dictionary[query_date].get("Efficiency")
        if efficiency is None:
            self.updateForDate(query_date)
            efficiency = 0        
        return efficiency

    def extendDates(self, extension_date):
        processed_dates = self.getProcessedDates()
        earliest_date = min(processed_dates)
        last_date = max(processed_dates)
        success = False
        if extension_date < earliest_date:
            dates_list = (list(reversed(OINKM.getDatesBetween(extension_date, earliest_date))))
            success = True
        elif extension_date > last_date:
            dates_list = (list(reversed(OINKM.getDatesBetween(last_date, extension_date))))
            success = True
        #else:
            #print extension_date," failed for some reason."
        if success:
            for date_ in dates_list:
                self.updateForDate(date_)
        return success

    def getWriterStatsForDate(self, query_date):
        lwd = MOSES.getLastWorkingDate(self.user_id, self.password, query_date)
        lwd_efficiency = None
        lwd_cfm, lwd_gseo, lwd_fatals = None, None, None
        previous_dictionary = self.result_dictionary.get(lwd)

        if lwd in self.getProcessedDates():
            lwd_efficiency = previous_dictionary.get("Efficiency")
            lwd_cfm = previous_dictionary.get("CFM")
            lwd_gseo = previous_dictionary.get("GSEO")
            lwd_fatals = previous_dictionary.get("Fatals")
        
        
        if lwd_efficiency is None:
            self.updateEfficiencyForDate(lwd)
            previous_dictionary = self.result_dictionary.get(lwd)
            lwd_efficiency = previous_dictionary.get("Efficiency")

        
        if lwd_cfm is None or lwd_gseo is None or lwd_fatals is None:
            self.updateQualityForDate(lwd)
            previous_dictionary = self.result_dictionary.get(lwd)
            lwd_cfm = previous_dictionary.get("CFM")
            lwd_gseo = previous_dictionary.get("GSEO")
            lwd_fatals = previous_dictionary.get("Fatals")

        stats_keys = ["Time Frame", "Efficiency", "CFM", "GSEO"]
        lwd_stats = [lwd, lwd_efficiency, lwd_cfm, lwd_gseo]

        first_date_of_week = MOSES.getFirstDayOfWeek(lwd)
        if first_date_of_week == lwd:
            cw_stats = lwd_stats
        else:
            cw_efficiency = MOSES.getEfficiencyForWeek(self.user_id, self.password, lwd, category_tree=self.category_tree)
            cw_cfm, cw_gseo, cw_fatals = MOSES.getCFMGSEOForWeek(self.user_id, self.password, lwd)

        cw_stats = ["Week #%d"%lwd.isocalendar()[1], cw_efficiency, cw_cfm, cw_gseo]

        cm_efficiency = MOSES.getEfficiencyForMonth(self.user_id, self.password, lwd, category_tree=self.category_tree)
        cm_cfm, cm_gseo, cm_fatals = MOSES.getCFMGSEOForMonth(self.user_id, self.password, lwd)
        
        cm_stats = ["Month: %s"%lwd.strftime("%b"), cm_efficiency, cm_cfm, cm_gseo]
        stats = [lwd_stats, cw_stats, cm_stats]
        return pd.DataFrame(stats, columns=stats_keys)
    
    def updateEfficiencyForDate(self, query_date):
        previous_dictionary = self.result_dictionary.get(query_date)
        efficiency = MOSES.getEfficiencyFor(self.user_id, self.password, query_date, category_tree=self.category_tree)
        updated_dict = {"Efficiency": efficiency}
        if previous_dictionary is not None:
            previous_dictionary.update(updated_dict)
        else:
            self.result_dictionary[query_date] = updated_dict

    def updateQualityForDate(self, query_date):
        previous_dictionary = self.result_dictionary.get(query_date)
        cfm, gseo, fatals = MOSES.getCFMGSEOFor(self.user_id, self.password, query_date)
        updated_dict = {"CFM": cfm, "GSEO": gseo, "Fatals": fatals}
        if previous_dictionary is not None:
            previous_dictionary.update(updated_dict)
        else:
            self.result_dictionary[query_date] = updated_dict

    def getEfficiencyForDateRange(start_date, end_date):
        pass