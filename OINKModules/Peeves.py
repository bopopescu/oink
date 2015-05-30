import datetime
import time
from PyQt4 import QtCore
import MOSES

        
class Peeves(QtCore.QThread):
    sendProgress = QtCore.pyqtSignal(int, int, datetime.datetime)
    sendData = QtCore.pyqtSignal(list)

    def __init__(self, user_id, password):
#       QtCore.QThread.__init__(self)
        super(Peeves, self).__init__()
        self.mode = 0 # 0 fetches all data. 1 fetches written entries. 2 fetches unwritten entries.
        self.search_type = 0 #0 searches for fsns. 1 searches for item_ids.
        self.search_function = [MOSES.seekFSN, MOSES.seekItemID]
        self.user_id = user_id
        self.password = password
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def run(self):
        """"""
        print "Peeves is running and ready to serve the Seeker."

    def __del__(self):
        """"""
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def fetchData(self, search_strings, mode, search_type):
        """"""
        self.stop_sending = True
        self.search_strings = search_strings
        self.mode = mode
        self.search_type = search_type
        self.processSearchStrings()

    def processSearchStrings(self):
        search_results = []
        self.stop_sending = False
        start_time = datetime.datetime.now()
        total = len(self.search_strings)
        counter = 1
        for search_string in self.search_strings:
            try:
                search_result= self.search_function[self.search_type](self.user_id, self.password, search_string)
            except:
                time.sleep(5)
                try:
                    search_result= self.search_function[self.search_type](self.user_id, self.password, search_string)
                except:
                    time.sleep(5)
                    try:
                        search_result= self.search_function[self.search_type](self.user_id, self.password, search_string)
                    except:
                        time.sleep(5)
                        try:
                            search_result= self.search_function[self.search_type](self.user_id, self.password, search_string)
                        except:
                            raise                        
            search_results.append(search_result)
            eta = MOSES.getETA(start_time, counter, total)
            self.sendProgress.emit(counter, total, eta)
            counter += 1
            if self.stop_sending:
                break
        self.sendData.emit(search_results)

