from __future__ import division
import os
import sys
import math
import time
import glob
import datetime

from PyQt4 import QtGui, QtCore
from ImageButton import ImageButton

class SharinganButton(ImageButton):
    def __init__(self, *args, **kwargs):
        super(SharinganButton, self).__init__(*args, **kwargs)
        self.createUI()
        self.mapEvents()
    def createUI(self):
        self.show()
    def mapEvents(self):
        pass

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
            file_pairs.append([os.path.basename(x) for x in mangyeko_pair])

    return file_pairs

if __name__ == "__main__":
    print getSharinganFileLists()

