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
        self.USP_button = QtGui.QPushButton("USP")
        self.clear_button = QtGui.QPushButton("Clear")
        self.addWidget(self.label,1)
        self.addWidget(self.filter_box,2)
        self.addWidget(self.PD_button,1)
        self.addWidget(self.RPD_button,1)
        self.addWidget(self.SEO_button,1)
        self.addWidget(self.USP_button,1)
        self.addWidget(self.clear_button,1)
        self.mapEvents()

    def mapEvents(self):
        self.PD_button.clicked.connect(self.selectPD)
        self.RPD_button.clicked.connect(self.selectRPD)
        self.SEO_button.clicked.connect(self.selectSEO)
        self.USP_button.clicked.connect(self.selectUSP)
        self.clear_button.clicked.connect(self.clear)
    
    def selectPD(self):
        self.filter_box.selectIfTextFound("Regular")
        #self.filter_box.select("Regular Description")

    def selectRPD(self):
        self.filter_box.selectIfTextFound("RPD")
        self.filter_box.selectIfTextFound("Rich Product Description")
        
    def selectSEO(self):
        self.filter_box.selectIfTextFound("SEO")

    def selectUSP(self):
        self.filter_box.selectIfTextFound("USP")

    def clear(self):
        self.filter_box.clearSelection()

    def getCheckedItems(self):
        if len(self.filter_box.getCheckedItems()) == 0:
            self.selectSEO()   
            self.selectRPD()   
            self.selectPD()
        return self.filter_box.getCheckedItems()



