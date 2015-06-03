import sys
import os
import random
import datetime
import numpy as np
from PyQt4 import QtGui, QtCore
import pandas as pd
from matplotlib.backends import qt4_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import MOSES
import Graphinator
import FileDialog

class GraphiteCanvas(FigureCanvasQTAgg):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.).
    Use this like any QWidget, always subclass it and when you need to plot something, then just override the 
    compute_initial_figure method.
    Also, pass a QWidget to it. Wtf is going on here?
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class Graphite(QtGui.QWidget):
    def __init__(self, user_id, password):
        super(Graphite, self).__init__()
        self.user_id, self.password = user_id, password
        self.createUI()
        self.createEvents()

    def createUI(self):
        self.graph_combobox_label = QtGui.QLabel("Select Graph:")
        self.graph_combobox = QtGui.QComboBox()
        self.graph_combobox.addItems(["Team Efficiency", "Team Quality", "Quality Trend"])
        self.refresh_button = QtGui.QPushButton("Refresh")
        self.graphite_canvas = GraphiteCanvas()
        self.graphite_canvas.setMinimumWidth(600)
        self.graphite_canvas.setMinimumHeight(400)
        self.progress_bar = QtGui.QProgressBar()
        progressbar_style = """
            .QProgressBar {
                 border: 1px solid black;
                 border-radius: 2px;
                 text-align: center;
             }
            .QProgressBar::chunk {
                 background-color: #05B8CC;
                 width: 20px;
             }"""
        self.progress_bar.setStyleSheet(progressbar_style)
        self.progress_bar.setFormat("Nothing's happening yet")
        self.progress_message = QtGui.QLabel("Your text here.")

        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.graph_combobox_label, 0, 0, 1, 1)
        self.layout.addWidget(self.graph_combobox, 0, 1, 1, 1)
        self.layout.addWidget(self.refresh_button, 0 , 2, 1, 2)
        self.layout.addWidget(self.graphite_canvas, 1, 0, 4, 4)
        self.layout.addWidget(self.progress_bar, 5, 0, 1, 4)
        self.layout.addWidget(self.progress_message, 6, 0, 1, 4)
        self.setLayout(self.layout)
        self.resize(600, 400)
        self.show()
        self.setWindowTitle("Graphite")

    def createEvents(self):
        self.refresh_button.clicked.connect(self.redraw)
        #self.graphinator_thread.gotEfficiencyThread.connect(self.plotEfficiency)

    def redraw(self):
        graph_type = self.graph_combobox.currentText()
        print "Plotting %s graph." %graph_type
        query_date = datetime.date(2015,5,29)
        data_set = Graphinator.getEfficiencyData(query_date)
        #print data_set
        #first plot the efficiency
        data_set.sort(["Efficiency", "Status"],ascending=[0,0],inplace = True)
        #data_set.sort(["Status"],ascending=[0],inplace = True)

        efficiency_writers_order = list(data_set["Employee Name"])
        efficiency_list = list(data_set["Efficiency"])
        efficiency_colors = list(data_set["Efficiency Color"])
        efficiency_width = 0.5
        data_length = len(data_set.index)
        positions = np.arange(data_length)+0.5

        #start plotting
        self.graphite_canvas.axes.set_xlabel("Writers")
        self.graphite_canvas.axes.set_ylabel("Efficiency")
        #print efficiency_writers_order, efficiency_list, efficiency_colors
        for counter in range(data_length):
            bar_set = self.graphite_canvas.axes.bar(positions[counter], efficiency_list[counter], width=efficiency_width, color = efficiency_colors[counter])
        self.graphite_canvas.axes.grid(True, lw=0.5, ls="--", c="0.05")
        self.graphite_canvas.axes.set_title("Efficiency Graph For %s" % query_date)
        ax = self.graphite_canvas.axes
        ax.xaxis.set_major_locator(ticker.FixedLocator(positions))
        ax.xaxis.set_major_formatter(ticker.FixedFormatter((efficiency_writers_order)))
        y_axis_tickers = np.arange(40)*2.5
        
        self.graphite_canvas.axes.set_yticks(np.arange(min(efficiency_list), max(efficiency_list)+1, max(efficiency_list)/20))
        labels = self.graphite_canvas.axes.get_xticklabels()
        #self.graphite_canvas.fig.setp(labels, rotation = 90.0)
        #self.graphite_canvas.axes.subplots_adjust(bottom=0.2)
        self.graphite_canvas.axes.set_ylim(min(efficiency_list))
        self.graphite_canvas.draw()

        #file_name = "Efficiency_Graph_%d%d%d.png" %(query_date.year,query_date.month, query_date.day)
        #self.graphite_canvas.axes.savefig(file_name, dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    user_id, password = MOSES.getBigbrotherCredentials()
    graphite = Graphite(user_id, password)
    sys.exit(app.exec_())
