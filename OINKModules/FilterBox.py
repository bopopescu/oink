#!/usr/bin/python2
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import sys

class FilterBox(QtGui.QWidget):
	def __init__(self, title = None):
		super(FilterBox, self).__init__()
		self.item_counter = 0
		self.checkbox_list = []
		if title is not None:
			self.filters_label = QtGui.QLabel(title)
			self.filters_label.setMinimumWidth(100)
			self.filters_label.setMaximumWidth(100)
		self.selection_label = QtGui.QLabel("<b>No filter set!</b>")
		self.selection_label.setToolTip("This label shows how many filters are selected.")
		self.selection_label.setMinimumWidth(120)
		styleSheet = """
		.QLabel {
			border: 1px solid black;
			border-radius: 5px;
		}
		"""
		self.selection_label.setStyleSheet(styleSheet)

		self.drop_button = QtGui.QPushButton(u"\u25BC")
		self.drop_button.setCheckable(True)
		self.drop_button.setAutoDefault(False)
		#self.drop_button.setFlat(True)
		self.drop_button.setMaximumWidth(20)
		self.drop_button.setMaximumHeight(20)
		self.drop_button.setToolTip("Click to show filters.")
		
		self.filters_widget = QtGui.QListWidget()
		self.filters_widget.setVisible(False)
		if title is not None:
			self.filters_widget.setMinimumWidth(280)
			self.filters_widget.setMaximumWidth(280)
		else:	
			self.filters_widget.setMinimumWidth(210)
			self.filters_widget.setMaximumWidth(210)
		self.filters_widget.setMinimumHeight(50)
		self.filters_widget.setMaximumHeight(50)
		self.filters_widget.setSortingEnabled(True)
		self.filters_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.filters_layout = QtGui.QVBoxLayout()
		self.filters_layout.setMargin(0)
		self.filters_widget.setLayout(self.filters_layout)
		self.filters_widget.itemSelectionChanged.connect(self.setSelectionLabel)
		self.filters_widget.setToolTip("Click to select a filter option.\nHold CTRL while clicking to select multiple items.\nClick once and then hold SHIFT and click again to select all items\nthat lie between those two items.\nClick CTRL-A to select all items.\nClick on the blank space at the very bottom to clear selection.")

		self.drop_button.clicked.connect(self.filters_widget.setVisible)
		
#		self.clear_button = QtGui.QPushButton(u"\u2612")
		self.clear_button = QtGui.QPushButton(u"\u2612")
		self.clear_button.clicked.connect(self.clearFilters)
		self.clear_button.setMaximumWidth(30)
		self.clear_button.setMaximumHeight(20)
		style = """.QPushButton {font-weight: bold; font-size: 14px;}"""
		self.clear_button.setToolTip("Click to clear filters.")
		self.clear_button.setStyleSheet(style)
		#self.clear_button.setFlat(True)
		
		self.toplayout = QtGui.QHBoxLayout()
		if title is not None:
			self.toplayout.addWidget(self.filters_label)
		self.toplayout.addWidget(self.selection_label)
		self.toplayout.addWidget(self.drop_button)
		self.toplayout.addWidget(self.clear_button)
		
		self.layout = QtGui.QVBoxLayout()
		self.layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
		self.layout.addLayout(self.toplayout)
		self.layout.addWidget(self.filters_widget)
		#Testing buttons
		#self.print_selection = QtGui.QPushButton("Print Selection")
		#self.layout.addWidget(self.print_selection)
		#self.print_selection.clicked.connect(self.getFilters)
		#End Test Section
		self.mainLayout = QtGui.QHBoxLayout()
		self.mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
		self.mainLayout.addLayout(self.layout)
		self.setLayout(self.mainLayout)
		#self.show()
			
	def addItems(self, items):
		"""Adds 1 or more items into the filter options list if that item doesn't already exist in it."""
		if type(items) == type(""):
			items = [items]
		#print existing_list_items
		for item in items:
			if item not in self.getExistingFilters():
				self.filters_widget.addItem(item)
	
	def collapse(self):
		self.drop_button.setChecked(False)
		self.filters_widget.setChecked(False)

	def toggle(self):
		new_state = not self.drop_button.isChecked()
		self.drop_button.setChecked(new_state)
		self.filters_widget.setChecked(new_state)

	def getExistingFilters(self):
		existing_list_items = []
		for index in range(self.filters_widget.count()):
			existing_list_items.append(str(self.filters_widget.item(index).text()))
		return existing_list_items

	def getFilters(self):
		filter_objects = self.filters_widget.selectedItems()
		filters = []
		for filter_object in filter_objects:
			filters.append(str(filter_object.text()))
		return filters
	
	def clearFilters(self):
		""""""
		filter_objects = self.filters_widget.selectedItems()
		for filter_object in filter_objects:
			self.filters_widget.setItemSelected(filter_object, False)
	
	def setSelectionLabel(self):
		""""""
		selectedItems =len(self.filters_widget.selectedItems())
		if selectedItems == 0:
			self.selection_label.setText("<b>No filter set!</b>")
		elif selectedItems == 1:
			self.selection_label.setText("<b>1 filter selected.</b>")
		else:
			self.selection_label.setText("<b>%d filters selected.</b>" % selectedItems)

def main():
	app = QtGui.QApplication(sys.argv)
	filter = FilterBox()
	filter.addItems(["Hi","Hello"])
	filter.addItems("Namaskar")
	filter.addItems("Namaskar")
	filter.addItems("a")
	#filter.sortItems()
	sys.exit(app.exec_())
	
if __name__ == "__main__":
	main()