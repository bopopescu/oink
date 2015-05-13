from __future__ import division
import datetime
import numpy
import sys
from PyQt4 import QtCore, QtGui

import MOSES

class EventManager(QtGui.QWidget):
    def __init__(self, user_id, password):
        super(QtGui.QWidget,self).__init__()
        self.user_id = user_id
        self.password = password
        #self.event_manager_thread = EventManagerThread()
        self.createUI()
        self.mapEvents()
        self.setWindowTitle("Event Manager")
        self.setMinimumWidth(800)
        self.setMaximumWidth(800)
        self.setMinimumHeight(500)
        #self.setMaximumHeight(500)

        self.show()


    def createUI(self):
        self.event_list = QtGui.QListWidget()
        self.edit_event_button = QtGui.QPushButton("Edit Selected Event")
        self.copy_event_button = QtGui.QPushButton("Copy Selected Event")

        self.event_viewer = QtGui.QWidget()
        self.event_viewer_layout = QtGui.QVBoxLayout()
        self.event_viewer_layout.addWidget(self.event_list,3)
        self.event_viewer_layout.addWidget(self.edit_event_button,0)
        self.event_viewer_layout.addWidget(self.copy_event_button,0)
        self.event_viewer.setLayout(self.event_viewer_layout)
        
        self.event_form = QtGui.QWidget()
        
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.event_viewer,0)
        self.layout.addWidget(self.event_form,2)

        self.event_form_layout = QtGui.QGridLayout()

        #Creating widgets for row 1
        self.event_type_label = QtGui.QLabel("Event Type:")
        self.event_type_combobox = QtGui.QComboBox()
        event_types = ["One on One", "Skip Level Meeting", "Fun Activity", "HR Meeting", "Training", "Personal Project", "Group Discussion", "Editor Feedback", "New Employee Join In", "Employee Send Off"]
        self.event_type_combobox.addItems(event_types)
        self.event_details_label = QtGui.QLabel("Event Details:")
        self.event_details_lineedit = QtGui.QLineEdit()

        #Adding row 1 to the grid
        self.event_form_layout.addWidget(self.event_type_label,0,0)
        self.event_form_layout.addWidget(self.event_type_combobox,0,1)
        self.event_form_layout.addWidget(self.event_details_label,0,2)
        self.event_form_layout.addWidget(self.event_details_lineedit,0,3)

        #Creating widgets for row 2
        self.event_start_label = QtGui.QLabel("Event Start Time:")
        self.event_start_time = QtGui.QDateTimeEdit()
        self.event_start_time.setDateTime(datetime.datetime.now())
        self.event_start_time.setDisplayFormat("dd-MMM-yyyy hh:mm AP")
        
        self.event_end_label = QtGui.QLabel("Event End Time:")
        
        self.event_end_time = QtGui.QDateTimeEdit()
        self.event_end_time.setDateTime(datetime.datetime.now())
        self.event_end_time.setDisplayFormat("hh:mm AP")

        #Adding row 2 to the grid
        self.event_form_layout.addWidget(self.event_start_label,1,0)
        self.event_form_layout.addWidget(self.event_start_time,1,1)

        self.event_form_layout.addWidget(self.event_end_label,1,2)
        self.event_form_layout.addWidget(self.event_end_time,1,3)

        #Creating widgets for row 3
        self.participants_label = QtGui.QLabel("Event Participants:")
        self.ex_participants_label = QtGui.QLabel("Excepted Participants:")
        #Adding row 3
        self.event_form_layout.addWidget(self.participants_label,2,0,1,2)
        self.event_form_layout.addWidget(self.ex_participants_label,2,2,1,2)
        #Creating widgets for row 4
        self.participants_list = QtGui.QListWidget()
        self.participants_list.setToolTip("Select the participants by holding\nthe SHIFT key or the CTRL key.")
        self.employees_data = MOSES.getCurrentEmployeesList(self.user_id, self.password, datetime.date.today())
        employees = []
        for employee in self.employees_data:
            employees.append(employee["Name"])
        employees.sort()
        self.participants_list.addItems(employees)
        self.participants_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.participants_list.setMinimumHeight(100)
        self.participants_list.setMaximumHeight(100)
        self.ex_participants_list = QtGui.QListWidget()
        self.ex_participants_list.setToolTip("Select the participants who do not require\na relaxed efficiency by holding the \nnSHIFT key or the CTRL key.")

        self.ex_participants_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ex_participants_list.setMaximumHeight(100)
        self.ex_participants_list.setMinimumHeight(100)
        #Adding row 4
        self.event_form_layout.addWidget(self.participants_list,3,0,2,2)
        self.event_form_layout.addWidget(self.ex_participants_list,3,2,2,2)
        
        #Creating widgets for row 5
        self.appl_relax_checkbox = QtGui.QCheckBox("Applicable for Relaxation")
        #Hidden widgets
        self.relax_type_label = QtGui.QLabel("Relaxation Type:")
        self.relax_type_combobox = QtGui.QComboBox()
        relax_types = ["Additive","Divisor"]
        self.relax_type_combobox.addItems(relax_types)

        #Adding row 5
        self.event_form_layout.addWidget(self.appl_relax_checkbox,5,0)
        self.event_form_layout.addWidget(self.relax_type_label,5,2)
        self.event_form_layout.addWidget(self.relax_type_combobox,5,3)

        #Creating Widgets for row 6
        self.comments_label = QtGui.QLabel("Comments:")
        self.comments_lineedit = QtGui.QLineEdit()
        self.approval_label = QtGui.QLabel("Approval Status")
        self.approval_combobox = QtGui.QComboBox()
        approval_types = ["Approved", "Pending","Rejected"]
        self.approval_combobox.addItems(approval_types)
        #Adding row 6
        self.event_form_layout.addWidget(self.comments_label,6,0)
        self.event_form_layout.addWidget(self.comments_lineedit,6,1)
        self.event_form_layout.addWidget(self.approval_label,6,2)
        self.event_form_layout.addWidget(self.approval_combobox,6,3)

        #Creating Widgets for row 7
        #More Hidden Widgets
        self.calc_duration_label = QtGui.QLabel("Calculated Duration")
        self.calc_duration_datetimeedit = QtGui.QDateTimeEdit()
        self.calc_duration_datetimeedit.setDisplayFormat("hh:mm:ss")

        self.calc_efficiency_relax_label = QtGui.QLabel("Calculated Relaxations:")
        self.calc_efficiency_relax_table = QtGui.QTableWidget()
        self.calc_efficiency_relax_table.setMaximumHeight(100)
        self.calc_efficiency_relax_table.setMinimumWidth(550)
        self.calc_efficiency_relax_table.setMaximumWidth(550)
        self.calc_efficiency_relax_table.setMinimumHeight(100)
        self.calc_efficiency_relax_table.setRowCount(1)
        self.calc_efficiency_relax_table.setColumnCount(3)
        labels = ["Name","Calculated Relaxation","Total Relaxation For the Day"]
        self.calc_efficiency_relax_table.setHorizontalHeaderLabels(labels)
        self.calc_efficiency_relax_table.resizeRowsToContents()
        self.calc_efficiency_relax_table.resizeColumnsToContents()
        self.recalc_button = QtGui.QPushButton("Refresh")
        #Adding row 7
        self.event_form_layout.addWidget(self.calc_duration_label,7,0)
        self.event_form_layout.addWidget(self.calc_duration_datetimeedit,7,1)
        self.event_form_layout.addWidget(self.recalc_button,7,3)
        #Adding row 8
        self.event_form_layout.addWidget(self.calc_efficiency_relax_label,8,0)
        #Adding row 9
        self.event_form_layout.addWidget(self.calc_efficiency_relax_table,9,0,2,4)

        #Creating widgets for row 10
        self.submit_button = QtGui.QPushButton("Submit")
        self.clear_button = QtGui.QPushButton("Clear")
        self.delete_button = QtGui.QPushButton("Delete")
        #Adding row 8
        self.event_form_layout.addWidget(self.submit_button,11,1)
        self.event_form_layout.addWidget(self.clear_button,11,2)
        self.event_form_layout.addWidget(self.delete_button,11,3)

        self.event_form_layout.setRowMinimumHeight(0,10)
        self.event_form_layout.setRowMinimumHeight(1,10)
        self.event_form_layout.setRowMinimumHeight(2,20)
        self.event_form_layout.setRowMinimumHeight(3,20)
        self.event_form_layout.setRowMinimumHeight(4,20)
        self.event_form_layout.setRowMinimumHeight(5,20)
        self.event_form_layout.setRowMinimumHeight(6,20)
        self.event_form_layout.setRowMinimumHeight(7,20)
        self.event_form_layout.setRowMinimumHeight(8,20)
        self.event_form_layout.setRowMinimumHeight(9,20)
        self.event_form_layout.setRowMinimumHeight(10,20)
        self.event_form_layout.setRowMinimumHeight(11,20)

        self.layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.event_form.setLayout(self.event_form_layout)
        
        self.setLayout(self.layout)


    def mapEvents(self):
        """Maps events"""
        self.event_start_time.dateTimeChanged.connect(self.limitEndTime)
        self.event_end_time.dateTimeChanged.connect(self.endTimeEdited)
        self.participants_list.itemSelectionChanged.connect(self.setExcludableItems)
        self.submit_button.clicked.connect(self.testy)
        self.recalc_button.clicked.connect(self.populateRelaxationTable)

    def toggleRelaxation(self):
        """"""
        #When Relaxation is checked, this method unhides the relaxation specific widget areas.
        #When unchecked, it hides them.
    
    def testy(self):
        print "Unrelaxed Participants are: %s" %self.getUnrelaxedParticipants()
        print "Relaxed Participants are: %s" %self.getRelaxedParticipants()
    
    def calculateRelaxation(self):
        """"""
        #Calculates relaxations and populates the table.

    def selectParticipant(self):
        """"""
        #When a participant is selected in the main list, his\her name is added to the exclusion list for selection.

    def limitEndTime(self):
        self.start_time = self.event_start_time.dateTime().toPyDateTime()
        self.event_end_time.setMinimumDateTime(self.start_time)
        self.event_end_time.setDateTime(self.start_time)
    
    def setExcludableItems(self):
        self.ex_participants_list.clear()
        participants = self.getAllParticipants()
        self.ex_participants_list.addItems(participants)

    def getAllParticipants(self):
        participants_iterable = self.participants_list.selectedItems()
        participants = []
        for participant in participants_iterable:
            participants.append(str(participant.text()))
        participants.sort()
        return participants

    def getRelaxedParticipants(self):
        participants = self.getAllParticipants()
        unrelaxed_participants = self.getUnrelaxedParticipants()
        relaxed_participants = [participant for participant in participants if participant not in unrelaxed_participants]
        return relaxed_participants
    
    def getUnrelaxedParticipants(self):
        unrelaxed_participants_iterable = self.ex_participants_list.selectedItems()
        unrelaxed_participants = []
        for unrelaxed_participant in unrelaxed_participants_iterable:
            unrelaxed_participants.append(str(unrelaxed_participant.text()))
        unrelaxed_participants.sort()

        return unrelaxed_participants
    
    def endTimeEdited(self):
        #There's a slight problem with how this works. It'll fail if we ever have events scheduled past midnights
        """Max event length is 8 hours.
        Events cannot cross over dates.

        """
        self.start_time = self.event_start_time.dateTime().toPyDateTime()
        self.end_time = self.event_end_time.dateTime().toPyDateTime()
        duration_seconds = (self.end_time - self.start_time).total_seconds()
        if self.end_time >= self.start_time:
            if 0 <= duration_seconds <= (8*3600):
                self.showDuration(duration_seconds)
                self.showDuration(duration_seconds)
            else:
                self.event_end_time.setDateTime(self.start_time)
        else:
            self.event_end_time.setDateTime(self.start_time)

    def populateRelaxationTable(self):
        relaxed_participants = self.getRelaxedParticipants()
        self.calc_efficiency_relax_table.setRowCount(0)
        row_index = 0
        col_index = 0
        self.spinboxes_dict = {}
        for participant in relaxed_participants:
            #Insert a new row and add a spinbox corresponding to a participant's name.
            self.calc_efficiency_relax_table.insertRow(row_index)
            self.spinboxes_dict.update({participant: QtGui.QDoubleSpinBox()})
            self.spinboxes_dict[participant].setSingleStep(0.05)
            self.spinboxes_dict[participant].setDecimals(2)
            self.spinboxes_dict[participant].setSuffix("%")
            #Get the participant's employee ID and find out how much time he's been spending in events for a given day.
            participant_id = self.getEmployeeID(participant)
            participant_duration = self.getTotalDurationFor(participant_id)
            current_duration = self.getDuration()
            total_duration = participant_duration + current_duration
            shrinkage = 8*3600*0.125
            if total_duration <= shrinkage:
                relaxation = 0.0
            else:
                if participant_duration < shrinkage:
                    difference = shrinkage - participant_duration
                    valid_duration = current_duration - difference
                else:
                    valid_duration = current_duration
                #The relaxation is awarded for minutes of this event provided the 
                relaxation = (valid_duration)/(8*3600)
                print "Valid Duration : %d, Relaxation: %s." %(valid_duration,relaxation)

            self.spinboxes_dict[participant].setValue((relaxation*100))
            self.calc_efficiency_relax_table.setItem(row_index, 0, QtGui.QTableWidgetItem(str(participant)))
            self.calc_efficiency_relax_table.setCellWidget(row_index, 1, self.spinboxes_dict[participant])
            row_index+=1
        self.calc_efficiency_relax_table.resizeColumnsToContents()
        #self.calc_efficiency_relax_table.resizeRowsToContents()

    def getEmployeeID(self, employee_name):
        return [employee["Employee ID"] for employee in self.employees_data if employee["Name"] == employee_name][0]

    def getDuration(self):
        self.start_time = self.event_start_time.dateTime().toPyDateTime()
        self.end_time = self.event_end_time.dateTime().toPyDateTime()
        duration_seconds = (self.end_time - self.start_time).total_seconds()
        return duration_seconds
    
    def getTotalDurationFor(self, employee_id):
        from random import randint
        total_duration = randint(0,3600)
        #print "Generated random duration of %d" %total_duration
        return total_duration

    def showDuration(self, duration_seconds):
        h, remainder = divmod(duration_seconds, 3600)
        m, s = divmod(remainder, 60)
        h = int(h)
        m = int(m)
        s = int(s)
        self.duration = datetime.time(h,m,s)
        self.calc_duration_datetimeedit.setTime(self.duration)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    u, p = MOSES.getBigbrotherCredentials()
    events = EventManager(u,p)
    sys.exit(app.exec_())

    #select * from managermapping where `Employee ID` = '62487' AND `Revision Date` = (SELECT MAX(`Revision Date`) from managermapping where `Revision Date`<='2015-05-01');