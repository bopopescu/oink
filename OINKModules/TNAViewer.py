from __future__ import division
import math
import os
import datetime

import MySQLdb
import numpy as np
import pandas as pd
from PyQt4 import QtGui, QtCore
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
        self.populateInputEditorAndWritersList()
        self.populateComparisonEditorAndWritersList()
        self.populateAuditParameters()
        self.parameters_all_button.setChecked(True)

    def populateInputEditorAndWritersList(self):
        self.input_data_set_group.populateEditorAndWritersList()

    def populateComparisonEditorAndWritersList(self):
        self.comparison_data_set_group.populateEditorAndWritersList()

    def populateAuditParameters(self):
        parameters_date = self.input_data_set_group.getDates()[0]
        self.audit_parameters_dataframe = MOSES.getAuditParametersData(self.user_id, self.password, parameters_date)
        self.audit_parameters = self.audit_parameters_dataframe["Column Descriptions"]
        self.parameters_combobox.clear()
        self.parameters_combobox.addItems(self.audit_parameters)

    
    def createUI(self):
        self.input_data_set_group = FilterForm(
                                            self.user_id,   
                                            self.password,    
                                            (0,0,0),   
                                            self.category_tree,   
                                            self.viewer_level,    
                                            "Input Data Set")
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
        self.plot_types.sort()
        self.plot_type_combobox.addItems(self.plot_types)
        self.plot_separate_charts_for_each_parameter = QtGui.QCheckBox("Parameter Charts")
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

        plot_options_layout = QtGui.QVBoxLayout()
        plot_options_row_1 = QtGui.QHBoxLayout()
        plot_options_row_1.addWidget(self.plot_type_label,0)
        plot_options_row_1.addWidget(self.plot_type_combobox,0)
        plot_options_row_1.addWidget(self.plot_separate_charts_for_each_parameter,0)
        plot_options_layout.addLayout(plot_options_row_1)
        plot_options_row_2 = QtGui.QHBoxLayout()
        plot_options_row_2.addWidget(self.load_data_button,0)
        plot_options_row_2.addWidget(self.plot_button,0)
        plot_options_row_2.addWidget(self.plot_save_button,0)
        plot_options_row_2.addStretch(1)
        plot_options_layout.addLayout(plot_options_row_2)
        plot_options_row_3 = QtGui.QHBoxLayout()
        plot_options_row_3.addWidget(self.plot_zoom_slider,3)
        plot_options_row_3.addWidget(self.plot_zoom_label,1)
        plot_options_layout.addLayout(plot_options_row_3)

        
        self.plot_options_group.setLayout(plot_options_layout)

        self.plot_viewer_group = QtGui.QGroupBox("Charts")
        self.plot_viewer = ImageLabel()
        plot_viewer_layout = QtGui.QHBoxLayout()
        plot_viewer_layout.addWidget(self.plot_viewer)
        self.plot_viewer_group.setLayout(plot_viewer_layout)

        self.progress_bar = ProgressBar()
        self.status_label = QtGui.QLabel("He who seeks glory, finds death.")

        row_1_layout = QtGui.QHBoxLayout()
        row_1_layout.addWidget(self.input_data_set_group)
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
    
    def loadData(self):
        input_filter = self.input_data_set_group.getFilters()
        comparison_filter = self.comparison_data_set_group.getFilters()
        audit_parameter_selection = self.parameters_combobox.getCheckedItems()
        audit_parameters = audit_parameter_selection if len(audit_parameter_selection)>0 else None

        input_data_set = MOSES.getRawDataWithFilters(self.user_id, self.password, input_filter, audit_parameters)
        comparison_data_set = MOSES.getRawDataWithFilters(self.user_id, self.password, comparison_filter, audit_parameters)

        if input_data_set is not None:
            input_count = input_data_set.shape[0]
        else:
            input_count = 0

        if comparison_data_set is not None:
            comparison_count = comparison_data_set.shape[0]
        else:
            comparison_count = 0

        self.alertMessage("Retrieved Data","Retrieved %d rows for the input filters and %d rows for output."%(input_count, comparison_count))

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



