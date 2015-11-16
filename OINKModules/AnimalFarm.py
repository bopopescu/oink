import random
import time
import os
import textwrap


from PyQt4 import QtCore
class AnimalFarm(QtCore.QThread):
    quoteSent = QtCore.pyqtSignal(str)

    def __init__(self, width=None, parent=None):
        super(AnimalFarm, self).__init__(parent)
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        path_to_quotes_file = os.path.join(os.getcwd(),"Data","Quotes.txt")

        if os.path.exists(path_to_quotes_file):
            self.quotes = open(path_to_quotes_file,"r").read().split("\n")
            random.shuffle(self.quotes)
        else:
            self.quotes = ["""Heard joke once: Man goes to doctor. Says he's depressed. Says life seems harsh and cruel. Says he feels all alone in a threatening world where what lies ahead is vague and uncertain. Doctor says, "Treatment is simple. Great clown Pagliacci is in town tonight. Go and see him. That should pick you up." Man bursts into tears. Says, "But doctor...I am Pagliacci"."""]
       # print "Starting Animal Farm thread."
        self.quotes_size = len(self.quotes)
        if width is None:
            self.width = 80
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
                    delay = 0.03
                    self.quoteSent.emit(quote_part)
                    time.sleep(delay)
                time.sleep(5)
        self.mutex.lock()

