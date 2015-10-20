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
from QColorButton import QColorButton
from CategoryFinder import CategoryFinder

class CategorySelector(QtGui.QWidget):
    def __init__(self, category_tree, *args, **kwargs):
        super(CategorySelector,self).__init__(*args, **kwargs)
        self.createUI()
        self.mapEvents()
        

class FilterForm(QtGui.QGroupBox):
    def __init__(self, user_id, password, color, category_tree, viewer_level, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.password = password
        self.category_tree = category_tree
        self.viewer_level = viewer_level
        #the viewer level controls the scope of the program.
        #A Level 0 limits the visibility to the current user, and shows the team's quality in comparison.
        #A level 1 allows choosing the users.
        self.createUI()
        self.mapEvents()

    def createUI(self):
        self.writer_label = QtGui.QLabel("Writer(s):")
        self.writer_combobox = CheckableComboBox("Writer")
        self.editor_label = QtGui.QLabel("Editor(s):")
        self.editor_combobox = CheckableComboBox("Editors")
        self.pd_button = QtGui.QPushButton("PD")
        self.rpd_button = QtGui.QPushButton("RPD")
        self.seo_button = QtGui.QPushButton("SEO")
        self.all_button = QtGui.QPushButton("All")
        self.date_field_label = QtGui.QLabel("Date Range:")
        self.date_field_start = QtGui.QDateEdit()
        self.date_field_end = QtGui.QDateEdit()
        self.date_field_start.setMinimumDate(datetime.date(2015,1,1))
        self.date_field_start.setMaximumDate(datetime.date.today())
        self.date_field_start.setDate(datetime.date.today())
        self.date_field_start.setCalendarPopup(True)
        self.date_field_end.setMinimumDate(datetime.date(2015,1,1))
        self.date_field_end.setMaximumDate(datetime.date.today())
        self.date_field_end.setDate(datetime.date.today())
        self.date_field_end.setCalendarPopup(True)
        self.graph_color_label = QtGui.QLabel("Graph Color")
        self.graph_color = QColorButton()

        layout = QtGui.QGridLayout()
        alignment = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft
        row = 0
        column = 0
        row_width = 1
        column_width = 1
        layout.addWidget(self.writer_label, row, column, row_width, column_width)
        column += column_width
        column_width = 2
        layout.addWidget(self.writer_combobox, row, column, row_width, column_width)
        column += column_width
        column_width = 1
        layout.addWidget(self.editor_label, row, column, row_width, column_width)
        column += column_width
        column_width = 2
        layout.addWidget(self.editor_combobox, row, column, row_width, column_width)
        column += column_width
        column_width=1
        layout.addWidget(self.graph_color_label, row, column, row_width, column_width)
        column += column_width
        column_width=1
        layout.addWidget(self.graph_color, row, column, row_width, column_width)
        row += row_width
        column = 0
        row_width = 1
        column_width = 1
        layout.addWidget(self.pd_button, row, column, row_width, column_width)
        column+=column_width
        layout.addWidget(self.rpd_button, row, column, row_width, column_width)
        column+=column_width
        layout.addWidget(self.seo_button, row, column, row_width, column_width)
        column+=column_width
        layout.addWidget(self.all_button, row, column, row_width, column_width)
        column+=column_width
        layout.addWidget(self.date_field_label, row, column, row_width, column_width)
        column+=column_width
        column_width = 2
        layout.addWidget(self.date_field_start, row, column, row_width, column_width)
        column+=column_width
        layout.addWidget(self.date_field_end, row, column, row_width, column_width)
        self.setLayout(layout)

    def mapEvents(self):
        pass

    def getFilters(self):
        pass

    def populateFilter(self):
        pass

    def populateEditorAndWritersList(self):
        comparison_date = self.date_field_end.date().toPyDate()
        self.writer_and_editor_dataframe = MOSES.getWriterAndEditorData(self.user_id, self.password, comparison_date)
        self.writers_list = list(set(self.writer_and_editor_dataframe["Writer Name"]))
        self.editors_list = list(set(self.writer_and_editor_dataframe["Editor Name"]))
        self.writers_list.sort()
        self.editors_list.sort()
        self.writer_combobox.clear()
        self.writer_combobox.addItems(self.writers_list)
        self.editor_combobox.clear()
        self.editor_combobox.addItems(self.editors_list)
    def getDates(self):
        return self.date_field_start.date().toPyDate(), self.date_field_end.date().toPyDate()


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
        self.input_data_set_group = FilterForm(self.user_id, self.password, (0,0,0), self.category_tree, self.viewer_level, "Input Data Set")
        self.comparison_data_set_group = FilterForm(self.user_id, self.password, (0,0,0), self.category_tree, self.viewer_level, "Comparison Data Set")


        self.analysis_parameters_group = QtGui.QGroupBox("Analysis Parameters")
        self.parameters_label = QtGui.QLabel("Compare:")
        self.parameters_combobox = CheckableComboBox("Parameters")
        self.parameters_all_button = QtGui.QPushButton("All")
        self.parameters_cfm_button = QtGui.QPushButton("CFM")
        self.parameters_gseo_button = QtGui.QPushButton("GSEO")

        parameters_layout = QtGui.QGridLayout()
        row = 0
        column = 0
        row_width = 1
        column_width = 1
        alignment = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft
        parameters_layout.addWidget(self.parameters_label, row, column, row_width, column_width, alignment)
        column += column_width
        column_width = 6
        parameters_layout.addWidget(self.parameters_combobox, row, column, row_width, column_width)
        row += row_width
        column_width = int(math.floor(column/3))
        column = column_width
        column_width = 1
        parameters_layout.addWidget(self.parameters_all_button, row, column, row_width, column_width, alignment)
        column += column_width
        column_width = 1
        parameters_layout.addWidget(self.parameters_cfm_button, row, column, row_width, column_width, alignment)
        column += column_width
        column_width = 1
        parameters_layout.addWidget(self.parameters_gseo_button, row, column, row_width, column_width, alignment)
        self.analysis_parameters_group.setLayout(parameters_layout)

        self.plot_options_group = QtGui.QGroupBox("Plotting Options")
        self.plot_type_label = QtGui.QLabel("Plot:")
        self.plot_type_combobox = CheckableComboBox("Chart Types")
        self.plot_types = ["Histogram","Pareto","Daily Trend","Weekly Trend","Monthly Trend","Quarterly Trend","Half-Yearly Trend","Radar Scatter Chart"]
        self.plot_types.sort()
        self.plot_type_combobox.addItems(self.plot_types)
        self.plot_separate_charts_for_each_parameter = QtGui.QCheckBox("Plot Parameter Charts")
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

        plot_options_layout = QtGui.QGridLayout()
        row = 0
        column = 0
        row_width = 1
        column_width = 1
        alignment = QtCore.Qt.AlignVCenter
        plot_options_layout.addWidget(self.plot_type_label, row, column, row_width, column_width, alignment)
        column+=column_width
        column_width = 2
        plot_options_layout.addWidget(self.plot_type_combobox, row, column, row_width, column_width, alignment)
        column+=column_width
        column_width = 3        
        plot_options_layout.addWidget(self.plot_separate_charts_for_each_parameter, row, column, row_width, column_width, alignment)
        row += row_width
        column_width = int(math.floor(column/3))
        column = column_width
        column_width = 1
        plot_options_layout.addWidget(self.load_data_button, row, column, row_width, column_width, alignment)
        column+=column_width
        column_width = 1
        plot_options_layout.addWidget(self.plot_button, row, column, row_width, column_width, alignment)
        column+=column_width
        column_width = 1
        plot_options_layout.addWidget(self.plot_save_button, row, column, row_width, column_width, alignment)
        row += row_width
        column = 0
        column_width = 2
        plot_options_layout.addWidget(self.plot_zoom_slider, row, column, row_width, column_width, alignment)
        column+=column_width
        column_width = 2
        alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        plot_options_layout.addWidget(self.plot_zoom_label, row, column, row_width, column_width, alignment)

        self.plot_options_group.setLayout(plot_options_layout)

        self.plot_viewer_group = QtGui.QGroupBox("Charts")
        self.plot_viewer = ImageLabel()
        #self.plot_viewer.setFixedWidth(200)
        plot_viewer_layout = QtGui.QHBoxLayout()
        plot_viewer_layout.addWidget(self.plot_viewer)
        self.plot_viewer_group.setLayout(plot_viewer_layout)

        self.progress_bar = ProgressBar()
        self.status_label = QtGui.QLabel("He who seeks glory, finds death.")

        tna_viewer_layout = QtGui.QGridLayout()
        row = 0
        column = 0
        row_width = 2
        column_width = 4
        alignment = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        tna_viewer_layout.addWidget(self.input_data_set_group, row, column, row_width, column_width)
        column+=column_width
        tna_viewer_layout.addWidget(self.comparison_data_set_group, row, column, row_width, column_width)
        row += row_width
        column = 0
        column_width = 2
        row_width = 1
        tna_viewer_layout.addWidget(self.analysis_parameters_group, row, column, row_width, column_width)
        column+=column_width
        column_width = 6
        row_width = 6
        tna_viewer_layout.addWidget(self.plot_viewer_group, row, column, row_width, column_width)
        row +=1
        row_width = 1
        column = 0
        column_width = 2
        tna_viewer_layout.addWidget(self.plot_options_group, row, column, row_width, column_width)
        column = 0
        row +=5
        column_width = 8
        row_width = 1
        alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        tna_viewer_layout.addWidget(self.progress_bar, row, column, row_width, column_width)
        row+=row_width
        column = 0
        column_width = 8
        tna_viewer_layout.addWidget(self.status_label, row, column, row_width, column_width)

        self.setLayout(tna_viewer_layout)
        self.show()
        self.setWindowTitle("Training Needs Analyser")

    def mapEvents(self):
        pass