from PyQt4 import QtGui, QtCore
import os, datetime
class DailyGraphView(QtGui.QWidget):
    def __init__(self,graph_date=None):
        super(DailyGraphView, self).__init__()
        if graph_date is None:
            self.enable_plotting = False
            self.enable_plotting = True
            self.graph_date = datetime.date.today()
        else:
            self.enable_plotting = True
            self.graph_date = graph_date
        self.createUI()
        self.refresh_graphs.clicked.connect(self.plotGraph)

    def createUI(self):
        self.refresh_graphs = QtGui.QPushButton("Refresh Graphs")
        self.eff_graph = QtGui.QLabel("")
        self.eff_graph.setMinimumSize(400, 300)
        self.eff_graph.setMaximumSize(400, 300)
        self.quality_graph = QtGui.QLabel("")
        self.quality_graph.setMinimumSize(400, 300)
        self.quality_graph.setMaximumSize(400, 300)
        self.hist_quality_graph = QtGui.QLabel("")
        self.hist_quality_graph.setMinimumSize(400, 300)
        self.hist_quality_graph.setMaximumSize(400, 300)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.refresh_graphs,0)
        self.graphs_layout = QtGui.QHBoxLayout()
        self.graphs_layout.addWidget(self.eff_graph)
        self.graphs_layout.addWidget(self.quality_graph)  
        self.graphs_layout.addWidget(self.hist_quality_graph)
        self.layout.addLayout(self.graphs_layout,3)
        self.setLayout(self.layout)
        self.setWindowTitle("Daily Graphs")
        self.plotGraph()

    def plotGraph(self):
        if self.enable_plotting:
            paths = self.getGraphNames()
            eff_image = QtGui.QImage(paths[0])
            quality_image = QtGui.QImage(paths[1])
            hist_quality_image = QtGui.QImage(paths[2])
            eff_pp = QtGui.QPixmap.fromImage(eff_image)
            quality_pp = QtGui.QPixmap.fromImage(quality_image)
            hist_quality_pp = QtGui.QPixmap.fromImage(hist_quality_image)
            
            self.eff_graph.setPixmap(eff_pp.scaled(
                    self.eff_graph.size(),
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation))

            self.quality_graph.setPixmap(quality_pp.scaled(
                    self.quality_graph.size(),
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation))

            self.hist_quality_graph.setPixmap(hist_quality_pp.scaled(
                    self.hist_quality_graph.size(),
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation))
    
    def getGraphNames(self):
        eff_path = datetime.datetime.strftime(self.graph_date,"%Y%m%d")+"_Efficiency_Graph.png"
        quality_path = datetime.datetime.strftime(self.graph_date,"%Y%m%d")+ "_CFM_GSEO_Graph.png"
        hist_quality_path = datetime.datetime.strftime(self.graph_date,"%Y%m%d")+"_HistoricalQuality_Graph.png"
        return eff_path, quality_path, hist_quality_path

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([])
    im = DailyGraphView()
    im.show()
    sys.exit(app.exec_())
