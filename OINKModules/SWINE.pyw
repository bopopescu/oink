from __future__ import division
import sys, os, csv, datetime, subprocess, urllib, urllib2, socket, httplib

from PIL import Image, ImageQt
from PyQt4 import QtGui, QtCore
from bs4 import BeautifulSoup

class SwineThread(QtCore.QThread):
    sendStatus = QtCore.pyqtSignal(str,int,bool,datetime.datetime)
    #Sends a message, rough integer percentage value, boolean completion status, and the ETA\time of completion.
    sendData = QtCore.pyqtSignal(dict)
    sendException = QtCore.pyqtSignal(str)
    def __init__(self):
        super(SwineThread, self).__init__()
        self.get_images = False
        self.image_save_location = None
        self.get_all_images = False
        self.image_name_mask = ["FSN"]
        self.use_subfolders = False
        self.image_name_mask_delimiter = "(None)"
        self.get_data = False
        self.required_data = []
        self.allow_run = False
        self.fsn_list = []
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
                processed_fsns = []
                total = len(self.fsn_list)
                counter = 0
                start_time = datetime.datetime.now()
                return_data_set_keys = ["WS Name", "Brand"]
                if self.get_images:
                    return_data_set_keys += ["Image"]
                if self.get_data:
                    return_data_set_keys += self.required_data
                self.return_data_set = {}
                for fsn in self.fsn_list:
                    self.return_data_set.update({fsn:dict(zip(return_data_set_keys, [None for each_value in return_data_set_keys]))})
                for fsn in self.fsn_list:
                    if fsn not in processed_fsns:
                        self.fsn = fsn
                        counter += 1
                        status_message = "Beginning to process %d of %d fsns. Current FSN: %s." %(counter, total, fsn)
                        process_percentage = int(counter/total*100)
                        completion_state = False
                        eta = self.getETA(start_time, counter, total)
                        self.sendStatus.emit(status_message,process_percentage,completion_state,eta)
                        fsn_soup, soup_success = self.getSoupFromFSN(fsn)
                        if soup_success:
                            #print "Succeeded fetching page for %s." %fsn
                            processed_fsns.append(fsn)
                            send_data = False
                            self.return_data_set[fsn]["WS Name"] = self.getWSNameFromSoup(fsn_soup)
                            self.return_data_set[fsn]["Brand"] = self.return_data_set[fsn]["WS Name"][:self.return_data_set[fsn]["WS Name"].find(" ")]

                            if self.get_images:
                                status_message = "Fetching images for %d of %d fsns." %(counter, total)
                                self.sendStatus.emit(status_message,process_percentage,completion_state,eta)
                                image_success = self.extractImages(fsn_soup)
                                self.return_data_set[fsn]["Image"] = "Successfully Extracted Image(s)."
                                status_message = "Finished fetching images for %d of %d fsns." %(counter, total)
                                eta = self.getETA(start_time, counter, total)
                                self.sendStatus.emit(status_message,process_percentage,completion_state,eta)
                                send_data = True

                            if self.get_data:
                                status_message = "Fetching selected data for %d of %d fsns." %(counter, total)
                                self.extractData(fsn_soup)
                                status_message = "Finished fetching selected data for %d of %d fsns." %(counter, total)
                                eta = self.getETA(start_time, counter, total)
                                self.sendStatus.emit(status_message,process_percentage,completion_state,eta)
                                send_data = True
                            if send_data:
                                self.sendData.emit(self.return_data_set)
                        else:
                            print "Failed fetching page for %s." %fsn
                if len(processed_fsns) == len(self.fsn_list):
                    self.allow_run = False
                    status_message = "Completed"
                    process_percentage = 100
                    completion_state = True
                    eta = datetime.datetime.now()
                    self.sendStatus.emit(status_message,process_percentage,completion_state,eta)

    def getSoupFromFSN(self,fsn):
        """Improve this method at a later stage."""
        url = "http://www.flipkart.com/search?q=" + fsn
        while True:
            try:
                html = urllib2.urlopen(url, timeout=120)
                break
            except urllib2.HTTPError:
                error = "Server response error for %s. Retrying" %fsn
                self.sendException.emit(error)
                continue
            except socket.error:
                error = "Socket error for %s. Retrying" %fsn
                self.sendException.emit(error)
                continue
            except httplib.BadStatusLine:
                error = "Bad status line error for %s. Retrying" %fsn
                self.sendException.emit(error)
                continue

        soup = BeautifulSoup(html)
        try:
            item_id = self.getItemIDFromHTML(html)
            success = True
        except:
            success = False
            pass

        if item_id is None:
            success = False
        return soup, success
    
    def getItemIDFromHTML(self, html_object):
        """Takes an urllib2 html object, gets the current url from geturl and then extracts the item id."""
        upload_link = html_object.geturl()
        item_id_prefix_position = upload_link.find(r"/p/")
        if item_id_prefix_position > -1:
            item_id_start_position = item_id_prefix_position + len(r"/p/")
            item_id_length = 16
            item_id_end_position = item_id_start_position + item_id_length
            item_id = upload_link[item_id_start_position: item_id_end_position]
        else:
            item_id = None
        return item_id

    def getWSNameFromSoup(self, soup_object):
        ws_name_tag = soup_object.find_all("h1",{"class":"title","itemprop":"name"})
        return str(ws_name_tag[0].string).strip()
    
    def extractImages(self, soup_object):
        """"""
        success = True
        image_urls = []
        #First, get the current productImage
        image_tag = soup_object.findAll("img", {"class":"productImage  current"})
        #print image_tag
        image_counter = 1
        image_counter += 1 
        image_attributes = image_tag[0].attrs
        try:
            image_url = image_attributes["data-zoomimage"]
        except:
            error = "Product page doesn't have zoomed-in image. Extracting original from thumbnail."
            self.sendException.emit(error)
            image_url = image_attributes["data-src"]
            image_url = image_url.replace("400x400","original")
        image_urls.append(image_url)

        #Next, get the remaining productImages.
        image_tags = soup_object.findAll("img", {"class":"productImage "})
        for image_tag in image_tags:
            image_attributes = image_tag.attrs
            try:
                image_url = image_attributes["data-zoomimage"]
            except:
                error = "Product page doesn't have zoomed-in image. Extracting original from thumbnail."
                self.sendException.emit(error)
                image_url = image_attributes["data-src"]
                image_url = image_url.replace("400x400","original")
            image_urls.append(image_url)
        
        #print len(image_urls)
        #raw_input(">")
        image_name =""
        counter = 0
        #print self.image_name_mask
        if self.image_name_mask_delimiter == "(None)":
            delimiter = ""
        elif self.image_name_mask_delimiter == "(Space)":
            delimiter = " "
        else:
            delimiter = self.image_name_mask_delimiter
        for mask in self.image_name_mask:
            if counter > 0:
                image_name += delimiter
            if mask == "FSN":
                image_name += self.fsn
            else:
                image_name += self.return_data_set[self.fsn][mask]
            counter += 1
        image_extension = ".jpeg"
        if self.use_subfolders:
            if self.image_name_mask[0] == "FSN":
                sub_folder_name = self.fsn
            else:
                sub_folder_name = self.return_data_set[self.fsn][self.image_name_mask[0]]
            current_save_location = os.path.join(self.image_save_location,sub_folder_name)
        else:
            current_save_location = self.image_save_location
        if not(os.path.exists(current_save_location)):
            os.makedirs(current_save_location)
        image_save_name = os.path.join(current_save_location,image_name)
        image_counter = 0
        if self.get_all_images:
            """"""
            required_images = image_urls
        else:
            required_images = image_urls[:1]
        for image_url in required_images:
            image_counter += 1
            trial_counter = 0
            while True:
                try:
                    trial_counter += 1
                    if self.get_all_images:
                        image_save_final_name = image_save_name + delimiter + "%2d"%image_counter + image_extension
                    else:
                        image_save_final_name = image_save_name + image_extension
                    urllib.urlretrieve(image_url, image_save_final_name)
                    if int(os.stat(image_save_final_name).st_size)>1000:
                        break
                    else:
                        error = "Extracted image is less than 1kb. Retrying again."
                        self.sendException.emit(error)
                        if trial_counter < 10:
                            continue
                        else:
                            error = "No image available, or obtained image is too small."
                            self.sendException.emit(error)
                            success = False
                            break
                except urllib.ContentTooShortError:
                    #print "Retrying image fetch for %s." %image_name
                    error = "Failed retrieving the image. Retrying."
                    self.sendException.emit(error)
                    continue
        return success

    def extractData(self, soup_object):
        """"""
        #find the section in this thing.
        spec_section_area = soup_object.find(class_ = "productSpecs specSection")
        #get model name
        specTables = spec_section_area.find_all(class_ = "specTable")
        groupHeads_list = []
        specsKeys_list = []
        specsValues_list = []
        empty_counter = 0
        specifications = {}
        counter = 1
        last_found_entity = None
        last_found_string_value = None
        current_group_head = None
        for specTable in specTables:
            #Stupid Failkart tables aren't formatted properly. There will be more than one "spectable", 
            #and what's more, each row may or may not have a header cell. I need to circumvent all this
            #or I need to rewrite this for the Console. Eventually, that'll be the best method.

            #step 1: loop through each row.
            spec_table_rows = specTable.find_all("tr")
            #step 2: loop through each of these rows.
            for spec_row in spec_table_rows:
                #step 3: determine what that row has: a groupHead, a specKey or specValue.
                for spec_subrow in spec_row:
                    try:
                        current_class = str(spec_subrow["class"][0])
                        current_string_value = str(spec_subrow.string).strip()
                        if counter >1:
                            if (last_found_entity == "specsKey") and (current_class == "specsValue"):
                                if (len(last_found_string_value) > 0) and (last_found_string_value != ""):
                                    specifications[last_found_string_value] = current_string_value
                                else:
                                    specifications[current_group_head] = current_string_value
                            elif (last_found_string_value == "groupHead") and (current_class == "specsValue"):
                                specifications[last_found_string_value] = current_string_value
                            elif (last_found_string_value == "specsKey") and ((current_class == "groupHead") or (current_class == "specsKey")):
                                specifications[last_found_string_value] = None
                            elif current_class == "groupHead":
                                current_group_head = str(spec_subrow.string).strip()
                        last_found_entity = current_class
                        last_found_string_value = str(spec_subrow.string).strip()
                        counter += 1
                    except TypeError:
                        pass
        for column in self.required_data:
            if column in specifications.keys():
                self.return_data_set[self.fsn][column]=specifications[column]
            elif column not in ["WS Name","Brand","Image"]:
                #print self.return_data_set[self.fsn]
                self.return_data_set[self.fsn][column]="NA"

    def getETA(self, start_time, counter, total):
        now = datetime.datetime.now()
        time_spent = now - start_time
        mean_time = time_spent.total_seconds()/counter
        ETA = start_time + datetime.timedelta(seconds=(mean_time*total))
        return ETA


class Swine(QtGui.QMainWindow):
    def __init__(self):
        super(Swine, self).__init__()
        self.swine_thread = SwineThread()
        self.clip = QtGui.QApplication.clipboard()
        self.createUI()
        self.mapEvents()

    def createUI(self):
        self.instruction_label = QtGui.QLabel("<b>Paste FSNs in the dialog below:</b>")
        self.fsn_list_text_edit = QtGui.QTextEdit()
        self.fsn_list_text_edit.setToolTip("Paste a list of FSNs here, separated either by a new line or by a comma.")
        self.log = QtGui.QTextEdit()
        self.log.setReadOnly(False)
        self.log.setToolTip("Action log.")
        self.get_images_check_box = QtGui.QCheckBox("Download Images")
        self.get_images_check_box.setToolTip("Check this if you'd like to download images.")
        self.images_types_box = QtGui.QCheckBox("Download All Product Images")
        self.images_types_box.setToolTip("Check this if you'd like to extract all product images and not just the current image.")
        self.images_types_box.setEnabled(False)
        self.get_data_dump_check_box = QtGui.QCheckBox("Download Spec Table Data")
        self.get_data_dump_types_box = QtGui.QTextEdit()
        self.get_data_dump_types_box.setToolTip("Enter the exact name of the attribute that you'd find on a product page.\nSeparate by a semi-colon(;), no spaces required.")
        self.get_data_dump_types_box.setEnabled(False)
        self.pull_button = QtGui.QPushButton("Run")
        self.pull_button.setToolTip("Click to extract data.")
        self.progress_bar = QtGui.QProgressBar()
        self.status_label = QtGui.QLabel("Status")
        self.process_table = QtGui.QTableWidget(0,0)
        style_string = """
        .QTableWidget {
            gridline-color: rgb(0, 0, 0);
        }
        """
        self.process_table.setStyleSheet(style_string)
        self.setStyleSheet(style_string)
        self.tabs = QtGui.QTabWidget()
        self.tabs.addTab(self.process_table,"Tabulated Data")
        self.tabs.addTab(self.log,"Log")
        self.tabs.setMinimumWidth(500)
        self.tabs.setMinimumHeight(500)
        self.data_dump_instruction = QtGui.QLabel("Paste the details to extract")
        self.images_name_masks = QtGui.QHBoxLayout()
        self.image_mask_instruction = QtGui.QLabel("Select Image Rename Pattern")
        self.image_masks = [QtGui.QComboBox() for i in range(3)]
        self.joiner_mask_instruction = QtGui.QLabel("Join masks by:")
        self.joiner_mask = QtGui.QComboBox()
        self.joiner_mask.addItems(["(Space)","-","_","(Null)"])
        self.joiner_mask.setEnabled(False)
        self.joiner = QtGui.QHBoxLayout()
        self.joiner.addWidget(self.joiner_mask_instruction,0)
        self.joiner.addWidget(self.joiner_mask,0)
        self.image_mask_options = ["FSN","WS Name","Brand"]
        for image_mask in self.image_masks:
            self.images_name_masks.addWidget(image_mask,0)
            image_mask.setEnabled(False)
            image_mask.addItems(self.image_mask_options)
            image_mask.setCurrentIndex(-1)
        self.reset_masks = QtGui.QPushButton("Reset Name Pattern")
        self.reset_masks.setToolTip("Reset the renaming guidelines.")
        self.reset_masks.setEnabled(False)
        self.images_name_masks.addWidget(self.reset_masks,0)
        self.output_location_line_edit = QtGui.QLineEdit()
        self.output_path = os.path.join(os.getcwd(),"output")
        self.output_location_line_edit.setText(self.output_path)
        self.output_location_line_edit.setEnabled(False)
        self.output_location_selector = QtGui.QPushButton("...")
        self.output_location_selector.setToolTip("Files will be saved in %s.\nClick to select a new save location."%self.output_path)
        self.output_location_selector.setEnabled(False)
        self.subfolder_check_box = QtGui.QCheckBox("Save Images in Sub-Folders (Using First Name Mask)")
        self.subfolder_check_box.setToolTip("When checked, all images are downloaded into sub folders, based on the first name mask that you've selected.")
        self.subfolder_check_box.setEnabled(False)
        self.output_location_layout = QtGui.QHBoxLayout()
        self.output_location_layout.addWidget(self.output_location_line_edit,2)
        self.output_location_layout.addWidget(self.output_location_selector,0)
        self.open_output_location = QtGui.QPushButton("Open saved location")
        self.open_output_location.setEnabled(False)
        self.options = QtGui.QGroupBox("Inputs")
        self.options_layout = QtGui.QVBoxLayout()
        self.options.setLayout(self.options_layout)
        self.options_layout.addWidget(self.instruction_label,0)
        self.options_layout.addWidget(self.fsn_list_text_edit,5)
        self.options_layout.addWidget(self.get_images_check_box,0)
        self.options_layout.addWidget(self.images_types_box,0)
        self.options_layout.addWidget(self.image_mask_instruction,0)
        self.options_layout.addLayout(self.images_name_masks,0)
        self.options_layout.addLayout(self.joiner,0)
        self.options_layout.addLayout(self.output_location_layout,0)
        self.options_layout.addWidget(self.subfolder_check_box,0)
        self.options_layout.addWidget(self.open_output_location,0)
        self.options_layout.addWidget(self.get_data_dump_check_box,0)
        self.options_layout.addWidget(self.data_dump_instruction,0)
        self.options_layout.addWidget(self.get_data_dump_types_box,1)
        self.options_layout.addWidget(self.pull_button,0)
        self.options_and_tabs = QtGui.QHBoxLayout()
        self.options_and_tabs.addWidget(self.options,0)
        self.options_and_tabs.addWidget(self.tabs,5)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.options_and_tabs,0)
        self.layout.addWidget(self.progress_bar,0)
        self.layout.addWidget(self.status_label,0)
        self.setWindowIcon(QtGui.QIcon("oink.ico"))

        self.main_widget = QtGui.QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.show()
        self.setWindowTitle("Swine: The Flipkart Data Extraction Application")
        self.center()

    def mapEvents(self):
        """"""
        self.output_location_selector.clicked.connect(self.changeImageSaveLocation)
        self.get_data_dump_check_box.stateChanged.connect(self.toggleDataProcurement)
        self.get_images_check_box.stateChanged.connect(self.toggleImagesProcurement)
        self.open_output_location.clicked.connect(self.openOutputLocation)
        self.image_masks[0].currentIndexChanged.connect(self.limitMask1)
        self.image_masks[1].currentIndexChanged.connect(self.limitMask2)
        self.reset_masks.clicked.connect(self.resetNameMask)
        self.pull_button.clicked.connect(self.runJob)
        self.swine_thread.sendStatus.connect(self.displayProgress)
        self.swine_thread.sendData.connect(self.populateTable)
        self.swine_thread.sendException.connect(self.log.append)
    
    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_C:
                table_to_copy = self.process_table
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

    def populateTable(self, data_list):
        fsns = data_list.keys()
        data_columns = data_list[fsns[0]].keys()
        if "Image" in data_columns:
            data_columns.remove("Image")
            data_columns = ["Image"] + data_columns
        if "WS Name" in data_columns:
            data_columns.remove("WS Name")
            data_columns = ["WS Name"] + data_columns
        if "Brand" in data_columns:
            data_columns.remove("Brand")
            data_columns = ["Brand"] + data_columns
        column_headers = ["FSN"] + data_columns
        self.process_table.setColumnCount(0)
        self.process_table.setRowCount(0)
        self.process_table.setColumnCount(len(column_headers))
        self.process_table.setSortingEnabled(False)
        row_index = 0
        for fsn in fsns:
            self.process_table.insertRow(row_index)
            self.process_table.setItem(row_index, 0, QtGui.QTableWidgetItem(str(fsn)))
            column_index = 1
            for column in column_headers[1:]:
                self.process_table.setItem(row_index, column_index, QtGui.QTableWidgetItem(str(data_list[fsn][column])))
                column_index += 1
            row_index += 1
        self.process_table.setHorizontalHeaderLabels(column_headers)
        self.process_table.setSortingEnabled(True)
        self.process_table.resizeColumnsToContents()
        self.process_table.resizeRowsToContents()

    def limitMask1(self):
        self.image_masks[1].clear()
        for image_mask in self.image_mask_options:
            if image_mask not in [str(self.image_masks[0].currentText())]:
                self.image_masks[1].addItem(image_mask)
        self.image_masks[1].setCurrentIndex(-1)

    def limitMask2(self):
        self.image_masks[2].clear()
        for image_mask in self.image_mask_options:
            if image_mask not in [str(self.image_masks[0].currentText()),str(self.image_masks[1].currentText())]:
                self.image_masks[2].addItem(image_mask)
        self.image_masks[2].setCurrentIndex(-1)

    def openOutputLocation(self):
        subprocess.Popen(r'explorer /open,"%s"'%os.path.join(self.output_path,""))

    def toggleDataProcurement(self):
        if self.get_data_dump_check_box.isChecked():
            self.get_data_dump_types_box.setEnabled(True)
        else:
            self.get_data_dump_types_box.setEnabled(False)

    def toggleImagesProcurement(self):
        if self.get_images_check_box.isChecked():
            state = True
        else:
            state = False
        self.images_types_box.setEnabled(state)
        for image_mask in self.image_masks:
            image_mask.setEnabled(state)
        self.joiner_mask.setEnabled(state)
        #self.options.setEnabled(state)
        self.output_location_selector.setEnabled(state)
        self.open_output_location.setEnabled(state)
        self.reset_masks.setEnabled(state)
        self.subfolder_check_box.setEnabled(state)

    def resetNameMask(self):
        self.image_masks[0].setCurrentIndex(-1)
        self.image_masks[1].setCurrentIndex(-1)
        self.image_masks[2].setCurrentIndex(-1)
        self.joiner_mask.setCurrentIndex(-1)

    def runJob(self):
        self.pull_button.setEnabled(False)
        self.pull_button.setText("Pulling Data...")
        text_edit_contents = str(self.fsn_list_text_edit.toPlainText()).strip()
        #print "Got text!"
        if '"' in text_edit_contents:
            text_edit_contents.replace('"',"")
            #print "Removing quotes"
        if " " in text_edit_contents:
            text_edit_contents.replace(' ', "")
            #print "Removing spaces"
        if "\n" in text_edit_contents:
            search_items = list(set(text_edit_contents.split("\n")))
        if "," in text_edit_contents:
            search_items = list(set(text_edit_contents.split(",")))
        if len(text_edit_contents) in [13, 16]:
            search_items = [text_edit_contents]
        #print search_items
        fsn_list = [fsn for fsn in search_items if ((len(fsn) == 16) or (len(fsn) == 13))]

        if len(fsn_list) == 0:
            self.alertMessage("No input data provided.","Please paste at least 1 FSN in the entry field before trying to pull data.")
        else:
            #Set the variables.
            self.swine_thread.fsn_list = fsn_list
            if self.get_images_check_box.isChecked():
                #Set the image save location
                self.swine_thread.image_save_location = self.output_path
                #Set the image mask.
                self.swine_thread.get_all_images = self.images_types_box.isChecked()
                if self.image_masks[0].currentIndex() == -1:
                    self.swine_thread.image_name_mask = ["FSN"]
                else:
                    self.swine_thread.image_name_mask = [str(self.image_masks[0].currentText())]
                    if self.image_masks[1].currentIndex() != -1:
                        self.swine_thread.image_name_mask.append(str(self.image_masks[1].currentText()))
                        if self.image_masks[2].currentIndex() != -1:
                            self.swine_thread.image_name_mask.append(str(self.image_masks[2].currentText()))

                self.swine_thread.image_name_mask_delimiter = str(self.joiner_mask.currentText())
                self.swine_thread.use_subfolders = self.subfolder_check_box.isChecked()
                self.swine_thread.get_images = True
            if self.get_data_dump_check_box.isChecked():
                self.swine_thread.get_data = True
                spec_table_names = str(self.get_data_dump_types_box.toPlainText()).strip()
                if "," in spec_table_names:
                    spec_table_names = spec_table_names.split(",")
                    spec_table_names = [spec.strip() for spec in spec_table_names if len(spec)>1]
                elif ";" in spec_table_names:
                    spec_table_names = spec_table_names.split(";")
                else:
                    spec_table_names = [spec_table_names]
                self.swine_thread.required_data = spec_table_names
            self.swine_thread.allow_run = True

    def changeImageSaveLocation(self):
        self.output_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.output_location_selector.setToolTip("Files will be saved in %s.\nClick to select a new save location."%self.output_path)
        self.output_location_line_edit.setText(self.output_path)

    def displayProgress(self,status_message,process_percentage,completion_state,eta):
        self.progress_bar.setValue(process_percentage)
        if not completion_state:
            display_message = "%s ETA: %s." %(status_message, eta.strftime("%H:%M:%S"))
        else:
            self.pull_button.setEnabled(True)
            self.pull_button.setText("Run")
            display_message = "Completed Pulling the Required Information at %s from Flipkart." %eta.strftime("%H:%M:%S")
            self.alertMessage("Completed Running",display_message)
        self.status_label.setText(display_message)
        self.log.append(display_message)

    def alertMessage(self, title, message):
        """Vindaloo."""
        QtGui.QMessageBox.about(self, title, message)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    swine = Swine()
    swine.show()
    sys.exit(app.exec_())