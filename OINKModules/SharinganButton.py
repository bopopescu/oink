from __future__ import division
import os
import sys
import math
import time
import glob
import datetime

from PyQt4 import QtGui, QtCore
from PIL import Image, ImageQt
import PIL

from ImageButton import ImageButton

class ThreadOfSixPaths(QtCore.QThread):
    updateImage = QtCore.pyqtSignal(ImageQt.ImageQt)
    def __init__(self):
        super(ThreadOfSixPaths, self).__init__()
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.delay = 5
        self.rotation_delay = 0.05
        self.active = True
        self.sharingan_file_lists = getSharinganFileLists()
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def run(self):
        while True:
            if self.active:
                for sharingan_list in self.sharingan_file_lists:
                    self.useImages(sharingan_list)
                    time.sleep(self.delay)
                    self.useImages(list(reversed(sharingan_list)))
                    time.sleep(self.delay)


    def useImages(self, sharingan_images_list):
        sweep = 360
        frames_per_delay = 10
        image_rotation_delay = self.rotation_delay
        forward_sweep_angle_steps = range(0, sweep, frames_per_delay)
        reversed_sweep_steps = list(reversed(forward_sweep_angle_steps))
        reversed_sweep_steps.extend(forward_sweep_angle_steps) #Pillow will rotate counterclockwise.
        sweep_steps = reversed_sweep_steps
        for sharingan_stage_image in sharingan_images_list:
            for i in sweep_steps:
                self.updateImage.emit(self.rotateImage(sharingan_stage_image, i))
                time.sleep(image_rotation_delay)

    def rotateImage(self, sharingan_stage_image, angle):
        image_object = Image.open(sharingan_stage_image).convert("RGBA").rotate(angle)
        return ImageQt.ImageQt(image_object)



class SharinganButton(ImageButton):
    def __init__(self, *args, **kwargs):
        super(SharinganButton, self).__init__(*args, **kwargs)
        self.ashura = ThreadOfSixPaths()
        self.ashura.updateImage.connect(self.updateImage)

    def updateImage(self, image_object):
        super(SharinganButton, self).updateImage(image_object)

def getSharinganFileLists():
    import os
    import glob
    path_to_folder = os.path.join(os.getcwd(),"Images","sharingan") if "OINKModules" not in os.getcwd() else os.path.join(os.getcwd(),"..","Images","sharingan")
    base_sharingan_file = os.path.join(path_to_folder,"sharingan_base.png")
    search_string = os.path.join(path_to_folder,"sharingan_mangyeko_*.png")
    mangyeko_file_list = glob.glob(search_string)
    file_pairs = []
    used_files = []
    for mangyeko_file in  mangyeko_file_list:
        if mangyeko_file not in used_files:
            mangyeko_pair = [base_sharingan_file, mangyeko_file]
            used_files.append(mangyeko_file)
            eternal_mangyeko_search_string = os.path.join(
                                                    path_to_folder,
                                                    os.path.splitext(os.path.basename(mangyeko_file))[0]+"_*.png")
            eternal_mangyeko_file_list = sorted(glob.glob(eternal_mangyeko_search_string))
            mangyeko_pair.extend(eternal_mangyeko_file_list)
            used_files.extend(eternal_mangyeko_file_list)
            file_pairs.append([x for x in mangyeko_pair])

    return file_pairs

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    sharingan_button = SharinganButton(os.path.join("..","Images","sharingan","uchiha_eye"),100,100)
    test_window = QtGui.QMainWindow()
    test_window.setCentralWidget(sharingan_button)
    test_window.show()
    sys.exit(app.exec_())


