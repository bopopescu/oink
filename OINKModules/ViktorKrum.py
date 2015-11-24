from __future__ import division
import sys
import datetime
import math
import time

import pandas as pd
from PyQt4 import QtCore

class ViktorKrum(QtCore.QThread):
    sendResult = QtCore.pyqtSignal(pd.DataFrame)
    def __init__(self, category_tree, category_tree_headers, *args, **kwargs):
        super(ViktorKrum, self).__init__(*args, **kwargs)
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.allow_run = False
        self.category_tree = category_tree
        self.category_tree_headers = category_tree_headers
        self.search_string = ""
        self.search_criteria = "Any"

        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def __del__(self):
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def run(self):
        self.allow_run = True
        while True:
            self.mutex.unlock()
            if self.allow_run:
                self.findIdentifier()
                self.allow_run = False
            self.mutex.lock()

    def startFindingIdentifier(self, search_string, search_criteria):
        self.search_string = search_string
        self.search_criteria = search_criteria
        self.allow_run = True

    def findIdentifier(self):
        if self.search_string != "":
            self.result_dataframe = None
            if self.search_criteria != "Any":
                self.result_dataframe = self.findIdentifierInCategoryTree(self.search_string, self.search_criteria)
                self.category_tree[self.category_tree[self.search_criteria].str.contains(self.search_string)]
                self.result_dataframe.drop_duplicates(subset=self.category_tree_headers, inplace=True)
                self.result_dataframe = self.result_dataframe.reset_index()
            else:
                dfs = []
                for self.search_criteria in self.category_tree_headers:
                    dfs.append(self.findIdentifierInCategoryTree(self.search_string, self.search_criteria))
                self.result_dataframe = pd.concat(dfs)
                self.result_dataframe.drop_duplicates(subset=self.category_tree_headers, inplace=True)
                self.result_dataframe = self.result_dataframe.reset_index()
            
            if self.result_dataframe is None:
                self.result_dataframe = pd.DataFrame(index=None, columns=self.category_tree_headers)
            self.sendResult.emit(self.result_dataframe)

    def findIdentifierInCategoryTree(self, search_string, search_criteria):        
        dfs = [self.category_tree[self.category_tree[search_criteria].str.contains(search_string)]]
        dfs.append(self.category_tree[self.category_tree[search_criteria].str.contains(search_string.lower())])
        dfs.append(self.category_tree[self.category_tree[search_criteria].str.contains(search_string.capitalize())])
        dfs.append(self.category_tree[self.category_tree[search_criteria].str.contains(search_string.upper())])
        return pd.concat(dfs)