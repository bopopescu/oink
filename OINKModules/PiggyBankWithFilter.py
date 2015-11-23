from __future__ import division
import datetime, os, sys
import math
import random

import pandas as pd
from PyQt4 import QtGui, QtCore

import MOSES
from CheckableComboBox import CheckableComboBox
from CategorySelector import CategorySelector
from PiggyBankSummarizer import PiggyBankSummarizer
from CopiableQTableWidget import CopiableQTableWidget
from DescriptionTypeSelector import DescriptionTypeSelector

class PiggyBankWithFilter(QtGui.QWidget):
    def __init__(self, user_id, password, category_tree=None, brands=None):
        super(PiggyBankWithFilter, self).__init__()
        self.user_id, self.password = user_id, password
        if category_tree is not None:
            self.category_tree = category_tree
        else:
            self.category_tree = MOSES.getCategoryTree(self.user_id, self.password)
        if brands is None:
            print "Pulling Brand list in PiggyBankWithFilter"
            self.brands = MOSES.getBrandValues(self.user_id, self.password)
        else:
            self.brands = brands
        self.createUI()
        self.piggybank_data = []
        self.mapEvents()
        self.changePage()
        self.populateBrand()
        self.populateWriters()
        self.show()


    def createUI(self):
        self.instruction_label = QtGui.QLabel("<b>Select filters from the following:</b>")

        self.writers_filter_box = CheckableComboBox("Writers")
        self.writers_filter_box.setToolTip("Select the writers whose data you'd like to extract.")

        self.category_selector = CategorySelector(self.category_tree)

        self.brands_filter_box = CheckableComboBox("Brands")
        self.brands_filter_box.setToolTip("Select the Brands you'd like to extract.")

        self.start_date_edit = QtGui.QDateTimeEdit()
        self.start_date_edit.setToolTip("Select the start date for the data set you'd like to extract.")
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("MMMM dd, yyyy")
        self.start_date_edit.setMinimumDate(QtCore.QDate(2015,1,1))
        
        lwd = MOSES.getLastWorkingDate(self.user_id, self.password, queryUser="All")
        self.start_date_edit.setDate(lwd)

        self.end_date_edit = QtGui.QDateTimeEdit()
        self.end_date_edit.setToolTip("Select the End Date for the data set you'd like to extract.")
        self.end_date_edit.setDate(QtCore.QDate(datetime.date.today()))
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("MMMM dd, yyyy")
        self.end_date_edit.setMinimumDate(self.start_date_edit.date().toPyDate())
        self.end_date_edit.setMaximumDate(datetime.date.today())
        self.end_date_edit.setDate(lwd)

        self.all_time_dates = QtGui.QCheckBox("Pull All Time Data")
        self.all_time_dates.setToolTip("Check this box to pull data for the selected filter from all available data.")

        self.piggybank_summarizer = PiggyBankSummarizer()
        self.piggybank_summarizer.setToolTip("This widget can be used to summarize the piggybank in various ways.")
        self.piggybank_summarizer.setEnabled(False)

        self.piggybank = CopiableQTableWidget(0,0)
        self.piggybank.setToolTip("This table shows all available data for the selected filters.")
        self.piggybank.setStyleSheet("gridline-color: rgb(0, 0, 0)")


        self.piggybank_summary_widget = QtGui.QWidget()
        self.piggybank_summary_column_chooser_label = QtGui.QLabel("Select Column(s):")
        self.piggybank_summary_column_chooser = CheckableComboBox("Columns")
        self.piggybank_summary_column_chooser.setToolTip("Select the piggy bank columns you'd like to summarize.")
        self.piggybank_summary_column_chooser.addItems(["Writer Name","Source", "Description Type", "BU","Super-Category", "Category", "Sub-Category", "Vertical", "Brand"])
        self.piggybank_summary_refresh_button = QtGui.QPushButton("Refresh Summary Table")
        self.piggybank_summary_refresh_button.setToolTip("Click this button to recalculate the audit plan and break up for the selected parameters.")
        
        self.piggybank_summary = CopiableQTableWidget(0,0)
        self.piggybank_summary.setToolTip("This table displays a break up of all the available data between the selected dates, for the chosen filters,\nbased on the summarization columns you've picked.")
        self.piggybank_summary.setStyleSheet("gridline-color: rgb(0, 0, 0)")

        self.piggybank_summary_random_fsns = CopiableQTableWidget(0,0)
        self.piggybank_summary_random_fsns.setToolTip("This table displays a list of random FSNs each editor must audit to satisfy his or her requirements for the selected duration.")
        self.piggybank_summary_random_fsns.setStyleSheet("gridline-color: rgb(0, 0, 0)")
        self.piggybank_summary_editor_summary = CopiableQTableWidget(0,0)
        self.piggybank_summary_editor_summary.setStyleSheet("gridline-color: rgb(0, 0, 0)")
        self.piggybank_summary_audit_percentage_label = QtGui.QLabel("Audit Percentage:")
        self.piggybank_summary_audit_percentage = QtGui.QSpinBox()
        self.piggybank_summary_audit_percentage.setToolTip("This shows the audit percentage for the selected editor(s).")
        self.piggybank_summary_audit_percentage.setRange(0,100)
        self.piggybank_summary_audit_percentage.setSuffix("%")
        self.piggybank_summary_editors_label = QtGui.QLabel("Editor:")
        self.piggybank_summary_editors_list = QtGui.QComboBox()
        self.piggybank_summary_editors_list.setToolTip("Select an editor to display his or her constraints for the chosen time frame.")
        self.piggybank_summary_editors_list.setToolTip("Select an editor to view his or her constraints.")
        self.resetEditorConstraints()
        editors_list = self.editor_audit_constraints.keys()
        editors_list.sort()
        self.piggybank_summary_editors_list.addItems(editors_list)
        self.piggybank_summary_editors_equality_checkbox = QtGui.QCheckBox("Use Equal Targets For All Editors")
        self.piggybank_summary_editors_equality_checkbox.setToolTip("When checked, this nullifies all the personal constraints for editors and treats them equally.\nThis is enabled by default when you purposely remove writer names' from the columns filter.\nUse this when calibrating.")
        self.piggybank_summary_editors_equality_checkbox.setCheckState(False)
        self.piggybank_summary_editor_utilization_label = QtGui.QLabel("Editor Utilization:")
        self.piggybank_summary_editor_utilization = QtGui.QDoubleSpinBox()
        self.piggybank_summary_editor_utilization.setToolTip("Set a utilization factor here.\n1.0 indicates 100%% for a duration of 1 day. If there are multiple working dates selected, then the utilization changes accordingly.\nNote: This doesn't accomodate for leaves taken by editors as of this version.")
        self.piggybank_summary_editor_utilization.setRange(0,3000.0)
        self.piggybank_summary_editor_utilization.setSingleStep(0.05)
        self.piggybank_summary_editor_minimum_wc_label = QtGui.QLabel("Minimum Word Count:")
        self.piggybank_summary_editor_minimum_wc = QtGui.QSpinBox()
        self.piggybank_summary_editor_minimum_wc.setRange(0,5000)
        self.piggybank_summary_editor_minimum_wc.setSingleStep(100)
        self.piggybank_summary_editor_minimum_wc.setToolTip("Set the selected editors(s) minimum word count for a single day.\nNote: this will reinforce a rule that makes the maximum word count at least 1000 words more than itself.")
        self.piggybank_summary_editor_maximum_wc_label = QtGui.QLabel("Maximum Word Count:")
        self.piggybank_summary_editor_maximum_wc = QtGui.QSpinBox()
        self.piggybank_summary_editor_maximum_wc.setRange(0,5000)
        self.piggybank_summary_editor_maximum_wc.setSingleStep(100)
        self.piggybank_summary_editor_maximum_wc.setToolTip("Set the selected editors(s) maximum word count for a single day.\nNote: When changed, it will change the minimum word count so as to satisfy a range of at least 1000 words.")
        self.piggybank_summary_editor_total_wc_label = QtGui.QLabel("Total Word Count (Auto):")
        self.piggybank_summary_editor_total_wc = QtGui.QSpinBox()
        self.piggybank_summary_editor_total_wc.setValue(0)
        self.piggybank_summary_editor_total_wc.setRange(0,3000000)
        self.piggybank_summary_editor_total_wc.setEnabled(False)
        self.piggybank_summary_editor_total_wc.setToolTip("This is an auto-generated field which shows the optimum word count calculated by the system.")
        self.piggybank_summary_reset_stats = QtGui.QPushButton("Reset Editor Stats")


        self.piggybank_summary_tables = QtGui.QTabWidget()
        tab_style = """
            QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid black;
            position: absolute;
            top: -0.5em;
        }

        QTabWidget::tab-bar {
            alignment: center;
        }

        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QTabBar::tab {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                        stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
            border: 2px solid #C4C4C3;
            border-bottom-color: black; /* same as the pane color */
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 8ex;
            padding: 2px;
        }

        QTabBar::tab:selected, QTabBar::tab:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                        stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
        }

        QTabBar::tab:selected {
            border-color: #9B9B9B;
            border-bottom-color: black; /* same as pane color */
        }
        """
        #self.piggybank_summary_tables.setStyleSheet(tab_style)
        self.piggybank_summary_tables.addTab(self.piggybank_summary,"Piggy Bank Summary")
        self.piggybank_summary_tables.addTab(self.piggybank_summary_editor_summary, "Editor Summary")
        self.piggybank_summary_tables.addTab(self.piggybank_summary_random_fsns,"Random FSNs")
        
        self.piggybank_summary_layout = QtGui.QGridLayout()
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_column_chooser_label,0,0)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_column_chooser,0,1)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_editors_equality_checkbox,0,2)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_refresh_button,0,3)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_reset_stats,0,4)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_editors_label,1,0)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_editors_list,1,1)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_audit_percentage_label,1,2)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_audit_percentage,1,3)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_editor_utilization_label,1,4)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_editor_utilization,1,5)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_editor_minimum_wc_label,2,0)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_editor_minimum_wc,2,1)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_editor_maximum_wc_label,2,2)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_editor_maximum_wc,2,3)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_editor_total_wc_label,2,4)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_editor_total_wc,2,5)
        self.piggybank_summary_layout.addWidget(self.piggybank_summary_tables,3,0,8,8)
        self.piggybank_summary_widget.setLayout(self.piggybank_summary_layout)
        
        self.piggybank_tabs = QtGui.QTabWidget()
        self.piggybank_tabs.addTab(self.piggybank,"Piggy Bank")
        self.piggybank_tabs.addTab(self.piggybank_summary_widget,"Audit Planner")
        
        self.reset_button = QtGui.QPushButton("Reset Selected Filters")
        self.reset_button.setToolTip("Click here to reset all chosen filters.")
        self.reset_button.setMinimumWidth(120)
        self.reset_button.setMinimumHeight(20)
        reset_style_string = """
            .QPushButton {
                background-color: red;
                color: white;
                font: 8pt;
            }
            .QPushButton:hover {
                background-color: black;
                color: red;
                font: bold 8pt;
            }
            """
        #self.reset_button.setStyleSheet(reset_style_string)
        self.pull_button = QtGui.QPushButton("Pull Data")
        self.pull_button.setToolTip("Click here to extract data from the OINK server for the selected filters.")
        self.pull_button.setMinimumWidth(150)
        self.pull_button.setMinimumHeight(30)
        style_string = """
        .QPushButton {
            background-color: #0088D6;
            color: #FDDE2E;
            font: 12pt;
        }
        .QPushButton:hover {
            background-color: #FDDE2E;
            color: #0088D6;
            font: bold 12pt;
        }
        """
        #self.pull_button.setStyleSheet(style_string)

        self.description_types_selector = DescriptionTypeSelector(self.category_tree)

        self.sources_label = QtGui.QLabel("Source:")
        self.sources_filter_box = CheckableComboBox("Sources")
        sources = list(set(self.category_tree["Source"]))
        self.sources_filter_box.addItems(sources)


        sources_layout = QtGui.QHBoxLayout()
        sources_layout.addWidget(self.sources_label,0)
        sources_layout.addWidget(self.sources_filter_box,1)
        sources_layout.addStretch(2)

        filters_layout = QtGui.QVBoxLayout()
        filters_layout.addWidget(self.instruction_label)
        filters_sub_layouts = [QtGui.QHBoxLayout() for i in range(5)]
        filters_sub_layouts[0].addWidget(self.all_time_dates,0)
        filters_sub_layouts[0].addWidget(self.start_date_edit,0)
        filters_sub_layouts[0].addWidget(self.end_date_edit,0)
        filters_sub_layouts[0].addWidget(self.writers_filter_box,0)
        filters_sub_layouts[1].addLayout(self.description_types_selector,0)
        filters_sub_layouts[2].addLayout(sources_layout,0)
        filters_sub_layouts[3].addLayout(self.category_selector,1)
        filters_sub_layouts[4].addWidget(self.brands_filter_box,0)
        filters_sub_layouts[4].addWidget(self.reset_button,0)
        filters_sub_layouts[4].addWidget(self.pull_button,2)

        for each_layout in filters_sub_layouts:
            filters_layout.addLayout(each_layout)
        filters_layout.addWidget(self.piggybank_summarizer,2)
        filter_and_piggybank_layout = QtGui.QHBoxLayout()
        filter_and_piggybank_layout.addLayout(filters_layout,0)
        filter_and_piggybank_layout.addWidget(self.piggybank_tabs,2)
        layout = QtGui.QVBoxLayout()
        layout.addLayout(filter_and_piggybank_layout,3)
        self.status = QtGui.QLabel("")
        layout.addWidget(self.status,0)
        self.setLayout(layout)
        self.setWindowTitle("Piggy Bank and Audit Planner")
        if "OINKModules" in os.getcwd():
            icon_file_name_path = os.path.join(os.path.join('..',"Images"),'PORK_Icon.png')
        else:
            icon_file_name_path = os.path.join('Images','PORK_Icon.png')
        self.setWindowIcon(QtGui.QIcon(icon_file_name_path))
        self.move(120,100)

    def mapEvents(self):
        self.start_date_edit.dateChanged.connect(self.limitEndDate)
        self.end_date_edit.dateChanged.connect(self.changeEndDate)
        self.all_time_dates.stateChanged.connect(self.toggleDates)
        self.pull_button.clicked.connect(self.pullData)
        self.piggybank_summary_refresh_button.clicked.connect(self.summarize)
        self.piggybank_summary_editors_equality_checkbox.stateChanged.connect(self.toggleEditorEquality)
        self.piggybank_summary_editors_list.currentIndexChanged.connect(self.changePage)
        self.piggybank_summary_editor_utilization.valueChanged.connect(self.changeUtilization)
        self.piggybank_summary_audit_percentage.valueChanged.connect(self.changeAuditPercentage)
        self.piggybank_summary_editor_maximum_wc.valueChanged.connect(self.changeMaxWordCount)
        self.piggybank_summary_editor_minimum_wc.valueChanged.connect(self.changeMinWordCount)
        self.piggybank_summary_reset_stats.clicked.connect(self.summaryFormReset)
        self.reset_button.clicked.connect(self.resetFilters)

    def resetFilters(self):
        self.description_types_filter_box.clearSelection()
        self.sources_filter_box.clearSelection()
        self.writers_filter_box.clearSelection()
        self.category_selector.clearFilters()
        self.brands_filter_box.clearSelection()
        self.start_date_edit.setDate(datetime.date.today())
        self.end_date_edit.setDate(datetime.date.today())

    def changeUtilization(self):
        current_page = str(self.piggybank_summary_editors_list.currentText())
        self.editor_audit_constraints[current_page]["Editor Utilization"] = self.piggybank_summary_editor_utilization.value()

    def changeAuditPercentage(self):
        current_page = str(self.piggybank_summary_editors_list.currentText())
        self.editor_audit_constraints[current_page]["Audit Percentage"] = self.piggybank_summary_audit_percentage.value()
        
    def changeMaxWordCount(self):
        new_word_count = self.piggybank_summary_editor_maximum_wc.value()
        self.piggybank_summary_editor_minimum_wc.setMaximum((new_word_count-1000))
        current_page = str(self.piggybank_summary_editors_list.currentText())
        self.editor_audit_constraints[current_page]["Maximum Word Count"] = new_word_count

    def changeMinWordCount(self):
        new_word_count = self.piggybank_summary_editor_minimum_wc.value()
        self.piggybank_summary_editor_maximum_wc.setMinimum((new_word_count+1000))
        current_page = str(self.piggybank_summary_editors_list.currentText())
        self.editor_audit_constraints[current_page]["Minimum Word Count"] = new_word_count

    def changePage(self):
        current_page = str(self.piggybank_summary_editors_list.currentText())
        self.piggybank_summary_audit_percentage.setValue(self.editor_audit_constraints[current_page]["Audit Percentage"])
        self.piggybank_summary_editor_utilization.setValue(self.editor_audit_constraints[current_page]["Editor Utilization"])
        self.piggybank_summary_editor_minimum_wc.setValue(self.editor_audit_constraints[current_page]["Minimum Word Count"])
        self.piggybank_summary_editor_maximum_wc.setValue(self.editor_audit_constraints[current_page]["Maximum Word Count"])
        self.piggybank_summary_editor_total_wc.setValue(self.editor_audit_constraints[current_page]["Total Word Count"])

    def limitEndDate(self):
        self.end_date_edit.setMinimumDate(self.start_date_edit.date())
        self.end_date_edit.setDate(self.start_date_edit.date())
        self.populateWriters()
        #self.resetEditorConstraints()
        #self.changePage()

    def changeEndDate(self):
        pass
        #self.resetEditorConstraints()
        #self.changePage()

    def toggleDates(self,state):
        if state == 0:
            self.start_date_edit.setEnabled(True)
            self.end_date_edit.setEnabled(True)
        else:
            self.start_date_edit.setEnabled(False)
            self.end_date_edit.setEnabled(False)
    
    def toggleEditorEquality(self, state):
        if state == 0:
            self.piggybank_summary_editors_list.setEnabled(True)
        else:
            self.piggybank_summary_editors_list.setEnabled(False)
            self.piggybank_summary_editors_list.setCurrentIndex(self.piggybank_summary_editors_list.findText("All"))

    def populateWriters(self):
        self.writers_filter_box.clear()
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()
        self.writers_list = MOSES.getWritersList(self.user_id, self.password, start_date)

        writers = list(set(self.writers_list["Name"]))
        writers.sort()
        self.writers_filter_box.addItems(writers)

    def populateBrand(self):
        self.brands_filter_box.clear()
        self.brands_filter_box.addItems(self.brands)

    def pullData(self):
        #print "Pulling data!"
        self.pull_button.setEnabled(False)
        self.piggybank_summarizer.setEnabled(False)
        self.piggybank.showDataFrame(None)
        message = "processing..."
        self.status.setText(message)
        self.alertMessage("Please Wait","Depending on the filters you have chosen, this step could take a second or a minute, though definitely not more than 60s. Please wait, and remember, <i>Roma die uno non aedificata est</i>.")
        filters = self.getFilters()
        data = MOSES.getPiggyBankWithFilters(self.user_id, self.password, filters)
        if data is None:
            message = "No data for selected filters."
            self.status.setText(message)            
            self.alertMessage("No Data Available","There is no data pertaining to the selected filters. This could have occurred for several reasons:\n1. You may have selected too many filters which have no result, or\n2. You could have selected a date range between which there have been no articles.")        
        else:
            if data.shape[0] <=0:
                self.status.setText(message)            
                message = "No data for selected filters."
                self.alertMessage("No Data Available","There is no data pertaining to the selected filters. This could have occurred for several reasons:\n1. You may have selected too many filters which have no result, or\n2. You could have selected a date range between which there have been no articles, or, simply\n3. There is no data.")
            else:            
                self.piggybank_data = data
                self.piggybank.showDataFrame(self.piggybank_data)
                #populate the summary next.
                self.piggybank_summarizer.setEnabled(True)
                self.piggybank_summarizer.setPiggyBank(data)
                message = "Retrieved %d rows of data pertaining to your filters."%(data.shape[0])
                self.alertMessage("Retrieved Data",message)
                self.status.setText(message)
                #self.summarize()
        self.pull_button.setEnabled(True)

    def showDataFrameInTable(self, dataframe, table_object):
        table_object.showDataFrame(dataframe)

    def getSummarizeParameters(self):
        summarize_parameters = self.piggybank_summary_column_chooser.getCheckedItems()
        if summarize_parameters == []:
            summarize_parameters = ["Writer Name","Category","Description Type"]
        return summarize_parameters

    def getBreakUpTableFromPiggyBank(self):
        data = self.piggybank_data
        summarize_parameters = self.getSummarizeParameters()
        #Build a summary matrix with the different types of the selected summarize parameters.
        matrix = []
        for row in data:
            row_qualifier = dict((key,None) for key in summarize_parameters)
            for key in summarize_parameters:
                row_qualifier[key] = row[key]
            matrix.append(row_qualifier)
        #Build a dictionary which the values for the selected summarize parameters.
        result = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in matrix)]
        return result, summarize_parameters


    def summarize(self):
        """
        This is the audit planner and summarization method. It does several things.
        1. It summarizes the piggy bank that has been pulled. 
            By default, it summarizes by writer x description type x category. This can be changed using the filterbox provided for the summarization columns.
        2. It also computes the optimum audit plan given a set of constraints that can be changed at will using the form. An equalized method may also be used, depending upon need. This is mainly designed for calibration at a later stage.
            (a) Note that there are some problems with how audit numbers will be pulled up. 
                This has nothing to do with the code, but it is rooted in the process itself.
            (b) If a writer reports irregular numbers on a regular basis, this will increase the editors' work for a 
                timeframe as opposed to situations where he posts regular work. 
                The solution for this is to even out the spikes in efficiency.
            (c) In situations where evening out the efficiency spikes is impossible, calibration of audit numbers over a timeframe is recommended. This is out of the scope of this code for the time being, and depending upon
                feedback and feasibility, it may be incorporated at a later stage.
            (d) Long story short, if a writer reports 0% on one day and 200% on the next, the code will decrease an editor's
                overall audit percentage to equalize the fairness of the audit percentage. Although this solves the problem
                for the current time frame, if repeated regularly, it will give that writer a much lesser audit percentage
                than the rest of the team. If this is acceptable, then there's no cause for concern.
                If this isn't acceptable, then the editor will need to generate the audit plan for a set of dates, and check
                the difference in audit numbers. The editor will need to pick up extra audits as required, and naturally, these
                are outside the 100% efficiency for his or her day. This will give the editor extra efficiency for the day.
            (e) General Note:
        3. After pulling the audit plan, it loops through the piggy bank and pulls up random fsns to satisfy the requirements pf the plan and displays this data.
        """
        result, summarize_parameters = self.getBreakUpTableFromPiggyBank()
        #Now process for audit percentages
        #First, check if you're looking at this at a writer level
        #If writer level, check if all editors' efficiency is equalized.
        #If the following are satisfied, use overall stats, not the editors' values.
        equalize_editors = True
        if "Writer Name" in summarize_parameters:
            if not self.piggybank_summary_editors_equality_checkbox.isChecked():
                equalize_editors = False
                summarize_parameters.append("Editor Name")

        #Set a bool to check the audit conditions.
        audit_conditions_satisfied = False

        #Now calculate the upper and lower limits based on the utilization and min/max word counts.
        for editor in self.editor_audit_constraints.keys():
            editor_data = self.editor_audit_constraints[editor]
            editor_data["Audit Conditions Satisfied"] = False
            editor_data["Target Maximum Word Count"] = editor_data["Editor Utilization"]*editor_data["Maximum Word Count"]
            editor_data["Target Minimum Word Count"] = editor_data["Editor Utilization"]*editor_data["Minimum Word Count"]
    
        #Now, for as long as the audit conditions aren't satisfied, keep repeating the following steps.
        first_run = True
        counter = 0
        while not audit_conditions_satisfied:
            counter+=1
            for editor in self.editor_audit_constraints.keys():
                if not self.editor_audit_constraints[editor]["Audit Conditions Satisfied"]:
                    self.editor_audit_constraints[editor]["Total Word Count"] = 0
                    self.editor_audit_constraints[editor]["Audit Count"] = 0
                    #print "Resetting %s's word count." %editor

            #For each row in the result, count the numbers from the piggy bank data set.
            for qualifier_row in result:
                if first_run:
                    qualifier_row["Article Count"] = 0
                    qualifier_row["Word Count"] = 0
                    for row in self.piggybank_data:
                        row_match = True
                        for key in qualifier_row:
                            if (key not in ["Article Count", "Word Count", "Suggested Audits","Approx. Word Count of Audits"]):
                                if qualifier_row[key] != row[key]:
                                    row_match = False
                        if row_match:
                            qualifier_row["Article Count"] += 1
                            qualifier_row["Word Count"] += row["Word Count"]
                #Now, plan the suggested audits.
                #If the editors have equalized targets.
                if equalize_editors:
                    audit_percentage = self.editor_audit_constraints["All"]["Audit Percentage"]/100
                    qualifier_row["Suggested Audits"] = int(math.ceil(audit_percentage*qualifier_row["Article Count"]))
                    self.editor_audit_constraints["All"]["Audit Count"] += qualifier_row["Suggested Audits"]
                    qualifier_row["Approx. Word Count of Audits"] = int(math.ceil(qualifier_row["Suggested Audits"]*qualifier_row["Word Count"]/qualifier_row["Article Count"]))
                    self.editor_audit_constraints["All"]["Total Word Count"] += qualifier_row["Approx. Word Count of Audits"]
                else:
                    try:
                        editor_name = self.getEditorName(qualifier_row["Writer Name"])
                        if not self.editor_audit_constraints[editor_name]["Audit Conditions Satisfied"]:
                            qualifier_row["Editor Name"] = editor_name
                            audit_percentage = self.editor_audit_constraints[editor_name]["Audit Percentage"]/100
                            qualifier_row["Suggested Audits"] = int(math.ceil(audit_percentage*qualifier_row["Article Count"]))
                            self.editor_audit_constraints[editor_name]["Audit Count"] += qualifier_row["Suggested Audits"]
                            qualifier_row["Approx. Word Count of Audits"] = int(math.ceil(qualifier_row["Suggested Audits"]*qualifier_row["Word Count"]/qualifier_row["Article Count"]))
                            self.editor_audit_constraints[editor_name]["Total Word Count"] += qualifier_row["Approx. Word Count of Audits"]
                    except KeyError:
                        print "PiggyBankWithFilter:Summarize: %s doesn't have a mapped editor."%qualifier_row["Writer Name"]
                    except Exception, e:
                        print "PiggyBankWithFilter:Summarize: Encountered error: %s."%repr(e)

            #Check if the audit conditions have been satisfied.
            if equalize_editors:
                scope = "All"
                if self.editor_audit_constraints[scope]["Total Word Count"] <= self.editor_audit_constraints[scope]["Target Minimum Word Count"]:
                    self.editor_audit_constraints[scope]["Audit Percentage"] += self.piggybank_summary_audit_percentage.singleStep()
                    if self.editor_audit_constraints[scope]["Audit Percentage"] > 100:
                        self.alertMessage("Error Planning Audits","Audit percentage is out of bounds. Set to %d%%" %(self.editor_audit_constraints[scope]["Audit Percentage"]))
                        self.editor_audit_constraints[scope]["Audit Conditions Satisfied"] = True
                    else:
                        #print "Increasing audit percentage to", self.editor_audit_constraints[scope]["Audit Percentage"]
                        self.editor_audit_constraints[scope]["Audit Percentage"] += self.piggybank_summary_audit_percentage.singleStep()
                elif self.editor_audit_constraints[scope]["Total Word Count"] >= self.editor_audit_constraints[scope]["Target Maximum Word Count"]:
                    #Editors are over-utilized
                    #print "Over-utilizing %s!" %scope
                    #print """Target Max and Min WCs : %(Target Maximum Word Count)d, %(Target Minimum Word Count)d. Total WC: %(Total Word Count)d""" %(self.editor_audit_constraints[scope])
                    if self.editor_audit_constraints[scope]["Audit Percentage"] <= 1:
                        #print self.editor_audit_constraints[scope]
                        self.alertMessage("Error Planning Audits","Audit percentage is out of bounds. Set to %d%%" %(self.editor_audit_constraints[scope]["Audit Percentage"]))
                        self.editor_audit_constraints[scope]["Audit Conditions Satisfied"] = True
                    else:
                        self.editor_audit_constraints[scope]["Audit Percentage"] -= self.piggybank_summary_audit_percentage.singleStep()
                        #print "Decreasing audit percentage to", self.editor_audit_constraints[scope]["Audit Percentage"]
                elif (self.editor_audit_constraints[scope]["Total Word Count"] >= self.editor_audit_constraints[scope]["Target Minimum Word Count"]) and (self.editor_audit_constraints[scope]["Total Word Count"] <= self.editor_audit_constraints[scope]["Target Maximum Word Count"]):
                    #print "%s is well used.!" %scope
                    if self.editor_audit_constraints[scope]["Audit Percentage"] < 0:
                        raise Exception
                    #print """Target Max and Min WCs : %(Target Maximum Word Count)d, %(Target Minimum Word Count)d. Total WC: %(Total Word Count)d""" %(self.editor_audit_constraints[scope])
                    self.editor_audit_constraints[scope]["Audit Conditions Satisfied"] = True
                else:
                    raise Exception
                audit_conditions_satisfied = self.editor_audit_constraints[scope]["Audit Conditions Satisfied"]
            else:
                editors = self.editor_audit_constraints.keys()
                editors.remove("All")
                editors.sort()
                audit_conditions_satisfied = True
                for editor in editors:
                    scope = editor
                        #Editors are under-utilized
                    if self.editor_audit_constraints[scope]["Total Word Count"] <= self.editor_audit_constraints[scope]["Target Minimum Word Count"]:
                        #print "Under-utilizing %s!" %scope
                        #print """Target Max and Min WCs : %(Target Maximum Word Count)d, %(Target Minimum Word Count)d. Total WC: %(Total Word Count)d""" %(self.editor_audit_constraints[scope])
                        if self.editor_audit_constraints[scope]["Audit Percentage"] >= 100:
                            self.alertMessage("Error Planning Audits","%s's audit percentage is out of bounds. Set to %d%%" %(scope,self.editor_audit_constraints[scope]["Audit Percentage"]))
                            self.editor_audit_constraints[scope]["Audit Conditions Satisfied"] = True
                        else:
                            #print "Increasing audit percentage to", self.editor_audit_constraints[scope]["Audit Percentage"]
                            self.editor_audit_constraints[scope]["Audit Percentage"] += self.piggybank_summary_audit_percentage.singleStep()
                    elif self.editor_audit_constraints[scope]["Total Word Count"] >= self.editor_audit_constraints[scope]["Target Maximum Word Count"]:
                        #Editors are over-utilized
                        #print "Over-utilizing %s!" %scope
                        #print """Target Max and Min WCs : %(Target Maximum Word Count)d, %(Target Minimum Word Count)d. Total WC: %(Total Word Count)d""" %(self.editor_audit_constraints[scope])
                        if self.editor_audit_constraints[scope]["Audit Percentage"] <= 1:
                            self.alertMessage("Error Planning Audits","%s's audit percentage is out of bounds. Set to %d%%" %(scope,self.editor_audit_constraints[scope]["Audit Percentage"]))
                            self.editor_audit_constraints[scope]["Audit Conditions Satisfied"] = True
                        else:
                            #print "Decreasing audit percentage to", self.editor_audit_constraints[scope]["Audit Percentage"]
                            self.editor_audit_constraints[scope]["Audit Percentage"] -= self.piggybank_summary_audit_percentage.singleStep()
                    elif (self.editor_audit_constraints[scope]["Total Word Count"] >= self.editor_audit_constraints[scope]["Target Minimum Word Count"]) and (self.editor_audit_constraints[scope]["Total Word Count"] <= self.editor_audit_constraints[scope]["Target Maximum Word Count"]):
                        #print "%s is well used.!" %scope
                        if self.editor_audit_constraints[scope]["Audit Percentage"] < 0:
                            self.alertMessage("Error Planning Audits","%s's audit percentage is out of bounds. Set to %d%%" %(scope,self.editor_audit_constraints[scope]["Audit Percentage"]))
                            raise Exception
                        #print """Target Max and Min WCs : %(Target Maximum Word Count)d, %(Target Minimum Word Count)d. Total WC: %(Total Word Count)d""" %(self.editor_audit_constraints[scope])
                        self.editor_audit_constraints[scope]["Audit Conditions Satisfied"] = True
                    else:
                        raise Exception
                    audit_conditions_satisfied = self.editor_audit_constraints[editor]["Audit Conditions Satisfied"] and audit_conditions_satisfied
            if counter >= 100:
                self.alertMessage("Infinite Loop","Since the code was stuck in an infinite loop trying to calculate an optimum audit breakup, the program has triggered a failsafe.")
                audit_conditions_satisfied = True
            first_run = False
        headers = summarize_parameters + ["Article Count", "Word Count", "Suggested Audits","Approx. Word Count of Audits"]
        self.piggybank_summary.setRowCount(len(result))
        self.piggybank_summary.setColumnCount(len(headers))
        row_index = 0
        self.piggybank_summary.setSortingEnabled(False)
        for qualifier_row in result:
            column_index = 0
            for key in headers:
                self.piggybank_summary.setItem(row_index, column_index, QtGui.QTableWidgetItem(str(qualifier_row[key])))
                column_index += 1
            row_index += 1
        self.piggybank_summary.setSortingEnabled(True)
        self.piggybank_summary.setHorizontalHeaderLabels(headers)
        self.piggybank_summary.resizeColumnsToContents()
        self.piggybank_summary.resizeRowsToContents()
        
        self.piggybank_summary_editor_summary.setSortingEnabled(False)
        editors = self.editor_audit_constraints.keys()
        editors.remove("All")
        editors.sort()
        row_index = 0
        self.piggybank_summary_editor_summary.setRowCount(3)
        editor_summary_labels = ["Editor Name", "Audit Count", "Total Word Count", "Target Minimum Word Count", "Target Maximum Word Count", "Audit Percentage"]
        self.piggybank_summary_editor_summary.setColumnCount(len(editor_summary_labels))
        for editor in editors:
            self.piggybank_summary_editor_summary.setItem(row_index,0,QtGui.QTableWidgetItem(editor))
            self.piggybank_summary_editor_summary.setItem(row_index,1,QtGui.QTableWidgetItem(str(self.editor_audit_constraints[editor]["Audit Count"])))
            self.piggybank_summary_editor_summary.setItem(row_index,2,QtGui.QTableWidgetItem(str(self.editor_audit_constraints[editor]["Total Word Count"])))
            self.piggybank_summary_editor_summary.setItem(row_index,3,QtGui.QTableWidgetItem(str(self.editor_audit_constraints[editor]["Target Minimum Word Count"])))
            self.piggybank_summary_editor_summary.setItem(row_index,4,QtGui.QTableWidgetItem(str(self.editor_audit_constraints[editor]["Target Maximum Word Count"])))
            self.piggybank_summary_editor_summary.setItem(row_index,5,QtGui.QTableWidgetItem(str(self.editor_audit_constraints[editor]["Audit Percentage"])))
            row_index +=1
        self.piggybank_summary_editor_summary.setSortingEnabled(True)
        self.piggybank_summary_editor_summary.setHorizontalHeaderLabels(editor_summary_labels)
        self.piggybank_summary_editor_summary.resizeColumnsToContents()
        self.piggybank_summary_editor_summary.resizeRowsToContents()
        self.audit_break_up = result
        self.alertMessage("Completed Audit Plan","Completed Audit Plan for %s"%self.start_date_edit.date().toPyDate())
        self.changePage()
        self.randomizeAudits()

    def getEditorName(self, writer_name):
        editors = [name for name in self.editor_audit_constraints.keys()]
        editors.remove("All")
        for editor in editors:
            if writer_name in self.editor_audit_constraints[editor]["Writers"]:
                return editor

    def getFilters(self):

        if self.all_time_dates.isChecked():
            start_date = datetime.date(2015,1,1)
            end_date = datetime.date.today()
        else:
            start_date = self.start_date_edit.date().toPyDate()
            end_date = self.end_date_edit.date().toPyDate()

        writers = self.writers_filter_box.getCheckedItems()
        if len(writers) > 0:
            writers_filter = writers
        else:
            writers_filter = None

        selected_category_tree = self.category_selector.getFilters()

        if selected_category_tree.shape[0]>0:
            category_tree_filter = selected_category_tree
        else:

            category_tree_filter = None

        description_types = self.description_types_selector.getCheckedItems()
        if len(description_types) > 0:
            description_types_filter = description_types
        else:            
            description_types_filter = None

        brands = self.brands_filter_box.getCheckedItems()
        if len(brands) > 0:
            brands_filter = brands
        else:
            brands_filter = None
        
        sources = self.sources_filter_box.getCheckedItems()
        if len(sources) > 0:
            sources_filter = sources
        else:
            sources_filter = None
        

        return {
            "Dates": [start_date, end_date],
            "Writers": writers_filter,
            "Category Tree": category_tree_filter,
            "Description Types": description_types_filter,
            "Brands": brands_filter,
            "Sources": sources_filter
        }

    def summaryFormReset(self):
        self.resetEditorConstraints()
        self.changePage()

    def resetEditorConstraints(self):
        self.editor_audit_constraints = {
        "Varkey": {
            "Audit Percentage":30, 
            "Minimum Word Count": 4000, 
            "Maximum Word Count": 5000,
            "Editor Utilization": 1.0*len(MOSES.getWorkingDatesBetween(self.user_id,self.password,self.start_date_edit.date().toPyDate(),self.end_date_edit.date().toPyDate(),mode="All")),
            "Target Minimum Word Count": 0,
            "Target Maximum Word Count": 0,
            "Total Word Count": 0,
            "Audit Count": 0,
            "Audit Conditions Satisfied": False,
            "Writers": MOSES.getWritersListForEditor(self.user_id, self.password, "Varkey")
            },
        "Varun Chhabria": {
            "Audit Percentage":30, 
            "Minimum Word Count": 2000, 
            "Maximum Word Count": 5000,
            "Editor Utilization": 1.0*len(MOSES.getWorkingDatesBetween(self.user_id,self.password,self.start_date_edit.date().toPyDate(),self.end_date_edit.date().toPyDate(),mode="All")),
            "Target Minimum Word Count": 0,
            "Target Maximum Word Count": 0,
            "Total Word Count": 0,
            "Audit Count": 0,
            "Audit Conditions Satisfied": False,
            "Writers": MOSES.getWritersListForEditor(self.user_id, self.password, "Varun Chhabria")
            },
        "Manasa Prabhu": {
            "Audit Percentage":30, 
            "Minimum Word Count": 4000, 
            "Maximum Word Count": 5000,
            "Editor Utilization": 1.0*len(MOSES.getWorkingDatesBetween(self.user_id,self.password,self.start_date_edit.date().toPyDate(),self.end_date_edit.date().toPyDate(),mode="All")),
            "Target Minimum Word Count": 0,
            "Target Maximum Word Count": 0,
            "Total Word Count": 0,
            "Audit Count": 0,
            "Audit Conditions Satisfied": False,
            "Writers": MOSES.getWritersListForEditor(self.user_id, self.password, "Manasa Prabhu")
            },
        "All": {
            "Audit Percentage":30, 
            "Minimum Word Count": 4000, 
            "Maximum Word Count": 5000,
            "Editor Utilization": 3.0*len(MOSES.getWorkingDatesBetween(self.user_id,self.password,self.start_date_edit.date().toPyDate(),self.end_date_edit.date().toPyDate(),mode="All")),
            "Target Minimum Word Count": 0,
            "Target Maximum Word Count": 0,
            "Total Word Count": 0,
            "Audit Count": 0,
            "Audit Conditions Satisfied": False,
            "Writers": MOSES.getWritersListForEditor(self.user_id, self.password)
            }
        }

    def randomizeAudits(self):
        """
        This method:
        1. loops through each row of the audit planner table.
        2. extracts n FSNs from the displayed piggybank, using the data set in the audit planner as a filter. The value n is the suggested audit number.
        3. adds these FSNs to the result table.
        """
        #print "Randomizing audits"
        audit_plan = self.audit_break_up
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()
        random_fsn_set = []
        for row in audit_plan:
            required_fsns = row["Suggested Audits"]
            constraint_keys = row.keys()
            unnecessary_keys = ["Article Count", "Word Count", "Suggested Audits","Approx. Word Count of Audits","Editor Name"]
            for key in unnecessary_keys:
                if key in constraint_keys:
                    constraint_keys.remove(key)

            requirement_filters = dict((key,row[key]) for key in constraint_keys)
            pulled_fsns = self.getRandomFSNs(requirement_filters, required_fsns)
            random_fsn_set.append(pulled_fsns)
        final_fsn_set = [item for sublist in random_fsn_set for item in sublist]
        self.piggybank_summary_random_fsns.setRowCount(len(final_fsn_set))
        self.piggybank_summary_random_fsns.setSortingEnabled(False)
        if "Editor Name" in audit_plan[0].keys():
            random_fsn_data_set_keys = ["Editor Name"]
        else:
            random_fsn_data_set_keys = []
        random_fsn_data_set_keys += (["FSN","Article Date"] + constraint_keys + ["Upload Link", "Word Count"])
        row_index = 0
        self.piggybank_summary_random_fsns.setColumnCount(len(random_fsn_data_set_keys))
        for row in final_fsn_set:
            column_index = 0
            for key in random_fsn_data_set_keys:
                if key == "Editor Name":
                    self.piggybank_summary_random_fsns.setItem(row_index,column_index,QtGui.QTableWidgetItem(self.getEditorName(row["Writer Name"])))
                else:
                    self.piggybank_summary_random_fsns.setItem(row_index,column_index,QtGui.QTableWidgetItem(str(row[key])))
                column_index += 1
            row_index += 1
        self.piggybank_summary_random_fsns.setSortingEnabled(True)
        self.piggybank_summary_random_fsns.setHorizontalHeaderLabels(random_fsn_data_set_keys)
        self.alertMessage("Pulled Random FSNs","Successfully pulled %d random FSNs for the selected dates." % len(final_fsn_set))
            
    def getRandomFSNs(self, constraints, quantity):
        valid_rows = []
        for row in self.piggybank_data:
            valid = True
            for key in constraints.keys():
                if row[key] != constraints[key]:
                    valid = False
            if valid:
                valid_rows.append(row)
        random.shuffle(valid_rows)
        random_fsns = valid_rows[0:quantity]
        return random_fsns

    def alertMessage(self, title, message):
        """Vindaloo."""
        QtGui.QMessageBox.about(self, title, message)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    QtGui.qApp.setStyle(QtCore.QString(u'Plastique'))
    u, p = MOSES.getBigbrotherCredentials()
    piggybank = PiggyBankWithFilter(u,p)
    piggybank.show()
    sys.exit(app.exec_())