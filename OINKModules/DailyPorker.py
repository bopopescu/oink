from __future__ import division

import sys
import math
import datetime
import os
from PyQt4 import QtGui, QtCore
import numpy
import pandas as pd

import MOSES
from DailyGraphView import DailyGraphView
import Graphinator
from ProgressBar import ProgressBar
from CopiableQTableWidget import CopiableQTableWidget
from CheckableComboBox import CheckableComboBox
from PorkLane import PorkLane

class DailyPorker(QtGui.QWidget):
    def __init__(self, user_id, password, category_tree=None):
        super(DailyPorker, self).__init__()
        self.user_id, self.password = user_id, password
        self.report_list = []
        if category_tree is None:
            self.category_tree = MOSES.getCategoryTree(self.user_id, self.password)
        else:
            self.category_tree = category_tree
        #self.pork_kent = PorkKent(self.user_id, self.password)
        style_string = """
        .QTableWidget {
            gridline-color: rgb(0, 0, 0);
        }
        """
        self.setStyleSheet(style_string)
        self.clip = QtGui.QApplication.clipboard()
        self.createUI()
        self.mapEvents()
        self.initiate()

    def initiate(self):
        self.center()
        self.populateWritersComboBox()
        self.writers_combobox.selectAll()
        self.refreshSortFilter()

    def center(self):
        #frameGm = self.frameGeometry()
        #screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        #centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        #frameGm.moveCenter(centerPoint)
        #self.move(frameGm.topLeft())
        self.move(70,50)

    def createUI(self):

        self.start_date_label = QtGui.QLabel("<b>Date:</b>")
        self.start_date_edit = QtGui.QDateTimeEdit()
        self.start_date_edit.setToolTip("Set the date for which you want to generate the report.")
        lwd = MOSES.getLastWorkingDate(self.user_id, self.password, queryUser="All")
        self.start_date_edit.setDate(lwd)
        self.start_date_edit.setDisplayFormat("MMMM dd, yyyy")
        self.start_date_edit.setMinimumDate(QtCore.QDate(2015,1,1))
        self.start_date_edit.setCalendarPopup(True)

        self.end_date_edit = QtGui.QDateTimeEdit()
        self.end_date_edit.setToolTip("Select an end date. Only working days will be considered for the calculation.\nThis field will be disabled if the checkbox isn't marked to calculate the average statistics between dates.")
        self.end_date_edit.setDate(self.start_date_edit.date())
        self.end_date_edit.setDisplayFormat("MMMM dd, yyyy")
        self.end_date_edit.setMinimumDate(self.start_date_edit.date())
        self.end_date_edit.setCalendarPopup(True)

        self.writers_combobox = CheckableComboBox("Writers")
        self.writers_combobox.setToolTip("Select a group of writers if you want to check their performance for some time frame.")

        report_names = ["Article Count","Efficiency","Audit Count","CFM","GSEO","Stack Rank Index","Efficiency KRA","CFM KRA","GSEO KRA"]#,"Audit Percentage"]
        self.parameters_combobox = CheckableComboBox("Report Values")
        self.parameters_combobox.addItems(report_names)
        self.parameters_combobox.select(["Efficiency","CFM","GSEO", "Stack Rank Index"])

        self.report_time_frames_combobox = CheckableComboBox("Timeframe")
        self.report_time_frames_combobox.addItems(["Daily","Weekly","Monthly","Quarterly","Half-Yearly"])
        self.report_time_frames_combobox.select(["Daily","Weekly"])

        self.sorting_filter_label = QtGui.QLabel("<b>Sort By:</b>")
        self.sorting_filter_combobox = QtGui.QComboBox()
        self.sorting_filter_combobox.setToolTip("Select the parameter you want to sort the generated reports by.")

        self.build_button = QtGui.QPushButton("Build")
        self.build_button.setToolTip("Click this button to start building the report")

        self.plot_button = QtGui.QPushButton("Plot")
        self.plot_button.setToolTip("Check this if you want to automatically plot the graphs.")
        
        self.build_dbr_button = QtGui.QPushButton("Build DBR Report")
        self.build_dbr_button.setToolTip("Check this if you want to automatically plot the graphs.")
        
        self.build_wbr_button = QtGui.QPushButton("Build WBR Report")
        self.build_wbr_button.setToolTip("Check this if you want to automatically plot the graphs.")
        
        self.progress_bar = ProgressBar()

        self.export_graphs_button = QtGui.QPushButton("Save")
        self.export_graphs_button.setToolTip("Click this button to save the generated reports and graphs in a desired folder location.")

        self.report = CopiableQTableWidget(0, 0)
        self.t_report = CopiableQTableWidget(0, 0)
        self.dbr_report = CopiableQTableWidget(0, 0)
        self.wbr_report = CopiableQTableWidget(0, 0)

        self.graphs = DailyGraphView()
        self.t_graphs = DailyGraphView()

        self.reports_tab = QtGui.QTabWidget()
        self.reports_tab.addTab(self.report,"Writers' Report")
        self.reports_tab.addTab(self.graphs, "Writers' Graphs")
        self.reports_tab.addTab(self.t_report,"Team Report")
        self.reports_tab.addTab(self.t_graphs, "Team Graphs")
        self.reports_tab.addTab(self.dbr_report, "DBR Report")
        self.reports_tab.addTab(self.wbr_report, "WBR Report")

        self.status = QtGui.QLabel("I'm a Porkitzer Prize Winning Reporter.")


        options_layout_row_1 = QtGui.QHBoxLayout()
        options_layout_row_1.addWidget(self.start_date_label,0)
        options_layout_row_1.addWidget(self.start_date_edit,1)
        options_layout_row_1.addWidget(self.end_date_edit,1)
        options_layout_row_1.addWidget(self.writers_combobox,1)
        options_layout_row_1.addWidget(self.parameters_combobox,1)
        options_layout_row_1.addWidget(self.report_time_frames_combobox,1)
        options_layout_row_1.addStretch(2)
        
        
        options_layout_row_2 = QtGui.QHBoxLayout()
        options_layout_row_2.addWidget(self.sorting_filter_label,0)
        options_layout_row_2.addWidget(self.sorting_filter_combobox,1)
        options_layout_row_2.addWidget(self.build_button,0)
        options_layout_row_2.addWidget(self.plot_button,0)
        options_layout_row_2.addWidget(self.build_dbr_button,0)
        options_layout_row_2.addWidget(self.build_wbr_button,0)
        options_layout_row_2.addStretch(2)

        options_layout = QtGui.QVBoxLayout()
        options_layout.addLayout(options_layout_row_1,0)
        options_layout.addLayout(options_layout_row_2,0)

        options = QtGui.QGroupBox("Report Options")
        options.setLayout(options_layout)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(options,1)
        layout.addWidget(self.reports_tab,3)
        layout.addWidget(self.progress_bar,0)
        layout.addWidget(self.status,0)

        self.setLayout(layout)
        self.setWindowTitle("The Daily Porker: Straight from the Pigs")

        if "OINKModules" in os.getcwd():
            icon_file_name_path = os.path.join(os.path.join('..',"Images"),'PORK_Icon.png')
        else:
            icon_file_name_path = os.path.join('Images','PORK_Icon.png')
        self.setWindowIcon(QtGui.QIcon(icon_file_name_path))

    def mapEvents(self):
        self.build_button.clicked.connect(self.buildReport)
        self.start_date_edit.dateChanged.connect(self.changedStartDate)
        self.pork_lane = PorkLane(self.user_id, self.password, self.category_tree)
        self.pork_lane.sendReport.connect(self.populateReport)
        self.pork_lane.sendProgress.connect(self.displayProgress)
        self.pork_lane.sendGraphs.connect(self.displayGraphs)
        self.report_time_frames_combobox.changedSelection.connect(self.refreshSortFilter)
        self.parameters_combobox.changedSelection.connect(self.refreshSortFilter)
        self.build_dbr_button.clicked.connect(self.buildDBR)
        self.build_wbr_button.clicked.connect(self.buildWBR)

    def buildDBR(self):
        self.build_dbr_button.setEnabled(False)
        self.alertMessage("Please Wait","This could take a while.")
        dbr = MOSES.getDBR(self.user_id, self.password, self.start_date_edit.date().toPyDate(), self.category_tree)
        self.dbr_report.showDataFrame(dbr)
        self.dbr_report.adjustToColumns()
        self.build_dbr_button.setEnabled(True)
        self.alertMessage("Success","Successfully Pulled the DBR")

    def buildWBR(self):
        self.build_wbr_button.setEnabled(False)
        self.alertMessage("Please Wait","This could take a while.")
        wbr = MOSES.getWBR(self.user_id, self.password, self.start_date_edit.date().toPyDate(), self.category_tree)
        self.wbr_report.showDataFrame(wbr)
        self.wbr_report.adjustToColumns()
        self.build_wbr_button.setEnabled(True)
        self.alertMessage("Success","Successfully Pulled the WBR")


    def getWritersList(self):
        self.writers_data_frame = MOSES.getWritersList(self.user_id, self.password, self.start_date_edit.date().toPyDate())
        writer_names_list = list(set(self.writers_data_frame["Name"]))
        writer_names_list.sort()
        return writer_names_list

    def displayGraphs(self,handle):
        if handle:
            self.graphs.graph_date = self.pork_lane.start_date
            self.graphs.enable_plotting = True
            self.graphs.plotGraph()
            self.progress_bar.setRange(0,100)
            self.progress_bar.setFormat("Completed at %s." %(datetime.datetime.strftime(datetime.datetime.now(),"%H:%M:%S")))
            self.status.setText("Beware the alien, the mutant, the heretic.")  
            self.progress_bar.setValue(100)
            #self.export_graphs_button.setEnabled(True)
        else:
            self.export_graphs_button.setEnabled(False)
            self.status.setText("Creating Graphs...")        
            self.progress_bar.setValue(0)
            self.progress_bar.setRange(0,0)


    def refreshSortFilter(self):
        report_types = self.getRequiredReportTypes()
        self.sorting_filter_combobox.clear()
        if len(report_types) > 0:
            self.sorting_filter_combobox.setEnabled(True)
            self.sorting_filter_combobox.addItems(report_types)
        else:
            self.sorting_filter_combobox.setEnabled(False)
        self.sorting_filter_combobox.setCurrentIndex(-1)


    def buildReport(self):
        self.build_button.setEnabled(False)
        report_types = self.getRequiredReportTypes()
        if len(report_types) > 0:
            self.build = True
            self.pork_lane.writers_data_frame = self.writers_data_frame
            self.pork_lane.parameter_list = self.parameters_combobox.getCheckedItems() #set pork lane report types.]
            self.pork_lane.time_frame_list = self.report_time_frames_combobox.getCheckedItems()
            selected_writers_list = self.writers_combobox.getCheckedItems()
            if len(selected_writers_list)>0:
                self.pork_lane.writers_list = selected_writers_list
            else:
                self.writers_combobox.selectAll()
                selected_writers_list = self.writers_combobox.getCheckedItems()
                self.pork_lane.writers_list = selected_writers_list
            self.pork_lane.start_date = self.start_date_edit.date().toPyDate()
            self.pork_lane.end_date = self.end_date_edit.date().toPyDate()
            self.pork_lane.allowRun = True #allow building.
        else:
            self.build = False
            self.alertMessage("Error","Please select at least one parameter in the checklist before attempting to build the report.")
        self.build_button.setEnabled(True)
            
    def changedStartDate(self):
        self.end_date_edit.setMinimumDate(self.start_date_edit.date())
        self.end_date_edit.setDate(self.start_date_edit.date())
        self.populateWritersComboBox()

    def populateWritersComboBox(self):
        self.writers_combobox.clear()
        self.writers_combobox.addItems(self.getWritersList())

    def getRequiredReportTypes(self):
        parameter_list = self.parameters_combobox.getCheckedItems()
        time_frame_list = self.report_time_frames_combobox.getCheckedItems()
        reports_list = ["%s %s"%(time_frame, parameter_type) for time_frame in time_frame_list for parameter_type in parameter_list]
        return reports_list

    def populateReport(self, report):
        mode = self.pork_lane.mode
        columns = ["Report Date", "Writer ID", "Writer Email ID", "Writer Name", "Reporting Manager"]
        columns += mode
        self.report.setRowCount(0)
        row_counter = 0

        self.report.setColumnCount(len(columns))
        self.report.setHorizontalHeaderLabels(columns)
        self.report.setSortingEnabled(False)
        red = QtGui.QColor(231, 90, 83)
        green = QtGui.QColor(60, 179, 113)
        blue = QtGui.QColor(23, 136, 216)

        for writer_row in report:
            self.report.insertRow(row_counter)
            column_counter = 0
            for column_name in columns:
                if ("Efficiency" in column_name) and ("KRA" not in column_name):
                    steps = [1.00, 1.05, 1.10]
                elif (("CFM" in column_name) or ("GSEO" in column_name)) and ("KRA" not in column_name):
                    steps = [0.95, 0.97]
                elif ("KRA" in column_name) or ("Index" in column_name):
                    steps = [3.0,4.0,5.0]
                else:
                    steps = []
                parameter = writer_row[column_name]

                if (type(parameter) == str):
                    parameter_is_valid = False
                elif (parameter is None):
                    parameter_is_valid = False
                elif type(parameter) == float:
                    if math.isnan(parameter):
                        parameter_is_valid = False
                    else:
                        parameter_is_valid = True
                elif type(parameter) == datetime.date:
                    parameter_is_valid = False    
                else:
                    parameter_is_valid = True
                
                if parameter_is_valid:
                    if "Count" in column_name:
                        parameter_as_string = "%03d" % parameter
                    elif ("Stack Rank Index" in column_name) or ("KRA" in column_name):
                        parameter_as_string = "%01.2f" % parameter
                    else:
                        if math.isnan(parameter):
                            parameter_as_string = "-"
                        else:
                            parameter_as_string = "%06.2f%%" %(round(parameter*100,4))
                elif column_name in ["Report Date", "Writer ID", "Writer Name", "Writer Email ID", "Reporting Manager"]:
                    parameter_as_string = str(parameter)
                else:
                    parameter_as_string = "-"

                writer_cell_item = QtGui.QTableWidgetItem(parameter_as_string)
                writer_cell_item.setTextAlignment(QtCore.Qt.AlignCenter)
                if parameter_is_valid:
                    if steps != []:
                        if round(parameter,4) < steps[0]:
                            writer_cell_item.setBackgroundColor(red)
                        elif steps[0] <= (round(parameter,4)) <= steps[1]:
                            writer_cell_item.setBackgroundColor(green)
                        elif (round(parameter,4)) > steps[1]:
                            writer_cell_item.setBackgroundColor(blue)
                self.report.setItem(row_counter, column_counter, writer_cell_item)
                column_counter += 1
            row_counter += 1 
        self.report.setSortingEnabled(True)
        self.report.resizeColumnsToContents()
        self.report.resizeRowsToContents()
        sorting_factor = self.getSortColumn()
        if sorting_factor is not "NA":
            sort_index = mode.index(sorting_factor) + 5
            self.report.sortItems(sort_index,QtCore.Qt.DescendingOrder)

    def getSortColumn(self):
        if self.sorting_filter_combobox.currentIndex() != -1:
            return str(self.sorting_filter_combobox.currentText())
        else:
            return "NA"
            
    def displayProgress(self, progress_text, eta, progress, state):
        if state:
            self.pork_lane.allowRun = False
            self.build_button.setEnabled(True)
            self.progress_bar.setFormat("Completed at %s." %(datetime.datetime.strftime(eta,"%H:%M:%S")))        
            self.progress_bar.setValue(progress)
        else:
            self.build_button.setEnabled(False)
            self.progress_bar.setFormat("%s ETA: %s" %(progress_text, datetime.datetime.strftime(eta,"%H:%M:%S")))
            self.progress_bar.setValue(progress)

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([])
    u, p = MOSES.getBigbrotherCredentials()
    dailyporker = DailyPorker(u,p)
    dailyporker.show()
    sys.exit(app.exec_())