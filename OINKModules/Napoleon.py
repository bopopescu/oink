from PyQt4 import QtGui

import MOSES

class Napoleon(QtGui.QMainWindow):
    """Napoleon Class Definition.
    Napoleon includes a set of tools for Bigbrother, including options to launch PORK, BACON, VINDALOO,
    to rebuild the database, to take backups, to send mails of backups etc.
    """
    def __init__(self, user_id, password):
        super(QtGui.QMainWindow, self).__init__()
        self.user_id, self.password = user_id, password
        self.create_widgets()

    def create_widgets(self):
        self.oink_handler_label = QtGui.QLabel("Select the Application:")
        self.oink_handler_combobox = QtGui.QComboBox()
        self.oink_handler_combobox.addItems(["Pork","Bacon","Vindaloo"])
        self.oink_handler_user_label = QtGui.QLabel("Select User:")
        self.oink_handler_user_combobox = QtGui.QComboBox()
        self.oink_handler_user_combobox.addItems([self.user_id])
        self.oink_launch_button = QtGui.QPushButton("Launch Pork")

        self.host_id_change_button = QtGui.QPushButton("Change Host ID")
        self.user_management_button = QtGui.QPushButton("Open User Management")
        self.connection_monitor = QtGui.QPushButton("View Server Connection Statuses")

        self.oink_handler_layout = QtGui.QGridLayout()
        self.oink_handler_layout.addWidget(self.oink_handler_label, 0, 0)
        self.oink_handler_layout.addWidget(self.oink_handler_combobox, 0, 1)
        self.oink_handler_layout.addWidget(self.oink_handler_user_label, 1, 0)
        self.oink_handler_layout.addWidget(self.oink_handler_user_combobox, 1, 1)
        self.oink_handler_layout.addWidget(self.oink_launch_button, 2, 0, 1, 2)
        
        
        self.oink_handler_group = QtGui.QGroupBox("OINK Launcher")
        self.oink_handler_group.setLayout(self.oink_handler_layout)

        self.tools_layout = QtGui.QVBoxLayout()
        self.tools_layout.addWidget(self.host_id_change_button)
        self.tools_layout.addWidget(self.user_management_button)
        self.tools_layout.addWidget(self.connection_monitor)

        self.tools_group = QtGui.QGroupBox("Tools")
        self.tools_group.setLayout(self.tools_layout)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.oink_handler_group)
        self.layout.addWidget(self.tools_group)

        self.main_widget = QtGui.QWidget()
        self.main_widget.setLayout(self.layout)
        
        self.setCentralWidget(self.main_widget)

        self.setWindowTitle("Napoleon v0.1 - The Brave Survive")
        self.resize(200, 200)
        self.setWindowIcon(QtGui.QIcon('Images\PORK_Icon.png'))
        self.tray_icon = QtGui.QSystemTrayIcon(QtGui.QIcon('Images\PORK_Icon.png'), self)
        self.tray_icon.show()
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Heil Hitler.")
        self.show()

    def createEvents(self):
        self.oink_handler_combobox.currentIndexChanged.connect(self.changeLaunchLabel)

    def changeLaunchLabel(self):
        application_name = str(self.oink_handler_combobox.currentText())
        self.oink_launch_button.setText("Launch %s" %application_name)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([])
    u, p = MOSES.getBigbrotherCredentials()
    napoleon = Napoleon(u,p)
    sys.exit(app.exec_())