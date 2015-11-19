from __future__ import division
import os
import time
import datetime
import sys
from PyQt4 import QtGui, QtCore
from PIL import ImageQt
from PIL import Image
import PIL

class IconButton(QtGui.QPushButton):
    def __init__(self, label, image_path, height=None, width=None, mouseover_image_path=None):
        super(IconButton, self).__init__()
        self.setText(label)
        self.setMouseTracking(True)
        
        if height is None:
            self.height = 75
        else:
            self.height = height

        if width is None:
            self.width = 75
        else:
            self.width = width

        self.image_path = image_path
        
        if mouseover_image_path is None:
            self.mouseover_image_path = image_path
        else:
            self.mouseover_image_path = mouseover_image_path
            self.setFlat(True)

        self.showImage(self.image_path)

    def showImage(self, image_path):
        type_ = os.path.splitext(os.path.basename(str(image_path)))[1]
        image_pixmap = QtGui.QPixmap(image_path, type_)

        image_pixmap = image_pixmap.scaled(
                                        QtCore.QSize(self.width, self.height),
                                        QtCore.Qt.KeepAspectRatio, 
                                        QtCore.Qt.SmoothTransformation)
        icon = QtGui.QIcon(image_pixmap)
        self.setIcon(icon)
        self.setIconSize(image_pixmap.rect().size())
        #self.setFixedSize(image_pixmap.rect().size())

    def enterEvent(self, evnt):
        super(IconButton, self).enterEvent(evnt)
        self.showImage(self.mouseover_image_path)

    def leaveEvent(self, evnt):
        self.showImage(self.image_path)

        super(IconButton, self).leaveEvent(evnt)
    
    def updateImage(self, qimage_object):
        type_ = os.path.splitext(os.path.basename(str(self.image_path)))[1]
        image_pixmap = QtGui.QPixmap(self.image_path, type_)
        conversion_status = image_pixmap.convertFromImage(qimage_object)
        image_pixmap = image_pixmap.scaled(
                                        QtCore.QSize(self.width, self.height),
                                        QtCore.Qt.KeepAspectRatio, 
                                        QtCore.Qt.SmoothTransformation)
        icon = QtGui.QIcon(image_pixmap)
        self.setIcon(icon)
        self.setIconSize(image_pixmap.rect().size())
        self.setFixedSize(image_pixmap.rect().size())