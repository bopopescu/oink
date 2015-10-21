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
        self.all_button.setFixedWidth(30)
        self.rpd_button.setFixedWidth(30)
        self.pd_button.setFixedWidth(30)
        self.seo_button.setFixedWidth(30)
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

        layout = QtGui.QVBoxLayout()
        
        row_1_layout = QtGui.QHBoxLayout()
        row_1_layout.addWidget(self.writer_label,0)
        row_1_layout.addWidget(self.writer_combobox,0)
        row_1_layout.addWidget(self.editor_label,0)
        row_1_layout.addWidget(self.editor_combobox,0)
        row_1_layout.addWidget(self.graph_color_label,0)
        row_1_layout.addWidget(self.graph_color,0)
        row_1_layout.addWidget(self.pd_button,0)
        row_1_layout.addWidget(self.rpd_button,0)
        row_1_layout.addWidget(self.seo_button,0)
        row_1_layout.addWidget(self.all_button,0)
        row_1_layout.addStretch(1)
        
        row_2_layout = QtGui.QHBoxLayout()
        row_2_layout.addWidget(self.date_field_label,0)
        row_2_layout.addWidget(self.date_field_start,0)
        row_2_layout.addWidget(self.date_field_end,0)
        row_2_layout.addStretch(1)

        layout.addLayout(row_1_layout,1)
        layout.addLayout(row_2_layout,1)
        layout.addWidget(self.category_selector,2)
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

