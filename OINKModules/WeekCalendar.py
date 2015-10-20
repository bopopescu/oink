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
        holiday_color = QtGui.QColor(59,59,59) 
        #Coordinates of the rectangle.

        

        date_ = date.toPyDate()
        center_coords = rect.center()
        y_bottom = rect.bottom()
        y_top = rect.top()
        x_left = rect.left()
        x_right = rect.right()
        x_range = x_right - x_left
        y_range = y_top - y_bottom
        
        if date_ not in self.datesData:
            painter.fillRect(rect, disabled_color)
            #print date_, " is a disabled date."
        else:
            #print "%s found!" % date_
            #print len(self.datesData)
            status = self.datesData[date_][0]
            relaxation = self.datesData[date_][1]
            efficiency = self.datesData[date_][2]
            if len(self.datesData[date_])>3:
                cfm = self.datesData[date_][3]
                gseo = self.datesData[date_][4]
            else:
                cfm = None
                gseo = None
            #Start painting the cell.
            if date == datetime.date.today():
                cell_color = today_color
            elif date == self.selectedDate():
                cell_color = selection_color
            elif status == "Working":
                cell_color = white_color
            elif status == "Leave" or status == "Holiday":
                cell_color = holiday_color
            else:
                cell_color = disabled_color

            painter.fillRect(rect, cell_color)
            #if status == "Working":

            #Fill the efficiency bar
            if efficiency is None:
                progress_bar_color = cell_color
            elif efficiency <= 0.25:
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
            #Create a gradient across the progress bar section.
            #Calculate the origin and finish points for the progressbars.
            #For this, we need to use two points which go from the bottom left to the top right corner.
            progress_origin = QtCore.QPoint(x_left, y_bottom) 
            progress_end = QtCore.QPoint(x_right, (y_bottom+0.1*y_range))
            efficiency_gradient = QtGui.QLinearGradient(progress_origin, progress_end)
            efficiency_gradient.setSpread(QtGui.QGradient.PadSpread)
            steps = [float(x)/100.00 for x in range(int(efficiency*100))]
            for x in steps:
                efficiency_gradient.setColorAt(x, progress_bar_color)
            efficiency_gradient.setColorAt(efficiency, cell_color)
            efficiency_gradient.setColorAt(1, cell_color)
            #Create 
            efficiency_bar_rect_topleft = QtCore.QPoint(x_left, (y_bottom+0.1*y_range))
            efficiency_bar_rect_bottomright = QtCore.QPoint(x_right, y_bottom)
            efficiency_bar_rect = QtCore.QRect(efficiency_bar_rect_topleft, efficiency_bar_rect_bottomright)
            painter.fillRect(efficiency_bar_rect, efficiency_gradient)
            #Paint CFM and GSEO
            #CFM at (0.25x-0.30x, 0.3y)self.
            #GSEO at (0.70x-0.75x, 0.3y)
            color_red = QtGui.QColor(237, 28, 36)
            color_orange = QtGui.QColor(242, 190, 13)
            color_yellow = QtGui.QColor(255,255,0)
            color_green = QtGui.QColor(50, 182, 122)
            color_blue = QtGui.QColor(0, 162, 232)
            color_black = QtGui.QColor(0, 0, 0)

            if cfm is not None:
                if cfm == 0.0:
                    cfm_color = color_black
                elif cfm < 0.95:
                    cfm_color = color_red
                elif 0.95<= cfm <1.00:
                    cfm_color = color_green
                else:
                    cfm_color = color_blue

                cfm_marker_left = (x_left+0.20*x_range)
                cfm_marker_right = (x_left+0.30*x_range)
                cfm_marker_top = (y_bottom+0.30*y_range)
                cfm_marker_bottom = (y_bottom+0.20*y_range)
                cfm_marker_topright = QtCore.QPoint(cfm_marker_right, cfm_marker_top)
                cfm_marker_bottomleft = QtCore.QPoint(cfm_marker_left, cfm_marker_bottom)
                cfm_marker_topleft = QtCore.QPoint(cfm_marker_left, cfm_marker_top)
                cfm_marker_bottomright = QtCore.QPoint(cfm_marker_right,cfm_marker_bottom)
                cfm_gradient = QtGui.QLinearGradient(cfm_marker_bottomleft, cfm_marker_topright)
                cfm_gradient.setSpread(QtGui.QGradient.PadSpread)
                cfm_gradient.setColorAt(0, cfm_color)
                cfm_gradient.setColorAt(1, cfm_color)
                cfm_marker_rect = QtCore.QRect(cfm_marker_topleft, cfm_marker_bottomright)
                painter.fillRect(cfm_marker_rect, cfm_gradient)
            
            if gseo is not None:
                if gseo == 0.0:
                    gseo_color = color_black
                elif 0 < gseo < 1.0:
                    gseo_color = color_red
                else:
                    gseo_color = color_blue

                gseo_marker_left = (x_left+0.70*x_range)
                gseo_marker_right = (x_left+0.80*x_range)
                gseo_marker_top = (y_bottom+0.30*y_range)
                gseo_marker_bottom = (y_bottom+0.20*y_range)
                gseo_marker_topright = QtCore.QPoint(gseo_marker_right, gseo_marker_top)
                gseo_marker_bottomleft = QtCore.QPoint(gseo_marker_left, gseo_marker_bottom)
                gseo_marker_topleft = QtCore.QPoint(gseo_marker_left, gseo_marker_top)
                gseo_marker_bottomright = QtCore.QPoint(gseo_marker_right,gseo_marker_bottom)
                gseo_gradient = QtGui.QLinearGradient(gseo_marker_bottomleft, gseo_marker_topright)
                gseo_gradient.setSpread(QtGui.QGradient.PadSpread)
                gseo_gradient.setColorAt(0, gseo_color)
                gseo_gradient.setColorAt(1, gseo_color)
                gseo_marker_rect = QtCore.QRect(gseo_marker_topleft, gseo_marker_bottomright)
                painter.fillRect(gseo_marker_rect, gseo_gradient)
        #Finally, paint the date over the cell.
        painter.drawText(QtCore.QPoint((x_left+x_range*0.4), (y_bottom + y_range*0.5)), "%s" %date.toPyDate().day)
        
