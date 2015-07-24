#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os, datetime, sys, math
from PyQt4 import QtGui, QtCore

from PassResetDialog import PassResetDialog
from OINKMethods import version
import MOSES

class Bacon(QtGui.QMainWindow):
    def __init__(self, user_id, password):
        super(Bacon, self).__init__()
        self.user_id = user_id
        self.password = password
        self.createUI()
        self.mapEvents()

    def createUI(self):
        self.main_widget = QtGui.QWidget()
        self.setCentralWidget(self.main_widget)

        self.audit_queue = QtGui.QTableWidget(0,0)
        self.audit_plan = QtGui.QTableWidget(0,0)

        self.audit_percentage_monitor = AuditPercentageMonitor(self.user_id, self.password)
        self.quality_analyser = QualityAnalyser(self.user_id, self.password)
        self.editor_metrics = EditorMetricsViewer(self.user_id, self.password)
        self.editor_calendar = EditorCalendar(self.user_id, self.password)

        


    def mapEvents():
        """"""


