from __future__ import division
import os
from PyQt4 import QtGui, QtCore


class ImageLabel(QtGui.QLabel):
    def __init__(self, image_path=None, height=None, width=None, *args, **kwargs):
        super(ImageLabel, self).__init__(*args, **kwargs)
        if height is None:
            self.height = 75
        else:
            self.height = height
        if width is None:
            self.width = 75
        else:
            self.width = width
            
        if image_path is not None:
            self.showImage(image_path, self.height, self.width)
        else:
            self.setText("No image.")
            self.setFixedSize(150,20)

    def showImage(self, image_path, height, width):
        self.setText("")
        type = os.path.splitext(os.path.basename(str(image_path)))[1]
        image_pixmap = QtGui.QPixmap(image_path, type)
        image_pixmap = image_pixmap.scaled(
                                        QtCore.QSize(width, height),
                                        QtCore.Qt.KeepAspectRatio, 
                                        QtCore.Qt.SmoothTransformation)
        self.setPixmap(image_pixmap)
        self.setFixedSize(image_pixmap.rect().size())