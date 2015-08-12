#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os, datetime, sys, math

from PyQt4 import QtGui, QtCore

from PassResetDialog import PassResetDialog
from OINKMethods import version
import MOSES
from ProgressBar import ProgressBar
from AuditPercentageMonitor import AuditPercentageMonitor
from QualityAnalyser import QualityAnalyser
from EditorMetricsViewer import EditorMetricsViewer
from EditorCalendar import EditorCalendar
from AuditToolBox import AuditToolBox

class Bacon(QtGui.QMainWindow):
    """"""
    def __init__(self, user_id, password):
        super(Bacon, self).__init__()
        self.user_id = user_id
        self.password = password
        self.current_processing_date = MOSES.getLastWorkingDate(self.user_id, self.password,datetime.date.today(),"All")
        self.createUI()
        self.mapEvents()

    def createUI(self):
        """"""
        self.audit_percentage_monitor = AuditPercentageMonitor()
        self.quality_analyser = QualityAnalyser()
        self.editor_metrics = EditorMetricsViewer()
        self.editor_calendar = EditorCalendar()
        self.audit_tool_box = AuditToolBox()
        
        self.progress_bar = ProgressBar()
        self.status = self.statusBar()

        self.reports_tab_widget = QtGui.QTabWidget()
        self.reports_tab_widget.setMinimumSize(600,400)
        self.reports_tab_widget.addTab(self.audit_percentage_monitor,"Audit Percentage Monitor")
        self.reports_tab_widget.addTab(self.quality_analyser,"Quality Analyser")
        self.reports_tab_widget.addTab(self.editor_metrics, "Editor Metrics")
        self.tool_box = QtGui.QGroupBox("Tools")
        self.tool_box_layout = QtGui.QVBoxLayout()
        self.tool_box_layout.addWidget(self.editor_calendar,0)
        self.tool_box_layout.addWidget(self.audit_tool_box,0)
        self.tool_box.setLayout(self.tool_box_layout)

        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.tool_box, 0, 0, 3, 2)
        self.layout.addWidget(self.reports_tab_widget, 0, 2, 7, 7)
        self.layout.addWidget(self.progress_bar, 7, 0, 1, 9)
        
        self.main_widget = QtGui.QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("BACON - Version %s. Server: %s. User: %s (%s)."%(version(), MOSES.getHostID(), self.user_id,MOSES.getEmpName(self.user_id) if self.user_id != "bigbrother" else "Administrator"))
        self.status.showMessage("BACON Begins")
        self.show()
        
    def mapEvents(self):
        """"""
        pass


if __name__ == "__main__":
    u, p = MOSES.getBigbrotherCredentials()
    app = QtGui.QApplication(sys.argv)
    QtGui.qApp.setStyle(QtCore.QString(u'Plastique'))
    bacon = Bacon(u,p)
    sys.exit(app.exec_())



