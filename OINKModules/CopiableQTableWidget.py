from PyQt4 import QtCore, QtGui

class CopiableQTableWidget(QtGui.QTableWidget):
    def __init__(self, *args, **kwargs):
        super(CopiableQTableWidget, self).__init__(*args, **kwargs)
        self.clip = QtGui.QApplication.clipboard()
        pass

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_C:
                selected = self.selectedRanges()
                s = '\t'+"\t".join([str(self.horizontalHeaderItem(i).text()) for i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1)])
                s = s + '\n'
                for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
                    s += str(r+1) + '\t' 
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(self.item(r,c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)
            else:
                super(CopiableQTableWidget, self).keyPressEvent(e)
        else:
            super(CopiableQTableWidget, self).keyPressEvent(e)
            

    def showDataFrame(self, dataframe):
        if dataframe is not None:
            row_count = dataframe.shape[0]
            column_count = dataframe.shape[1]
            self.setRowCount(row_count)
            self.setColumnCount(column_count)
            for row_index in range(row_count):
                for col_index in range(column_count):
                    self.setItem(row_index, col_index, QtGui.QTableWidgetItem(str(dataframe.iat[row_index, col_index])))
            self.setHorizontalHeaderLabels(list(dataframe.columns))
            #self.setVerticalHeaderLabels(list(dataframe.index))
            self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self.verticalHeader().setStretchLastSection(False)
            self.verticalHeader().setVisible(True)

            self.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self.horizontalHeader().setStretchLastSection(True)
            self.horizontalHeader().setVisible(True)
        else:
            self.setRowCount(0)
            

