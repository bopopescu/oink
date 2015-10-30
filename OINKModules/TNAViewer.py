from __future__ import division
import math
import os
import datetime

import MySQLdb
import numpy as np
import pandas as pd
from PyQt4 import QtGui, QtCore
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import MOSES
from ProgressBar import ProgressBar
from ImageLabel import ImageLabel
from CheckableComboBox import CheckableComboBox
from FilterForm import FilterForm

class TNAViewer(QtGui.QWidget):
    def __init__(self, user_id, password, category_tree, viewer_level=None, *args, **kwargs):
        super(TNAViewer, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.password = password
        self.category_tree = category_tree
        parameters_date = datetime.date.today()
        self.audit_parameters_dataframe = MOSES.getAuditParametersData(self.user_id, self.password, parameters_date)
        #the viewer level controls the scope of the program.
        #A Level 0 limits the visibility to the current user, and shows the team's quality in comparison.
        #A level 1 allows choosing the users.
        if (viewer_level is not None) and  viewer_level in [0, 1]:
            self.viewer_level = viewer_level
        else:
            self.viewer_level = 0
        self.createUI()
        self.mapEvents()
        self.initiate()

    def initiate(self):
        self.populateBaseEditorAndWritersList()
        self.populateComparisonEditorAndWritersList()
        self.populateAuditParameters()

    def populateBaseEditorAndWritersList(self):
        self.base_data_set_group.populateEditorAndWritersList()

    def populateComparisonEditorAndWritersList(self):
        self.comparison_data_set_group.populateEditorAndWritersList()

    def populateAuditParameters(self):
        parameters_date = self.base_data_set_group.getDates()[0]
        self.audit_parameters_dataframe = MOSES.getAuditParametersData(self.user_id, self.password, parameters_date)
        self.audit_parameters = self.audit_parameters_dataframe["Column Descriptions"]
        self.parameters_combobox.clear()
        self.parameters_combobox.addItems(self.audit_parameters)

    
    def createUI(self):
        self.base_data_set_group = FilterForm(
                                            self.user_id,   
                                            self.password,    
                                            (0,0,0),   
                                            self.category_tree,   
                                            self.viewer_level,    
                                            "Base Data Set")
        self.comparison_data_set_group = FilterForm(
                                            self.user_id, 
                                            self.password, 
                                            (0,0,0), 
                                            self.category_tree, 
                                            self.viewer_level, 
                                            "Comparison Data Set")


        self.analysis_parameters_group = QtGui.QGroupBox("Analysis Parameters")
        self.parameters_label = QtGui.QLabel("Compare:")
        self.parameters_combobox = CheckableComboBox("Parameters")
        self.parameters_all_button = QtGui.QPushButton("All")
        self.parameters_cfm_button = QtGui.QPushButton("CFM")
        self.parameters_gseo_button = QtGui.QPushButton("GSEO")
        self.parameters_fatal_button = QtGui.QPushButton("Fatals")
        self.parameters_clear_button = QtGui.QPushButton("None")



        parameters_layout = QtGui.QVBoxLayout()
        
        parameter_selection_row = QtGui.QHBoxLayout()
        parameter_selection_row.addWidget(self.parameters_label)
        parameter_selection_row.addWidget(self.parameters_combobox)

        parameters_buttons_layout = QtGui.QHBoxLayout()
        parameters_buttons_layout.addWidget(self.parameters_all_button, QtCore.Qt.AlignTop)
        parameters_buttons_layout.addWidget(self.parameters_cfm_button, QtCore.Qt.AlignTop)
        parameters_buttons_layout.addWidget(self.parameters_gseo_button, QtCore.Qt.AlignTop)
        parameters_buttons_layout.addWidget(self.parameters_fatal_button, QtCore.Qt.AlignTop)
        parameters_buttons_layout.addWidget(self.parameters_clear_button, QtCore.Qt.AlignTop)

        parameters_layout.addLayout(parameter_selection_row)
        parameters_layout.addLayout(parameters_buttons_layout)
        
        self.analysis_parameters_group.setLayout(parameters_layout)

        self.plot_options_group = QtGui.QGroupBox("Plotting Options")
        self.plot_type_label = QtGui.QLabel("Plot:")
        self.plot_type_combobox = CheckableComboBox("Chart Types")
        self.plot_types = [
                            "Histogram",
                            "Pareto",
                            "Daily Trend",
                            "Weekly Trend",
                            "Monthly Trend",
                            "Quarterly Trend",
                            "Half-Yearly Trend",
                            "Radar Scatter Chart"
                        ]
        self.plot_type_combobox.addItems(self.plot_types)
        self.plot_separate_charts_for_each_parameter = QtGui.QCheckBox("Parameter Charts")
        self.use_minimum_acceptable_scores = QtGui.QCheckBox("Consider an acceptable article to be the base")
        self.use_minimum_acceptable_scores.setToolTip("If checked, the tool will plot charts by considering an article with\n96% CFM and 95% GSEO article to be the base.\nOtherwise, it compares scores against a 100 article.")

        self.load_data_button = QtGui.QPushButton("Load Data")
        self.plot_button = QtGui.QPushButton("Plot Charts")
        self.plot_save_button = QtGui.QPushButton("Save Charts")
        self.plot_zoom_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.plot_zoom_label = QtGui.QLabel("100%")
        self.plot_zoom_slider.setRange(10,500)
        self.plot_zoom_slider.setValue(100)
        self.plot_zoom_slider.setSingleStep(1)
        #self.plot_zoom_slider.valueChanged.connect(self.zoomInOut)
        self.plot_zoom_slider.setTickInterval(10)
        self.plot_zoom_slider.setTickPosition(2)

        self.plot_button.setEnabled(False)
        self.plot_save_button.setEnabled(False)

        plot_options_layout = QtGui.QVBoxLayout()

        plot_options_row_1 = QtGui.QHBoxLayout()
        plot_options_row_1.addWidget(self.plot_type_label,0)
        plot_options_row_1.addWidget(self.plot_type_combobox,0)
        plot_options_row_1.addWidget(self.plot_separate_charts_for_each_parameter,0)
        plot_options_layout.addLayout(plot_options_row_1)

        plot_options_row_2 = QtGui.QHBoxLayout()
        plot_options_row_2.addWidget(self.use_minimum_acceptable_scores,1)
        plot_options_layout.addLayout(plot_options_row_2)
        
        plot_options_row_3 = QtGui.QHBoxLayout()
        plot_options_row_3.addWidget(self.load_data_button,0)
        plot_options_row_3.addWidget(self.plot_button,0)
        plot_options_row_3.addWidget(self.plot_save_button,0)
        plot_options_row_3.addStretch(1)
        plot_options_layout.addLayout(plot_options_row_3)

        plot_options_row_4 = QtGui.QHBoxLayout()
        plot_options_row_4.addWidget(self.plot_zoom_slider,3)
        plot_options_row_4.addWidget(self.plot_zoom_label,1)
        plot_options_layout.addLayout(plot_options_row_4)

        
        self.plot_options_group.setLayout(plot_options_layout)

        self.plot_viewer_group = QtGui.QGroupBox("Charts and Data")
        self.plot_viewer = ImageLabel()
        self.plot_data_table = QtGui.QTableWidget(0,0)

        self.plot_tabs = QtGui.QTabWidget()
        self.plot_tabs.addTab(self.plot_data_table, "Data")
        self.plot_tabs.addTab(self.plot_viewer, "Charts")

        plot_viewer_layout = QtGui.QHBoxLayout()
        plot_viewer_layout.addWidget(self.plot_tabs)
        self.plot_viewer_group.setLayout(plot_viewer_layout)

        self.progress_bar = ProgressBar()
        self.status_label = QtGui.QLabel("He who seeks glory, finds death.")

        row_1_layout = QtGui.QHBoxLayout()
        row_1_layout.addWidget(self.base_data_set_group)
        row_1_layout.addWidget(self.comparison_data_set_group)
        
        column_1_layout = QtGui.QVBoxLayout()
        column_1_layout.addWidget(self.analysis_parameters_group,1)
        column_1_layout.addWidget(self.plot_options_group,1)
        column_1_layout.addStretch(3)
        
        row_2_layout = QtGui.QHBoxLayout()
        row_2_layout.addLayout(column_1_layout,0)
        row_2_layout.addWidget(self.plot_viewer_group,3)

        
        row_3_layout = QtGui.QVBoxLayout()
        row_3_layout.addWidget(self.progress_bar,0)
        row_3_layout.addWidget(self.status_label,0)
        
        tna_viewer_layout = QtGui.QVBoxLayout()
        tna_viewer_layout.addLayout(row_1_layout,1)
        tna_viewer_layout.addLayout(row_2_layout,3)
        tna_viewer_layout.addLayout(row_3_layout,0)

        self.setLayout(tna_viewer_layout)
        self.show()
        self.move(0,0)
        self.setWindowTitle("Training Needs Analyser")
        self.setWindowIcon(QtGui.QIcon(os.path.join('Images','PORK_Icon.png')))

    def mapEvents(self):
        self.load_data_button.clicked.connect(self.loadData)
        self.parameters_all_button.clicked.connect(self.selectAllParameters)
        self.parameters_cfm_button.clicked.connect(self.selectCFMParameters)
        self.parameters_gseo_button.clicked.connect(self.selectGSEOParameters)
        self.parameters_fatal_button.clicked.connect(self.selectFatalParameters)
        self.parameters_clear_button.clicked.connect(self.clearParameterSelections)
        self.plot_button.clicked.connect(self.plotCharts)
        self.base_data_set_group.changedStartDate.connect(self.populateAuditParameters)

        self.base_data_set_group.changedFilter.connect(self.changedFilters)
        self.comparison_data_set_group.changedFilter.connect(self.changedFilters)

    def changedFilters(self):
        self.plot_button.setEnabled(False)

    def plotCharts(self):
        audit_parameter_selection = self.parameters_combobox.getCheckedItems()
        audit_parameters = audit_parameter_selection
        plot_types = self.plot_type_combobox.getCheckedItems()

        if len(plot_types)==0:
            self.alertMessage("No chart types selected!","You'll need to select a type of chart that you want to plot.")
        else:
            if len(audit_parameters)==0:
                self.selectGSEOParameters()
                self.selectCFMParameters()
                audit_parameters = self.parameters_combobox.getCheckedItems()
                self.alertMessage("No parameters selected!","Since you've not selected any audit parameters, GSEO and CFM have been auto selected for you.")
            if "Pareto" in plot_types:
                pareto_image = self.plotPareto(audit_parameters)

    def plotPareto(self, audit_parameter_selection):
        #print self.audit_parameters_dataframe
        parameter_column_names = self.getParameterColumnNames(audit_parameter_selection)
        parameter_class_list = [x[:(len(x)-2)] for x in parameter_column_names]
        #self.printMessage(parameter_column_names)
        parameter_summary_data = []
        counter = 0
        for parameter in audit_parameter_selection:
            parameter_column_name = parameter_column_names[counter]
            if not self.use_minimum_acceptable_scores.isChecked():
                acceptable_score = self.getMaximumScoreForParameter(parameter)
            else:
                acceptable_score = self.getMinimumScoreForParameter(parameter)
            #if "FAT" in parameter_column_name:
            #    self.printMessage("%s-%s: Max. Score: %s"%(parameter_column_name, parameter, acceptable_score))
            if type(acceptable_score) == str:
                #The acceptable score can be a string or a number.
                base_deviant_positions = self.base_data_set[parameter_column_name] != acceptable_score
            else:
                base_deviant_positions = self.base_data_set[parameter_column_name] < acceptable_score

            base_deviation_frequency = self.base_data_set[base_deviant_positions][parameter_column_name].count()
            base_deviation_frequency_percentage = base_deviation_frequency/self.base_data_set.shape[0]
            if self.comparison_data_set is None:
                comparison_deviation_frequency_percentage = "-"
                verdict = "NA"
            else:
                if type(acceptable_score) == str:
                    comparison_deviant_positions = self.comparison_data_set[parameter_column_name] != acceptable_score
                else:
                    comparison_deviant_positions = self.comparison_data_set[parameter_column_name] < acceptable_score

                comparison_deviation_frequency = self.comparison_data_set[comparison_deviant_positions][parameter_column_name].count()
                comparison_deviation_frequency_percentage = comparison_deviation_frequency/self.comparison_data_set.shape[0]
                if base_deviation_frequency_percentage<comparison_deviation_frequency_percentage:
                    verdict = "Better"
                elif base_deviation_frequency_percentage==comparison_deviation_frequency_percentage:
                    verdict = "No Change"
                else:
                    verdict = "Worse"

            parameter_data = [parameter, base_deviation_frequency_percentage, comparison_deviation_frequency_percentage, verdict]
            counter +=1
            parameter_summary_data.append(parameter_data)

        #self.printMessage(parameter_summary_data)
        summary_data_frame = pd.DataFrame(parameter_summary_data, index=parameter_class_list, columns =["Parameter Description", "Base Deviation Frequency", "Comparison Deviation Frequency","Verdict"]).sort_values(["Base Deviation Frequency"], ascending=False)
        #self.printMessage(summary_data_frame)
        #Clear the canvas
        fig, ax = plt.subplots()

        x_positions = np.arange(len(summary_data_frame.index))
        width = 0.35

        base_data_list = [x*100 for x in summary_data_frame["Base Deviation Frequency"]]
        base_bar_graphs = ax.bar(x_positions, base_data_list, width, color='y')
        ax.set_xticks(x_positions+width)
        parameter_names = [self.wordWrap(x) for x in list(summary_data_frame["Parameter Description"])]
        ax.set_xticklabels(parameter_names, rotation=90)
        #Set x and y labels.
        ax.set_xlabel("Quality Parameters")
        ax.set_ylabel("Deviation Frequency Percentage\n(Lower the bar, better the performance)")
        
        user_name = MOSES.getEmpName(self.user_id)
        time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        ax.set_title("Pareto Chart\n[Generated by OINK for %s at %s]"%(user_name, time_stamp))
        
        base_label = self.base_data_set_group.getLabel()
        reference_label = self.comparison_data_set_group.getLabel()

        if self.comparison_data_set is not None:
            comparison_data_list = [x*100 for x in summary_data_frame["Comparison Deviation Frequency"]]
            comparison_bar_graphs = ax.bar(x_positions+width, comparison_data_list, width, color='g')
            ax.legend((base_bar_graphs[0], comparison_bar_graphs[0]), (base_label, reference_label))
        
        self.showDataFrames(summary_data_frame)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.5)
        filename = os.path.join(os.getcwd(),"cache","Pareto_%s_vs_%s_%s.png"%(base_label.replace(" ","_"), reference_label.replace(" ","_"), time_stamp))

        plt.savefig("%s"%filename)
        self.plot_viewer.showImage(filename, int(self.plot_data_table.size().width()),int(self.plot_data_table.size().height()))
        plt.show()

        pareto_image_object = True
        return pareto_image_object

    def wordWrap(self, base_text):
        if " " in base_text:
            output_text = base_text[:base_text.find(" ")] + "\n" + base_text[base_text.find(" ")+1:]
        else:
            output_text = base_text
        return output_text

    def showDataFrames(self, dataframe):
        row_count = dataframe.shape[0]
        column_count = dataframe.shape[1]
        self.plot_data_table.setRowCount(row_count)
        self.plot_data_table.setColumnCount(column_count)

        for row_index in range(row_count):
            for col_index in range(column_count):
                self.plot_data_table.setItem(row_index, col_index, QtGui.QTableWidgetItem(str(dataframe.iat[row_index, col_index])))
        self.plot_data_table.setHorizontalHeaderLabels(list(dataframe.columns))
        self.plot_data_table.setVerticalHeaderLabels(list(dataframe.index))
        self.plot_data_table.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.plot_data_table.verticalHeader().setStretchLastSection(False)
        self.plot_data_table.verticalHeader().setVisible(True)

        self.plot_data_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.plot_data_table.horizontalHeader().setStretchLastSection(True)
        self.plot_data_table.horizontalHeader().setVisible(True)     

    
    def getMaximumScoreForParameter(self, parameter_name):
        matching_indices = self.audit_parameters_dataframe["Column Descriptions"]==parameter_name
        rating_type = list(self.audit_parameters_dataframe[matching_indices]["Rating Type"])[0]
        if rating_type!="Mandatory":
            maximum_score = list(self.audit_parameters_dataframe[matching_indices]["Maximum Score"])[0]
        else:
            maximum_score = "No" #No denotes that there's no fatal.
        return maximum_score
    def getMinimumScoreForParameter(self, parameter_name):
        matching_indices = self.audit_parameters_dataframe["Column Descriptions"]==parameter_name
        rating_type = list(self.audit_parameters_dataframe[matching_indices]["Rating Type"])[0]
        if rating_type!="Mandatory":
            minimum_score = list(self.audit_parameters_dataframe[matching_indices]["Minimum Acceptable Score"])[0]
        else:
            minimum_score = "No" #No denotes that there's no fatal.
        return minimum_score

    def getParameterColumnNames(self, audit_parameter_selection):
        audit_parameter_classes = list(self.audit_parameters_dataframe[self.audit_parameters_dataframe["Column Descriptions"].isin(audit_parameter_selection)]["Parameter Class"])
        
        audit_parameter_class_indices = list(self.audit_parameters_dataframe[self.audit_parameters_dataframe["Column Descriptions"].isin(audit_parameter_selection)]["Parameter Class Index"])


        #self.printMessage(audit_parameter_selection)
        #self.printMessage(audit_parameter_classes)
        #self.printMessage(audit_parameter_class_indices)
        
        column_names = ["%s%02d"%(x,y) for (x,y) in zip(audit_parameter_classes, audit_parameter_class_indices)]
        #self.printMessage(column_names)
        return column_names



    def printMessage(self, msg):
        allow_print = True
        if allow_print:
            print "TNAViewer: %s"%msg
        
    def loadData(self):
        self.load_data_button.setEnabled(False)
        self.alertMessage("Please wait...","Depending on the filters you have chosen, this step could take a second or a minute, though definitely not more than 60s. Please wait, and remember, <i>Roma die uno non aedificata est</i>.")
        self.plot_button.setEnabled(False)
        base_filter = self.base_data_set_group.getFilters()
        comparison_filter = self.comparison_data_set_group.getFilters()

        self.base_data_set = MOSES.getRawDataWithFilters(self.user_id, self.password, base_filter)
        self.comparison_data_set = MOSES.getRawDataWithFilters(self.user_id, self.password, comparison_filter)

        if self.base_data_set is not None:
            base_count = self.base_data_set.shape[0]
        else:
            base_count = 0

        if self.comparison_data_set is not None:
            comparison_count = self.comparison_data_set.shape[0]
        else:
            comparison_count = 0

        if base_count >0:
            self.plot_button.setEnabled(True)
            if comparison_count == 0:
                self.alertMessage("Retrieved Data","Retrieved %d audits for the base filters. There don't seem to be any for the comparison data set. You can go ahead and still plot a chart to analyse the base data, albeit without a reference plotted against it."%(base_count))
            else:
                self.alertMessage("Retrieved Data","Retrieved %d audits matching the base filters and %d audits matching the comparison filters."%(base_count, comparison_count))

        else:
            self.plot_button.setEnabled(False)
            self.alertMessage("Insufficient Base Data","There are no audits matching the selected filters for the base data. It is impossible to plot a chart without base data. This could have occurred for several reasons:\n1. You may have selected too many filters which have no result in the base form, or\n2. You could have selected a date range between which there have been zero audits.")
        self.load_data_button.setEnabled(True)


    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    def selectAllParameters(self):
        self.selectGSEOParameters()
        self.selectCFMParameters()
        self.selectFatalParameters()


    def selectGSEOParameters(self):
        gseo_parameters = self.audit_parameters_dataframe["Column Descriptions"][self.audit_parameters_dataframe["Parameter Class"] == "GSEO"]
        for gseo_parameter in gseo_parameters:
            self.parameters_combobox.select(gseo_parameter)

    def selectCFMParameters(self):
        cfm_parameters = self.audit_parameters_dataframe["Column Descriptions"][self.audit_parameters_dataframe["Parameter Class"] == "CFM"]
        for cfm_parameter in cfm_parameters:
            self.parameters_combobox.select(cfm_parameter)

    def selectFatalParameters(self):
        fatal_parameters = self.audit_parameters_dataframe["Column Descriptions"][self.audit_parameters_dataframe["Parameter Class"] == "FAT"]
        for fatal_parameter in fatal_parameters:
            self.parameters_combobox.select(fatal_parameter)

    def clearParameterSelections(self):
        self.parameters_combobox.clearSelection()



