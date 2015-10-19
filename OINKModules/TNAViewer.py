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

class TNAViewer(QtGui.QWidget):
	def __init__(self, user_id, password, viewer_level=None, *args, **kwargs):
		super(TNAViewer, self).__init__(*args, **kwargs)
		self.user_id = user_id
		self.password = password
		#the viewer level controls the scope of the program.
		#A Level 0 limits the visibility to the current user, and shows the team's quality in comparison.
		#A level 1 allows choosing the users.
		if (viewer_level is not None) and  viewer_level in [0, 1]:
			self.viewer_level = viewer_level
		else:
			self.viewer_level = 0
		self.createUI()
		self.mapEvents()

	def createUI(self):
		self.input_data_set_group = QtGui.QGroupBox("Input Data Set")

		self.input_writer_label = QtGui.QLabel("Writer(s):")
		self.input_writer_combobox = CheckableComboBox("Writer")
		self.input_editor_label = QtGui.QLabel("Editor(s):")
		self.input_editor_combobox = CheckableComboBox("Editors")
		self.input_pd_button = QtGui.QPushButton("PD")
		self.input_rpd_button = QtGui.QPushButton("RPD")
		self.input_seo_button = QtGui.QPushButton("SEO")
		self.input_all_button = QtGui.QPushButton("All")
		self.input_date_field_label = QtGui.QLabel("Date Range:")
		self.input_date_field_start = QtGui.QDateEdit()
		self.input_date_field_end = QtGui.QDateEdit()

		input_data_set_layout = QtGui.QGridLayout()
		alignment = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft
		row = 0
		column = 0
		row_width = 1
		column_width = 1
		input_data_set_layout.addWidget(self.input_writer_label, row, column, row_width, column_width, alignment)
		column += column_width
		column_width = 3
		input_data_set_layout.addWidget(self.input_writer_combobox, row, column, row_width, column_width, alignment)
		column += column_width
		column_width = 1
		input_data_set_layout.addWidget(self.input_editor_label, row, column, row_width, column_width, alignment)
		column += column_width
		column_width = 3
		input_data_set_layout.addWidget(self.input_editor_combobox, row, column, row_width, column_width, alignment)
		row += row_width
		column = 0
		row_width = 1
		column_width = 1
		input_data_set_layout.addWidget(self.input_pd_button, row, column, row_width, column_width, alignment)
		column+=column_width
		input_data_set_layout.addWidget(self.input_rpd_button, row, column, row_width, column_width, alignment)
		column+=column_width
		input_data_set_layout.addWidget(self.input_seo_button, row, column, row_width, column_width, alignment)
		column+=column_width
		input_data_set_layout.addWidget(self.input_all_button, row, column, row_width, column_width, alignment)
		column+=column_width
		input_data_set_layout.addWidget(self.input_date_field_label, row, column, row_width, column_width, alignment)
		column+=column_width
		column_width = 2
		input_data_set_layout.addWidget(self.input_date_field_start, row, column, row_width, column_width, alignment)
		column+=column_width
		input_data_set_layout.addWidget(self.input_date_field_end, row, column, row_width, column_width, alignment)

		self.input_data_set_group.setLayout(input_data_set_layout)


		self.comparison_data_set_group = QtGui.QGroupBox("Comparison Data Set")
		self.comparison_writer_label = QtGui.QLabel("Writer(s):")
		self.comparison_writer_combobox = CheckableComboBox("Writers")
		self.comparison_editor_label = QtGui.QLabel("Editor(s):")
		self.comparison_editor_combobox = CheckableComboBox("Editors")
		self.comparison_pd_button = QtGui.QPushButton("PD")
		self.comparison_rpd_button = QtGui.QPushButton("RPD")
		self.comparison_seo_button = QtGui.QPushButton("SEO")
		self.comparison_all_button = QtGui.QPushButton("All")
		self.comparison_date_field_label = QtGui.QLabel("Date Range:")
		self.comparison_date_field_start = QtGui.QDateEdit()
		self.comparison_date_field_end = QtGui.QDateEdit()

		comparison_data_set_layout = QtGui.QGridLayout()
		row = 0
		column = 0
		row_width = 1
		column_width = 1
		comparison_data_set_layout.addWidget(self.comparison_writer_label, row, column, row_width, column_width, alignment)
		column += column_width
		column_width = 3
		comparison_data_set_layout.addWidget(self.comparison_writer_combobox, row, column, row_width, column_width, alignment)
		column += column_width
		column_width = 1
		comparison_data_set_layout.addWidget(self.comparison_editor_label, row, column, row_width, column_width, alignment)
		column += column_width
		column_width = 3
		comparison_data_set_layout.addWidget(self.comparison_editor_combobox, row, column, row_width, column_width, alignment)
		row += row_width
		column = 0
		row_width = 1
		column_width = 1
		comparison_data_set_layout.addWidget(self.comparison_pd_button, row, column, row_width, column_width, alignment)
		column+=column_width
		comparison_data_set_layout.addWidget(self.comparison_rpd_button, row, column, row_width, column_width, alignment)
		column+=column_width
		comparison_data_set_layout.addWidget(self.comparison_seo_button, row, column, row_width, column_width, alignment)
		column+=column_width
		comparison_data_set_layout.addWidget(self.comparison_all_button, row, column, row_width, column_width, alignment)
		column+=column_width
		comparison_data_set_layout.addWidget(self.comparison_date_field_label, row, column, row_width, column_width, alignment)
		column+=column_width
		column_width = 2
		comparison_data_set_layout.addWidget(self.comparison_date_field_start, row, column, row_width, column_width, alignment)
		column+=column_width
		comparison_data_set_layout.addWidget(self.comparison_date_field_end, row, column, row_width, column_width, alignment)

		self.comparison_data_set_group.setLayout(comparison_data_set_layout)


		self.analysis_parameters_group = QtGui.QGroupBox("Analysis Parameters")
		self.parameters_label = QtGui.QLabel("Compare:")
		self.parameters_list_box = CheckableComboBox("Parameters")
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
		column_width = 3
		parameters_layout.addWidget(self.parameters_list_box, row, column, row_width, column_width, alignment)
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
		self.plot_separate_charts_for_each_parameter = QtGui.QCheckBox("Plot Parameter Charts")
		self.load_data_button = QtGui.QPushButton("Load Data")
		self.plot_button = QtGui.QPushButton("Plot Charts")
		self.plot_save_button = QtGui.QPushButton("Save Charts")
		self.plot_zoom_slider = QtGui.QSlider()
		self.plot_zoom_label = QtGui.QLabel("100%")
		self.plot_zoom_slider.setRange(10,500)
		self.plot_zoom_slider.setValue(100)

		plot_options_layout = QtGui.QGridLayout()
		row = 0
		column = 0
		row_width = 1
		column_width = 1
		alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
		plot_options_group.addWidget(self.plot_type_label, row, column, row_width, column_width, alignment)
		column+=column_width
		column_width = 2
		plot_options_group.addWidget(self.plot_type_combobox, row, column, row_width, column_width, alignment)
		column+=column_width
		column_width = 3		
		plot_options_group.addWidget(self.plot_separate_charts_for_each_parameter, row, column, row_width, column_width, alignment)
		row += row_width
		column_width = int(math.floor(column/3))
		column = column_width
		column_width = 1
		plot_options_group.addWidget(self.load_data_button, row, column, row_width, column_width, alignment)
		column+=column_width
		column_width = 1
		plot_options_group.addWidget(self.plot_button, row, column, row_width, column_width, alignment)
		column+=column_width
		column_width = 1
		plot_options_group.addWidget(self.plot_save_button, row, column, row_width, column_width, alignment)
		row += row_width
		column = 0
		column_width = 2
		plot_options_group.addWidget(self.plot_zoom_slider, row, column, row_width, column_width, alignment)
		column+=column_width
		column_width = 2
		alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
		plot_options_group.addWidget(self.plot_zoom_label, row, column, row_width, column_width, alignment)

		self.plot_options_group.setLayout(plot_options_layout)

		self.plot_viewer_group = QtGui.QGroupBox("Charts")
		self.plot_viewer = ImageLabel()
		self.plot_viewer.setFixedSize(200,200)
		plot_viewer_layout = QtGui.QHBoxLayout()
		plot_viewer_layout.addWidget(self.plot_viewer)
		self.plot_viewer_group.setLayout(plot_viewer_layout)

		self.progress_bar = ProgressBar()
		self.status_label = QtGui.QLabel()

		tna_viewer_layout = QtGui.QGridLayout()
		row = 0
		column = 0
		row_width = 2
		column_width = 4
		alignment = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
		tna_viewer_layout.addWidget(self.input_data_set_group, row, column, row_width, column_width, alignment)
		column+=column_width
		tna_viewer_layout.addWidget(self.comparison_data_set_group, row, column, row_width, column_width, alignment)
		row += row_width
		column = 0
		tna_viewer_layout.addWidget(self.analysis_parameters_group, row, column, row_width, column_width, alignment)
		column+=column_width
		tna_viewer_layout.addWidget(self.plot_options_group, row, column, row_width, column_width, alignment)
		row += row_width
		column = 0
		column_width = 8
		row_width = 4
		tna_viewer_layout.addWidget(self.plot_viewer_group, row, column, row_width, column_width, alignment)
		row+=row_width
		column = 0
		column_width = 8
		alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
		tna_viewer_layout.addWidget(self.progress_bar, row, column, row_width, column_width, alignment)
		row+=row_width
		column = 0
		column_width = 8
		tna_viewer_layout.addWidget(self.status_label, row, column, row_width, column_width, alignment)

		self.setLayout(tna_viewer_layout)
		self.show()
		self.setWindowTitle("Training Needs Analyser")

	def mapEvents(self):
		pass