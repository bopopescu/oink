#!/usr/bin/python2
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

import datetime
from Porker import Porker

import MOSES

class WeekCalendar(QtGui.QCalendarWidget):
    def __init__(self, userID, password):
        """WeekCalendar"""
        self.userID = userID
        self.password = password
        QtGui.QCalendarWidget.__init__(self)
        self.setGridVisible(True)
        self.setHorizontalHeaderFormat(QtGui.QCalendarWidget.SingleLetterDayNames)
        self.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.counter = 0
        self.datesData = {datetime.date.today():["Working", "0", "0"]}
    
    def setDatesData(self, dates_data):
        self.datesData = dates_data
        self.updateCells()
        

    def paintCell(self, painter, rect, date):
        """WeekCalendar Paint method.

        This method paints the calendar cell based on the following criteria:

        1. The current date is always painted red.
        2. The last working date is always painted a light red.
        3. The days in the current week are painted light blue.
        4. All non-working days for the entire team are painted grey.
        5. The top left corner is painted yellow on all days where a leave has been applied.
        6. The top left corner is painted orange on all days where a leave has been approved.
        7. A unicode down-arrow is displayed just below the top left corner
            whenever a relaxation is provided for a particular date.
        8. A horizontal bar is painted at the bottom of each working day. The bar is red till 25%, 
            orange from 25% to 75%, a mix of both from 75% to 99.99% and green at and above 100%. 
        """
        #start inner function
        def paintCellThreaded(efficiency, cfm, gseo):
            gradient = QtGui.QLinearGradient(progress_origin, progress_end)
            gradient.setSpread(QtGui.QGradient.PadSpread)
            sub_rect = QtCore.QRect(sub_rect_topleft, sub_rect_bottomright)
            if efficiency <= 0.25:
                progress_bar_color = progress_bar_00_color
            elif 0.25 < efficiency <= 0.5:
                progress_bar_color = progress_bar_25_color
            elif 0.5 < efficiency <= 0.75:
                progress_bar_color = progress_bar_50_color
            elif 0.75< efficiency < 0.99: 
            #Fix this. The efficiency should not return 99.99999% even when the writers achieve target. 
                progress_bar_color = progress_bar_75_color
            elif 0.99 < efficiency <= 1.0:
                progress_bar_color = progress_bar_100_color
            else:
                progress_bar_color = progress_bar_101_color
            if efficiency > 1.0:
                efficiency = 1.0
            steps = [float(x)/100.00 for x in range(int(efficiency*100))]
            for x in steps:
                gradient.setColorAt(x, progress_bar_color)
            gradient.setColorAt(efficiency, white_color)
            gradient.setColorAt(1, white_color)
            painter.fillRect(sub_rect, gradient)
        self.counter +=1
        #if self.counter % 30 == 0:
        #    print "Repainting cells in weekcalendar. Counter: ", self.counter
        #end inner Function
        #Function main body.
        today_color = QtGui.QColor(237, 28, 36) #Red
        progress_bar_00_color = QtGui.QColor(255, 0, 0) #Red
        progress_bar_25_color = QtGui.QColor(237, 28, 36) #Red
        progress_bar_50_color = QtGui.QColor(240, 100, 15) #Orange
        progress_bar_75_color = QtGui.QColor(242, 190, 13) #Orange
        progress_bar_100_color = QtGui.QColor(50, 182, 122) #Green
        progress_bar_101_color = QtGui.QColor(0, 162, 232) #Blue
        #disabled_color = QtGui.QColor(227, 242, 237) #Greyed
        disabled_color = QtGui.QColor(192, 192, 192) #Greyed
        background_all_color = QtGui.QColor(192, 192, 192) #Greyed
        white_color = QtGui.QColor(255, 255, 255) #White
        selection_color = QtGui.QColor(0, 255, 255) #cyan
        leave_color = QtGui.QColor(96, 96, 96)
        #Coordinates of the rectangle.

        center_coords = rect.center()
        y_bottom = rect.bottom()
        y_top = rect.top()
        x_left = rect.left()
        x_right = rect.right()

        x_range = x_right - x_left
        y_range = y_top - y_bottom
        
        progress_origin = QtCore.QPoint(x_left, y_bottom)
        progress_end = QtCore.QPoint(x_right, (y_bottom+0.1*y_range))

        sub_rect_topleft = QtCore.QPoint(x_left, (y_bottom+0.1*y_range))
        sub_rect_bottomright = QtCore.QPoint(x_right, y_bottom)
        
        if date == datetime.date.today():
            painter.fillRect(rect, today_color)
        """Logic:
        Check if we're working on that date, then get the working status.
        Then, create a Porker to get efficiency.
        This shouldn't be a continuously running Porker.
        """
        if date == self.selectedDate():
            painter.fillRect(rect, selection_color)
        date_ = date.toPyDate()
        if date_ in self.datesData:
            #print "%s found!" % date_
            #print len(self.datesData)
            status = self.datesData[date_][0]
            relaxation = self.datesData[date_][1]
            efficiency = self.datesData[date_][2]
            cfm = self.datesData[date_][3]
            gseo = self.datesData[date_][4]
            if status == "Working":
                #status, relaxation = MOSES.getWorkingStatus(self.userID, self.password, date.toPyDate())
                if relaxation >= 0.0:
                    #efficiency = MOSES.getEfficiencyFor(self.userID, self.password, date.toPyDate()) 
                    paintCellThreaded(efficiency, cfm, gseo)
                elif relaxation > 0.0:
                    paintCellThreaded(efficiency, cfm, gseo)
                else:
                    painter.fillRect(rect, disabled_color)
            elif status == "Leave":
                painter.fillRect(rect, leave_color)

            elif status == "Holiday":
                painter.fillRect(rect, disabled_color)
        else:
            painter.fillRect(rect, disabled_color)
        painter.drawText(rect.center(), "%s" %date.toPyDate().day)
                #painter.fillRect(rect, QtGui.QColor(0, 0, 0, 90))
                    #self.setStyleSheet("background-color: linear-gradient(red 90%, white 10%);")
        #invoke the super paintCell method.
        
