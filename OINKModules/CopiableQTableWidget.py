from PyQt4 import QtCore, QtGui

class CopiableQTableWidget(QtGui.QTableWidget):
    def __init__(self, *args, **kwargs):
        super(CopiableQTableWidget, self).__init__(*args, **kwargs)
        self.setStyleSheet("gridline-color: rgb(0, 0, 0)")
        self.clip = QtGui.QApplication.clipboard()

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
            

    def showDataFrame(self, dataframe, highlight_rules=None):
        if dataframe is not None:
            row_count = dataframe.shape[0]
            column_count = dataframe.shape[1]
            self.setRowCount(row_count)
            self.setColumnCount(column_count)
            for row_index in range(row_count):
                match = False
                color = QtGui.QColor(255, 255, 255)
                if highlight_rules is not None:
                    for highlight_rule in highlight_rules:
                        matches = []
                        counter =0
                        for column in highlight_rule["Columns"]:
                            deciding_value = highlight_rule["Values"][counter]
                            value_in_dataframe = dataframe[column][row_index]
                            if type(deciding_value) == list:
                                if deciding_value[0] <= value_in_dataframe < deciding_value[1]:
                                    matches.append(True)
                                else:
                                    matches.append(False)
                            elif type(deciding_value) == str:
                                if value_in_dataframe == deciding_value:
                                    matches.append(True)
                                else:
                                    matches.append(False)
                            else:
                                matches.append(False)
                            counter +=1
                        if len(matches)>0 and False not in matches:
                            match = True
                        else:
                            match = False
                        if match:
                            # print ["%s=%s"%(x, y) for x,y in zip(highlight_rule["Columns"], highlight_rule["Values"])], " matched for row %d."%row_index
                            color = highlight_rule["Color"]
                for col_index in range(column_count):
                    widget_item = QtGui.QTableWidgetItem(str(dataframe.iat[row_index, col_index]))
                    widget_item.setBackgroundColor(color)
                    self.setItem(row_index, col_index, widget_item)
                    

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

    def adjustToColumns(self):
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Interactive)
        self.horizontalHeader().setStretchLastSection(False)
        self.horizontalHeader().setVisible(True)
            

