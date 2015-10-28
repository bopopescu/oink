from __future__ import division

import pandas as pd
from PyQt4 import QtGui, QtCore
from CheckableComboBox import CheckableComboBox
from CategoryFinder import CategoryFinder

class CategorySelector(QtGui.QVBoxLayout):
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
        row_1 = QtGui.QHBoxLayout()
        row_1.addWidget(self.label,0)
        row_1.addWidget(self.bu_combo_box,1)
        row_1.addWidget(self.super_category_combo_box,1)
        row_1.addWidget(self.category_combo_box,1)
        row_2 = QtGui.QHBoxLayout()
        row_2.addWidget(self.sub_category_combo_box)
        row_2.addWidget(self.vertical_combo_box)
        row_2.addStretch(2)
        row_2.addWidget(self.clear_button)

        self.addLayout(row_1)
        self.addLayout(row_2)
        self.addLayout(self.category_finder)

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

