from PyQt4 import QtCore
import random, time, os

class AnimalFarm(QtCore.QThread):
    quoteSent = QtCore.pyqtSignal(str)

    def __init__(self, width=None, parent=None):
        super(AnimalFarm, self).__init__(parent)
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.quotes = random.shuffle(open(os.path.join("Data","Quotes.txt","r")).read().split("\n"))
       # print "Starting Animal Farm thread."
        self.quotes_size = len(self.quotes)
        if width is None:
            self.width = 300
        else:
            self.width = width

        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)
    
    def setWidth(self, width):
        self.width = width
    
    def __del__(self):
        self.mutex.lock()
        #self.abort = True
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def run(self):
        self.mutex.unlock()
        #Max character length at 800x600 is 139 characters.
        while True:
            for quote in self.quotes:
                for characters in range(len(quote)+1):
                    quote_part = quote[:characters]
                    quote_len = len(quote_part)
                    if quote_len > self.width:
                        shorten = quote_part[quote_len - self.width:]
                    else:
                        shorten = quote_part    
                    self.quoteSent.emit(shorten)
                    time.sleep(0.03)
                time.sleep(5)
        self.mutex.lock()

