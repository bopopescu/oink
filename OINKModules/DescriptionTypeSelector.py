from PyQt4 import QtGui, QtCore
import pandas as pd
from CheckableComboBox import CheckableComboBox

class DescriptionTypeSelector(QtGui.QHBoxLayout):
	def __init__(self, category_tree, *args, **kwargs):
		super(DescriptionTypeSelector, self).__init__(*args, **kwargs)
		self.category_tree = category_tree
		self.createUI()

	def createUI(self):
		self.label = QtGui.QLabel("Description Type:")
		self.filter_box = CheckableComboBox("Description Types")
		self.filter_box.addItems(list(set(self.category_tree["Description Type"])))
		self.PD_button = QtGui.QPushButton("PD")
		self.RPD_button = QtGui.QPushButton("RPD")
		self.SEO_button = QtGui.QPushButton("SEO")
		self.clear_button = QtGui.QPushButton("Clear")
		self.addWidget(self.label,1)
		self.addWidget(self.filter_box,2)
		self.addWidget(self.PD_button,1)
		self.addWidget(self.RPD_button,1)
		self.addWidget(self.SEO_button,1)
		self.addWidget(self.clear_button,1)
		self.mapEvents()

	def mapEvents(self):
		self.PD_button.clicked.connect(self.selectPD)
		self.RPD_button.clicked.connect(self.selectRPD)
		self.SEO_button.clicked.connect(self.selectSEO)
		self.clear_button.clicked.connect(self.clear)
	
	def selectPD(self):
		self.filter_box.select("Regular Description")

	def selectRPD(self):
		self.filter_box.select("Rich Product Description")		
		self.filter_box.select("Rich Product Description Plan A")		
		self.filter_box.select("Rich Product Description Plan B")
		self.filter_box.select("RPD Updation")
		self.filter_box.select("RPD Variant")

	def selectSEO(self):
		self.filter_box.select("SEO Big")		
		self.filter_box.select("SEO Small")		
		self.filter_box.select("SEO Project")	

	def clear(self):
		self.filter_box.clearSelection()

	def getCheckedItems(self):
		return self.filter_box.getCheckedItems()	


