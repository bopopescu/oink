from PyQt4 import QtGui, QtCore
import sys, os

class CheckableComboBox(QtGui.QComboBox):
    changedSelection = QtCore.pyqtSignal(bool)
    def __init__(self, label):
        super(CheckableComboBox, self).__init__()
        self.label = label
        self.view().pressed.connect(self.handleItemPressed)
        self.clear()
        self.setCurrentIndex(0)
        self.installEventFilter(self)
        self.currentIndexChanged.connect(self.reset)

    def eventFilter(self, target, event):
        if(event.type()== QtCore.QEvent.Wheel):
            #wheel event is blocked here
            return True
        return False

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if "---" not in item.text():
            if item.checkState() == QtCore.Qt.Checked:
                item.setCheckState(QtCore.Qt.Unchecked)
            else:
                item.setCheckState(QtCore.Qt.Checked)
            self.changedSelection.emit(True)

    def reset(self):
        checked_items = len(self.getCheckedItems())
        if checked_items > 0:
            self.model().item(0).setText("----%s : %d options selected----"%(self.label, checked_items))
            self.setCurrentIndex(0)
        else:
            self.setItemText(0,"----%s----"%(self.label))
        if self.currentIndex() != 0:
            self.setCurrentIndex(0)

    def getCheckedItems(self):
        rows = self.model().rowCount()
        checked_items = []
        for item_index in range(rows)[1:]:
            item = self.model().item(item_index)
            if item.checkState() == QtCore.Qt.Checked:
                checked_items.append(str(item.text()))
        return checked_items

    def clear(self):
        super(CheckableComboBox,self).clear()
        firstItem = QtGui.QStandardItem("----%s----"%self.label)
        firstItem.setBackground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
        firstItem.setSelectable(False)
        self.setModel(QtGui.QStandardItemModel(self))
        self.model().setItem(0, 0, firstItem)
        self.model().item(0).setText("----%s----"%(self.label))
    
    def addItems(self,items_list):
        base_index = self.__len__()
        for item_index in range(len(items_list)):
            item_object = items_list[item_index]
            if item_object is not None:
                self.addItem(items_list[item_index])
                item = self.model().item(item_index+base_index, 0)
                item.setCheckState(QtCore.Qt.Unchecked)
        self.reset()

    def select(self, query, mute=None):
        if mute is None:
            mute = False
        if type(query) == str:
            rows = self.model().rowCount()
            found_item = False
            for item_index in range(rows)[1:]:
                if not found_item:
                    item = self.model().item(item_index)
                    item_text = str(item.text())
                    if (item_text == query):
                        found_item = True
                        if (item.checkState() != QtCore.Qt.Checked):
                            item.setCheckState(QtCore.Qt.Checked)
                else:
                    break
            
            if found_item and not(mute):
                self.reset()
                self.changedSelection.emit(True)
        elif type(query) == list:
            for query_item in query:
                self.select(query_item, True)
            self.reset()
            self.changedSelection.emit(True)

    def selectIfTextFound(self, query_string):
        rows = self.model().rowCount()
        found_item = False
        for item_index in range(rows)[1:]:
            item = self.model().item(item_index)
            item_text = str(item.text())
            if (query_string in item_text):
                found_item = True
                if (item.checkState() != QtCore.Qt.Checked):
                    item.setCheckState(QtCore.Qt.Checked)
        if found_item:
            self.reset()
            self.changedSelection.emit(True)

    def selectAll(self):
        rows = self.model().rowCount()
        for item_index in range(rows)[1:]:
            item = self.model().item(item_index)
            if (item.checkState() != QtCore.Qt.Checked):
                item.setCheckState(QtCore.Qt.Checked)
        self.reset()
        self.changedSelection.emit(True)

    def clearSelection(self):
        rows = self.model().rowCount()
        for item_index in range(rows)[1:]:
            item = self.model().item(item_index)
            if (item.checkState() == QtCore.Qt.Checked):
                item.setCheckState(QtCore.Qt.Unchecked)
        self.reset()
        self.changedSelection.emit(True)


class Dialog_01(QtGui.QMainWindow):
    def __init__(self):
        super(QtGui.QMainWindow,self).__init__()
        myQWidget = QtGui.QWidget()
        myBoxLayout = QtGui.QVBoxLayout()
        myQWidget.setLayout(myBoxLayout)
        self.setCentralWidget(myQWidget)
        self.ComboBox = CheckableComboBox("Some Label")
        for i in range(3):
            self.ComboBox.addItem("Combobox Item " + str(i))
            item = self.ComboBox.model().item(i+1, 0)
            item.setCheckState(QtCore.Qt.Unchecked)
        self.button = QtGui.QPushButton("Go!")
        self.button.clicked.connect(self.ComboBox.getCheckedItems)
        myBoxLayout.addWidget(self.ComboBox)
        myBoxLayout.addWidget(self.button)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog_1 = Dialog_01()
    dialog_1.show()
    dialog_1.resize(480,320)
    sys.exit(app.exec_())