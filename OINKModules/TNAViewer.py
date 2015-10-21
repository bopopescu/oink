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
        self.category_tree = category_tree
        self.category_tree_headers = ["BU","Super-Category","Category","Sub-Category","Vertical"]

        self.createUI()
        self.populateAll()
        self.mapEvents()

    def createUI(self):
        self.label = QtGui.QLabel("Categories:")
        self.bu_combo_box = CheckableComboBox("BU")
        self.super_category_combo_box = CheckableComboBox("Super-Category")
        self.category_combo_box = CheckableComboBox("Category")
        self.sub_category_combo_box = CheckableComboBox("Sub-Category")
        self.vertical_combo_box = CheckableComboBox("Vertical")
        self.category_finder = CategoryFinder(self.category_tree)
        self.clear_button = QtGui.QPushButton("Clear\nFilters")
        layout = QtGui.QGridLayout()
        layout.addWidget(self.label,0,0,1,1)
        layout.addWidget(self.bu_combo_box,0,1,1,1)
        layout.addWidget(self.super_category_combo_box,0,2,1,1)
        layout.addWidget(self.category_combo_box,1,0,1,1)
        layout.addWidget(self.sub_category_combo_box,1,1,1,1)
        layout.addWidget(self.vertical_combo_box,1,2,1,1)
        layout.addWidget(self.clear_button,0,3,2,1, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        layout.addLayout(self.category_finder,2,0,1,3)
        self.setLayout(layout)

    def mapEvents(self):
        self.category_finder.pickRow.connect(self.selectRow)
        self.vertical_combo_box.changedSelection.connect(self.changedVerticals)
        self.sub_category_combo_box.changedSelection.connect(self.changedSubCategories)
        self.category_combo_box.changedSelection.connect(self.changedCategories)
        self.super_category_combo_box.changedSelection.connect(self.changedSuperCategories)
        self.clear_button.clicked.connect(self.clearFilters)

    def populateAll(self):
        #Populate the values
        bus = list(set(self.category_tree["BU"]))
        bus.sort()
        super_categories = list(set(self.category_tree["Super-Category"]))
        super_categories.sort()
        categories = list(set(self.category_tree["Category"]))
        categories.sort()
        sub_categories = list(set(self.category_tree["Sub-Category"]))
        sub_categories.sort()
        verticals = list(set(self.category_tree["Vertical"]))
        verticals.sort()

        self.bu_combo_box.clear()
        self.bu_combo_box.addItems(bus)
        self.super_category_combo_box.clear()
        self.super_category_combo_box.addItems(super_categories)
        self.category_combo_box.clear()
        self.category_combo_box.addItems(categories)
        self.sub_category_combo_box.clear()
        self.sub_category_combo_box.addItems(sub_categories)
        self.vertical_combo_box.clear()
        self.vertical_combo_box.addItems(verticals)

    def getSelectedCategories(self):
        selected_categories_data_frame = []
        return selected_categories_data_frame

    def selectRow(self, row_dict):
        self.bu_combo_box.select(row_dict["BU"])
        self.super_category_combo_box.select(row_dict["Super-Category"])
        self.category_combo_box.select(row_dict["Category"])
        self.sub_category_combo_box.select(row_dict["Sub-Category"])
        self.vertical_combo_box.select(row_dict["Vertical"])


    def changedSuperCategories(self):
        selected_super_categories = self.super_category_combo_box.getCheckedItems()
        required_bus = list(set(self.category_tree[self.category_tree["Super-Category"].isin(selected_super_categories)]["BU"]))
        for bu in required_bus:
            self.bu_combo_box.select(bu)

    def changedCategories(self):
        selected_categories = self.category_combo_box.getCheckedItems()
        required_super_categories = list(set(self.category_tree[self.category_tree["Category"].isin(selected_categories)]["Super-Category"]))
        for super_category in required_super_categories:
            self.super_category_combo_box.select(super_category)

    def changedSubCategories(self):
        selected_sub_categories = self.sub_category_combo_box.getCheckedItems()
        required_categories = list(set(self.category_tree[self.category_tree["Sub-Category"].isin(selected_sub_categories)]["Category"]))
        for category in required_categories:
            self.category_combo_box.select(category)

    def changedVerticals(self):
        selected_verticals = self.vertical_combo_box.getCheckedItems()
        required_sub_categories = list(set(self.category_tree[self.category_tree["Vertical"].isin(selected_verticals)]["Sub-Category"]))
        for sub_category in required_sub_categories:
            self.sub_category_combo_box.select(sub_category)

    def clearFilters(self):
        self.bu_combo_box.clearSelection()
        self.super_category_combo_box.clearSelection()
        self.category_combo_box.clearSelection()
        self.sub_category_combo_box.clearSelection()
        self.vertical_combo_box.clearSelection()

    def getFilters(self):
        #First, get the checked verticals.
        verticals = self.vertical_combo_box.getCheckedItems()
        vertical_filter_data_frame = self.category_tree[self.category_tree["Vertical"].isin(verticals)]
        
        sub_categories = self.sub_category_combo_box.getCheckedItems()
        accounted_sub_categories = list(set(vertical_filter_data_frame["Sub-Category"]))
        unaccounted_sub_categories = [sub_category for sub_category in sub_categories if sub_category not in accounted_sub_categories]
        if len(unaccounted_sub_categories) > 0:
            print "Found unaccounted_sub_categories", unaccounted_sub_categories
            sub_category_filter_data_frame = self.category_tree[self.category_tree["Sub-Category"].isin(unaccounted_sub_categories)]
            sub_cat_vert_filter_data_frame = pd.concat([sub_category_filter_data_frame, vertical_filter_data_frame])
        else:
            sub_cat_vert_filter_data_frame = vertical_filter_data_frame

        categories = self.category_combo_box.getCheckedItems()
        accounted_categories = list(set(sub_cat_vert_filter_data_frame["Category"]))
        unaccounted_categories = [category for category in categories if category not in accounted_categories]
        if len(unaccounted_categories) >0:
            print "Found unaccounted_categories", unaccounted_categories
            category_filter_data_frame = self.category_tree[self.category_tree["Category"].isin(unaccounted_categories)]
            cat_sub_cat_vert_filter_data_frame = pd.concat([category_filter_data_frame, sub_cat_vert_filter_data_frame])
        else:
            cat_sub_cat_vert_filter_data_frame = sub_cat_vert_filter_data_frame


        super_categories = self.super_category_combo_box.getCheckedItems()
        accounted_super_categories = list(set(cat_sub_cat_vert_filter_data_frame["Super-Category"]))
        unaccounted_super_categories = [super_category for super_category in super_categories if super_category not in accounted_super_categories]
        if len(unaccounted_super_categories) >0:
            print "Found unaccounted_super_categories", unaccounted_super_categories
            super_category_filter_data_frame = self.category_tree[self.category_tree["Super-Category"].isin(unaccounted_super_categories)]
            supcat_cat_sub_cat_vert_filter_data_frame = pd.concat([super_category_filter_data_frame, cat_sub_cat_vert_filter_data_frame])
        else:
            supcat_cat_sub_cat_vert_filter_data_frame = cat_sub_cat_vert_filter_data_frame

        bus = self.bu_combo_box.getCheckedItems()
        accounted_bus = list(set(supcat_cat_sub_cat_vert_filter_data_frame["BU"]))
        unaccounted_bus = [bu for bu in bus if bu not in accounted_bus]
        if len(unaccounted_bus) >0:
            print "Found unaccounted_bus", unaccounted_bus
            bu_filter_data_frame = self.category_tree[self.category_tree["BU"].isin(unaccounted_bus)]
            filter_data_frame = pd.concat([bu_filter_data_frame, supcat_cat_sub_cat_vert_filter_data_frame])
        else:
            filter_data_frame = supcat_cat_sub_cat_vert_filter_data_frame
        return filter_data_frame.drop_duplicates(subset=self.category_tree_headers)[self.category_tree_headers]


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
        self.category_selector = CategorySelector(self.category_tree)

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
        row+=row_width
        column_width = column
        column = 0
        row_width = 3
        layout.addWidget(self.category_selector, row, column, row_width, column_width)
        self.setLayout(layout)

    def mapEvents(self):
        pass

    def getFilters(self):
        filter = self.category_selector.getFilters()
        return filter

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

    def getData(self):
        pass


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
        self.load_data_button.clicked.connect(self.loadData)
    
    def loadData(self):
        self.filter = self.input_data_set_group.getFilters()
        #print self.filter