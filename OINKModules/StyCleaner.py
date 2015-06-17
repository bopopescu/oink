from __future__ import division
import os
import gspread
import json
import time
import datetime
import csv
from oauth2client.client import SignedJwtAssertionCredentials
from PyQt4 import QtGui, QtCore
import pandas as pd
import numpy as np
import httplib2

import MOSES
def getWeekNum(inputDate):
    if type(inputDate) == type(datetime.date.today()):
        return inputDate.isocalendar()[1]

def getDatesInWeekOf(inputDate):
    """Returns all the dates in the week containing a particular date."""
    if type(inputDate) == type(datetime.date.today()):
        #inputDate
        counter = 1
        stopthis = False
        dates=[inputDate]
        while not stopthis:
            previousDate = inputDate - datetime.timedelta(days = counter)
            todayWeek = getWeekNum(inputDate)
            previousDateWeek = getWeekNum(previousDate)
            if todayWeek == previousDateWeek:
                dates.append(previousDate)
            else:
                stopthis = True
            counter += 1
        return dates
    else:
        return "Error, please input a python datetime object to getDatesInWeekOf."

def summarizeClarificationSheet(gc, sheet_name, query_date, worksheet_names=None):
    #import os
    #print "Loading credentials from the JSON."
    #auto_file_name = os.path.join("Data","GoogleAuthInfo.json")
    #json_key = json.load(open(auto_file_name))
    #scope = ['https://spreadsheets.google.com/feeds']
    #credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    #gc = gspread.authorize(credentials)
    if worksheet_names is None:
        worksheet_names = ["FMCG & Others", "Lifestyle, Home & Furniture","MT, C/IT & LA", "Auto Acc & Others","SHA, PHC & CE"]
        raw_data_file_name = "Clarification_Data_%s_All.csv" %query_date
        summary_file_name = "Clarification_Summary_Sheet_%s_All.csv"%query_date

    elif type(worksheet_names) == str:
        worksheet_names = [worksheet_names]
        raw_data_file_name = "Clarification_Data_%s_%s.csv" %(query_date,worksheet_names[0])
        summary_file_name = "Clarification_Summary_Sheet_%s_%s.csv"%(query_date,worksheet_names[0])
    else:
        raw_data_file_name = "Clarification_Data_%s_%s.csv" %(query_date,worksheet_names[0])
        summary_file_name = "Clarification_Summary_Sheet_%s_%s.csv"%(query_date,worksheet_names[0])

    over_all_data = []
    counter = 0
    for work_sheet in worksheet_names:
        #print "Opening sheet: %s" %work_sheet
        wks = gc.open(sheet_name).worksheet(work_sheet)
        data = wks.get_all_values()
        for row in data[1:]:
            if counter == 0:
                #print row
                assigned_date_index = row.index("Assigned Date")
                actioned_date_index = row.index("Actioned Date")
                status_index = row.index("Status")
                #over_all_data.append(["Assigned Date","Actioned Date","Status"])
            else:
                assigned_date = row[assigned_date_index] if row[assigned_date_index].strip() != "" else np.NaN
                actioned_date = row[actioned_date_index] if row[actioned_date_index].strip() != "" else np.NaN
                status = row[status_index] if row[status_index].strip() != "" else np.NaN
                over_all_data.append({
                            "Assigned Date": assigned_date,
                            "Actioned Date": actioned_date,
                            "Status": status.upper() if type(status) == str else status
                            })
            counter +=1
    data_frame = pd.DataFrame(over_all_data)
    if data_frame.shape[0] == 0:
        print "No records found for the %s table." % worksheet_names[0]
    else:
        data_frame = data_frame[pd.notnull(data_frame["Assigned Date"])]
        #data_frame.to_csv(raw_data_file_name,sep=',')
        #print data_frame
        print "Completed fetching the data for %s." % worksheet_names[0]
        output_headers = ["Total Pending","Raised","Closed","Closed Within TAT","Pending Outside TAT","Tat Met %"]
        week_dates = getDatesInWeekOf(query_date)
        output_dictionary = dict((week_date,{}) for week_date in week_dates)
        assigned_dates = []
        actioned_dates = []
        cleaned_list = []
        for index, row in data_frame.iterrows():
            if (row["Assigned Date"].strip() not in ["Assigned Date", ""]) and (type(row["Assigned Date"]) != type(np.NaN)):
                try:
                    assigned_date = datetime.datetime.strptime(row["Assigned Date"],"%m/%d/%Y").date()
                    if type(row["Actioned Date"]) != type(np.NaN):
                        actioned_date = datetime.datetime.strptime(row["Actioned Date"],"%m/%d/%Y").date()
                    else:
                        actioned_date = np.NaN
                except:
                    print index, row
                    raise
            else:
                assigned_date = np.NaN
                actioned_date = np.NaN
            assigned_dates.append(assigned_date)
            actioned_dates.append(actioned_date)
        #print data_frame.loc[data_frame["Assigned Date"] == ""]
        #print data_frame.shape
        #print len(assigned_dates)
        #print len(actioned_dates)
        data_frame["Corrected Assigned Date"] = assigned_dates
        data_frame["Corrected Actioned Date"] = actioned_dates
        for week_date in week_dates:
            #the tat is 4 working days, so for Monday to Wednesday, the TAT is 4 + 2
            if week_date.isoweekday() in [1,2,3,4]:
                allowed_tat_gap = 6 #datetime.timedelta(days=6)
            else:
                allowed_tat_gap = 4 #datetime.timedelta(days=4)
            #Count all those which are pending
            pending_location = (data_frame["Corrected Assigned Date"] <= week_date) & (data_frame["Status"] != "CLOSED") & (data_frame["Assigned Date"] != np.NaN)
            #count all those entries which were raised on this date.
            raised_location = (data_frame["Corrected Assigned Date"] == week_date) & (data_frame["Assigned Date"] != np.NaN)
            #count entries closed on  this date.
            closed_location = (data_frame["Corrected Actioned Date"] == week_date) & (data_frame["Status"] == "CLOSED") & (data_frame["Assigned Date"] != np.NaN)
            #print data_frame
            #why is this in an exception catcher?
            try:
                #Count entries closed on this date within TAT date.
                within_tat_location = ((data_frame["Corrected Actioned Date"] == week_date) & ((data_frame["Corrected Actioned Date"]-data_frame["Corrected Assigned Date"]) <= allowed_tat_gap) & (data_frame["Status"] != "CLOSED")) & (data_frame["Assigned Date"] != np.NaN)
            except:
                #print data_frame
                print "I should not be in this part of the code. There's a problem with the closed within tat numbers."
                within_tat_location = []
                for index, row in data_frame.iterrows():
                    if type(row["Corrected Actioned Date"]) != type(datetime.date.today()):
                        verdict = (week_date - row["Corrected Assigned Date"]) > datetime.timedelta(days=allowed_tat_gap)
                    else:
                        try:
                            verdict = (row["Corrected Actioned Date"]-row["Corrected Assigned Date"]) > datetime.timedelta(days=allowed_tat_gap)
                        except:
                            print row["Corrected Actioned Date"], row["Corrected Assigned Date"]
                            raise
                    within_tat_location.append(verdict)

            #count entries that are pending and within tat as of this date.
            pending_within_tat_location = (data_frame["Corrected Assigned Date"] <= week_date) & (data_frame["Status"] != "CLOSED") & (data_frame["Assigned Date"] != np.NaN) &((week_date-data_frame["Corrected Assigned Date"]) <= allowed_tat_gap)
            #print data_frame.loc[pending_location]

            total_pending = len(data_frame.loc[pending_location,"Assigned Date"].values)
            total_raised = len(data_frame.loc[raised_location,"Assigned Date"].values)
            closed = len(data_frame.loc[closed_location,"Assigned Date"].values)
            within_tat = len(data_frame.loc[within_tat_location,"Assigned Date"].values)
            tat_met = within_tat/total_pending
            pending_within_tat = len(data_frame.loc[pending_within_tat_location,"Assigned Date"].values)
            output_dictionary[week_date] = {
                            "Total Pending" : total_pending,
                            "Raised": total_raised,
                            "Closed": closed,
                            "Closed Within TAT": within_tat,
                            "Pending Outside TAT": total_pending - pending_within_tat,
                            "Tat Met %": "%.2f%%"%(tat_met*100)
                            }
        output_data_frame = pd.DataFrame(output_dictionary)
        #print list(output_data_frame.columns.values)
        output_data_frame = output_data_frame.transpose()[output_headers]

        #output_data_frame.to_csv(summary_file_name,sep=",")
        #print "Completed summarizing the clarification sheet for %s categories(s)." % worksheet_names[0] if len(worksheet_names) == 1 else worksheet_names
        return output_data_frame
    
    

def main():
    print "Welcome to the Clarification Tracker summarization program."
    while True:
        query_date_string = raw_input("Enter a date in the week you wish to summarize. (YYYY-MM-DD): ")
        try:
            query_date = datetime.datetime.strptime(query_date_string, '%Y-%m-%d').date()
            break
        except:
            print "%s is not an acceptable input. Please try again." %query_date_string
            raw_input("Hit Enter to continue:")
            pass
    query_tables = ["SHA, PHC & CE", "FMCG & Others", "Lifestyle, Home & Furniture","MT, C/IT & LA", "Auto Acc & Others"]
    for query_table in query_tables:
        print "Trying to summarize the %s clarification sheet." %query_table
        summarizeClarificationSheet(query_date, query_table)
    raw_input("Completed. Hit enter to exit.>")

class StyCleaner(QtGui.QWidget):
    def __init__(self):
        super(StyCleaner, self).__init__()
        self.clip = QtGui.QApplication.clipboard()
        self.sty_hand = StyHand()
        self.createUI()
        self.mapEvents()

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)
    
    def createUI(self):
        """"""
        self.dates_picker = QtGui.QHBoxLayout()
        self.date_label = QtGui.QLabel("<b>Select a date:</b>")
        self.date_edit = QtGui.QDateTimeEdit()
        self.date_edit.setDisplayFormat("MMM dd, yy")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumDate(QtCore.QDate(2015,1,1))
        self.date_edit.setDate(QtCore.QDate(datetime.date.today()))

        self.submit_button = QtGui.QPushButton("OK")
        
        self.dates_picker.addWidget(self.date_label)
        self.dates_picker.addWidget(self.date_edit)
        self.dates_picker.addWidget(self.submit_button)

        self.category_selection_label = QtGui.QLabel("<b>Select Sheets to Summarize:</b>")
        self.category_selection = QtGui.QListWidget()
        self.category_selection.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.query_tables = ["SHA, PHC & CE", "FMCG & Others", "Lifestyle, Home & Furniture","MT, C/IT & LA", "Auto Acc & Others"]
        #query_tables = 
        self.query_tables.sort()
        self.clarification_sheet_label = QtGui.QLabel("<b>Clarification Spreadsheet Name:</b>")
        self.clarification_sheet_line_edit = QtGui.QLineEdit()
        self.clarification_sheet_line_edit.setText("Content VAS - Clarification Tracker")
        self.category_selection.addItems(self.query_tables)
        self.summary_table_tab = QtGui.QTabWidget()

        self.summary_table_tab.setMinimumWidth(460)
        self.summary_table_tab.setMinimumHeight(160)
        self.summary_tables = dict((sheet, QtGui.QTableWidget()) for sheet in self.query_tables)
        for sheet in self.query_tables:
            self.summary_table_tab.addTab(self.summary_tables[sheet],"%s..."%sheet[:4])
        self.options_layout = QtGui.QVBoxLayout()
        self.options_layout.addWidget(self.clarification_sheet_label,1)
        self.options_layout.addWidget(self.clarification_sheet_line_edit,1)
        self.options_layout.addWidget(self.category_selection_label,1)
        self.options_layout.addWidget(self.category_selection,4)
        self.options_layout.addLayout(self.dates_picker,1)
        self.options_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.progress_bar = QtGui.QProgressBar()
        progress_bar_style = """
            .QProgressBar {
                 text-align: center;
             }"""
        self.progress_bar.setStyleSheet(progress_bar_style)
        self.tabs_layout = QtGui.QVBoxLayout()
        self.tabs_layout.addWidget(self.summary_table_tab)
        self.tabs_layout.addWidget(self.progress_bar)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addLayout(self.options_layout, 1)
        self.layout.addLayout(self.tabs_layout, 4)
        self.setWindowTitle("Sty Cleaner: We Clean the Shiz.")
        self.setLayout(self.layout)

    
    def mapEvents(self):
        """"""
        self.submit_button.clicked.connect(self.fetchSummarySheet)
        self.sty_hand.sendSummary.connect(self.populateSummaries)
        self.sty_hand.sendProgress.connect(self.displayProgress)

    def fetchSummarySheet(self):
        """"""
        query_date = self.date_edit.date().toPyDate()
        selected_sheets = self.getSelectedSheets()
        sheet_name = str(self.clarification_sheet_line_edit.text()).strip()
        self.sty_hand.restartSending(sheet_name,selected_sheets, query_date)

    def populateSummaries(self, data_dict, selected_sheets, query_date, completion=False):
        for sheet in selected_sheets:
            if (data_dict[sheet] is None) and completion:
                self.alertMessage("No Data","There is no data to fetch for %s the week of %s." %(sheet, query_date))
            elif not (data_dict[sheet] is None):
                self.summary_tables[sheet].setColumnCount(len(data_dict[sheet].columns))
                self.summary_tables[sheet].setRowCount(len(data_dict[sheet].index))
                self.summary_tables[sheet].setHorizontalHeaderLabels(data_dict[sheet].columns)
                index_list = [str(index_data) for index_data in data_dict[sheet].index]
                self.summary_tables[sheet].setVerticalHeaderLabels(index_list)
                for row_number in range(len(data_dict[sheet].index)):
                    for col_number in range(len(data_dict[sheet].columns)):
                        self.summary_tables[sheet].setItem(row_number, col_number, QtGui.QTableWidgetItem(str(data_dict[sheet].iget_value(row_number, col_number))))
                self.summary_tables[sheet].resizeColumnsToContents()
                self.summary_tables[sheet].resizeRowsToContents()
                self.summary_tables[sheet].setStyleSheet("gridline-color: rgb(0, 0, 0)")
                self.summary_table_tab.setCurrentIndex(self.query_tables.index(sheet))
                if completion:
                    self.alertMessage("Success","Fetched data for %s for the week of %s." %(sheet, query_date))

    def getSelectedSheets(self):
        selection = self.category_selection.selectedItems()
        return [str(selection_label.text()) for selection_label in selection]
    
    def displayProgress(self, status, eta, progress):
        if status == "Completed":
            self.progress_bar.setFormat("Completed summaries")
            self.progress_bar.setValue(100)
        else:
            time_string = datetime.datetime.strftime(eta, "%d %B, %H:%M:%S")
            self.progress_bar.setValue(int(progress))
            self.progress_bar.setFormat("%s ETA: %s." %(status, time_string))

    def keyPressEvent(self, e):
        """Found this code online. Go through it and try to improve it."""
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_C: #copy
                current_tab = self.summary_table_tab.currentIndex()
                table_name = self.query_tables[current_tab]
                table_to_copy = self.summary_tables[table_name]
                selected = table_to_copy.selectedRanges()
                s = '\t'+"\t".join([str(table_to_copy.horizontalHeaderItem(i).text()) for i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1)])
                s = s + '\n'

                for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
                    s += table_to_copy.verticalHeaderItem(r).text() + '\t'
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(table_to_copy.item(r,c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)

class StyHand(QtCore.QThread):
    sendSummary = QtCore.pyqtSignal(dict, list, datetime.date, bool)
    sendProgress = QtCore.pyqtSignal(str, datetime.datetime, float)
    def __init__(self):
        super(StyHand, self).__init__()
        self.send = False
        self.sheet_names = []
        self.query_date = datetime.datetime.today()
        self.stop_sending = False
        auth_file_name = os.path.join("Data","GoogleAuthInfo.json")
        json_key = json.load(open(auth_file_name))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
        self.google_credentials = gspread.authorize(credentials)
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def run(self):
        while True:
            if self.send:
                self.process()

    def process(self):
        self.stop_sending = False
        data_dict = dict((sheet, None) for sheet in self.sheet_list)
        start_time = datetime.datetime.now()
        last_update_time = datetime.datetime.now()
        counter = 1
        total = len(self.sheet_list)
        for sheet in self.sheet_list:
            progress = ((counter-1)/total)*100
            self.sendProgress.emit("(Please Wait): Processing summary for %s." %sheet, MOSES.getETA(start_time, counter, total), progress)
            data_dict[sheet] = summarizeClarificationSheet(self.google_credentials, self.sheet_name, self.query_date, sheet)
            self.sendSummary.emit(data_dict, self.sheet_list, self.query_date, False)
            counter +=1
        if not self.stop_sending:
            self.sendSummary.emit(data_dict, self.sheet_list, self.query_date, True)
            self.sendProgress.emit("Completed", datetime.datetime.now(), 100)
            self.send = False


    def __del__(self):
        """"""
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def restartSending(self, sheet_name, sheet_list, query_date):
        self.sheet_name = sheet_name
        self.stop_sending = True
        self.sheet_list = sheet_list
        self.query_date = query_date
        self.send = True


if __name__ == "__main__":
    #main()
    import sys
    app = QtGui.QApplication([])
    sty = StyCleaner()
    sty.show()
    sys.exit(app.exec_())
