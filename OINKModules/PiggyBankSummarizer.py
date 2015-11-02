from __future__ import division
import os
import math

import numpy as np
import matplotlib
import pandas as pd
from PyQt4 import QtGui, QtCore

from ImageButton import ImageButton
import MOSES

class PiggyBankSummarizer(QtGui.QWidget):
    changedPiggyBank = QtCore.pyqtSignal()

    def __init__(self, piggy_bank=None, category_tree=None, *args, **kwargs):
        super(PiggyBankSummarizer, self).__init__(*args, **kwargs)
        self.createUI()
        self.mapEvents()
        if piggy_bank is not None:
            self.setPiggyBank(piggy_bank)

    def createUI(self):
        self.summarization_label = QtGui.QLabel("Summarize by:")

        self.available_methods_list_widget = QtGui.QListWidget()
        self.selected_methods_list_widget = QtGui.QListWidget()

        path_to_images_folder = os.path.join(os.getcwd(),"Images") if "OINKModules" not in os.getcwd() else os.path.join(os.getcwd(),"..","Images")

        self.select_method_button = ImageButton(os.path.join(path_to_images_folder,"rightarrow.png"),25,25)
        self.deselect_method_button = ImageButton(os.path.join(path_to_images_folder,"leftarrow.png"),25,25)

        self.move_up_button = ImageButton(os.path.join(path_to_images_folder,"uparrow.png"),25,25)
        self.move_down_button = ImageButton(os.path.join(path_to_images_folder,"downarrow.png"),25,25)

        self.summarize_button = ImageButton(os.path.join(path_to_images_folder,"checkmark_green.png"),25,25)
        self.summarize_button.setToolTip("Click to summarize")

        self.reset_button = ImageButton(os.path.join(path_to_images_folder,"cross.png"),25,25)
        self.reset_button.setToolTip("Click to reset the summarization options")
        
        self.summary_table = QtGui.QTableWidget(0,0)


        select_buttons_layout = QtGui.QVBoxLayout()
        select_buttons_layout.addStretch(2)
        select_buttons_layout.addWidget(self.select_method_button,0)
        select_buttons_layout.addWidget(self.deselect_method_button,0)
        select_buttons_layout.addStretch(2)

        finish_buttons_layout = QtGui.QVBoxLayout()
        finish_buttons_layout.addStretch(2)
        finish_buttons_layout.addWidget(self.move_up_button,0)
        finish_buttons_layout.addWidget(self.move_down_button,0)
        finish_buttons_layout.addStretch(2)
        finish_buttons_layout.addWidget(self.summarize_button,0)
        finish_buttons_layout.addWidget(self.reset_button,0)
        finish_buttons_layout.addStretch(2)

        selector_layout = QtGui.QHBoxLayout()
        selector_layout.addWidget(self.available_methods_list_widget,1)
        selector_layout.addLayout(select_buttons_layout, 1)
        selector_layout.addWidget(self.selected_methods_list_widget,1)
        selector_layout.addLayout(finish_buttons_layout, 1)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.summarization_label)
        layout.addLayout(selector_layout)
        layout.addWidget(self.summary_table)

        self.setLayout(layout)

    def mapEvents(self):
        self.summarize_button.clicked.connect(self.summarize)
        self.reset_button.clicked.connect(self.reset)
        self.select_method_button.clicked.connect(self.select)
        self.deselect_method_button.clicked.connect(self.deselect)

    def reset(self):
        pass
    
    def select(self):
        self.pushFromTo(self.available_methods_list_widget, self.selected_methods_list_widget)
    
    def deselect(self):
        self.pushFromTo(self.selected_methods_list_widget, self.available_methods_list_widget)

    def setPiggyBank(self, piggy_bank=None):
        if piggy_bank is not None:
            self.piggy_bank = piggy_bank
        self.available_methods_list_widget.clear()
        self.selected_methods_list_widget.clear()
        if type(self.piggy_bank) == pd.DataFrame:
            columns = self.piggy_bank.columns
            self.available_methods_list_widget.addItems(columns)
            #self.available_methods_list_widget.setSortingEnabled(True)
            #self.available_methods_list_widget.sortItems()
            self.enableSummarize()
        else:
            self.disableSummarize()

    def enableSummarize(self):
        pass
    
    def summarize(self):
        no_of_selected_methods = self.selected_methods_list_widget.count()
        selected_methods = [str(self.selected_methods_list_widget.item(x).text()) for x in range(no_of_selected_methods)]
        if len(selected_methods)>0:
            print "Selected: %s"%selected_methods
        else:
            print "Select something, Jack." 


    def pushFromTo(self, source_list_widget, destination_list_widget):
        #identify the selected attributes
        selected_attribute_items = source_list_widget.selectedItems()
        #Store them in a list.
        selected_attributes = [str(selected_attribute_item.text()) for selected_attribute_item in selected_attribute_items]
        #Send them to the destination list.
        destination_list_widget.setSortingEnabled(False)
        destination_list_widget.addItems(selected_attributes)
        destination_list_widget.setSortingEnabled(True)
        destination_list_widget.sortItems()
        #Remove them from the source list
        for selected_item in selected_attribute_items:
            source_list_widget.takeItem(source_list_widget.row(selected_item))