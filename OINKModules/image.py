from PyQt4 import QtGui, QtCore
import sys
app = QtGui.QApplication([])
image = QtGui.QImage("HistoricalQuality_Graph_2015528.png")
pixmap = QtGui.QPixmap.fromImage(image)
b = QtGui.QLabel()
b.setPixmap(pixmap.scaled(
                    b.size(),
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation))
b.show()
sys.exit(app.exec_())