from __future__ import division
import os
import gspread
import json
import datetime
import csv
from oauth2client.client import SignedJwtAssertionCredentials
from PyQt4 import QtGui, QtCore
import pandas as pd
import numpy as np

from OpenSSL import crypto

from DateSelectorWidget import DateSelectorWidget
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

def summarizeClarificationSheet(gc, query_date, worksheet_names=None):
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
        print "Opening sheet: %s" %work_sheet
        wks = gc.open("Content VAS - Clarification Tracker").worksheet(work_sheet)
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
        print "Completed fetching the data and writing to file."
        output_headers = ["Total Pending","Raised","Closed","Within TAT","Outside TAT","Tat Met %"]
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
            if week_date.isoweekday() in [1,2,3,4]:
                allowed_tat_gap = 6 #datetime.timedelta(days=6)
            else:
                allowed_tat_gap = 4 #datetime.timedelta(days=4)
            pending_location = (data_frame["Corrected Assigned Date"] <= week_date) & (data_frame["Status"] != "CLOSED") & (data_frame["Assigned Date"] != np.NaN)
            #print pending_location
            raised_location = (data_frame["Corrected Assigned Date"] == week_date) & (data_frame["Assigned Date"] != np.NaN)
            closed_location = (data_frame["Corrected Actioned Date"] == week_date) & (data_frame["Status"] == "CLOSED") & (data_frame["Assigned Date"] != np.NaN)
            #print data_frame
            try:
                within_tat_location = (((data_frame["Corrected Actioned Date"]-data_frame["Corrected Assigned Date"]) > allowed_tat_gap) & (data_frame["Status"] != "CLOSED"))
            except:
                #print data_frame
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

            #print data_frame.loc[pending_location]

            total_pending = len(data_frame.loc[pending_location,"Assigned Date"].values)
            total_raised = len(data_frame.loc[raised_location,"Assigned Date"].values)
            closed = len(data_frame.loc[closed_location,"Assigned Date"].values)
            within_tat = len(data_frame.loc[within_tat_location,"Assigned Date"].values)
            tat_met = within_tat/total_pending
            output_dictionary[week_date] = {
                            "Total Pending" : total_pending,
                            "Raised": total_raised,
                            "Closed": closed,
                            "Within TAT": within_tat,
                            "Outside TAT": total_pending - within_tat,
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
        auto_file_name = os.path.join("Data","GoogleAuthInfo.json")
        json_key = json.load(open(auto_file_name))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
        self.google_credentials = gspread.authorize(credentials)
        self.clip = QtGui.QApplication.clipboard()
        self.createUI()
        self.mapEvents()


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
        self.category_selection.setMaximumHeight(80)
        self.query_tables = ["SHA, PHC & CE", "FMCG & Others", "Lifestyle, Home & Furniture","MT, C/IT & LA", "Auto Acc & Others"]
        #query_tables = 
        self.query_tables.sort()
        self.clarification_sheet_label = QtGui.QLabel("<b>Clarification Spreadsheet Name:</b>")
        self.clarification_sheet_line_edit = QtGui.QLineEdit()
        self.clarification_sheet_line_edit.setText("Content VAS - Clarification Tracker")
        self.category_selection.addItems(self.query_tables)
        self.summary_table_tab = QtGui.QTabWidget()

        self.summary_table_tab.setMaximumWidth(450)
        self.summary_table_tab.setMinimumWidth(450)
        self.summary_table_tab.setMaximumHeight(160)
        self.summary_table_tab.setMinimumHeight(160)
        self.summary_tables = dict((sheet, QtGui.QTableWidget()) for sheet in self.query_tables)
        for sheet in self.query_tables:
            self.summary_table_tab.addTab(self.summary_tables[sheet],"%s..."%sheet[:4])
        self.options_layout = QtGui.QVBoxLayout()
        self.options_layout.addWidget(self.clarification_sheet_label)
        self.options_layout.addWidget(self.clarification_sheet_line_edit)
        self.options_layout.addWidget(self.category_selection_label)
        self.options_layout.addWidget(self.category_selection)
        self.options_layout.addLayout(self.dates_picker)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addLayout(self.options_layout, 1)
        self.layout.addWidget(self.summary_table_tab, 4)
        self.setWindowTitle("Sty Cleaner: We Clean the Shiz.")
        self.setLayout(self.layout)
        self.show()
    
    def mapEvents(self):
        """"""
        self.submit_button.clicked.connect(self.fetchSummarySheet)
    def fetchSummarySheet(self):
        """"""
        query_date = self.date_edit.date().toPyDate()

        selected_sheets = self.getSelectedSheets()
        data_dict = dict((sheet, None) for sheet in selected_sheets)
        for sheet in selected_sheets:
            #print sheet
            data_dict[sheet] = summarizeClarificationSheet(self.google_credentials,query_date, sheet)
        for sheet in selected_sheets:
            if data_dict[sheet] is None:
                self.alertMessage("No Data","There is no data to fetch for the week of %s." %query_date)
            else:   
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
                self.alertMessage("Success","Fetched data for %s for the week of %s." %(sheet, query_date))

    def alertMessage(self, title, message):
        QtGui.QMessageBox.about(self, title, message)

    def getSelectedSheets(self):
        selection = self.category_selection.selectedItems()
        return [str(selection_label.text()) for selection_label in selection]

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
                    s += str(r+1) + '\t' 
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(table_to_copy.item(r,c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)

class StyHand(QtCore.QThread):
    sendSummary = QtCore.pyqtSignal()
    def __init__(self):
        super(StyHand, self).__init__()


if __name__ == "__main__":
    #main()
    import sys
    app = QtGui.QApplication([])
    sty = StyCleaner()
    sys.exit(app.exec_())
