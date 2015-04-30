from PyQt4 import QtCore
import random, time

class AnimalFarm(QtCore.QThread):
    quoteSent = QtCore.pyqtSignal(str)

    def __init__(self, width=100, parent=None):
        super(AnimalFarm, self).__init__(parent)
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.quotes = open("Data\\Quotes.txt","r").read().split("\n")
       # print "Starting Animal Farm thread."
        self.quotes_size = len(self.quotes)
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
            index = random.randint(0,(self.quotes_size-1))
            quote = self.quotes[index]
            for characters in range(len(quote)+1):
                quote_part = quote[:characters]
                quote_len = len(quote_part)
                if quote_len > self.width:
                    shorten = quote_part[quote_len - self.width:]
                else:
                    shorten = quote_part    
                #print "Sending ", quote_part
                self.quoteSent.emit(shorten)
                time.sleep(0.1)
            time.sleep(5)
        self.mutex.lock()

