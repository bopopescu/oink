#!/usr/bin/python2
# -*- coding: utf-8 -*-
import itertools
import math
import datetime
from PyQt4 import QtGui, QtCore
import numpy

from PassResetDialog import PassResetDialog
from EfficiencyCalculator import EfficiencyCalculator
from DateSelectorWidget import DateSelectorWidget
from FilterBox import FilterBox
from PiggyBank import PiggyBank
from PiggyBanker import PiggyBanker
from Former import Former
from Porker import Porker
from PorkKent import PorkKent
from OINKMethods import version
import MOSES

class Vindaloo(QtGui.QMainWindow):
    def __init__(self, userID, password):
        """Vindaloo initializer"""
        super(QtGui.QMainWindow,self).__init__()
        self.userID = userID
        self.password = password
        self.clip = QtGui.QApplication.clipboard()
        self.form_values_thread = Former(self.userID, self.password)
        self.generateUI()
        self.startDate, self.endDate = self.dates_picker.get_dates()
        self.pork_kent = PorkKent(self.userID, self.password, self.startDate, self.endDate)
        self.piggybanker = PiggyBanker(self.userID, self.password, self.startDate, self.endDate, {})
        self.create_layout()
        self.setVisuals()
        self.createActions()
        self.addMenus()
        self.createEvents()

    def generateUI(self):
        """Vindaloo UI Initializer"""
        self.mainWidget = QtGui.QWidget()
        self.setCentralWidget(self.mainWidget)
        self.dates_picker = DateSelectorWidget()
        self.pullDataButton = QtGui.QPushButton("Pull Data")
        self.pullDataButton.setMinimumWidth(300)
        self.pullDataButton.setMaximumWidth(300)
        self.exportButton = QtGui.QPushButton("Export Data and Reports")
        self.exportButton.setMinimumWidth(300)
        self.exportButton.setMaximumWidth(300)
        self.filtersButton = QtGui.QPushButton("Select Advanced Filters")
        self.filtersButton.setCheckable(True)
        self.filtersButton.setAutoDefault(False)
        self.filtersButton.setMinimumWidth(300)
        self.filtersButton.setMaximumWidth(300)

        #This consumes time, put them in a thread
        #writers = [Writer["Name"] for Writer in MOSES.getWritersList(self.userID, self.password)]
        #types = MOSES.getDescriptionTypes(self.userID, self.password)
        #sources = MOSES.getSources(self.userID, self.password)

        self.writers_filter = FilterBox("Writers:")
        #self.writers_filter.addItems(writers)
        self.type_filter = FilterBox("Description Type:")
        #self.type_filter.addItems(types)
        self.source_filter = FilterBox("Description Source:")
        #self.source_filter.addItems(sources)
        self.BU_filter = FilterBox("BU:")
        self.SupC_filter = FilterBox("Super-Category:")
        self.C_filter = FilterBox("Category:")
        self.SubC_filter = FilterBox("Sub-Category:")
        self.Vert_filter = FilterBox("Vertical:")
        self.Brand_filter = FilterBox("Brand:")
       
        self.team_report = QtGui.QTableWidget(0, 0)
        self.team_report.setStyleSheet("gridline-color: rgb(0, 0, 0)")
        
        self.and_logic = QtGui.QCheckBox("AND")
        self.and_logic.setToolTip("Select this option if you want to extract data which corresponds\nto all the selected filters.\nThis may result in null returns due to conflicting options.")
        self.or_logic = QtGui.QCheckBox("OR")
        self.or_logic.setToolTip("Select this option if you want to extract data which corresponds\nto at least one of the selected filters.\nUse this option if you're not sure what to choose.")
        self.or_logic.setChecked(True)
        
        self.logic_opn = QtGui.QButtonGroup()
        self.logic_opn.addButton(self.and_logic)
        self.logic_opn.addButton(self.or_logic)
        self.filter_logic_layout = QtGui.QHBoxLayout()
        self.filter_logic_layout.addWidget(self.and_logic)
        self.filter_logic_layout.addWidget(self.or_logic)

        self.filters_widget = QtGui.QWidget()
        self.filters_layout = QtGui.QVBoxLayout()
        self.filters_layout.setSpacing(0)
        self.filters_layout.addLayout(self.filter_logic_layout)
        self.filters_layout.addWidget(self.writers_filter)
        self.filters_layout.addWidget(self.type_filter)
        self.filters_layout.addWidget(self.source_filter)
        self.filters_layout.addWidget(self.BU_filter)
        self.filters_layout.addWidget(self.SupC_filter)
        self.filters_layout.addWidget(self.C_filter)
        self.filters_layout.addWidget(self.SubC_filter)
        self.filters_layout.addWidget(self.Vert_filter)
        self.filters_layout.addWidget(self.Brand_filter)
        self.filters_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.filters_widget.setLayout(self.filters_layout)
        self.filters_widget.setVisible(False)

        #self.team_report = QtGui.QTextEdit()
        self.tools_layout = QtGui.QVBoxLayout()
        self.tools_layout.addWidget(self.dates_picker, 1)
        self.tools_layout.addWidget(self.pullDataButton, 1)
        self.tools_layout.addWidget(self.exportButton, 1)
        self.tools_layout.addWidget(self.filtersButton, 1)
        self.tools_layout.addWidget(self.filters_widget, 1)
        self.tools_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.tools_layout.addStretch(3)
        self.statusLog = QtGui.QTextEdit()
        self.piggybank = PiggyBank()
        self.team_report_graphs = QtGui.QWidget()
        self.rawdata = QtGui.QWidget()
        self.summary_progress = QtGui.QProgressBar()
        progress_bar_style = """
            .QProgressBar {
                 text-align: center;
             }"""
        self.summary_progress.setStyleSheet(progress_bar_style)

    def create_layout(self):
        """Vindaloo."""

        self.stats_tabs = QtGui.QTabWidget()
        self.stats_tabs.addTab(self.team_report, "Team Report")
        self.stats_tabs.addTab(self.team_report_graphs, "Graphs")
        self.stats_tabs.addTab(self.piggybank, "Piggy Bank")
        self.stats_tabs.addTab(self.rawdata, "Quality Raw Data")
        self.stats_tabs.addTab(self.statusLog, "Log")

        self.finalLayout = QtGui.QHBoxLayout()
        self.finalLayout.addLayout(self.tools_layout,1)
        self.finalLayout.addWidget(self.stats_tabs,4)
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.finalLayout)
        self.layout.addWidget(self.summary_progress)
        self.mainWidget.setLayout(self.layout)

    def createEvents(self):
        """Vindaloo."""
        self.pullDataButton.clicked.connect(self.updateTables)
        self.filtersButton.clicked.connect(self.applyFilters)
        self.exportButton.clicked.connect(self.exportData)
        self.filtersButton.clicked.connect(self.filters_widget.setVisible)
        self.piggybanker.piggybankChanged.connect(self.displaypiggybank)
        self.form_values_thread.gotBUValues.connect(self.BU_filter.addItems)
        self.form_values_thread.gotSupCValues.connect(self.SupC_filter.addItems)
        self.form_values_thread.gotCatValues.connect(self.C_filter.addItems)
        self.form_values_thread.gotSubCValues.connect(self.SubC_filter.addItems)
        self.form_values_thread.gotVertValues.connect(self.Vert_filter.addItems)
        self.form_values_thread.gotBrandValues.connect(self.Brand_filter.addItems)
        self.pork_kent.gotSummary.connect(self.displayPiggyBankSummary)
        self.pork_kent.processingSummary.connect(self.displayProgress)

    def displayProgress(self, done, total):
        progress = float(done)/float(total)
        self.summary_progress.setFormat("Compiling summary sheet. Finished %d of %d" %(done, total))
        self.summary_progress.setValue(int(progress*100))

    def addMenus(self):
        """Vindaloo menus."""
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("&File")
        self.exportMenu = self.fileMenu.addMenu("E&xport")
        self.toolsMenu = self.menu.addMenu("&Tools")
        self.reportMenu = self.toolsMenu.addMenu("Reports")
        self.qualityMenu = self.reportMenu.addMenu("Quality Reports")
        self.teamQualityReportOption = self.qualityMenu.addAction(self.teamQualityReport)
        self.categoryQualityReportOption = self.qualityMenu.addAction(self.categoryQualityReport)
        self.productivityMenu = self.reportMenu.addMenu(\
            "Productivity Reports")
        self.wordCountTrendsOption = self.productivityMenu.addAction(\
            self.wordCountTrends)
        self.effiencyTrendsOption = self.productivityMenu.addAction(\
            self.efficiencyTrends)
        self.WBRReportOption = self.reportMenu.addAction(self.WBRReport)
        self.dailyReportOption = self.reportMenu.addAction(self.dailyReport)
        self.weeklyReportOption = self.reportMenu.addAction(self.weeklyReport)

        self.catTreeMenu = self.toolsMenu.addMenu("Category &Tree and Targets")
        self.targetRevOption = self.catTreeMenu.addAction(self.targetRev)
        self.changeCatTreeOption = self.catTreeMenu.addAction(self.changeCatTree)
        self.openEffCalcOption = self.catTreeMenu.addAction(self.openEffCalc)
        self.resetPasswordsOption = self.toolsMenu.addAction(self.resetPasswordsAction)
        self.overrideFSNOption = self.toolsMenu.addAction(self.overrideFSNAction)
        self.commMenu = self.menu.addMenu("Co&mmunication")
        self.leaveMenu = self.commMenu.addMenu("Leave Management")
        self.leaveApprovalOption = self.leaveMenu.addAction(self.leaveApproval)
        self.leaveTrackerOption = self.leaveMenu.addAction(self.leaveTracker)
        self.workforceLossOption = self.leaveMenu.addAction(self.workforceLoss)
        
        self.KRAMenu = self.toolsMenu.addMenu("&KRA Tools")
        self.askEditor = self.commMenu.addAction(self.callAskAnEditor)
        self.reviseAudit = self.commMenu.addAction(\
            self.raiseAuditRevisionTicket)
        self.chatmessenger = self.commMenu.addAction(self.callOpenChat) 
        self.helpMenu = self.menu.addMenu("&Help")

    def createActions(self):
        """Vindaloo."""
        self.resetPasswordsAction = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"), "Reset user passwords manually", self)
        self.resetPasswordsAction.triggered.connect(self.resetPasswords)
        self.overrideFSNAction = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"), "Authorize an FSN Override", self)
        self.overrideFSNAction.triggered.connect(self.overrideFSN)
        self.dailyReport = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Daily Report",self)
        self.weeklyReport = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Weekly Report",self)
        self.teamQualityReport = QtGui.QAction(\
            QtGui.QIcon("Images\_Icon.png"),"Team Quality Report",self) 
        self.categoryQualityReport = QtGui.QAction(\
            QtGui.QIcon("Images\_Icon.png"),"Category Quality Report",self) 
        self.WBRReport = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Generate WBR Report",self)
        self.wordCountTrends = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "View Trends in Word Count",self)
        self.efficiencyTrends = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "View Trends in Efficiency Spikes",self)
        self.leaveApproval = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Leave Approval",self)
        self.leaveTracker = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Leave Tracker",self)
        self.workforceLoss = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Calculate Work Force Loss Due to Leaves",self)
        self.targetRev = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Revise Targets",self)
        self.raiseAuditRevisionTicket = QtGui.QAction(\
                        QtGui.QIcon("Images\_Icon.png"),\
                        "Raise a Revision Ticket for an Audit",self)
        self.callAskAnEditor = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Ask an Editor",self)
        self.openEffCalc = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Efficiency Calculator",self)
        self.callOpenChat = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Open Chat",self)
        self.changeCatTree = QtGui.QAction(QtGui.QIcon("Images\_Icon.png"),\
                        "Change Category Tree",self)

    def resetPasswords(self):
        """Opens a dialog to facilitate resetting the password of one or more users."""
    
    def overrideFSN(self):
        """Opens a dialog to allow TLs to paste a list of FSNs, identify duplicates and allow overrides if necessary."""
   
    def alertMessage(self, title, message):
        """Vindaloo."""
        QtGui.QMessageBox.about(self, title, message)

    def updateTables(self):
        """Vindaloo."""
        self.startDate, self.endDate = self.dates_picker.get_dates()
        self.piggybanker.setStartDate(self.startDate)
        self.piggybanker.setEndDate(self.endDate)
        self.pork_kent.getSummary(self.startDate, self.endDate)

    def displayPiggyBankSummary(self, summary):
        """Vindaloo: Methods to display the efficiency and quality."""
        #print "Running displayPiggyBankSummary."
        self.team_report.setRowCount(len(summary))
        keys = ["Report Date", "Writer ID", "Writer Email ID", "Writer Name", "Efficiency", "CFM", "GSEO", "Weekly Efficiency", "Weekly CFM", 
            "Weekly GSEO", "Monthly Efficiency", "Monthly CFM", "Monthly GSEO", "Quarterly Efficiency", 
            "Quarterly CFM", "Quarterly GSEO", "Average Efficiency", "Average CFM", "Average GSEO"]
        self.team_report.setColumnCount(len(keys))
        row_index = 0
        for writer_data in summary:
            #print writer_data
            report_date = str(writer_data["Report Date"])
            writer_id = writer_data["Writer ID"]
            writer_email = writer_data["Writer Email ID"]
            writer_name = writer_data["Writer Name"]
            writer_efficiency = writer_data["Efficiency"]
            writer_CFM = writer_data["CFM"]
            writer_GSEO = writer_data["GSEO"]
            writer_w_efficiency = writer_data["Weekly Efficiency"]
            writer_w_CFM = writer_data["Weekly CFM"]
            writer_w_GSEO = writer_data["Weekly GSEO"]
            writer_m_efficiency = writer_data["Monthly Efficiency"]
            writer_m_CFM = writer_data["Monthly CFM"]
            writer_m_GSEO = writer_data["Monthly GSEO"]
            writer_q_efficiency = writer_data["Quarterly Efficiency"]
            writer_q_CFM = writer_data["Quarterly CFM"]
            writer_q_GSEO = writer_data["Quarterly GSEO"]
            writer_a_efficiency = writer_data["Average Efficiency"]
            writer_a_CFM = writer_data["Average CFM"]
            writer_a_GSEO = writer_data["Average GSEO"]
            #QWidgetItem Conversion
            writer_items_list = []
            writer_items_list.append(QtGui.QTableWidgetItem(str(report_date)))
            writer_items_list.append(QtGui.QTableWidgetItem(str(writer_id)))
            writer_items_list.append(QtGui.QTableWidgetItem(str(writer_email)))
            writer_items_list.append(QtGui.QTableWidgetItem(str(writer_name)))
            
            #red = QtGui.QColor(204, 50, 20)
            #green = QtGui.QColor(119, 178, 18)
            #blue = QtGui.QColor(25, 94, 255)
            red = QtGui.QColor(255, 12, 7)
            green = QtGui.QColor(49,255, 102)
            blue = QtGui.QColor(86, 89, 232)

            if (writer_efficiency is None) or (math.isnan(writer_efficiency)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_efficiency))))
                if writer_efficiency < 0.99:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.99 <= writer_efficiency <= 1.05:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_efficiency > 1.05:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_CFM is None) or (math.isnan(writer_CFM)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_CFM))))
                if writer_CFM < 0.95:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.95 <= writer_CFM <= 0.98:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_CFM > 0.98:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_GSEO is None) or (math.isnan(writer_GSEO)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_GSEO))))
                if writer_GSEO < 0.95:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.95 <= writer_GSEO <= 0.98:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_GSEO > 0.98:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_w_efficiency is None) or (math.isnan(writer_w_efficiency)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_w_efficiency))))
                if writer_w_efficiency < 0.99:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.99 <= writer_w_efficiency <= 1.05:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_w_efficiency > 1.05:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_w_CFM is None) or (math.isnan(writer_w_CFM)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_w_CFM))))
                if writer_w_CFM < 0.95:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.95 <= writer_w_CFM <= 0.98:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_w_CFM > 0.98:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_w_GSEO is None) or (math.isnan(writer_w_GSEO)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_w_GSEO))))
                if writer_w_GSEO < 0.95:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.95 <= writer_w_GSEO <= 0.98:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_w_GSEO > 0.98:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_m_efficiency is None) or (math.isnan(writer_m_efficiency)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_m_efficiency))))
                if writer_m_efficiency < 0.99:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.99 <= writer_m_efficiency <= 1.05:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_m_efficiency > 1.05:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_m_CFM is None) or (math.isnan(writer_m_CFM)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_m_CFM))))
                if writer_m_CFM < 0.95:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.95 <= writer_m_CFM <= 0.98:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_m_CFM > 0.98:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_m_GSEO is None) or (math.isnan(writer_m_GSEO)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_m_GSEO))))
                if writer_m_GSEO < 0.95:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.95 <= writer_m_GSEO <= 0.98:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_m_GSEO > 0.98:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_q_efficiency is None) or (math.isnan(writer_q_efficiency)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_q_efficiency))))
                if writer_q_efficiency < 0.99:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.99 <= writer_q_efficiency <= 1.05:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_q_efficiency > 1.05:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_q_CFM is None) or (math.isnan(writer_q_CFM)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_q_CFM))))
                if writer_q_CFM < 0.95:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.95 <= writer_q_CFM <= 0.98:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_q_CFM > 0.98:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_q_GSEO is None) or (math.isnan(writer_q_GSEO)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_q_GSEO))))
                if writer_m_GSEO < 0.95:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.95 <= writer_m_GSEO <= 0.98:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_m_GSEO > 0.98:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_a_efficiency is None) or (math.isnan(writer_a_efficiency)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_a_efficiency))))
                if writer_a_efficiency < 0.99:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.99 <= writer_a_efficiency <= 1.05:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_a_efficiency > 1.05:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_a_CFM is None) or (math.isnan(writer_a_CFM)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_a_CFM))))
                if writer_a_CFM < 0.95:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.95 <= writer_a_CFM <= 0.98:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_a_CFM > 0.98:
                    writer_items_list[-1].setBackgroundColor(blue)

            if (writer_a_GSEO is None) or (math.isnan(writer_a_GSEO)):
                writer_items_list.append(QtGui.QTableWidgetItem("-"))
            else:
                writer_items_list.append(QtGui.QTableWidgetItem("%.2f%%" %(100*(writer_a_GSEO))))
                if writer_a_GSEO < 0.95:
                    writer_items_list[-1].setBackgroundColor(red)
                elif 0.95 <= writer_a_GSEO <= 0.98:
                    writer_items_list[-1].setBackgroundColor(green)
                elif writer_a_GSEO > 0.98:
                    writer_items_list[-1].setBackgroundColor(blue)


            column_index = 0
            self.team_report.setSortingEnabled(False)
            for widget_item in writer_items_list:
                widget_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.team_report.setItem(row_index, column_index, widget_item)
                column_index += 1
            self.team_report.setSortingEnabled(True)
            self.team_report.sortItems(1)
            self.team_report.resizeColumnsToContents()
            self.team_report.resizeRowsToContents()
            row_index += 1
        self.team_report.setHorizontalHeaderLabels(keys)

    def displaypiggybank(self, piggy_data, targets_date):
        """Vindaloo: Pulls all data for a start and end date"""
        #print "Trying to displaypiggybank."
        self.piggybank.setData(piggy_data, targets_date)
        self.piggybank.displayData()
        if self.startDate != self.endDate:
            date_string = "for all working dates between %s and %s" % (self.startDate, self.endDate)
        else:
            date_string = "for %s." % (self.startDate)
        entries = self.piggybank.rowCount()
        self.alertMessage("Success!", "Displayed %d entries %s." %(entries, date_string))

    def applyFilters(self):
        """Applying filters."""

    def exportData(self):
        """Opens a dialog, asking for an output folder.
        If cancelled, it selects the default output folder 
        within the current working director.
        Then, it takes the data presented in the statistics 
        and builds a complete report."""

    def keyPressEvent(self, e):
        """Vindaloo: Found this code online. Go through it and try to improve it."""
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_C: #copy
                current_tab = self.stats_tabs.currentIndex()
                print "Currently displaying tab #%d",current_tab
                if current_tab == 0:
                    table_to_copy = self.team_report
                elif current_tab == 2:
                    table_to_copy = self.piggybank
                selected = table_to_copy.selectedRanges()
                s = '\t'+"\t".join([str(table_to_copy.horizontalHeaderItem(i).text()) for i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1)])
                s = s + '\n'

                for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
                    s += str(r+1) + '\t' 
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(table_to_copy.item(r,c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)

    def log(self, message):
        """Vindaloo."""
        with open("CSVs\Log.txt", "a") as logFile: logFile.write("\n@%s: %s" %(datetime.datetime.now(),message))
        self.statusLog.append(message)

    def notify(self,title,message):
        """Vindaloo."""
        self.trayIcon.showMessage(title,message)

    def displayStatus(self,message):
        """Vindaloo."""
        self.statusBar().showMessage(message)

    def setVisuals(self):
        """Vindaloo."""
        self.setWindowTitle("V.I.N.D.A.L.O.O. - A Part of the O.I.N.K. Report Management System")
        self.resize(800, 600)
        self.move(250, 40)
        self.show()
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))     
        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('Images\PORK_Icon.png'), self)
        self.trayIcon.show()
        self.notify("Welcome to Vindaloo", "All animals are created equal.")
        self.statusBar().showMessage("Big Brother is Watching You.")
