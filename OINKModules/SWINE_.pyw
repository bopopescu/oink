#!/usr/bin/python2
#! coding: utf-8

#SWINE - SWeet Information Extractor.

import sys, time
from datetime import datetime
import os
import csv
import urllib2

import numpy

from PyQt4 import QtGui, QtCore, Qt

from bs4 import BeautifulSoup


class SWINE(QtGui.QMainWindow):
    def __init__(self):
        """Initializer function."""
        super(SWINE, self).__init__()
        self.styles = {
                "Buttons" : "QPushButton {font-family: Garamond; font-size: 16px;}"
        }
        self.create_widgets()
        self.create_layouts()
        self.set_tooltips()
        self.set_styles()
        self.create_visuals()
        self.create_events()

    def create_widgets(self):
        """Widget Generator"""
        
        self.FSN_Label = QtGui.QLabel("<b>FSN(s):<b>")
        self.FSN_list = QtGui.QTextEdit()
        self.FSN_list.setMinimumSize(QtCore.QSize(300,10))
        self.check_button = QtGui.QPushButton("Fetch information")
        self.open_file = QtGui.QPushButton("Get FSNs from file")
        self.selectData_button = QtGui.QPushButton("Select Parameters")
        self.exportData_button = QtGui.QPushButton("Fetch data and\nexport to CSVs")
        self.data_tabulator = SWINE_data_tabulator()
        self.central_widget = QtGui.QWidget()

    def set_styles(self):
        self.check_button.setStyleSheet(self.styles["Buttons"])
        self.open_file.setStyleSheet(self.styles["Buttons"])
        self.selectData_button.setStyleSheet(self.styles["Buttons"])
        self.exportData_button.setStyleSheet(self.styles["Buttons"])
    
    def create_layouts(self):
        self.FSN_Buttons_layout = QtGui.QVBoxLayout()
        self.FSN_Buttons_layout.addWidget(self.check_button)
        self.FSN_Buttons_layout.addWidget(self.open_file)
        self.FSN_Buttons_layout.addWidget(self.selectData_button)
        self.FSN_Buttons_layout.addWidget(self.exportData_button)

        self.FSN_layout = QtGui.QHBoxLayout()
        self.FSN_layout.addWidget(self.FSN_Label)
        self.FSN_layout.addWidget(self.FSN_list)
        self.FSN_layout.addLayout(self.FSN_Buttons_layout)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.FSN_layout)
        self.layout.addWidget(self.data_tabulator)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def set_tooltips(self):
        """Maps tooltips to the widgets."""
        self.FSN_list.setToolTip("Paste FSN(s) here.")
        self.check_button.setToolTip("Click to start pulling the data.")
        self.open_file.setToolTip("Click to open a file and get FSNs from it.")
        self.exportData_button.setToolTip("Click to extract data and export all the crawled data to (an) output file(s).")
        self.selectData_button.setToolTip("Click to select what data you'd like to crawl from the site.")

    def create_visuals(self):
        """Creates all visual aspects."""
        self.setWindowTitle("SWINE Flipkart Data Crawler")
        self.move(350, 150)
        self.resize(300, 400)
        self.show()

    def create_events(self):
        self.check_button.clicked.connect(self.pull_information)
        self.open_file.clicked.connect(self.processBulkFSNs)

    def check_FSN(self):
        """Checks if an input is an FSN or not."""
        querystring = self.get_FSN()
        isFSN = False
        isFSNLength = len(querystring) == 16
        isISBNLength = len(querystring) == 13
        isAllUpper = querystring.isupper()
        isAllNumber = querystring.isdigit()
        hasXAtEnd = (querystring[:len(querystring)-1].isdigit()) and (querystring[len(querystring)-1:] == "X")
        hasNoSpaces = (querystring.find(" ") == -1)
        isFSN = ((isFSNLength and isAllUpper) or (isISBNLength and (isAllNumber or hasXAtEnd)) and hasNoSpaces)
        return isFSN
    
    def processBulkFSNs(self):
        FSNList = []
        FSN_file = QtGui.QFileDialog.getOpenFileName(self, "Open File","/")
        if len(FSN_file):
            f = open(FSN_file, "r")
            FSNList = f.read().split("\n")
            f.close()
            #print FSNList
            output_file = QtGui.QFileDialog.getSaveFileName(self, "Save File", "/")
            print "Output file is: %s" %output_file
            if len(output_file):
                output_file_link = open(output_file, "w")
                dictwrite = csv.DictWriter(output_file_link, fieldnames = self.getEmptyDataList())
                number_of_FSNs = 0
                dictwrite.writeheader()
                for FSN in FSNList:
                    if len(FSN):
                        number_of_FSNs += 1
                        self.post_to_log("Processing FSN #%d" %number_of_FSNs, "Append")
                        try:
                            #thread_run = thread.Thread(target=self.getDataForFSN, args = (FSN))
                            dictwrite.writerow(self.getDataForFSN(FSN))
                        except Exception, e:
                            print "Error encountered while getting data. Printing verbatim:\n%s" %repr(e)
                output_file_link.close()
                #self.alertMessage("Success!", "Successfully processed %d FSNs." % number_of_FSNs)
                os.startfile(output_file)
        return FSNList
    
    def getDataForFSN(self, FSN):
        """Gets a dictionary of relevant data for a given FSN."""
        url = "http://www.flipkart.com/search?q=" + FSN
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html)
        try:
            ws_name = self.get_wsname(soup)
        except:
            ws_name = "Error retrieving WSName data"
        
        self.get_spectable(soup)

        #self.post_to_log("<b>WSName:<b> %s" % ws_name[0])
        book_data = soup.find("div", {"class": "bookDetails unit size1of3"})
        #self.post_to_log(str(book_data), "Append")
        FSN_Dict = {"FSN": FSN, "WSName": ws_name}
        print FSN_Dict
        return FSN_Dict

    def getEmptyDataList(self):
        data_list = ["FSN", "WSName"] #, "Publishing House", "Genre(s)", "Author(s)", "Page Count", "Language", "Has Image", "Has Description", "Binding"]
        data_dict = dict((item, item) for item in data_list)
        return data_list
    
    def pull_information(self):
        """Pulls information for the FSN"""
        isFSN = self.check_FSN()
        isISBN = self.check_if_ISBN()
        if isFSN:
            url = "http://www.flipkart.com/search?q=" + self.get_FSN()
            html = urllib2.urlopen(url)
            soup = BeautifulSoup(html)
            ws_name = self.get_wsname(soup)
            self.post_to_log("<b>WSName:<b> %s" % ws_name[0])
            if isISBN:                
                book_data = soup.find("div", {"class": "bookDetails unit size1of3"})
                self.post_to_log(str(book_data), "Append")

#            imags = soup.findAll("div", {"class":"mainImage"})
#            imag_list = []
            #print type(imags)
#            for imag in imags:
#               print imag.img['src'].split("data-src=")
            #print imag_list
    
    def post_data(self, data_dict, ):
        """Takes a dictionary of data and feeds it to the tabulator widget."""



class SWINE_data_tabulator(QtGui.QWidget):
    def __init__(self):
        """Initializes the entire widget."""
        super(SWINE_data_tabulator, self).__init__()
        self.tables = 1
        self.create_widgets()
        self.create_tabulator_tabs()
        self.create_layout()
        self.set_tooltips()
        self.create_events()
        self.create_visuals()

    def create_visuals(self):
        """Creates the visuals."""

    def create_widgets(self):
        """Creates the widgets."""
        self.tables_list = [QtGui.QTableWidget()]
        self.save_location_button = QtGui.QPushButton("Set Save Location")
        self.export_sheet_button = QtGui.QPushButton("Export Active Sheet")
        self.export_all_sheets_button = QtGui.QPushButton("Export All Data")
        self.log = QtGui.QTextEdit()
        self.tabulator_tab = QtGui.QTabWidget()
    
    def set_tooltips(self):
        self.save_location_button.setToolTip("Click to set or change the save location.\nThe default save location is the folder where this application is located.")
        self.export_sheet_button.setToolTip("Click to export the data only in the active sheet into a file.")
        self.export_all_sheets_button.setToolTip("Click to export all the crawled data into separate files.")

    def create_layout(self):
        """Creates the layout."""
        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addWidget(self.save_location_button)
        self.buttons_layout.addWidget(self.export_sheet_button)
        self.buttons_layout.addWidget(self.export_all_sheets_button)
       
        self.tabulator_layout = QtGui.QVBoxLayout()

        self.tabulator_layout.addWidget(self.tabulator_tab)
        self.tabulator_layout.addLayout(self.buttons_layout)
        self.setLayout(self.tabulator_layout)

    def create_tabulator_tabs(self):
        """adds tabs to the tabulator based on the number of tables required."""
        for item in range(self.tables):
            self.tabulator_tab.addTab(self.tables_list[item], "Table #%d" %(item + 1))
        self.tabulator_tab.addTab(self.log, "Log")

    def create_events(self):
        """Creates all related events."""
        self.save_location_button.clicked.connect(self.set_save_location)
        self.export_sheet_button.clicked.connect(self.save_active_sheet)
        self.export_all_sheets_button.clicked.connect(self.save_all_sheets)
   
    def save_active_sheet(self):
        """"""

    def save_all_sheets(self):
        """"""

    def get_tables_as_list(self):
        """Returns a list containing table elements."""

    
    def get_data_from_table(self, list_of_headers):
        """Returns the data in the table as a dictionary, and returns a list which dictates the order of the keys."""
    
    def add_table(self, list_of_headers):
        """Adds a new tab, and that tab will have a table corresponding to a list of headers."""
    
    
    def export_data_to_csvs(self, save_location):
        """For each table in the current instance of the tabulator, this will generate separate csvs in the specified location."""
    
    def generate_file_name(self, list_of_headers):
        """Given a list of headers, returns a possible file name for cataloguing purposes."""
    
    def get_table_headers_list(self, table_object):
        """Returns the list of headers of a specified table object."""
    
    def add_FSN_and_data(self, FSN_data_dict, headers_list_in_order):
        """Given a dictionary of data related to an FSN. This method will pick which table that it can 
        add this data to. In case there is no table, it will attempt to add one."""
    def set_save_location(self):
        """Set a save location."""

    def post_to_log(self, text, mode=None):
        """Appends a message to the log. Appends or overwrites based on the mode."""
        if mode == None:
            self.log.clear()
            self.log.append(text)
        elif mode == "Append":
            self.log.append(text)
        else:
            print "Error. Mode %s isn't valid." %mode
        mode = None
        return 0

#####################################################################
#########################General functions###########################
#####################################################################

def get_page_link(self, html_object):
    """Fetches the WS Link for the given urllib2 object."""
    return html_object.geturl()

def get_FSN(self):
    """Returns the FSN entered into the line edit, removes trailing spaces."""
    return str(self.FSN_list.text()).strip()

def check_if_ISBN(self):
    """Checks if the FSN is an ISBN."""
    isISBN = False
    querystring = self.get_FSN()
    if self.check_FSN():
        isISBNLength = (len(querystring) == 13)
        isAllNumber = querystring.isdigit()
        hasXAtEnd = (querystring[:len(querystring)-1].isdigit()) and (querystring[len(querystring)-1:] == "X")
        hasNoSpaces = (querystring.find(" ") == -1)
        isISBN = isISBNLength and (isAllNumber or hasXAtEnd) and hasNoSpaces
    return isISBN

def get_Goodreads_link(ISBN):
    """Given an ISBN, it generates the link for the Goodreads page."""

def get_item_id(html_object):
    """Takes an urllib2 object, gets the current url from geturl and then extracts the item id."""
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

def get_brand(soup_object):
    """Takes a urllib2 object and creates a soup object that crawls for the brand name and returns it."""

def check_FK_description(soup_object):
    """Takes a urllib2 object and creates a soup object that crawls for the description text and returns 
    True if it is available."""

def pull_description_text(soup_object):
    """Takes a urllib2 object and creates a soup object that crawls for the description text and returns it."""

def get_wsname(soup_object):
    """Takes a soup object that crawls for the WSName and returns it."""
    #return soup_object.find("h1", {"itemprop": "name"}).contents[0] #The item is a list
    return soup_object.find("h1", {"itemprop": "name"}).string.strip()

def get_spectable(soup_object):
    """Takes a urllib2 object and creates a soup object that crawls for the Specification Table and returns a dictionary of all the items in it as well as a list that maintains the order of the keys"""
    spec_section_area = soup_object.find(class_ = "productSpecs specSection")
    #print spec_section_area
    specTables = spec_section_area.find_all(class_ = "specTable")
    groupHeads_list = []
    specsKeys_list = []
    specsValues_list = []
    for specTable in specTables:
        groupHeads = specTable.find_all(class_ = "groupHead")
        for groupHead in groupHeads:
            groupHeads_list.append(str(groupHead.string).strip())
        specsKeys = specTable.find_all(class_ = "specsKey")
        for specsKey in specsKeys:
            specsKeys_list.append(str(specsKey.string).strip())
        
        specsValues = specTable.find_all(class_ = "specsValue")
        for specsValue in specsValues:
            specsValues_list.append(str(specsValue.string).strip())
    
    specifications = dict(zip(specsKeys_list, specsValues_list))

    #print "Group Heads: ", groupHeads_list
    #print "Specifications: "
    #for key in specifications:
    #    print "%s: %s" %(key, specifications[key])
    return groupHeads_list, specifications

def get_path_list(soup_object):
    """Takes a urllib2 object and creates a soup object that crawls for the path and returns a list that contains all items in the path except "Home"."""
    if check_if_out_of_stock(soup_object):
        path = "Item out of stock. Path cannot be retrieved."
    else:
        try:
            path_list_in_soup = soup_object.find(attrs = {"data-tracking-id": "product_breadCrumbs"})
        #    item = path_list_in_soup.find(class_ = "fk-inline-block")
            path = []
            anchor_items = path_list_in_soup.find_all("a")
            #print anchor_items
            for tag in anchor_items:
                path.append(str(tag.string.strip()))
        except AttributeError, e:
            path = "Error Retrieving Path"
            #print repr(e)
        #print path
    return path

def check_if_out_of_stock(soup_object):
    """Checks if a product is out of stock. Returns True if the product is not in stock, and False if it is."""
    stock_section = soup_object.find(class_ = "out-of-stock-status")
    out_of_stock = False
    if stock_section != None:
        out_of_stock = True
    return out_of_stock

def get_warranty_section_items(soup_object):
    """Takes a urllib2 object and creates a soup object that crawls for the contents of the "warranty" section and returns what it finds."""

def get_category_tree_from_path(soup_object):
    """Takes a list containing the Flipkart WS path and returns a dictionary for the category tree."""

def get_flipkart_search_url(FSN):
    "Returns the search query url for Flipkart, given an FSN or ISBN."
    return "http://www.flipkart.com/search?q=" + FSN

def getFlipkarSearchURL(FSN):
    "Returns the search query url for Flipkart, given an FSN or ISBN."
    return "http://www.flipkart.com/search?q=" + FSN

def main():
    app = QtGui.QApplication(sys.argv)
    researcher = SWINE()
    sys.exit(app.exec_())

def check_link_redirection(html_object):
    item_id = get_item_id(html_object)
    redirection = False
    if item_id != None:
        redirection = True
    return redirection

def save_essentials_to_csv(fsn, wsname, item_id, path_list, brand):
    if os.path.isfile("essentials.csv"):
        ess_file = open("essentials.csv", "a")
        csv_link = csv.writer(ess_file)
    else:
        ess_file = open("essentials.csv", "wt")
        csv_link = csv.writer(ess_file)
        csv_link.writerow(["FSN", "WSName", "Item ID", "Path", "Brand", "Time Stamp"])
    if type(path_list) == type(""):
        path = path_list
    else:
        path = ">".join(path_list)
    csv_link.writerow([fsn, wsname.replace(",", "+"), item_id, path, brand, "%s" % datetime.now()])
    ess_file.close()

def record_skipped_FSN(fsn, error):
    if os.path.isfile("skipped.csv"):
        skip_file = open("skipped.csv", "a")
        csv_link = csv.writer(skip_file)
    else:
        skip_file = open("skipped.csv", "wt")
        csv_link = csv.writer(skip_file)
        csv_link.writerow(["FSN","Error", "Time"])
    csv_link.writerow([fsn, error, "%s" % datetime.now()])

def test():
    print "Running trial"
    original_start_time = datetime.now()
    FSNs = open("fsns_dom_filtered.csv","r").read().split("\n")
   #FSNs = ["TABDPZRVEKXBBKC7", "TABEFMVHTSEBTQBF", "TABDQSQ7FH6RXWZA", "TABDVF4WZJ27FBWF", "TABDVUTGE9RCWNUY", "TABDRBHFDH8JRXGG", "TABDFWGG86GVKFRW", "TABDTZ63H8MGGZDR", "TABDTZ63TKM7TXCY", "CBKDEKGSJTHUW59B", "CBKDEKGSKNWYQGZH", "CBKDEKGSM6XP5H88", "9781409128236"]
    #FSNs = ["9781409128236"]
    print "Beginning to process %d FSNs." %len(FSNs)
    times = []
    total_FSNS = len(FSNs)
    counter = 1
    errors = 0
    for fsn in FSNs:
        startTime = datetime.now()
        try:
            html = urllib2.urlopen(get_flipkart_search_url(fsn))
            item_id = get_item_id(html)
            if check_link_redirection(html):
                #print "Led to %s" % html.geturl()
                soup = BeautifulSoup(html)
                path_list = get_path_list(soup)
                wsname = get_wsname(soup)
                print "******************"
                print "Successfully processing %d of %d. Success(es): %d, Failures: %d." %(counter, total_FSNS, (counter - errors), errors)
                print "Total time elapsed: %s" % (datetime.now() - original_start_time)
                #print "FSN: ", fsn
                #print "Item ID: ", item_id
                #print "WSName: ", wsname
                #print "Path: ", path_list
                #print "Specification Table Items:"
                spec_headers, specs = get_spectable(soup)
                save_essentials_to_csv(fsn, wsname, item_id, path_list, specs["Brand"])
                #save_essentials_to_csv(fsn, wsname, item_id, path_list, specs.keys())
                print "******************"
                counter += 1 
                endTime = datetime.now()
                times.append(endTime - startTime)
                time.sleep(5)
            else:
                print "********elseerror*********"
                errors += 1
                print "Failed in processing %d of %d. Success(es): %d, Failure(s): %d." %(counter, total_FSNS, (counter - errors), errors)
                print "Total time elapsed: %s" % (datetime.now() - original_start_time)
                error = "Redirection Error"
                record_skipped_FSN(fsn, error)
                counter +=1
                print "******************"
                time.sleep(1)
        #except (AttributeError, urllib2.HTTPError), e:
        except Exception, e:
            print "******************"
            errors += 1
            print "Failed in processing %d of %d. Success(es): %d, Failure(s): %d." %(counter, total_FSNS, (counter - errors), errors)
            print "Total time elapsed: %s" % (datetime.now() - original_start_time)
            error = repr(e)
            record_skipped_FSN(fsn, error)
            counter += 1
            print "******************"
            time.sleep(2)
            #raise
            #print "Error: ", repr(e)
        #except Exception, e:
            #raise

    print "Run time diagnostics:"
#    print times
    print "Total Time Spent: %s" % (datetime.now() - original_start_time)
#    print "Mean run time per FSN:", numpy.mean(times)
#    print "Median of the run time per FSN:", numpy.median(times)
#    print "Total run time:", numpy.sum(times)
    print "Finished trial. Total errors: %d" %errors


#Cleaned SWINE functions.


def checkForRedirection(html_object):
    """Checks the URL of the object and determines if it got redirected or not."""

    return True

def getWSNameFromSoup(soup_object):
    WSName = "NA"
    try:
        WSName = soup_object.find("h1", {"itemprop": "name"}).string.strip()
    except Exception, e:
        print "Error in getWSNameFromSoup."
        print repr(e)
        print "Leaving getWSNameFromSoup."
        pass

def getItemIDFromURLLib2Object(html_object):
    """Takes an urllib2 object, gets the current url from geturl and then extracts the item id."""
    upload_link = html_object.geturl()
    item_id_prefix_position = upload_link.find(r"/p/")
    if item_id_prefix_position > -1:
        item_id_start_position = item_id_prefix_position + len(r"/p/")
        item_id_length = 16 #Right now, that's what it looks like.
        item_id_end_position = item_id_start_position + item_id_length
        item_id = upload_link[item_id_start_position: item_id_end_position]
    else:
        item_id = None
    return item_id

def getSpecsFromSoup(soup_object):
    """Takes a urllib2 object and creates a soup object that crawls for the Specification Table and returns a dictionary of all the items in it as well as a list that maintains the order of the keys"""
    #Rewrite this to use pandas.DataFrame
    import pandas
    spec_section_area = soup_object.find(class_ = "productSpecs specSection")
    #print spec_section_area
    specTables = spec_section_area.find_all(class_ = "specTable")
    groupHeads_list = []
    specsKeys_list = []
    specsValues_list = []
    for specTable in specTables:
        groupHeads = specTable.find_all(class_ = "groupHead")
        for groupHead in groupHeads:
            groupHeads_list.append(str(groupHead.string).strip())
        specsKeys = specTable.find_all(class_ = "specsKey")
        for specsKey in specsKeys:
            specsKeys_list.append(str(specsKey.string).strip())
        
        specsValues = specTable.find_all(class_ = "specsValue")
        for specsValue in specsValues:
            specsValues_list.append(str(specsValue.string).strip())
    
    specifications = dict(zip(specsKeys_list, specsValues_list))

    #print "Group Heads: ", groupHeads_list
    #print "Specifications: "
    #for key in specifications:
    #    print "%s: %s" %(key, specifications[key])
    return specifications

def checkForPlagiarism(featured_description):
    return False

def getPathFromSoup(soup_object):
    """Takes a urllib2 object and creates a soup object that crawls for the path and returns a list that contains all items in the path except "Home"."""
    if check_if_out_of_stock(soup_object):
        path = "Item out of stock. Path cannot be retrieved."
    else:
        try:
            path_list_in_soup = soup_object.find(attrs = {"data-tracking-id": "product_breadCrumbs"})
        #    item = path_list_in_soup.find(class_ = "fk-inline-block")
            path = []
            anchor_items = path_list_in_soup.find_all("a")
            #print anchor_items
            for tag in anchor_items:
                path.append(str(tag.string.strip()))
        except AttributeError, e:
            path = "Error Retrieving Path"
            #print repr(e)
        #print path
    return path

def scrapeFlipkart(FSN):
    """This method does the following things:
    1. Gets the flipkart search URL.
    2. If redirected to the product page, it proceeds to the next steps. For now, there is no else action.
    3. It extracts the Item ID.
    4. It extracts the WSName.
    5. It extracts the specifications table.
    6. [Experimental] It extracts the description text.
    7. [Experimental] It extracts the RPD text.
    8. [Experimental] It analyses the extracted text to check if it is unique.
    9. [Experimental] It gets the product images.
    10. It creates a pandas.DataFrame from all the extracted data. The columns are:
        a. Attribute Names[FSN, URL, Item ID, WS Name, Spec Table Headers (Multiple columns), Image URL(s) (list), Article Text, Article Text Type, Article Text Word Count (int), Plagiarism (Boolean)]
        b. Values
        c. [Experimental] Reliable Booleans. Each row will have a bool to value whether it can be trusted.
    11. Returns the DataFrame.
    12. For now, if it fails in redirection, it returns a list with the FSN and a False.
    """
    import pandas
    url = get_flipkart_search_url(FSN)
    fk_page_code = urllib2.urlopen(url, timeout=5)
    proceed = checkForRedirection(fk_page_code)
    if proceed:

        item_id = getItemIDFromURLLib2Object(fk_page_code)
        #print item_id
        fk_page_soup = BeautifulSoup(fk_page_code)
        path = getPathFromSoup(fk_page_soup)
        #print path
        ws_name = getWSNameFromSoup(fk_page_soup)
        #print ws_name
        spec_table_data = getSpecsFromSoup(fk_page_soup)
        #print spec_table_data
        #regular_description = getRegularDescriptionFromSoup(fk_page_soup)
        #rich_product_description = getRichProductDescriptionFromSoup(fk_page_soup)
        #featured_description = getFeaturedDescription(regular_description, rich_product_description)
        
        #plagiarized = checkForPlagiarism(featured_description)
        
        #image_urls = getImagesFromSoup(fk_page_soup)
        #image_sizes = getURLFileSize(image_urls)
        data_dictionary = {
                    "FSN": FSN,
                    "Scrape Success": True,
                    "Item ID": item_id,
                    "WS Name": ws_name,
        }
        data_dictionary.update(spec_table_data)

        data = pandas.DataFrame.from_dict(data_dictionary, orient="index")
        data.columns = ["Attribute"]
        #print data
    else:
        data_dictionary = {
                    "FSN": FSN,
                    "Scrape Success": False
        }
        data = pandas.DataFrame.from_dict(data_dictionary, orient="index")
        data.columns = ["Attribute"]
        #data.columns = ["Attribute", "Value"]
        
        #Later, write code that catches the first product page and enters that. Then, restart the previous process.
        #data = [FSN, False]
    return data

def findDescription(fsn):
    url = get_flipkart_search_url(fsn)
    try:
        fk_page_code = urllib2.urlopen(url, timeout=60)
        proceed = checkForRedirection(fk_page_code)
    except:
        proceed = False
    if proceed:
        fk_page_soup = BeautifulSoup(fk_page_code)
        rpd_content = getRPDFromSoup(fk_page_soup).encode("utf8")
        #print rpd_content
        pd_content = getPDFromSoup(fk_page_soup).encode("utf8")
        #print pd_content.encode("utf8")
        if rpd_content == "NA":
            isRPD = False
        else:
            #print rpd_content
            isRPD = True
        if pd_content == "NA":
            isPD = False
        else:
            isPD = True
        if isRPD and isPD:
            return 3
        elif isRPD:
            return 1
        elif isPD:
            return 2
        else:
            return 0
    else:
        return 0

def runtest():
    import datetime
    import MOSES
    FSN_list = MOSES.getFSNListWithoutUploadedType()
    counter = 1
    total = len(FSN_list)
    start_time = datetime.datetime.now()
    last_update_time = datetime.datetime.now() - datetime.timedelta(seconds=60)
    print "Received %d FSNs from the Piggy Bank. Starting process at %s." %(total, datetime.datetime.strftime(start_time,"%H:%M:%S"))
    for fsn in FSN_list:
        description_type = findDescription(fsn)
        if description_type == 0:
            MOSES.updateUploadedTypeInPiggyBank(fsn,"Not Uploaded")
        elif description_type == 1:
            MOSES.updateUploadedTypeInPiggyBank(fsn,"RPD")
        elif description_type == 2:
            MOSES.updateUploadedTypeInPiggyBank(fsn,"PD")
        elif description_type == 3:
            MOSES.updateUploadedTypeInPiggyBank(fsn,"RPD,PD")
        if datetime.datetime.now() - last_update_time >= datetime.timedelta(seconds=60):
            print "%d of %d completed. ETA : %s" %(counter, total, datetime.datetime.strftime(MOSES.getETA(start_time, counter, total),"%d-%m, %H:%M:%S"))
            last_update_time = datetime.datetime.now()
        counter += 1

    print "Completed."
    raw_input("Hit enter> ")

def getRPDFromSoup(soup_object):
    """
    class="rpdSection"
    """
    #rpd_section = soup_object.find(class_ = "rpdSection")
    rpd_section = soup_object.find("div", {"class": "rpdSection"})
    if len(str(rpd_section)) > 0:
        try:
            rpd = rpd_section.getText()
        except Exception, e:
            rpd= "NA"
            #print rpd_section
            print repr(e)

        if type(rpd) == None:
            rpd = "NA"
        else:
            rpd = rpd.strip()
            if len(rpd) == 0:
                rpd = "NA"
    else:
        rpd = "NA"
    return rpd

def getPDFromSoup(soup_object):
    """
    <div class="description specSection">
    class="rpdSection"
    """
    #rpd_section = soup_object.find(class_ = "rpdSection")
    pd_section = soup_object.find("div", {"class": "description specSection"})
    #print str(pd_section)
    if len(str(pd_section)) > 0:
        try:
            pd = pd_section.getText()
        except Exception, e:
            pd= "NA"
            #print pd_section
            #print repr(e)

        if type(pd) == None:
            pd = "NA"
        else:
            pd = pd.strip()
            if len(pd) == 0:
                pd = "NA"
    else:
        pd = "NA"
    return pd


if __name__ == "__main__":
    #main()
    test()