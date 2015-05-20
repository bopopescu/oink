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
        self.mode = 1
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

    def fetchData(self, fsns, mode):
        """"""
        self.stop_sending = True
        self.fsns = fsns
        self.mode = mode
        self.processFSNs()

    def processFSNs(self):
        fsn_data = []
        self.stop_sending = False
        start_time = datetime.datetime.now()
        total = len(self.fsns)
        counter = 1
        for fsn in self.fsns:
            try:
                fsn_dict= MOSES.seekFSN(self.user_id, self.password, fsn)
            except:
                time.sleep(5)
                try:
                    fsn_dict= MOSES.seekFSN(self.user_id, self.password, fsn)
                except:
                    time.sleep(5)
                    try:
                        fsn_dict= MOSES.seekFSN(self.user_id, self.password, fsn)
                    except:
                        time.sleep(5)
                        try:
                            fsn_dict= MOSES.seekFSN(self.user_id, self.password, fsn)
                        except:
                            raise                        
            fsn_data.append(fsn_dict)
            eta = MOSES.getETA(start_time, counter, total)
            self.sendProgress.emit(counter, total, eta)
            counter += 1
            if self.stop_sending:
                break
        self.sendData.emit(fsn_data)

