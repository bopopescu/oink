#
#TNAViewer class definition
#This class allows users to plot various charts to 
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

from __future__ import division
import math
import os
import datetime

import numpy as np
import pandas as pd
from PyQt4 import QtGui, QtCore
import MOSES
from CheckableComboBox import CheckableComboBox
from QColorButton import QColorButton
from CategorySelector import CategorySelector

class FilterForm(QtGui.QGroupBox):
    changedStartDate = QtCore.pyqtSignal()
    changedFilter = QtCore.pyqtSignal()

    def __init__(self, user_id, password, color, category_tree, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.password = password
        self.category_tree = category_tree
        self.user_name = MOSES.getEmpName(self.user_id)
        self.lock_mode = None
        self.createUI()
        self.mapEvents()
        self.all_button.setChecked(True)
        label = str(args[0]) if args is not None else "Data Set"
        self.filter_legend.setText(label)

    def createUI(self):
        self.filter_label = QtGui.QLabel("Label:")
        self.filter_legend = QtGui.QLineEdit()
        self.filter_legend.setToolTip("Type a meaningful name for this data set here.\nTry avoiding special characters as they could result in errors.")

        self.writer_label = QtGui.QLabel("Writer(s):")
        self.writer_combobox = CheckableComboBox("Writers")
        self.editor_label = QtGui.QLabel("Editor(s):")
        self.editor_combobox = CheckableComboBox("Editors")

        self.writer_all_button = QtGui.QPushButton("All")
        self.writer_all_button.setToolTip("Select all writers")
        self.writer_clear_button = QtGui.QPushButton("Clear")
        self.writer_clear_button.setToolTip("Clear writer selection")

        self.editor_all_button = QtGui.QPushButton("All")
        self.editor_all_button.setToolTip("Select all editors")        
        self.editor_clear_button = QtGui.QPushButton("Clear")
        self.editor_clear_button.setToolTip("Clear editor selection")

        self.pd_button = QtGui.QPushButton("PD")
        self.rpd_button = QtGui.QPushButton("RPD")
        self.seo_button = QtGui.QPushButton("SEO")
        self.all_button = QtGui.QPushButton("All")

        self.all_button.setFixedWidth(30)
        self.rpd_button.setFixedWidth(30)
        self.pd_button.setFixedWidth(30)
        self.seo_button.setFixedWidth(30)
        
        self.all_button.setCheckable(True)
        self.rpd_button.setCheckable(True)
        self.pd_button.setCheckable(True)
        self.seo_button.setCheckable(True)
        
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
        self.select_all_data = QtGui.QCheckBox("Select all audits")
        self.graph_color_label = QtGui.QLabel("Graph Color")
        self.graph_color_button = QColorButton()
        self.category_selector = CategorySelector(self.category_tree)

        row_0_layout = QtGui.QHBoxLayout()
        row_0_layout.addWidget(self.filter_label,0)
        row_0_layout.addWidget(self.filter_legend,1)
        
        row_1_layout = QtGui.QHBoxLayout()
        row_1_layout.addWidget(self.writer_label,0)
        row_1_layout.addWidget(self.writer_combobox,1)
        row_1_layout.addWidget(self.writer_all_button,0)
        row_1_layout.addWidget(self.writer_clear_button,0)
        row_1_layout.addStretch(1)
        
        row_2_layout = QtGui.QHBoxLayout()
        row_2_layout.addWidget(self.editor_label, 0)
        row_2_layout.addWidget(self.editor_combobox, 1)
        row_2_layout.addWidget(self.editor_all_button, 0)
        row_2_layout.addWidget(self.editor_clear_button, 0)
        row_2_layout.addWidget(self.graph_color_label, 0)
        row_2_layout.addWidget(self.graph_color_button, 0)
        row_2_layout.addStretch(1)
        
        row_3_layout = QtGui.QHBoxLayout()
        row_3_layout.addWidget(self.date_field_label, 0)
        row_3_layout.addWidget(self.date_field_start, 0)
        row_3_layout.addWidget(self.date_field_end, 0)
        row_3_layout.addWidget(self.select_all_data, 0)
        row_3_layout.addWidget(self.pd_button, 0)
        row_3_layout.addWidget(self.rpd_button, 0)
        row_3_layout.addWidget(self.seo_button, 0)
        row_3_layout.addWidget(self.all_button, 0)
        row_3_layout.addStretch(1)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(row_0_layout, 1)
        layout.addLayout(row_1_layout, 1)
        layout.addLayout(row_2_layout, 1)
        layout.addLayout(row_3_layout, 1)
        layout.addLayout(self.category_selector, 2)
        self.setLayout(layout)

    def lock(self, lock_mode=None):
        if lock_mode is not None:
            self.lock_mode = lock_mode
        if self.lock_mode is not None:
            self.editor_combobox.clearSelection()
            self.editor_combobox.setEnabled(False)
            self.editor_all_button.setEnabled(False)
            self.editor_clear_button.setEnabled(False)
            if self.lock_mode == 1:
                self.writer_combobox.clearSelection()
                self.writer_combobox.select(self.user_name)
                self.writer_combobox.setEnabled(False)
                self.writer_all_button.setEnabled(False)
                self.writer_clear_button.setEnabled(False)
            elif self.lock_mode == 2:
                self.writer_combobox.clearSelection()
                self.writer_combobox.selectAll()
                self.writer_combobox.setEnabled(False)

    def mapEvents(self):
        self.all_button.toggled.connect(self.toggleAll)
        self.pd_button.toggled.connect(self.toggleTypes)
        self.rpd_button.toggled.connect(self.toggleTypes)
        self.seo_button.toggled.connect(self.toggleTypes)

        self.select_all_data.toggled.connect(self.changeDateType)
        self.writer_all_button.clicked.connect(self.selectAllWriters)
        self.writer_clear_button.clicked.connect(self.clearWriters)
        self.editor_all_button.clicked.connect(self.selectAllEditors)
        self.editor_clear_button.clicked.connect(self.clearEditors)

        self.date_field_start.dateChanged.connect(self.changedDate)
        
        
        #Any change in the filter form should result in emitting the changedFilter signal.
        self.date_field_start.dateChanged.connect(self.changedFilter)
        self.date_field_end.dateChanged.connect(self.changedFilter)
        self.all_button.toggled.connect(self.changedFilter)
        self.pd_button.toggled.connect(self.changedFilter)
        self.rpd_button.toggled.connect(self.changedFilter)
        self.seo_button.toggled.connect(self.changedFilter)
        self.select_all_data.toggled.connect(self.changedFilter)
        self.writer_combobox.changedSelection.connect(self.changedFilter)
        self.editor_combobox.changedSelection.connect(self.changedFilter)
        self.category_selector.changedCategorySelection.connect(self.changedFilter)

    def changedDate(self):
        self.changedStartDate.emit()

    def selectAllWriters(self):
        self.writer_combobox.selectAll()
    
    def selectAllEditors(self):
        self.editor_combobox.selectAll()

    def clearWriters(self):
        self.writer_combobox.clearSelection()
        if self.lock_mode is not None:
            if self.lock_mode == 2:
                self.writer_combobox.select(self.user_name)


    
    def clearEditors(self):
        self.editor_combobox.clearSelection()

    def changeDateType(self):
        if self.select_all_data.isChecked():
            self.date_field_start.setEnabled(False)
            self.date_field_end.setEnabled(False)
        else:
            self.date_field_start.setEnabled(True)
            self.date_field_end.setEnabled(True)

    def getLabel(self):
        return str(self.filter_legend.text()).strip()

    def toggleAll(self):
        if self.all_button.isChecked():
            self.pd_button.setChecked(True)
            self.rpd_button.setChecked(True)
            self.seo_button.setChecked(True)
            self.all_button.setEnabled(False)

    def toggleTypes(self):
        if self.pd_button.isChecked() and self.rpd_button.isChecked() and self.seo_button.isChecked():
            self.all_button.setChecked(True)
            self.all_button.setEnabled(False)
        else:
            self.all_button.setEnabled(True)
            self.all_button.setChecked(False)

    def getFilters(self):
        category_tree_filter = self.category_selector.getFilters()

        writer_filter = self.writer_combobox.getCheckedItems()
        editor_filter = self.editor_combobox.getCheckedItems()
        
        start_date = self.date_field_start.date().toPyDate()
        end_date = self.date_field_end.date().toPyDate()
        
        get_pd = False
        get_rpd = False
        get_seo = False        
        
        if self.all_button.isChecked():
            get_pd = True
            get_rpd = True
            get_seo = True
        else:
            if self.pd_button.isChecked():
                get_pd = True
            if self.rpd_button.isChecked():
                get_rpd = True
            if self.seo_button.isChecked():
                get_seo = True

        description_type = []
        if get_pd:
            description_type.append("PD")
        if get_rpd:
            description_type.append("RPD")
        if get_seo:
            description_type.append("SEO")

        filter_settings = {
                    "Category Tree":category_tree_filter if category_tree_filter.shape[0]>0 else None,
                    "Writers": writer_filter if len(writer_filter)>0 else None,
                    "Editors": editor_filter if len(editor_filter)>0 else None,
                    "Dates": [start_date, end_date] if not(self.select_all_data.isChecked()) else None,
                    "Description Types": description_type if len(description_type)>0 else None
        }
        return filter_settings

    def getGraphColor(self):
        return self.graph_color_button.getColor()

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
        if self.select_all_data.isChecked():
            return datetime.date(2015,1,1), datetime.date.today()
        else:
            return self.date_field_start.date().toPyDate(), self.date_field_end.date().toPyDate()

    def getData(self):
        pass
