from __future__ import division
import os
from PyQt4 import QtGui, QtCore


class ImageButton(QtGui.QPushButton):
    def __init__(self, image_path, height=None, width=None, mouseover_image_path=None):
        super(ImageButton, self).__init__()
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

        self.showImage(self.image_path)

    def showImage(self, image_path):
        type = os.path.splitext(os.path.basename(str(image_path)))[1]
        image_pixmap = QtGui.QPixmap(image_path, type)

        image_pixmap = image_pixmap.scaled(
                                        QtCore.QSize(self.width, self.height),
                                        QtCore.Qt.KeepAspectRatio, 
                                        QtCore.Qt.SmoothTransformation)
        icon = QtGui.QIcon(image_pixmap)
        self.setIcon(icon)
        self.setIconSize(image_pixmap.rect().size())
        self.setFixedSize(image_pixmap.rect().size())

    def enterEvent(self, evnt):
        super(ImageButton, self).enterEvent(evnt)
        self.showImage(self.mouseover_image_path)

    def leaveEvent(self, evnt):
        self.showImage(self.image_path)

        super(ImageButton, self).leaveEvent(evnt)
                
