from __future__ import division
import math
import os
import sys
import datetime
import time
import random

from PyQt4 import QtGui, QtCore
from ProgressBar import ProgressBar
from Pork import Pork
from Vindaloo import Vindaloo
from Bacon import Bacon
from IncredibleBulk import IncredibleBulk
from ImageLabel import ImageLabel
from SharinganButton import SharinganButton
from OINKChooser import OINKChooser
import MOSES

class OINKLoader(QtGui.QWidget):
    def __init__(self, user_id, password):
        super(OINKLoader, self).__init__()
        self.user_id, self.password = user_id, password
        self.category_tree = None
        self.brand_list = None
        self.employees_list = None
        self.createUI()
        self.mapEvents()
        self.move(300,10)

    def createUI(self):
        path_to_image = os.path.join(MOSES.getPathToImages(), "OINK.png")
        self.image = ImageLabel(path_to_image, 800, 566)
        #self.sharingan = SharinganButton()
        self.progress_bar = ProgressBar()
        self.message = QtGui.QLabel("Not all those who wander are lost....")

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.image)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.message)
        self.setLayout(layout)
        self.setWindowTitle("Bulk Buster: The OINK Preloader Screen")
        icon_file_name_path = os.path.join(MOSES.getPathToImages(),'PORK_Icon.png')
        self.setWindowIcon(QtGui.QIcon(icon_file_name_path))
        self.show()

    def mapEvents(self):
        self.incredible_bulk = IncredibleBulk(self.user_id, self.password)
        self.incredible_bulk.sendActivity.connect(self.showProgress)
        self.incredible_bulk.sendCategoryTree.connect(self.useCategoryTree)
        self.incredible_bulk.sendBrandList.connect(self.useBrandList)
        self.incredible_bulk.sendEmployeesList.connect(self.useEmployeesList)


    def showProgress(self, progress, message):
        self.progress_bar.setValue(progress)
        self.message.setText(message)
        if progress == 100:
            self.initiate()
            self.close()

    def useCategoryTree(self, category_tree):
        self.category_tree = category_tree

    def useBrandList(self, brand_list):
        self.brand_list = brand_list

    def useEmployeesList(self, employees_list):
        self.employees_list = employees_list

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    def initiate(self):
        if self.user_id == "bigbrother":
            user_role = "Admin"
            access_list = ["Pork","Bacon","Vindaloo"]
        else:
            user_role = list(self.employees_list[self.employees_list["Employee ID"] == self.user_id]["Role"])[0]
            access_list = list(self.employees_list[self.employees_list["Employee ID"] == self.user_id]["OINK Access Level"])[0].split(",")
        if len(access_list)>0:
            userDict = {
                "Copy Editor": Bacon, 
                "Team Lead": Vindaloo,
                "Big Brother": Vindaloo,
                "Product Specialist": Bacon,
                "Manager": Vindaloo, 
                "Assistant Manager": Vindaloo,
                "Admin": Pork,
                "Content Writer": Pork
                }
            if user_role not in userDict.keys():
                self.alertMessage("Unauthorized User","This version of OINK is not coded for use by a %s. If you encounter this message, you're probably trying to use the compiled version of OINK that doesn't need Python. That version was developed for use by writers because it's easier to set up. If you'd like to use the source version instead, follow the initial setup chapter in the documentation."%user_role)
            else:
                if len(access_list)>1:
                    self.window = OINKChooser(self.user_id, self.password, access_list, self.category_tree, self.employees_list, self.brand_list)
                    self.window.show()
                else:
                    self.window = userDict[user_role](self.user_id, self.password, self.category_tree, self.employees_list, self.brand_list)
                    self.window.show()
        else:
           self.alertMessage("No Access","You seem to have no access to the OINK Database. Contact your Reporting Manager and ask him or her to grant you access if necessary.")

