from PyQt4 import QtGui, QtCore
import sys, os

class CheckableComboBox(QtGui.QComboBox):
    def __init__(self, label):
        super(CheckableComboBox, self).__init__()
        self.label = label
        self.view().pressed.connect(self.handleItemPressed)
        firstItem = QtGui.QStandardItem("----%s----"%self.label)
        firstItem.setBackground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
        firstItem.setSelectable(False)
        self.setModel(QtGui.QStandardItemModel(self))
        self.model().setItem(0, 0, firstItem)
        self.setCurrentIndex(0)
        self.installEventFilter(self)
        self.currentIndexChanged.connect(self.reset)

    def eventFilter(self,target,event):
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

    def reset(self):
        checked_items = len(self.getCheckedItems())
        if checked_items > 0:
            self.model().item(0).setText("----%s : %d options selected----"%(self.label, checked_items))
        else:
            self.model().item(0).setText("----%s----"%(self.label))
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