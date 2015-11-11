import time
import itertools
import MOSES
from PyQt4 import QtCore

class PiggyBanker(QtCore.QThread):
    piggybankChanged = QtCore.pyqtSignal(list, list)

    def __init__(self, user_id, password, start_date, end_date = None, query_dict = None, category_tree = None, parent = None):
        super(PiggyBanker, self).__init__(parent)
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.user_id = user_id
        self.password = password
        self.sleeper = 10
        self.start_date = start_date
        if query_dict is None:
            #get all data for a writer between dates if only dates are given.
            self.query_dict = {"WriterID": self.user_id}
        else:
            #If some query dictionary is supplied, get all data corresponding to that.
            self.query_dict = query_dict
        if end_date is None:
            self.end_date = self.start_date
        else:
            self.end_date = end_date
        if category_tree is None:
            self.category_tree = MOSES.getCategoryTree(self.user_id, self.password)
        else:
            self.category_tree = category_tree
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def __del__(self):
        self.mutex.lock()
        #self.abort = True
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def setStartDate(self, start_date):
        #print "Changing PiggyBanker start_Date to %s" %start_date
        self.start_date = start_date
        
    def setEndDate(self, end_date):
        #print "Changing PiggyBanker end_Date to %s" %end_date
        self.end_date = end_date
    
    def setDate(self, new_date):
        self.start_date = new_date
        self.end_date = new_date

    def setQueryDict(self, query_dict):
        self.query_dict = query_dict
    
    def run(self):
        self.mutex.unlock()
        current_data = []
        self.past_data = []
        while True:
            try:
                data = MOSES.getPiggyBankDataBetweenDates(self.start_date, self.end_date, self.query_dict, self.user_id, self.password)
            except:
                try:
                    time.sleep(self.sleeper)
                    data = MOSES.getPiggyBankDataBetweenDates(self.start_date, self.end_date, self.query_dict, self.user_id, self.password)
                except:
                    try:
                        time.sleep(self.sleeper)
                        data = MOSES.getPiggyBankDataBetweenDates(self.start_date, self.end_date, self.query_dict, self.user_id, self.password)
                    except:
                        try:
                            time.sleep(self.sleeper)
                            data = MOSES.getPiggyBankDataBetweenDates(self.start_date, self.end_date, self.query_dict, self.user_id, self.password)
                        except:
                            try:
                                time.sleep(self.sleeper)
                                data = MOSES.getPiggyBankDataBetweenDates(self.start_date, self.end_date, self.query_dict, self.user_id, self.password)
                            except:
                                raise

            cleaned_data = list(itertools.chain(*data))
            if cleaned_data != self.past_data:
                #print "Getting data for %s" %self.start_date
                #print "Emitting information!"
                #print "Sending %d articles." %len(cleaned_data)
                targets_data = []
                for entry in cleaned_data:
                    piggy_row = {
                        "Description Type": entry["Description Type"],
                        "Source": entry["Source"],
                        "BU": entry["BU"],
                        "Super-Category": entry["Super-Category"],
                        "Category": entry["Category"],
                        "Sub-Category": entry["Sub-Category"],
                        "Vertical": entry["Vertical"]
                    }
                    article_date = entry["Article Date"]
                    target = MOSES.getTargetFor(self.user_id, self.password, piggy_row, article_date, category_tree=self.category_tree)
                    targets_data.append(target)
                self.piggybankChanged.emit(cleaned_data, targets_data)
            self.past_data = cleaned_data
            self.sleeper = 10
        self.mutex.lock()

    def getPiggyBank(self):
        #self.sleeper = sleeper
        data = MOSES.getPiggyBankDataBetweenDates(self.start_date, self.end_date, self.query_dict, self.user_id, self.password)
        cleaned_data = list(itertools.chain(*data))
        targets_data = []
        for entry in cleaned_data:
            piggy_row = {
                        "Description Type": entry["Description Type"],
                        "Source": entry["Source"],
                        "BU": entry["BU"],
                        "Super-Category": entry["Super-Category"],
                        "Category": entry["Category"],
                        "Sub-Category": entry["Sub-Category"],
                        "Vertical": entry["Vertical"]
                    }
            target = MOSES.getTargetFor(self.user_id, self.password, piggy_row, entry["Article Date"], category_tree=self.category_tree)
            targets_data.append(target)
        
        self.piggybankChanged.emit(cleaned_data, targets_data)
        
                