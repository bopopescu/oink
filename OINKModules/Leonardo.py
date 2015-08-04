from __future__ import division
import os, sys, datetime, subprocess, glob, ntpath
from PyQt4 import QtGui, QtCore
import PIL
from PIL import Image

class DaVinci(QtCore.QThread):
    sendProgress = QtCore.pyqtSignal(str, int, bool, datetime.datetime)
    sendImageList = QtCore.pyqtSignal(list)
    def __init__(self):
        super(DaVinci,self).__init__()
        self.allow_run = False
        self.input_images = []
        self.watermark = None
        self.correct_color = True
        self.save_path = None
        self.resize_mode = None #use "Width","Height" or "Smart Detect" here.
        self.water_mark_position = [2,2] #Default setting, top right corner.
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def __del__(self):
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def run(self):
        while True:
            if self.allow_run:
                #do things.
                watermark_image = Image.open(self.watermark) # open watermark.
                total = len(self.input_images)
                counter = 0
                for image_path in self.input_images:
                    self.putWaterMarkAndSave(image_path, watermark_image)
                    counter += 1
                    image_name = os.path.basename(image_path)
                    eta = self.getETA(start_time, counter, total)
                    self.sendProgress("Working on %s."%image_name, int(counter/total),False, eta)
                self.sendProgress("Completed.", int(counter/total),True, eta)

    def getETA(self, start_time, counter, total):
        now = datetime.datetime.now()
        time_spent = now - start_time
        mean_time = time_spent.total_seconds()/counter
        ETA = start_time + datetime.timedelta(seconds=(mean_time*total))
        return ETA

    def putWaterMarkAndSave(self,image_path, watermark_image):
        """Takes 1 image and exports as required."""
        image_name = ntpath.basename(image_path)
        if self.correct_color:
            image_handler = Image.open(image_path).convert("RGBA")
        else:
            image_handler = Image.open(image_path)
        if self.resize_mode == "Width":
            watermark_size = ()
        elif self.resize_mode == "Length":
            watermark_size = ()
        elif self.resize_mode == "Smart Detect":
            watermark_size = ()
        resized_watermark =          


class Leonardo(QtGui.QMainWindow):
    """Image batch processing tool. V1 supports watermarking."""
    def __init__(self):
        super(Leonardo, self).__init__()
        self.input_location = os.getcwd()
        self.output_location = os.path.join(os.getcwd(),"output")
        self.watermark = os.path.join(os.getcwd(),"watermark.png")
        self.createUI()
        self.mapEvents()
        self.move(250,100)
        self.clip = QtGui.QApplication.clipboard()

    def createUI(self):
        self.input_location_instruction_label = QtGui.QLabel("Select the input location:")
        self.input_location_box = QtGui.QLineEdit()
        self.input_location_box.setToolTip("The chosen input folder location is displayed here.")
        self.input_location_box.setMinimumWidth(120)
        self.input_location_box.setReadOnly(True)
        self.input_location_box.setText(self.input_location)
        self.input_location_change_button = QtGui.QPushButton("...")
        self.input_location_change_button.setMinimumWidth(22)
        self.input_location_change_button.setMaximumWidth(22)
        self.input_location_change_button.setToolTip("Click this button to select a new input location.")
        self.open_input_location_button = QtGui.QPushButton("Open")
        self.open_input_location_button.setMinimumWidth(40)
        self.open_input_location_button.setMaximumWidth(40)
        self.open_input_location_button.setToolTip("Click to open the input folder.")

        input_location_widgets = QtGui.QHBoxLayout()
        input_location_widgets.addWidget(self.input_location_box,2)
        input_location_widgets.addWidget(self.input_location_change_button,0)
        input_location_widgets.addWidget(self.open_input_location_button,0)

        self.output_location_instruction_label = QtGui.QLabel("Select output directory or parameters:")
        self.output_location_check_box = QtGui.QCheckBox("Overwrite all files")
        self.output_location_check_box.setToolTip("Check this box to force overwrite the input files.")
        self.output_location_box = QtGui.QLineEdit()
        self.output_location_box.setMinimumWidth(120)
        self.output_location_box.setToolTip("Output folder location is displayed here.")
        self.output_location_box.setReadOnly(True)
        self.output_location_box.setText(self.output_location)
        self.output_location_change_button = QtGui.QPushButton("...")
        self.output_location_change_button.setToolTip("Click to change output location")
        self.output_location_change_button.setMinimumWidth(22)
        self.output_location_change_button.setMaximumWidth(22)
        self.open_output_location_button = QtGui.QPushButton("Open")
        self.open_output_location_button.setToolTip("Click to open the output folder.")
        self.open_output_location_button.setMinimumWidth(40)
        self.open_output_location_button.setMaximumWidth(40)

        output_location_widgets = QtGui.QHBoxLayout()
        output_location_widgets.addWidget(self.output_location_box,2)
        output_location_widgets.addWidget(self.output_location_change_button,0)
        output_location_widgets.addWidget(self.open_output_location_button,0)

        self.water_mark_instruction_label = QtGui.QLabel("Select a watermark image")
        self.water_mark_image_box = QtGui.QLineEdit()
        self.water_mark_image_box.setMinimumWidth(120)
        self.water_mark_image_box.setReadOnly(True)
        self.water_mark_image_box.setText(self.watermark)
        self.water_mark_image_box.setToolTip("The selected watermark image location is displayed here.")
        self.water_mark_change_button = QtGui.QPushButton("...")
        self.water_mark_change_button.setMinimumWidth(22)
        self.water_mark_change_button.setMaximumWidth(22)
        self.water_mark_change_button.setToolTip("Click to select a new watermark image.")
        self.open_water_mark_image = QtGui.QPushButton("Open")
        self.open_water_mark_image.setMinimumWidth(40)
        self.open_water_mark_image.setMaximumWidth(40)
        self.open_water_mark_image.setToolTip("Click to view the selected watermark image.")
        watermark_location_widgets = QtGui.QHBoxLayout()
        watermark_location_widgets.addWidget(self.water_mark_image_box)
        watermark_location_widgets.addWidget(self.water_mark_change_button)
        watermark_location_widgets.addWidget(self.open_water_mark_image)

        self.water_mark_convert_to_rgba = QtGui.QCheckBox("Keep watermark color.")
        self.water_mark_convert_to_rgba.setChecked(True)
        self.water_mark_convert_to_rgba.setToolTip("Click here to ensure that the watermark is always in color.")
        self.water_mark_aspect_ratio = QtGui.QCheckBox("Auto-resize watermark image based on: ")
        self.water_mark_aspect_ratio.setToolTip("Check this to resize the watermark image based on the image parameters")
        self.water_mark_aspect_ratio.setChecked(True)
        self.water_mark_aspect_ratio_constraint = QtGui.QComboBox()
        self.water_mark_aspect_ratio_constraint.setToolTip("Select the constraint parameter for by which to resize the watermark.")
        self.water_mark_aspect_ratio_constraint.addItems(["Width","Height","Smart Detect"])

        self.water_mark_positions = []
        vpos = {0: "Top", 1:"Middle", 2:"Bottom"}
        hpos = {0: "Left", 1:"Center", 2:"Right"}
        for i in range(3):
            self.water_mark_positions.append([QtGui.QRadioButton() for j in range(3)])
        #print self.water_mark_positions

        self.water_mark_radio_group = QtGui.QButtonGroup()
        for i in range(3):
            for j in range(3):
                self.water_mark_radio_group.addButton(self.water_mark_positions[i][j])
                self.water_mark_positions[i][j].setToolTip("This sets the position of the watermark to the %s %s of the image." %(vpos[i],hpos[j]))
        self.water_mark_radio_group.setExclusive(True)
        self.water_mark_positions[0][2].setChecked(True)
        
        self.water_mark_position_layout = QtGui.QGridLayout()
        for i in range(3):
            for j in range(3):
                self.water_mark_position_layout.addWidget(self.water_mark_positions[i][j],i,j,1,1,QtCore.Qt.AlignHCenter)
        self.water_mark_position_selector = QtGui.QGroupBox("Watermark Position:")
        self.water_mark_position_selector.setLayout(self.water_mark_position_layout)
                

        self.preview_image_button = QtGui.QPushButton("Update Preview Image")
        self.preview_image_button.setToolTip("Click here to view a preview of the output by performing the operation on a random image from your list.")
        self.run_button = QtGui.QPushButton("Run")
        self.run_button.setMinimumSize(100,50)
        self.run_button.setToolTip("Click here after setting all the input options to begin batch processing.")
        main_button_style = """
            .QPushButton {
                font: bold 14pt;
            }
            .QPushButton:hover {
                font: bold 18pt;
            }"""
        self.run_button.setStyleSheet(main_button_style)
        
        self.inputs_layout = QtGui.QVBoxLayout()

        self.inputs_layout.addWidget(self.input_location_instruction_label,0)
        self.inputs_layout.addLayout(input_location_widgets,0)
        
        self.inputs_layout.addWidget(self.output_location_instruction_label,0)
        self.inputs_layout.addWidget(self.output_location_check_box,0)
        self.inputs_layout.addLayout(output_location_widgets,0)

        self.inputs_layout.addWidget(self.water_mark_instruction_label,0)
        self.inputs_layout.addLayout(watermark_location_widgets,0)
        self.inputs_layout.addWidget(self.water_mark_convert_to_rgba,0)
        self.inputs_layout.addWidget(self.water_mark_aspect_ratio,0)
        self.inputs_layout.addWidget(self.water_mark_aspect_ratio_constraint,0)
        self.inputs_layout.addWidget(self.water_mark_position_selector,1)
        self.inputs_layout.addWidget(self.preview_image_button,0)
        self.inputs_layout.addWidget(self.run_button,0)
        
        self.inputs = QtGui.QGroupBox("Inputs:")
        self.inputs.setLayout(self.inputs_layout)

        self.preview_image = QtGui.QLabel("")
        self.preview_image.setToolTip("The preview image will be displayed here.")
        self.preview_image.setMinimumSize(400,400)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.inputs,0)
        self.layout.addWidget(self.preview_image,2)
        
        self.main_widget = QtGui.QWidget()
        self.main_widget.setLayout(self.layout)
        self.show()
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Leonardo: The Vinci of Flipkart")

    def mapEvents(self):
        for i in range(3):
            for j in range(3):
                self.water_mark_positions[i][j].toggled.connect(self.getPosition)
        self.input_location_change_button.clicked.connect(self.setInputFolder)
        self.output_location_change_button.clicked.connect(self.setOutputFolder)
        self.water_mark_change_button.clicked.connect(self.setWatermark)
        self.open_input_location_button.clicked.connect(self.openInputFolder)
        self.open_output_location_button.clicked.connect(self.openOutputFolder)
        self.open_water_mark_image.clicked.connect(self.openWaterMarkImage)

    def alertMessage(self, title, message):
        """Vindaloo."""
        QtGui.QMessageBox.about(self, title, message)

    def getPosition(self):
        for i in range(3):
            for j in range(3):
                if self.water_mark_positions[i][j].isChecked():
                    print "Selected Position is (%d,%d)" %(i,j)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def setInputFolder(self):
        self.input_location = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Input Files Directory"))
        self.input_location_box.setText(self.input_location)
    
    def setOutputFolder(self):
        self.output_location = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Output Files Directory"))
        self.output_location_box.setText(self.output_location)
    
    def setWatermark(self):
        self.watermark = str(QtGui.QFileDialog.getOpenFileName(self,"Select Watermark Image",os.getcwd()))
        self.water_mark_image_box.setText(self.watermark)

    def openInputFolder(self):
        subprocess.Popen(r'explorer /open,"%s"'%os.path.join(self.input_location,""))
        print self.getInputImagesList()
    
    def openOutputFolder(self):
        if not(os.path.exists(self.output_location)):
            os.makedirs(self.output_location)
        subprocess.Popen(r'explorer /open,"%s"'%os.path.join(self.output_location,""))

    def openWaterMarkImage(self):
        print self.watermark

    def getInputImagesList(self):
        format_types = ["*.jpeg", "*.png", "*.jpg"]
        input_images = []
        for format in format_types:
            input_images += glob.glob(os.path.join(self.input_location, format))
        return input_images

def main():
    app = QtGui.QApplication(sys.argv)
    leonardo = Leonardo()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()