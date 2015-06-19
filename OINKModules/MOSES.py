#!usr/bin/python2
# -*- coding: utf-8 -*-
#Modular OINK SQL Engagement Service
"""
Includes all the methods relevant to using MySQL-Python.
"""
from __future__ import division
import sys
import datetime
import csv
import os
import time
import getpass
import MySQLdb
import MySQLdb.cursors
import numpy
import OINKMethods as OINKM

def getOINKConnector(user_id, password):
    import MySQLdb
    import MySQLdb.cursors
    conn = MySQLdb.connect(host = getHostID(), user = user_id, passwd = password, db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
    return conn

#########################################################################
#Set up methods. These methods help set up the server for the first time.
#Be very careful while using these since they will delete all existing data.
#########################################################################

def setupmethods():
    """Set up methods."""
    print "This section is for setup."

def addToRawData(user_id, password, process_dict):
    columns, values = getDictStrings(process_dict)
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "INSERT INTO `rawdata` (%s) VALUES (%s);" % (columns, values)
    #print sqlcmdstring
    try:
        dbcursor.execute(sqlcmdstring)
        status = "Success"
    except MySQLdb.IntegrityError:
        status = "Duplicate"
        pass
        #raise
    except:
        status = "Error"
        pass
        #raise
    connectdb.commit()
    connectdb.close()
    return status

def getRawDataKeys():
    keys = [
        "WriterID", "Writer Email ID", "Writer Name",
        "Editor ID", "Editor Email ID", "Editor Name",
        "Category", "Sub-Category", "Audit Date", "WS Name",
        "WC", "FSN", "CFM01", "CFM02", "CFM03", "CFM04", "CFM05",
        "CFM06", "CFM07", "CFM08", "GSEO01", "GSEO02", "GSEO03",
        "GSEO04", "GSEO05", "GSEO06", "GSEO07", "FAT01", "FAT02",
        "FAT03", "CFM Quality", "GSEO Quality", "Overall Quality",
        "Fatals Count", "Non Fatals Count", "CFM01C", "CFM02C", "CFM03C",
        "CFM04C", "CFM05C", "CFM06C", "CFM07C", "CFM08C", "GSEO01C",
        "GSEO02C",  "GSEO03C",  "GSEO04C",  "GSEO05C", "GSEO06C",
        "GSEO07C", "FAT01C", "FAT02C", "FAT03C"
        ]
    return keys

def seekFSN(user_id, password, fsn):
    """"""
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """SELECT * from `piggybank` WHERE fsn="%s";""" %fsn
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    article_date = "NA"
    database_table = "NA"
    status = "NA"
    database_table = "NA"
    description_type = "NA"
    writer_id = "NA"
    writer_name = "NA"
    article_date = "NA"
    bu = "NA"
    super_category = "NA"
    category = "NA"
    sub_category = "NA"
    vertical = "NA"
    brand = "NA"
    item_id = "NA"

    if len(data) == 0:
        sqlcmdstring = """SELECT * from `fsndump` WHERE fsn="%s";""" %fsn
        cursor.execute(sqlcmdstring)
        data_fsn_dump = cursor.fetchall()
        if len(data_fsn_dump) == 0:
            status = "Not Written Yet"
        else:
            status = "Written"
            database_table = "FSN Dump"
            description_type = data_fsn_dump[0]["Description Type"]
    else:
        status = "Written"
        database_table = "Piggy Bank"
        description_type = data[0]["Description Type"]
        writer_id = data[0]["WriterID"]
        writer_name = data[0]["Writer Name"]
        article_date = data[0]["Article Date"]
        bu = data[0]["BU"]
        super_category = data[0]["Super-Category"]
        category = data[0]["Category"]
        sub_category = data[0]["Sub-Category"]
        vertical = data[0]["Vertical"]
        brand = data[0]["Brand"]
        item_id = data[0]["Item ID"]
    conn.close()
    fsn_dict = {
        "FSN": fsn,
        "Status": status,
        "Description Type": description_type,
        "Writer ID": writer_id,
        "Writer Name": writer_name,
        "Article Date": article_date,
        "Database table": database_table,
        "BU": bu,
        "Super-Category": super_category,
        "Category": category,
        "Sub-Category": sub_category,
        "Vertical": vertical,
        "Brand": brand,
        "Item ID": item_id
        }
    return fsn_dict


def seekItemID(user_id, password, item_id):
    """"""
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """SELECT * from `piggybank` WHERE `Item ID`="%s";""" %item_id
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    fsn = "NA"
    article_date = "NA"
    database_table = "NA"
    status = "NA"
    database_table = "NA"
    description_type = "NA"
    writer_id = "NA"
    writer_name = "NA"
    article_date = "NA"
    bu = "NA"
    super_category = "NA"
    category = "NA"
    sub_category = "NA"
    vertical = "NA"
    brand = "NA"

    if len(data) == 0:
        sqlcmdstring = """SELECT * from `fsndump` WHERE `Item ID`="%s";""" %item_id
        cursor.execute(sqlcmdstring)
        data_fsn_dump = cursor.fetchall()
        if len(data_fsn_dump) == 0:
            status = "Not Written Yet"
        else:
            status = "Written"
            database_table = "FSN Dump"
            fsn = data_fsn_dump[0]["FSN"]
            description_type = data_fsn_dump[0]["Description Type"]
    else:
        status = "Written"
        fsn = data[0]["FSN"]
        database_table = "Piggy Bank"
        description_type = data[0]["Description Type"]
        writer_id = data[0]["WriterID"]
        writer_name = data[0]["Writer Name"]
        article_date = data[0]["Article Date"]
        bu = data[0]["BU"]
        super_category = data[0]["Super-Category"]
        category = data[0]["Category"]
        sub_category = data[0]["Sub-Category"]
        vertical = data[0]["Vertical"]
        brand = data[0]["Brand"]
        fsn = data[0]["FSN"]
    conn.close()
    fsn_dict = {
        "FSN": fsn,
        "Status": status,
        "Description Type": description_type,
        "Writer ID": writer_id,
        "Writer Name": writer_name,
        "Article Date": article_date,
        "Database table": database_table,
        "BU": bu,
        "Super-Category": super_category,
        "Category": category,
        "Sub-Category": sub_category,
        "Vertical": vertical,
        "Brand": brand,
        "Item ID": item_id
        }
    return fsn_dict
    
def recursiveUploadRawDataFile(user_id, password):
    if not os.path.isfile("Archive\\RawData_Archive.csv"):
        print "No Input file found!"
    else:
        start_time = datetime.datetime.now()

        print "Rebuilding Raw Data Table"
        rebuildRawData(user_id, password)
        print "Uploading Raw data entries."
        rawdata_file = open("Archive\\RawData_Archive.csv", "r")
        failed_file = open("Archive\\RawData_Failures.csv","w")
        duplicates_file = open("Archive\\RawData_Duplicates.csv", "w")
        rawdata = csv.DictReader(rawdata_file)
        failed = csv.DictWriter(failed_file, getRawDataKeys())
        #duplicates = csv.DictWriter(duplicates_file, getRawDataKeys())
        #total = len(raw_data_file.read().split("\n"))
        total = 0
        for rawdata_row in rawdata:
            total+=1
        rawdata_file.seek(0)
        counter = 0
        success = 0
        failure = 0
        start_time = datetime.datetime.now()
        last_update_time = datetime.datetime.now()
        for rawdata_row in rawdata:
            counter+=1
            process_dict = rawdata_row
            try_to_add = addToRawData(user_id, password, process_dict)
            if try_to_add == "Success":
                success += 1
            else:
                failure += 1
                failed.writerow(process_dict)
            if (counter == 1) or (datetime.datetime.now() - last_update_time) > datetime.timedelta(seconds=60):
                print "Completed: %d. Pending: %d. Failed: %d.\nETA: %s\n*" %(counter, total-counter, failure, getETA(start_time, counter, total))
                last_update_time = datetime.datetime.now()
        print "Run Complete. Summary:\n%d succeeded. %d failed. Total %d" %(success, failure, counter)
        print "Time spent: %s" % (datetime.datetime.now() - start_time)
        rawdata_file.close()
        duplicates_file.close()
        failed_file.close()

def rebuildRawData(user_id, password):
    """This method deletes the current raw data and redefines it."""
    rawdatadb = getOINKConnector(user_id, password)
    rawdatadbcursor = rawdatadb.cursor()
    rawdatadbcursor.execute("DROP TABLE IF EXISTS `rawdata`")
    sqlcmdstring = """CREATE TABLE `rawdata` (
            `WriterID` VARCHAR(20) NOT NULL,
            `Writer Email ID` VARCHAR(100),
            `Writer Name` VARCHAR(100),
            `Editor ID` VARCHAR(20) NOT NULL,
            `Editor Email ID` VARCHAR(100),
            `Editor Name` VARCHAR(100),
            `Category` VARCHAR(100),
            `Sub-Category` VARCHAR(100),
            `Audit Date` DATE NOT NULL,
            `WS Name` VARCHAR(200) NOT NULL,
            `WC` INT(5) NOT NULL,
            `FSN` VARCHAR(200) NOT NULL,
            `CFM01` FLOAT(5,3) NOT NULL,
            `CFM02` FLOAT(5,3) NOT NULL,
            `CFM03` FLOAT(5,3) NOT NULL,
            `CFM04` FLOAT(5,3) NOT NULL,
            `CFM05` FLOAT(5,3) NOT NULL,
            `CFM06` FLOAT(5,3) NOT NULL,
            `CFM07` FLOAT(5,3) NOT NULL,
            `CFM08` FLOAT(5,3) NOT NULL,
            `GSEO01` FLOAT(5,3) NOT NULL,
            `GSEO02` FLOAT(5,3) NOT NULL,
            `GSEO03` FLOAT(5,3) NOT NULL,
            `GSEO04` FLOAT(5,3) NOT NULL,
            `GSEO05` FLOAT(5,3) NOT NULL,
            `GSEO06` FLOAT(5,3) NOT NULL,
            `GSEO07` FLOAT(5,3) NOT NULL,
            `FAT01` ENUM("Yes", "No") DEFAULT "NO" NOT NULL,
            `FAT02` ENUM("Yes", "No") DEFAULT "NO" NOT NULL,
            `FAT03` ENUM("Yes", "No") DEFAULT "NO" NOT NULL,
            `CFM Quality` FLOAT(5,3) NOT NULL,
            `GSEO Quality` FLOAT(5,3) NOT NULL,
            `Overall Quality` FLOAT(5,3) NOT NULL,
            `Fatals Count` INT(5) NOT NULL,
            `Non Fatals Count` INT(5) NOT NULL,
            `CFM01C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `CFM02C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `CFM03C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `CFM04C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `CFM05C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `CFM06C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `CFM07C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `CFM08C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `GSEO01C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `GSEO02C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `GSEO03C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `GSEO04C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `GSEO05C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `GSEO06C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `GSEO07C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `FAT01C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `FAT02C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            `FAT03C` VARCHAR(200) DEFAULT "NA" NOT NULL,
            PRIMARY KEY (`FSN`, `Audit Date`)
            )"""
    rawdatadbcursor = rawdatadb.cursor()
    #print sqlcmdstring #debug
    rawdatadbcursor.execute(sqlcmdstring)
    rawdatadb.commit()
    rawdatadb.close()
    return True

def uploadRawData(user_id, password):
    """Method to bulk upload raw data from a CSV file to MySQL.
    Notes to self:
    1. The writer name column in the csv file should be replaced with their employee Ids.
    2. The Audit Date should be reformatted into the YYYY-MM-DD format.
    """
    rawdatadb = getOINKConnector(user_id, password)
    rawdatadbcursor = rawdatadb.cursor()
    #delete all data in the current Raw Data field.
    rebuildRawData(user_id,password) 
    sqlcmdstring = """LOAD DATA LOCAL INFILE 'Database/rawdata.csv' INTO TABLE oink.rawdata 
    FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"""
    rawdatadbcursor.execute(sqlcmdstring)
    rawdatadb.commit()
    rawdatadb.close()
    #print sqlcmdstring
    return True

def rebuildPiggyBank(user_id, password):
    """Deletes the current piggy bank and redefines it."""
    piggybankdb = getOINKConnector(user_id, password)
    piggycursor = piggybankdb.cursor()
    sqlcmdstring = "DROP TABLE IF EXISTS `piggybank`;"
    piggycursor.execute(sqlcmdstring)
    sqlcmdstring = """CREATE TABLE `piggybank` (
        `Article Date` DATE,
        `WriterID` VARCHAR(20) NOT NULL,
        `Writer Email ID` VARCHAR(100),
        `Writer Name` VARCHAR(100),
        `FSN` VARCHAR(200) NOT NULL,
        `Description Type` ENUM('Regular Description','Rich Product Description','Rich Product Description Plan A', 'Rich Product Description Plan B','SEO Big', 'SEO Small', 'SEO Project','RPD Updation','RPD Variant') NOT NULL DEFAULT "Regular Description",
        `Source` ENUM('Inhouse','Crowdsourced') DEFAULT "Inhouse",
        `BU` VARCHAR(50),
        `Super-Category` VARCHAR(50),
        `Category` VARCHAR(50),
        `Sub-Category` VARCHAR(50),
        `Vertical` VARCHAR(50),
        `Brand` VARCHAR(50),
        `Word Count` INT(5) DEFAULT '0',
        `Upload Link` VARCHAR(500),
        `Reference Link` VARCHAR(500),
        `Start Time` DATETIME,
        `End Time` DATETIME,
        `Modification Time` TIMESTAMP,
        `PC User Name` VARCHAR(200),
        `Upload Date` DATE,
        `Item ID` VARCHAR(50),
        `Job Ticket` VARCHAR(50),
        `Target` INT(3),
        `Rewrite Ticket` INT(5) NOT NULL DEFAULT '0',
        PRIMARY KEY (`FSN`,`Description Type`,`Rewrite Ticket`)
        )"""
    piggycursor.execute(sqlcmdstring)
    piggybankdb.commit()
    piggybankdb.close()
    return True

def uploadPiggyBank(user_id,password):
    """Method to bulk upload piggy bank data from a CSV file to MySQL."""
    piggybankdb = getOINKConnector(user_id, password)
    piggycursor = piggybankdb.cursor()
    rebuildPiggyBank(user_id,password)
    #Write the code to read and upload all the data in a piggybank.csv 
    #file to the MySQL database.
    sqlcmdstring = "LOAD DATA LOCAL INFILE 'Database/piggybank.csv' INTO TABLE oink.piggybank FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    piggycursor.execute(sqlcmdstring)
    piggybankdb.commit()
    piggybankdb.close()
    return True

def recursiveUploadPiggyBank(user_id, password):
    """Method to upload piggy bank entries into the server, picking 1 line of data at a time."""
    """
    Algorithm:
    1. Read piggy bank file through DictReader.
    2. For each row, attempt to upload to the server.
        1. If upload fails, check for an override ticket.
        2. If override ticket isn't available, create one.
        3. In either case, increment the Rewrite Ticket by 1.
        4. Try uploading again. Rinse and repeat 10 times.
        5. If it fails at #10, record the FSN into an output CSV opened through CSV.DictWriter.
    """
    DO = False
    if DO:
    #if os.path.isfile("Archive\\PiggyBank_Archive_20150410.csv"):
        start = datetime.datetime.now()
        print "Rebuilding Piggy Bank"
        rebuildPiggyBank(user_id,password)
        print "Rebuilding Override Record"
        rebuildOverrideRecord(user_id,password)
        piggybank_file = open("Archive\\PiggyBank_Archive_20150410.csv", "r")
        piggybank = csv.DictReader(piggybank_file)
        failed_file = open("Archive\\Failed_Archive_20150410.csv", "w")
        failed = csv.DictWriter(failed_file, getPiggyBankKeys())
        unknownfailure = open("Archive\\UFailed_Archive_20150410.csv", "w")
        Ufailed = csv.DictWriter(unknownfailure, getPiggyBankKeys())
        counter = 0
        success_fsns = 0
        myst_fails = 0
        failed_fsns = 0

        for piggy_row in piggybank:
            counter += 1
            process_dict = piggy_row
            #build an SQL Command String to try uploading this information to the system?
            try_to_add = addToPiggyBank(process_dict, user_id, password)
            if try_to_add == "Override":
                fsn = process_dict["FSN"]
                report_date = OINKM.getDateFromString(process_dict["Article Date"], "YYYY-MM-DD")
                #print report_date
                override_status, override_count = checkForOverride(fsn, report_date, user_id, password)
                if not override_status:
                    addOverride(fsn, report_date, user_id, password)
                process_dict.update({"Rewrite Ticket": override_count+1})
                addToPiggyBank(process_dict, user_id, password)
                print "Successfully processed %d FSNs." %success_fsns
                success_fsns +=1
            elif try_to_add == "Failed":
                failed.writerow(process_dict)
                failed_fsns += 1
            elif try_to_add == True:
                print "Successfully processed %d FSNs." %success_fsns
                success_fsns +=1
            else:
                print "Mysterious failure."
                Ufailed.writerow(process_dict)
                myst_fails +=1
        print "Populating names and email IDs."
        populate_email_and_names_in_piggy_bank(user_id, password)
        print "Populating Targets."
        populatePiggyBankTargets(user_id, password)
        print "Run Complete. Summary:\n%d succeeded. %d failed. Mysterious Failures %d\nTotal %d" %(success_fsns, failed_fsns, myst_fails,counter)
        print "Time spent: %s" % datetime.datetime.now() - start
    else:
        print "No entry data file available."

def getPiggyBankKeys():
    keys = [
        "Article Date", "WriterID", "Writer Email ID", "Writer Name", 
        "FSN", "Description Type", "Source",  "BU", "Super-Category",  
        "Category", "Sub-Category", "Vertical",
        "Brand", "Word Count",  "Upload Link",
        "Reference Link",  "Start Time",  "End Time",
        "Modification Time", "PC User Name", "Upload Date", "Item ID", 
        "Job Ticket", "Target", "Rewrite Ticket"
        ]
    return keys

def rebuildEmployeesTable(user_id, password):
    """Rebuilds the employee table in the database."""
    employeedb = getOINKConnector(user_id, password)
    empcursor = employeedb.cursor()
    sqlcmdstring = "DROP TABLE IF EXISTS `employees`;"
    empcursor.execute(sqlcmdstring)
    sqlcmdstring = """CREATE TABLE `employees` (
`Employee ID` VARCHAR(15) NOT NULL,
`Name` VARCHAR(50) NOT NULL,
`Email ID` VARCHAR(50) NOT NULL,
`DOJ` DATE NOT NULL,
`DOL` DATE,
`Role` VARCHAR(30) NOT NULL,
`Band` VARCHAR(5),
`Date of Promotion` DATE,
`Former Role` VARCHAR(30),
PRIMARY KEY (`Employee ID`)
);
"""
    #print sqlcmdstring #debug
    empcursor.execute(sqlcmdstring)
    employeedb.commit()
    employeedb.close()
    
def uploadEmployeesTable(user_id, password):
    """Uploads the employees table from a csv file into the server."""
    rebuildEmployeesTable(user_id, password)
    employeedb = getOINKConnector(user_id, password)
    empcursor = employeedb.cursor()
    sqlcmdstring = """LOAD DATA LOCAL INFILE 
'Database/employeetable.csv' INTO TABLE %s.employees FIELDS 
TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;""" %getDBName()
    #print sqlcmdstring #debug
    empcursor.execute(sqlcmdstring)
    employeedb.commit()
    employeedb.close()
    

def uploadFSNDump(user_id,password):
    """Creates the fsndata table, and loads all the data into it."""
    fsndumpdb = getOINKConnector(user_id, password)
    fsncursor = fsndumpdb.cursor()
    sqlcmdstring="DROP TABLE IF EXISTS `fsndump`;"
    fsncursor.execute(sqlcmdstring)
    #print "Deleted the old FSN Dump table." #debug
    sqlcmdstring = "CREATE TABLE `fsndump` (`FSN` varchar(30) NOT NULL, `Description Type` Enum('Regular Description','Rich Product Description'),PRIMARY KEY (`FSN`,`description type`))"
    fsncursor.execute(sqlcmdstring)
    #print "Created the new table." #debug
    sqlcmdstring = "LOAD DATA LOCAL INFILE 'Database/fsndump.csv' INTO TABLE `fsndump` FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    fsncursor.execute(sqlcmdstring)
    #FIX
    #find a way to output how much time was spent on this.
    #print "Uploaded data." #debug
    fsndumpdb.commit()
    fsndumpdb.close()

def rebuildCategoryTree(user_id,password):
    """This method drops the current Category Tree and redefines it."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "DROP TABLE IF EXISTS `categorytree`;"
    dbcursor.execute(sqlcmdstring)
    sqlcmdstring = """CREATE TABLE `categorytree` (
`BU` VARCHAR(30) NOT NULL DEFAULT '',
`Super-Category` VARCHAR(30) NOT NULL DEFAULT '',
`Category` VARCHAR(30) NOT NULL DEFAULT '',
`Sub-Category` VARCHAR(30) NOT NULL DEFAULT '',
`Vertical` VARCHAR(100) NOT NULL DEFAULT '',
`Source` ENUM('Inhouse','Crowdsourced') NOT NULL DEFAULT "Inhouse",
`Description Type` ENUM('Regular Description','Rich Product Description','Rich Product Description Plan A', 'Rich Product Description Plan B','SEO Big', 'SEO Small', 'SEO Project','RPD Updation','RPD Variant') NOT NULL DEFAULT "Regular Description",
`Revision Date` DATE NOT NULL,
`Target` INT(3) NOT NULL,

PRIMARY KEY (`BU`,`Super-Category`,`Category`,`Sub-Category`,`Vertical`,
`Source`, `Description Type`, `Revision Date`)
);"""
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def uploadCategoryTree(user_id,password):
    rebuildCategoryTree(user_id,password)
    connectdb = getOINKConnector(user_id, password)

    dbcursor=connectdb.cursor()
    sqlcmdstring="""LOAD DATA LOCAL INFILE 'Database/categorytree.csv' INTO 
TABLE `categorytree` FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES"""
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def rebuildCosting(user_id,password):
    """This method drops the current Category Tree and redefines it."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "DROP TABLE IF EXISTS `costing`;"
    dbcursor.execute(sqlcmdstring)
    sqlcmdstring = """CREATE TABLE `costing` (
`Role` VARCHAR(10) NOT NULL,
`Band` VARCHAR(5),
`Avg. CTC` INT(30),
`Admin Cost` INT(30),
`Total Cost` INT(50),
PRIMARY KEY (`Role`)
)"""
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def initUsers(user_id, password):
    """Loops through the employees table and creates a user_id for each of the
    users listed."""
    for employee in getEmployeesList(user_id, password):
        createUser(employee["Employee ID"],employee["Role"],user_id,password)
        #resetPassword(employee["Employee ID"], user_id, password)
    return True

def rebuildWorkCalendar(user_id, password):
    connectdb = getOINKConnector(user_id, password)
    dbcursor=connectdb.cursor()
    sqlcmdstring="DROP TABLE IF EXISTS `workcalendar`;"
    dbcursor.execute(sqlcmdstring)
    sqlcmdstring ="""CREATE TABLE `workcalendar` (
    `Date` DATE NOT NULL,
    `Employee ID` VARCHAR(20) NOT NULL,
    `Status` ENUM('Working','Leave','Planned Leave','Sick Leave','Emergency Leave','Company Holiday') NULL DEFAULT 'Working',
    `Relaxation` FLOAT(3,2) NULL DEFAULT '0.00',
    `Entered By` VARCHAR(20) NULL DEFAULT NULL,
    `Comment` VARCHAR(500) NULL DEFAULT NULL,
    `Approval` ENUM('Approved','Pending','Rejected') NULL DEFAULT NULL,
    `Reviewed By` VARCHAR(20) NULL DEFAULT NULL,
    `Rejection Comment` VARCHAR(500) NULL DEFAULT NULL,
    `Efficiency` FLOAT NULL DEFAULT NULL,
    `CFM` FLOAT NULL DEFAULT NULL,
    `GSEO` FLOAT NULL DEFAULT NULL,
    `Posting Time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `Modification Time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`Date`, `Employee ID`)
)"""
#    print sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def uploadWorkCalendar(user_id,password):
    """Uploads all the data in the work calendar csv file into the database."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "LOAD DATA LOCAL INFILE 'Database/workcalendar.csv' INTO TABLE oink.workcalendar FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES;"
#    print sqlcmdstring
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def initiateDatabase():
    """This module initializes the server for use."""
    #if "V.I.N.D.A.L.O.O" in os.getcwd():
    user_id, password = getBigbrotherCredentials()
    print "Creating a new Raw Data table and uploading new data."
    uploadRawData(user_id,password)
    print "Creating a new piggy bank dump and uploading new data."
    uploadPiggyBank(user_id,password)
    print "Creating a new FSN Dump and uploading the new data."
    uploadFSNDump(user_id, password)
    print "Creating a new employee table and uploading the new data."
    uploadEmployeesTable(user_id,password)
    print "Creating a new category tree and uploading the new data."
    uploadCategoryTree(user_id,password)
    print "Creating the costing table."
    rebuildCosting(user_id,password)
    print "Creating the Work Calendar table."
    rebuildWorkCalendar(user_id,password)
    print "Uploading the Work Calendar table."
    uploadWorkCalendar(user_id,password)
    print "Creating a new clarifications table and uploading the table."
    rebuildClarifications(user_id, password)
    uploadClarifications(user_id, password)
    print "Creating the required users."
    initUsers(user_id,password)
    print "Creating a new Override table and uploading the table."
    rebuildOverideRecord(user_id, password)

def rebuildOverrideRecord(user_id, password):
    """Rebuilds the overriderecord table in the database"""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "DROP TABLE IF EXISTS `overriderecord`;"
    dbcursor.execute(sqlcmdstring)
    sqlcmdstring = """CREATE TABLE `overriderecord` (
`FSN` VARCHAR(200) NOT NULL,
`Override Date` DATE NOT NULL,
`Overridden By` VARCHAR(100) NOT NULL,
PRIMARY KEY (`FSN`, `Override Date`)
);"""
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def populatePiggyBankTargets(user_id, password):
    """Populates the Piggy Bank table with targets in the target column."""
    connectdb = getOINKConnector(user_id, password)
    startTime = datetime.datetime.now()
    dbcursor = connectdb.cursor()
    sqlcmdstring = """SELECT * FROM `piggybank` WHERE `Target`='-1' OR `Target`="0";"""
    dbcursor.execute(sqlcmdstring)
    piggybank_data = dbcursor.fetchall()
    total = len(piggybank_data)
    counter = 1
    start_time = datetime.datetime.now()
    print "Entries to be processed: ", total
    for piggy_entry in piggybank_data:
        if counter == 1 or counter%(10)==0:
            print "%d/%d" % (counter,total)
            print "ETA: %s"% getETA(start_time, counter, total)
        counter += 1
        time.sleep(0.05)
        target = getTargetForPiggyBankRow(user_id, password, piggy_entry)
        print target
        sqlcmdstring = """UPDATE `piggybank` SET `target` = "%d" WHERE `Article Date` = "%s" AND `FSN` = "%s" AND `Description Type` = "%s" AND `WriterID` = "%s";""" % \
            (target, piggy_entry["Article Date"], piggy_entry["FSN"], piggy_entry["Description Type"], piggy_entry["WriterID"])
        #print sqlcmdstring
        dbcursor.execute(sqlcmdstring)
        connectdb.commit()
    endTime = datetime.datetime.now()
    timeSpent = endTime - startTime
    print "Completed. Time spent: ", timeSpent
    connectdb.close()
    
def getTargetForPiggyBankRow(user_id, password, query_dict):
    """Gets the target given a Piggy Bank dictionary."""
    piggy_row = {
        "Description Type": query_dict["Description Type"],
        "Source": query_dict["Source"],
        "BU": query_dict["BU"],
        "Super-Category": query_dict["Super-Category"],
        "Category": query_dict["Category"],
        "Sub-Category": query_dict["Sub-Category"],
        "Vertical": query_dict["Vertical"]
    }
    target = getTargetFor(user_id, password, piggy_row, query_dict["Article Date"])
    return target

def rebuildTeamCalendar(user_id, password):
    """This method redefines the team calendar, which contains details about all the holidays, special holidays etc for the team.
    """
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "DROP TABLE IF EXISTS `teamcalendar`;"
    dbcursor.execute(sqlcmdstring)
    sqlcmdstring = """CREATE TABLE `teamcalendar` (
`Record Date` DATE NOT NULL,
`Work Status` ENUM ('Holiday','Special Holiday') NOT NULL,
`Comments` VARCHAR(300)
);
"""
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def uploadTeamCalendar(user_id, password):
    """Upload the holidays list."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "LOAD DATA LOCAL INFILE 'Database/teamcalendar.csv' INTO TABLE oink.teamcalendar FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES;"
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def rebuildClarificationsTracker(user_id, password):
    """This method creates a new clarification tracker."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "DROP TABLE IF EXISTS `clarifications`;"
    dbcursor.execute(sqlcmdstring)
    sqlcmdstring = """CREATE TABLE `clarifications` (
`Posting Date` DATE NOT NULL,
`Poster ID` VARCHAR(50) NOT NULL,
`Poster Name` VARCHAR(50),
`Poster Email ID` VARCHAR(50),
`FSN` VARCHAR(100) NOT NULL,
`Code` VARCHAR(30) NOT NULL,
`Comments` VARCHAR(300),
`Check Status` ENUM('Pending', 'Cleared', 'No Change Required', 'Escalated'),
`Checked By` VARCHAR(50),
`Check Date` DATE
);
"""
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def getClarifications(user_id, password):
    """Returns a list of all the clarifications."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT `Code` FROM clarifications"
    dbcursor.execute(sqlcmdstring)
    clarTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    clarList = [clar["Code"] for clar in clarTuple]
    return clarList

def initWorkCalendar(user_id, password, start_date, end_date):
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    employeesData = getEmployeesList(user_id, password, end_date)
    employeesList = [employee["Employee ID"] for employee in employeesData]
    total_employees = len(employeesList)
    #print total_employees
    start_time = datetime.datetime.now()
    last_update_time = start_time
    dates_ = OINKM.getDatesBetween(start_date, end_date)
    #print dates_
    total = len(writers_list) * len(dates_)
    counter = 1
    start_time = datetime.datetime.now()
    last_update_time = datetime.datetime.now()
    
    for process_date in dates_:
        #print "Trying."
        for employeeID in employeesList:
            if not OINKM.isWeekend(process_date):
                sqlcmdstring = "INSERT INTO `workcalendar` (`Date`, `Employee ID`,  `Status`, `Relaxation`, `Entered By`) VALUES ('%s', '%s', 'Working', '0.00', 'Big Brother')" % (convertToMySQLDate(process_date), employeeID)
                try:
                    dbcursor.execute(sqlcmdstring)
                    if ((datetime.datetime.now() - last_update_time) >= datetime.timedelta(seconds=60)):
                        print "Processed work information for %s for %s." %(employeeID, process_date)
                        last_update_time = datetime.datetime.now()
                except MySQLdb.IntegrityError:
                    #print "Duplicate"
                    pass
    connectdb.commit()
    connectdb.close()


def rebuildAuditScoreSheet(user_id, password):
    """This redefines the audit score sheet on the database."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """DROP TABLE IF EXISTS `auditscoresheet`;"""
    dbcursor.execute(sqlcmdstring)
    sqlcmdstring = """CREATE TABLE `auditscoresheet` (
`Revision Date` DATE NOT NULL,
`Parameter Class` ENUM('CFM', 'GSEO') NOT NULL,
`Parameter Class Index` INT(3) NOT NULL,
`Column Descriptions` VARCHAR(200) NOT NULL,
`Maximum Score` INT(3) NOT NULL,
`Weightage` FLOAT(10,9) NOT NULL,
`Rating Type` ENUM('Subjective', 'Quantified', 'Mandatory'),
`Rating Levels` ENUM('2', '3',' 5'),
PRIMARY KEY (`Revision Date`, `Parameter Class`, `Parameter Class Index`)
);"""
    #print sqlcmdstring
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def uploadAuditScoreSheet(user_id, password):
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """LOAD DATA LOCAL INFILE 'Database/auditscoresheet.csv' INTO TABLE `auditscoresheet` FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';"""
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()
    
def getRawDataTableAndAuditParameters(user_id=None, password=None, query_date=None):
    raw_data_table = 'rawdata'
    CFM = ["CFM01","CFM02","CFM03","CFM04","CFM05","CFM06","CFM07","CFM08"]
    GSEO = ["GSEO01","GSEO02","GSEO03","GSEO04","GSEO05","GSEO06","GSEO07"]
    return raw_data_table, CFM, GSEO

#########################################################################
#Regular methods
#These methods are regularly used while running the application.
#########################################################################

def regularmethods():
    """Regular methods."""
    print "This section is for regular methods."

def isHoliday(user_id, password, query_date):
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "Select * from `teamcalendar` WHERE `Record Date` = '%s'" % convertToMySQLDate(query_date)
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()        
    
    if len(data) == 0:
        status = False
        comment = "NA"
    else:
        status = True
        comment = data[0]["Comments"]

    return status, comment

def isWorkingDay(user_id, password, queryDate):
    """Method to check if the company is working on a particular date.
    """
    return not (OINKM.isWeekend(queryDate) or isHoliday(user_id, password, queryDate)[0])


def getWorkingDatesLists(query_date, group_size=None, quantity=None):
    user_id, password = getBigbrotherCredentials()
    if group_size is None:
        group_size = 1
    if quantity is None:
        quantity = 5
    dates_list = []
    required_no_of_working_dates = group_size * quantity
    no_of_working_dates = 0
    processing_date = query_date    
    while no_of_working_dates < required_no_of_working_dates:
        if isWorkingDay(user_id, password, processing_date):
            dates_list.append(processing_date)
            no_of_working_dates += 1
        processing_date -= datetime.timedelta(days=1)

    dates_lists = [[dates_list.pop() for y in range(group_size)] for x in range(quantity)]
    for dates_ in dates_list:
        dates_.sort()
    dates_list.sort()
    return dates_lists

def updatePiggyBankEntry(entry_dict, user_id, password):
    """Method to update the values in an entry in the piggybank. This cross-checks the FSN with the date. 
    possible bugs: 1. It will not allow updation of date, writerID or FSN.
    """
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """UPDATE `piggybank` SET `Source` = '%(Source)s', 
`Description Type` = '%(Description Type)s', `BU` = '%(BU)s', `Super-Category` = '%(Super-Category)s', 
`Category` = '%(Category)s', `Sub-Category` = '%(Sub-Category)s', `Vertical` = '%(Vertical)s', 
`Brand` = '%(Brand)s', `Word Count` = '%(Word Count)s', `Upload Link` = '%(Upload Link)s', 
`Reference Link` = '%(Reference Link)s', `Rewrite Ticket` = '%(Rewrite Ticket)s'
WHERE `FSN` = '%(FSN)s' AND `Article Date` = '%(Article Date)s' 
AND `WriterID` = '%(WriterID)s';""" % entry_dict
    try:
        dbcursor.execute(sqlcmdstring)
    except Exception, e:
        print "Unknown error while trying to upload piggybank."
        print "The command string is:\n%s" % sqlcmdstring
        print "The error is: ", repr(e)
    connectdb.commit()
    connectdb.close()

def addToPiggyBank(piggyBankDict, user_id, password):
    """Method to send a single entry to Piggy Bank from a
    python Dictionary"""
    #test dictionary
    #merge all keys and values names into one string, separated by commas.
    columnsList, valuesList = getDictStrings(piggyBankDict)
    #rebuildPiggyBank(user_id, password)
    piggybankdb = getOINKConnector(user_id, password)
    piggycursor = piggybankdb.cursor()
    sqlcmdstring = "INSERT INTO `piggybank` (%s) VALUES (%s);" % (columnsList, valuesList)
    #print sqlcmdstring #debug
    try:
        piggycursor.execute(sqlcmdstring)
        returnValue = True
    except MySQLdb.IntegrityError:
        #error = "Duplicate entry not possible. Request repeat instance approval."
        #print error
        #Raising this in order to increase rewrite ticket 1.
        returnValue = "Override"
    except Exception, e:
        error = repr(e)
        print error
        returnValue = "Failed" 
    piggybankdb.commit()
    piggybankdb.close()
    return returnValue

def getDictStrings(inputDict):
    """Takes any dictionary and returns a comma separated string of the 
    keys and the corresponding values."""
    keysHolder = inputDict.keys()
    keysString = []
    for key in keysHolder:
        if len(keysString) == 0:
            keysString = "`" + key + "`"
        else:
            keysString = keysString + ", `" + key + "`"

    valuesHolder = inputDict.values()
    valuesString = []
    for value in valuesHolder:
        if len(valuesString) == 0:
            valuesString = '"' + value + '"'
        else:
            valuesString = valuesString + ', "' + str(value) + '"'
    return keysString, valuesString

def markCalendar(calendarEntryDict):
    """Method to mark an entry into the work calendar from a 
    python dictionary."""
    return True

def readFromPorkChops(queryDict,user_id,password):
    """Method to read data from Pork Chops and return all data for
    a query."""
    return True

def readFromPiggyBank(queryDict, user_id, password):
    """Method to read data from Piggy Bank and return all data for
    a query."""
    piggybankdb = getOINKConnector(user_id, password)
    piggycursor = piggybankdb.cursor()
    numberOfConditions = len(queryDict)

    #print "There are %d conditions!" % numberOfConditions #debug
    counter = 0
    sqlcmdstring = "SELECT * FROM piggybank WHERE "
    for key in queryDict:
        sqlcmdstring = sqlcmdstring + ("`%s` = '%s'" % (key, queryDict[key]))
        if counter < numberOfConditions-1:
            sqlcmdstring += " AND "
        else:
            sqlcmdstring += ";"
        counter +=1
    try:
        #print sqlcmdstring #debug
        piggycursor.execute(sqlcmdstring)
        results = piggycursor.fetchall()
        #print results #Debug
    except MySQLdb.ProgrammingError, e:
        print "Tried to run SQL Command: \n%s" % sqlcmdstring
        error = repr(e)
        print "Raised exception: %s" % error
        results = error
    except Exception, e:
        print "Tried to run SQL Command: \n%s" % sqlcmdstring
        error = repr(e)
        print "Raised exception: %s" % error
        results = error
    resultsList = []
    for tupleRow in results:
        resultsList.append(tupleRow)
    return resultsList

def getPiggyBankKeysInOrder():
    keys_list = ["Article Date", "WriterID", "Writer Name", "Writer Email ID", "FSN", "Description Type", "Source", "BU", "Super-Category", "Category", "Sub-Category", "Vertical", "Brand", "Word Count", "Upload Link", "Reference Link", "Rewrite Ticket"]
    return keys_list

def writePorkChopsDictToFile(porkChopsDict):
    """Method to bulk export Pork Chops data to a file for a query."""
    return True

def writePiggyBankDictToFile(queryDict):
    """Method to bulk export Piggy Bank data to a file for a query."""
    return True

def getPiggyBankDataBetweenDates(startDate, endDate, queryDict, user_id, password):
    """Method to extract Piggy Bank data from the database in between
    two dates and corresponding to a query.
    The dates here are datetime dates.
    """
    #Get a list of dates.
    datesList = OINKM.getDatesBetween(startDate, endDate)
    #print datesList #Debug
    multiQueryDict = []
    counter = 0
    for eachDate in datesList:
        #print convertToMySQLDate(eachDate)[0] #debug
        #doing this because the 
        #function returns a list, irrespective of the number of items. 
        #2015-01-01 is returned as ['2015-01-01']
        #Convert each entry in the dates to MySQL compliant dates.
        if counter == 0:
            queryDict.update({"Article Date": convertToMySQLDate(eachDate)})
        else:
            queryDict["Article Date"] = convertToMySQLDate(eachDate)
        counter += 1
        #print queryDict #debug
        #Create a list of query dictionaries, with varying dates.
        multiQueryDict.append(queryDict.copy()) #create a shallow copy, 
        #lists in python are live links to the objects they reference.
    #print multiQueryDict
    #feed the dictionary to the getPiggyBankMultiQuery()
    return getPiggyBankMultiQuery(multiQueryDict, user_id, password)

def convertToMySQLDate(queryDate):
    """Takes a python datetime and changes it to the YYYY-MM-DD format 
    for MySQL. 
    Uses the OINKModule2 module's changeDatesToStrings method."""
    dateString = OINKM.changeDatesToStrings(queryDate,"YYYY-MM-DD")
    return dateString[0]

def getPiggyBankMultiQuery(queryDictList, user_id, password):
    """Method to extract Piggy Bank data from the database corresponding
    to multiple queries."""
    #Breaks down the list into separate dictionaries, and then feeds each 
    #query dictionary to the appropriate method, collects the answers and 
    #returns that.
    resultList = []
    for query in queryDictList:
        if type(query) == type({}):
            #print query #debug
            resultList.append(readFromPiggyBank(query, user_id, password))
        else:
            print "Unknown query, printing verbatim.\n%s" % query
    #print resultList
    return resultList

def createUser(newuser_id, userClass, user_id, password):
    """This method creates a new user with appropriate permissions 
    according to the userClass."""
    dbname = getDBName()
    connecteddb = getOINKConnector(user_id, password)
    dbcursor = connecteddb.cursor()
    sqlcmdstring = "CREATE USER '%s' IDENTIFIED BY 'password'" %newuser_id
    try:
        dbcursor.execute(sqlcmdstring)
    except MySQLdb.OperationalError, e:
        if newuser_id in getUsersList(user_id, password):
            print "There is already a user defined by %s, please contact bigbrother." %newuser_id
        else:
            print "Unknown Error!"
            error = repr(e)
            print error
    if userClass == "Content Writer":
        sqlcmdstring = "GRANT SELECT on %s.* TO '%s';" % (dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT ON %s.workcalendar To '%s';" %(dbname, newuser_id)
        #print sqlcmdstring #debug
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT ON %s.clarifications To '%s';" %(dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT ON %s.loginrecord To '%s';" %(dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT, DELETE ON %s.piggybank To '%s';" %(dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
    elif userClass == "Copy Editor":
        sqlcmdstring = "GRANT SELECT on %s.* TO '%s';" % (dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT ON %s.loginrecord To '%s';" %(dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT ON %s.clarifications To '%s';" %(dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT, DELETE ON %s.rawdata To '%s';" %(dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
    elif userClass in ["Team Lead", "Assistant Manager", "Manager"]:
        sqlcmdstring = "GRANT SELECT on %s.* TO '%s';" % (dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT ON %s.clarifications To '%s';" %(dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT ON %s.loginrecord To '%s';" %(dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT, DELETE ON %s.workcalendar To '%s';" %(dbname, newuser_id)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)      
    elif userClass == "Super":
        #print sqlcmdstring #debug
        sqlcmdstring = "GRANT ALL PRIVILEGES ON %s.* To '%s' WITH GRANT OPTION;" %(dbname, newuser_id)
    else:
        print "Wrong user class. Cannot set privileges for %s." % userClass
    connecteddb.commit()
    connecteddb.close()

def getUsersList(user_id, password):
    #Cannot use getOINKConnector() here, as the db which has the users list is mysql, not oink.
    superdb = MySQLdb.connect(host=getHostID(), user=user_id, passwd=password, db="mysql", cursorclass=MySQLdb.cursors.DictCursor)
    supercursor = superdb.cursor()
    sqlcmdstring = "SELECT user from user"
    supercursor.execute(sqlcmdstring)
    usersTuples = supercursor.fetchall()
    superdb.commit()
    superdb.close()
    usersList = []
    for userTuple in usersTuples:
        usersList.append(userTuple["user"])
    #print usersList #debug
    return usersList

def addEmployee(employeeDict, user_id, password):
    """Takes a dictionary with employee data. The fields are Employee ID, Name, Email-ID, DOJ and Current Class"""
    employeesdb = getOINKConnector(user_id, password)
    empcursor = employeesdb.cursor()
    keysString, valuesString = getDictStrings(employeeDict)
    sqlcmdstring = "INSERT INTO `employees` (%s) VALUES (%s);" % (keysString,valuesString)
    print sqlcmdstring
    try:
        empcursor.execute(sqlcmdstring)
        createUser(employeeDict["Employee ID"],employeeDict["Role"],user_id,password)
    except MySQLdb.ProgrammingError, e:
        if employeeDict["Employee ID"] in getEmployeeIDsList(user_id,password):
            print "There is already an employee with that ID."
        else:
            error = repr(e)
            print error
    except Exception, e:
        error = repr(e)
        print error
        raise
    employeesdb.commit()
    employeesdb.close()
    return True

def getCurrentEmployeesList(user_id, password, query_date):
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    date_string = convertToMySQLDate(query_date)
    sqlcmdstring = """SELECT * from `employees` WHERE `DOJ`<="{0}" AND (`DOL` IS NULL OR `DOL` >= "{0}");""".format(date_string)
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    conn.close()
    return data
    
def getEmployeeIDsList(user_id,password):
    """Returns a list of all the employees IDs currently in the table.
    Returns a list of dictionaries of IDs and the roles."""
    employeesdb = getOINKConnector(user_id, password)
    empcursor = employeesdb.cursor()
    sqlcmdstring = "SELECT `Employee ID` FROM employees"
    empcursor.execute(sqlcmdstring)
    employeesTuple = empcursor.fetchall()
    employeesList = []
    for employeeTuple in employeeTuples:
            employeesList.append(employeesTuple["employee id"])
    employeesdb.commit()
    employeesdb.close()
    return employeesList

def getEmployeesList(user_id, password, query_date=None):
    """Returns a list of dictionaries containing employee details."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor=connectdb.cursor()
    if query_date is None:
        sqlcmdstring="SELECT * from `employees`;"
    else:
        sqlcmdstring = """SELECT * from `employees` WHERE `DOJ`<="%s" AND (`DOL`>"%s" OR `DOL` IS NULL);"""%(query_date, query_date)
    #print sqlcmdstring
    dbcursor.execute(sqlcmdstring)
    employeesData=dbcursor.fetchall()
    #print employeesData
    connectdb.commit()
    connectdb.close()
    return employeesData

def getWritersList(user_id, password, queryDate = None):
    """Returns a list of dictionaries that pertain to writer information."""
    employees_data_list = getEmployeesList(user_id, password)
    writers_data_list = []
    for employee in employees_data_list:
        if employee["Role"] == "Content Writer":
            if queryDate == None:
                writers_data_list.append(employee)
            elif (queryDate >= employee["DOJ"]):
                if employee["DOL"] == None:
                    writers_data_list.append(employee)
                elif (queryDate <= employee["DOL"]):
                    writers_data_list.append(employee)
                #if a particular date is fed to the system, then check if the writer 
                #has joined on or after the request date, and if he/she has left 
                #after that date (i.e. he/she is still working in that team)
            #Fix this later
        #Limitation: Right now, this doesn't take promotions into account. 
        #Later, the code will need to look at the current role and former role.
    return writers_data_list

def checkuser_id(user_id):
    superID, superPassword = getBigbrotherCredentials()
    return user_id in getUsersList(superID, superPassword)

def checkPassword(user_id,password):
    success, error = False, "Unchecked"
    if checkuser_id(user_id):
        try:
            oinkdb = getOINKConnector(user_id, password)
            oinkCursor = oinkdb.cursor()
            oinkdb.commit()
            oinkdb.close()
            success = True
            error = None
        except Exception, e:
            error = getSQLErrorType(repr(e))
            print error
    else:
        success,error = False,"User ID does not exist."
    return success,error

def getBigbrotherCredentials():
    import codecs
    user_id = "bigbrother"
    password = str(codecs.decode('bejryy',"rot_13")) #using the rot_13 encryption method to hide password.
    #print password #debug
    return user_id, password

def getEmpName(employeeID):
    user_id, password = getBigbrotherCredentials()
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT `Name` FROM `employees` WHERE `Employee ID` = '%s'" %employeeID
    dbcursor.execute(sqlcmdstring)
    nameTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    name = nameTuple[0]["Name"]
    return name

def getEmpEmailID(employeeID):
    user_id, password = getBigbrotherCredentials()
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT `Email ID` FROM `employees` WHERE `Employee ID` = '%s';" %employeeID
    dbcursor.execute(sqlcmdstring)
    nameTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    name = nameTuple[0]["Email ID"]
    return name

def resetOwnPassword(user_id, password, newpassword):
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SET PASSWORD = PASSWORD('%s');" %newpassword
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()
    return True

def resetPassword(user_To_Reset, user_id, password):
    """Resets the password of user_To_Reset to 'password'."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor=connectdb.cursor()
    sqlcmdstring="SET PASSWORD FOR `%s` = PASSWORD('password');" %user_To_Reset
    print "Resetting password for ", user_To_Reset
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def getPiggyBankDataForDate(queryDate, user_id, password):
    return getPiggyBankDataBetweenDates(queryDate, queryDate, {}, user_id, password)

def getUserPiggyBankData(queryDate, user_id, password, queryUser = None):
    #print "In getUserPiggyBankData"
    if queryUser == None:
        queryUser = user_id
    queryDict = {"WriterID" : queryUser}
    return getPiggyBankDataBetweenDates(queryDate, \
                queryDate ,queryDict ,user_id ,password)[0]


#DONT USE THIS!
def getWorkingStatus(user_id, password, querydate, lookupuser=None):#DONT USE THIS!
    #DONT USE THIS!#DONT USE THIS!#DONT USE THIS!#DONT USE THIS!#DONT USE THIS!#DONT USE THIS!#DONT USE THIS!
    """Method to fetch the status for a writer on any particular date.
    Returns "Working" if the employee is delivering 100%.
    Returns "Leave" if the employee is on leave.
    Returns n/10 if the employee is granted a relaxation of n%
    Returns "Holiday" if the company has granted a holiday on a particular date.
    Returns False if there's no information.
    If lookupuser isn't specified, it'll just pull the status for the current user.
    """

    #DONT USE THIS!#DONT USE THIS!#DONT USE THIS!#DONT USE THIS!#DONT USE THIS!
    #DONT USE THIS!#DONT USE THIS!#DONT USE THIS!#DONT USE THIS!#DONT USE THIS!#DONT USE THIS!
    status = "Working"
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    if lookupuser is None:
        lookupuser = user_id
    sqlcmdstring = "SELECT `Status`, `Relaxation` FROM `workcalendar` WHERE `Date` = '%s' AND `Employee ID` = '%s';" % (convertToMySQLDate(querydate),lookupuser)
    #print sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()
    #print data
    if len(data) != 0:
        status = data[0]["Status"]
        relaxation = data[0]["Relaxation"]
        return status, relaxation
    else:
        return False, 0

def checkWorkStatus(user_id, password,queryDate, targetUser = None):
    """This method checks the work calendar in the database and checks whether the employee is 
    working or not on that particular date."""
    #print "In checkWorkStatus"
    if targetUser is None:
        targetUser = user_id
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT * FROM `workcalendar` WHERE `Employee ID` = '%s' AND `Date` = '%s'" %(targetUser, convertToMySQLDate(queryDate))
    #print sqlcmdstring
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    #print data
    try:
        data = data[0]
        status = data["Status"]
        relaxation = data["Relaxation"]
        approval = data["Approval"]
    except Exception, e:
        status = "Working"
        relaxation = 0.0
        approval = "Approved"
        #print "Unknown error in MOSES.checkWorkStatus.\nPrinting verbatim:\n%s" % repr(e)
    #print status, relaxation, approval
    #print "Leaving checkWorkStatus"
    return status, relaxation, approval

def getWorkingDatesBetween(user_id, password, start_date, end_date, query_user = None, mode = None):
    """Given two dates, it returns the working dates between two given dates for the requesting user. 
    If the mode is set to "All", it will procure a list of non-working days for the company."""
    if query_user is None:
        query_user = user_id
    if mode is None:
        mode = "Self"
    date_range = OINKM.getDatesBetween(start_date, end_date)
    #print date_range
    working_dates = []
    for each_date in date_range:
        if isWorkingDay(user_id, password, each_date):
            if mode == "All":
                working_dates.append(each_date)
            elif mode == "Self":
                status = checkWorkStatus(user_id, password, each_date, query_user)
                #print status
                if status[0] == "Working":
                    working_dates.append(each_date)
    return working_dates

def buildWritersDataFile():
    u, p = getBigbrotherCredentials()
    start_date = datetime.date(2015,1,1)
    end_date = datetime.date.today()
    dates_list = OINKM.getDatesBetween(start_date, end_date)
    start_time = datetime.datetime.now()
    output_file_name = "DataFile_%s.csv"%convertToMySQLDate(start_date)
    output_file = open(output_file_name, "w")
    data = {"Date":None,"Writer ID":None, "Writer Email ID":None, "Writer Name":None, "Status":None,"Relaxation":None, "Efficiency":None,"CFM":None,"GSEO":None, "Article Count": None}
    
    keys = data.keys()
    output = csv.DictWriter(output_file, keys)
    output.writerow(dict((key, key) for key in keys))
    counter = 0
    total = len(dates_list)
    for each_date in dates_list:
        counter += 1
        if isWorkingDay(u, p, each_date):
            print "Beginning processing for %s.\n%d dates processed. %d remaining.\nETA: %s" % (each_date, counter, (total-counter),getETA(start_time, counter, total))
            writers_list = getWritersList(u, p, each_date)
            for writer in writers_list:
                writer_id = writer["Employee ID"]
                writer_name = writer["Name"]
                print "Processing %s's data for %s." %(writer_name, each_date)
                status, relaxation, approval = checkWorkStatus(u, p, each_date, writer_id)
                data = {
                    "Date": each_date,
                    "Writer ID": writer_id, 
                    "Writer Email ID": writer["Email ID"], 
                    "Writer Name": writer_name, 
                    "Status": status,
                    "Relaxation": relaxation,
                    "Efficiency": getEfficiencyFor(u, p, each_date, writer_id),
                    "CFM": getCFMFor(u, p, each_date, writer_id),
                    "GSEO":getGSEOFor(u, p, each_date, writer_id),
                    "Article Count": getArticleCount(u, p, each_date, writer_id)
                    }
                output.writerow(data)
                time.sleep(5)
    print "Completed. Start Time: %s, End Time: %s" % (start_time,datetime.datetime.now())
    output_file.close()

def getETA(start_time, counter, total):
    #from __future__ import division
    now = datetime.datetime.now()
    time_spent = now - start_time
    mean_time = time_spent.total_seconds()/counter
    ETA = start_time + datetime.timedelta(seconds=(mean_time*total))
    return ETA

def getArticleCount(user_id, password, query_date, query_user=None):
    if query_user == None:
        query_user = user_id
    return getArticleCountBetween(user_id, password, query_date, query_date, query_user)

def getArticleCountBetween(user_id, password, start_date, end_date, query_user = None):
    if query_user == None:
        query_user = user_id
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """SELECT COUNT(*) from piggybank WHERE `Article Date` BETWEEN "%s" AND "%s" AND `WriterID`="%s";""" %(convertToMySQLDate(start_date), convertToMySQLDate(end_date), query_user)
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    conn.close()
    return int(data[0]["COUNT(*)"])

def getArticleCountForWeek(user_id, password, query_date, query_user=None):
    """"""
    if query_user is None:
        query_user = user_id
    current_day = query_date.isocalendar()[2]
    #Get the date of the monday in that week. Week ends on Sunday.
    subtractor = current_day - 1
    first_day_of_the_week = query_date - datetime.timedelta(subtractor)
    article_count = getArticleCountBetween(user_id, password, first_day_of_the_week, query_date, query_user)
    return article_count

def getArticleCountForMonth(user_id, password, query_date, query_user=None):
    """"""
    if query_user is None:
        query_user = user_id
    first_day_of_the_month = datetime.date(query_date.year, query_date.month, 1)
    article_count = getArticleCountBetween(user_id, password, first_day_of_the_month, query_date, query_user)
    return article_count

def getArticleCountForQuarter(user_id, password, query_date, query_user=None):
    """"""
    if query_user is None:
        query_user = user_id
    query_month = query_date.month
    quarter_first_month_mapped_dictionary = {
        1: 1, 2: 1, 3: 1,
        4: 4, 5: 4, 6: 4,
        7: 7, 8: 7, 9: 7,
        10: 10, 11: 10, 12: 10
    }
    first_month_of_the_quarter = quarter_first_month_mapped_dictionary[query_date.month]
    first_day_of_the_quarter = datetime.date(query_date.year, first_month_of_the_quarter, 1)
    article_count = getArticleCountBetween(user_id, password, first_day_of_the_quarter, query_date, query_user)
    return article_count

def getArticleCountForHalfYear(user_id, password, query_date, query_user=None):
    if query_user is None:
        query_user = user_id
    half_year_start_date = getHalfYearStartDate(query_date)

    return getArticleCountBetween(user_id, password, half_year_start_date, query_date, query_user)

def getAuditCount(user_id, password, query_date, query_user=None):
    if query_user == None:
        query_user = user_id
    return getAuditCountBetween(user_id, password, query_date, query_date, query_user)

def getAuditCountBetween(user_id, password, start_date, end_date, query_user = None):
    if query_user == None:
        query_user = user_id
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """SELECT COUNT(*) FROM rawdata WHERE `Audit Date` BETWEEN "%s" AND "%s" AND `WriterID`="%s";""" %(convertToMySQLDate(start_date), convertToMySQLDate(end_date), query_user)
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    conn.close()
    return data[0]["COUNT(*)"]

def getAuditCountForWeek(user_id, password, query_date, query_user = None):
    """"""
    if query_user is None:
        query_user = user_id
    current_day = query_date.isocalendar()[2]
    #Get the date of the monday in that week. Week ends on Sunday.
    subtractor = current_day - 1
    first_day_of_the_week = query_date - datetime.timedelta(subtractor)
    audit_count = getAuditCountBetween(user_id, password, first_day_of_the_week, query_date, query_user)
    return audit_count

def getAuditCountForMonth(user_id, password, query_date, query_user=None):
    """"""
    if query_user is None:
        query_user = user_id
    first_day_of_the_month = datetime.date(query_date.year, query_date.month, 1)
    audit_count = getAuditCountBetween(user_id, password, first_day_of_the_month, query_date, query_user)
    return audit_count

def getAuditCountForQuarter(user_id, password, query_date, query_user=None):
    """"""
    """"""
    if query_user is None:
        query_user = user_id
    query_month = query_date.month
    quarter_first_month_mapped_dictionary = {
        1: 1, 2: 1, 3: 1,
        4: 4, 5: 4, 6: 4,
        7: 7, 8: 7, 9: 7,
        10: 10, 11: 10, 12: 10
    }
    first_month_of_the_quarter = quarter_first_month_mapped_dictionary[query_date.month]
    first_day_of_the_quarter = datetime.date(query_date.year, first_month_of_the_quarter, 1)
    audit_count = getAuditCountBetween(user_id, password, first_day_of_the_quarter, query_date, query_user)
    return audit_count

def getAuditCountForHalfYear(user_id, password, query_date, query_user=None):
    if query_user is None:
        query_user = user_id
    half_year_start_date = getHalfYearStartDate(query_date)
    return getAuditCountBetween(user_id, password, half_year_start_date, query_date, query_user)


def getRawDataForDate(user_id, password, query_date, query_user=None):
    if query_user is None:
        query_user = user_id
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring ="""SELECT * FROM RAWDATA WHERE `WriterID` = "%s" and `Audit Date`="%s";""" %(query_user, convertToMySQLDate(query_date))
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def getWorkCalendarDataBetween(user_id, password, start_date, end_date, query_user=None):
    if query_user is None:
        query_user = user_id
    sqlcmdstring = """SELECT `Date`, `Status`,`Relaxation` from workcalendar where `Employee ID`="%s" and `Date` BETWEEN "%s" and "%s";""" %(query_user, start_date, end_date)
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    conn.close()
    return data

def getEfficiencyForDateRange(user_id, password, start_date, end_date, query_user=None):
    """
    For a given date range:
    1. Update the entire piggy bank table with the appropriate targets for each.
    2. Fetch the working dates for the query_user.
    3. Get the date-wise relaxation for the query_user.
    4. For all the dates before 11 May 2015, divide the total efficiency by the efficiency divisor.
    5. For all dates on or after 11 May, add the relaxation efficiency.
    """
    import numpy
    if query_user is None:
        query_user = user_id
    #get all piggybank data between these dates.
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """
    UPDATE piggybank SET piggybank.target = (
    SELECT target
    FROM categorytree
    WHERE 
    categorytree.`Revision Date` = (
    SELECT MAX(categorytree.`Revision Date`)
    FROM categorytree
    WHERE
    categorytree.`Revision Date` <= piggybank.`Article Date` AND categorytree.`Source`=piggybank.`Source` 
    AND categorytree.`BU`=piggybank.`BU` AND categorytree.`Description Type`= piggybank.`Description Type` AND
    categorytree.`Category` = piggybank.`Category` AND categorytree.`Super-Category`=piggybank.`Super-Category` AND
    categorytree.`Sub-Category` = piggybank.`Sub-Category` AND categorytree.`Vertical` = piggybank.`Vertical` AND
    categorytree.`Description Type` = piggybank.`Description Type`
    )  AND categorytree.`Source`=piggybank.`Source` 
    AND categorytree.`BU`=piggybank.`BU` AND categorytree.`Description Type`= piggybank.`Description Type` AND
    categorytree.`Category` = piggybank.`Category` AND categorytree.`Super-Category`=piggybank.`Super-Category` AND
    categorytree.`Sub-Category` = piggybank.`Sub-Category` AND categorytree.`Vertical` = piggybank.`Vertical` AND
    categorytree.`Description Type` = piggybank.`Description Type`
    ) WHERE
    piggybank.`Article Date` BETWEEN "%s" AND "%s" AND piggybank.`WriterID` = "%s";
    """ %(convertToMySQLDate(start_date), convertToMySQLDate(end_date), user_id)
    cursor.execute(sqlcmdstring)
    conn.commit()
    sqlcmdstring = """select * from `piggybank` WHERE 
    `WriterID`="%s" AND `Article Date` BETWEEN "%s" AND "%s";""" %(query_user, convertToMySQLDate(start_date), convertToMySQLDate(end_date))
    cursor.execute(sqlcmdstring)
    piggy_bank_data = cursor.fetchall()
    conn.close()
    #get all the dates during which a write is working.
    working_dates = getWorkingDatesBetween(user_id, password, start_date, end_date, query_user)
    work_calendar_data = getWorkCalendarDataBetween(user_id, password, start_date, end_date, query_user)
    working_dates = [entry["Date"] for entry in work_calendar_data if entry["Status"] == "Working"]
    #print "Found %d working dates." %len(working_dates)
    #build a dictionary for the writers which contains information at the date level.
    writer_dates_data = dict((date_,{}) for date_ in working_dates)
    for entry in work_calendar_data:
        if entry["Date"] in working_dates:
            date_ = entry["Date"]
            writer_dates_data[date_] = {
                            "Relaxation": entry["Relaxation"],
                            "Targets": []
            }
    #print writer_dates_data
    for piggy_entry in piggy_bank_data:
        entry_date = piggy_entry["Article Date"]
        target = piggy_entry["Target"]
        #target = getTargetForPiggyBankRow(user_id, password, piggy_entry)
        writer_dates_data[entry_date]["Targets"].append(target)
    #print writer_dates_data
    corrected_targets = []
    for date_ in working_dates:
        if date_< datetime.date(2015,5,11):
            relaxation = writer_dates_data[date_]["Relaxation"]
            target_correction = 1 - relaxation
            for target in writer_dates_data[date_]["Targets"]:
                if target is None:
                    target = 0
                corrected_targets.append(target*target_correction)
        else:
            for target in writer_dates_data[date_]["Targets"]:
                if target is None:
                    target = 0
                corrected_targets.append(target)
            
            relaxation = writer_dates_data[date_]["Relaxation"]
            if relaxation >0.0000:
                relaxation_factor = 1.0000/relaxation
                corrected_targets.append(relaxation_factor)
    utilizations = [target**-1 for target in corrected_targets if target > 0]
    efficiency = numpy.sum(utilizations)/len(working_dates)
    return efficiency

def getEfficiencyForDateRange_(user_id, password, start_date, end_date, query_user=None):
    """Returns the efficiency for an emplyoee for all dates between two dates."""
    #print "In getEfficiencyForDateRange"
    #Great, I need to rewrite this too?! Wth.
    if query_user is None:
        query_user = user_id
    datesList = getWorkingDatesBetween(user_id, password, start_date, end_date, query_user)
    efficiency = 0.0
    days = 0.0
    for each_date in datesList:
        efficiency += getEfficiencyFor(user_id, password, each_date, query_user)
        days += 1.0
    #print "Leaving getEfficiencyForDateRange"
    if days == 0:
        print "Zero day error for the following dates:", start_date, end_date
        return 0
    else:
        #print "Total efficiency: %f for %d days." % ((efficiency / days), days)
        return efficiency / days

def getEfficiencyFor(user_id, password, query_date, query_user=None):
    if query_user == None:
        query_user = user_id
    return getEfficiencyForDateRange(user_id, password, query_date, query_date, query_user)

def getEfficiencyFor_(user_id, password, queryDate, query_user = None):
    """Returns the total efficiency for a user for a particular date.
    NOTE: If calculating efficiency between a range of dates, do not consider
    dates on which a writer is given a leave.
    """
    #print "In getEfficiencyFor"
    if query_user == None:
        query_user = user_id
    requestedData = getUserPiggyBankData(queryDate, user_id, password, query_user)
    #print "Received a %s of %d length." %(type(requestedData),len(requestedData))
    efficiency = 0.0
    status, relaxation, approval = checkWorkStatus(user_id, password, queryDate, query_user)
    if (status == "Working") or (approval != "Approved"):
        #Calculate only for working days
        if relaxation > 0.0:
            efficiencyDivisor = (1.0-relaxation)
        else:
            efficiencyDivisor = 1.0
        #This doesn't account for negative relaxation, scenarios where a writer must make up. Does it need to? I don't really think so.
        for entry in requestedData:
            #pass the classification identifiers to the method.
            piggy_row = {
                "Description Type": entry["Description Type"],
                "Source": entry["Source"],
                "BU": entry["BU"],
                "Super-Category": entry["Super-Category"],
                "Category": entry["Category"],
                "Sub-Category": entry["Sub-Category"],
                "Vertical": entry["Vertical"]
            }
            target = getTargetFor(user_id, password, piggy_row, queryDate)
            if target == 0.0:
                efficiency += 0.0
            else:
                if queryDate < datetime.date(2015,6,11):
                    efficiency += 1.0/(target*efficiencyDivisor)
                else:
                    efficiency += 1.0/(target)
        if queryDate >= datetime.date(2015, 6, 11):
            efficiency += relaxation
    #elif status == "Leave" or status == "Company Holiday":
        #efficiency = 1.0
    #print efficiency
    #print "Leaving getEfficiencyFor"
    return efficiency

def getEfficiencyForWeek(user_id, password, query_date, query_user = None):
    """Returns the average efficiency for a query_user or the caller ID for the week in
    which the request date falls.
    It only considers those dates in the range which occur prior to the queryDate."""
    #Find out what day the given date falls on. 1 = Monday, 7 = Sunday.
    if query_user is None:
        query_user = user_id
    current_day = query_date.isocalendar()[2]
    #Get the date of the monday in that week. Week ends on Sunday.
    subtractor = current_day - 1
    first_day_of_the_week = query_date - datetime.timedelta(subtractor)
    efficiency = getEfficiencyForDateRange(user_id, password, first_day_of_the_week, query_date, query_user)
    return efficiency

def getEfficiencyForMonth(user_id, password, query_date, query_user = None):
    """Returns the average efficiency for a query_user or the caller ID for the month in
    which the request date falls.
    It only considers those dates in the range which occur prior to the queryDate."""
    
    if query_user is None:
        query_user = user_id

    first_day_of_the_month = datetime.date(query_date.year, query_date.month, 1)
    efficiency = getEfficiencyForDateRange(user_id, password, first_day_of_the_month, query_date, query_user)
    return efficiency

def getEfficiencyForQuarter(user_id, password, query_date, query_user=None):
    """Returns the average efficiency for a queryUser or the caller ID for the quarter in
    which the request date falls.
    It only considers those dates in the range which occur prior to the queryDate."""
    #JFM, AMJ, JAS, OND

    if query_user is None:
        query_user = user_id
    query_month = query_date.month

    #Create a dictionary which contains a 1:1 mapping for the first months of a quarter for any given month. 
    #If asked for the first month of JAS, it should return 7, i.e. July.

    quarter_first_month_mapped_dictionary = {
        1: 1, 2: 1, 3: 1,
        4: 4, 5: 4, 6: 4,
        7: 7, 8: 7, 9: 7,
        10: 10, 11: 10, 12: 10
    }
    first_month_of_the_quarter = quarter_first_month_mapped_dictionary[query_date.month]
    first_day_of_the_quarter = datetime.date(query_date.year, first_month_of_the_quarter, 1)
    efficiency = getEfficiencyForDateRange(user_id, password, first_day_of_the_quarter, query_date, query_user)
    return efficiency

def getEfficiencyForHalfYear(user_id, password, query_date, query_user=None):
    if query_user is None:
        query_user = user_id
    half_year_start_date = getHalfYearStartDate(query_date)
    return getEfficiencyForDateRange(user_id, password, half_year_start_date, query_date, query_user)

def getHalfYearStartDate(query_date):
    """Given a date, it returns the start of the half-year which contains it.
    Jan-June is one half, July to Dec is the other."""
    query_month = query_date.month
    query_year = query_date.year
    if query_month <=6:
        half_year_start_date = datetime.date(query_year, 1, 1)
    else:
        half_year_start_date = datetime.date(query_year, 7, 1)
    return half_year_start_date

def getbbc():
    return getBigbrotherCredentials()

def getTargetFor(user_id, password, query_dict, query_date=None, retry=None):
    """A new method to get the target for a particular query_dict.
    An example query is:
    SELECT `target`, MAX(`Revision Date`) FROM `categorytree` WHERE `BU`=%s AND ... AND `Revision Date`<='%(date)'
"""
    import numpy
    import pandas as pd
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    if query_date is None:
        query_date = datetime.date.today()
    if retry is None:
        retry = 0
    sqlcmdstring = """SELECT `Target`, `Revision Date` FROM `CategoryTree` WHERE %s AND `Revision Date` <= "%s";""" % (getOneToOneStringFromDict(query_dict), convertToMySQLDate(query_date))
    #print sqlcmdstring
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    #Convert the set to a list.
    entries = []
    for entry in data:
        entries.append(entry)
    if len(entries) == 0:
        retry += 1
        if retry == 1:
            #ignore the vertical and try again
            new_query = {
                "Description Type": query_dict["Description Type"],
                "Source": query_dict["Source"],
                "BU": query_dict["BU"],
                "Super-Category": query_dict["Super-Category"],
                "Category": query_dict["Category"],
                "Sub-Category": query_dict["Sub-Category"]
            }
            target = getTargetFor(user_id, password, new_query, query_date, retry)
        elif retry == 2:
            #ignore the sub category and vertical and try again.
            new_query = {
                "Description Type": query_dict["Description Type"],
                "Source": query_dict["Source"],
                "BU": query_dict["BU"],
                "Super-Category": query_dict["Super-Category"],
                "Category": query_dict["Category"]
            }
            target = getTargetFor(user_id, password, new_query, query_date, retry)
        elif retry == 3:
            #ignore the Category, sub category and vertical and try again.
            new_query = {
                "Description Type": query_dict["Description Type"],
                "Source": query_dict["Source"],
                "BU": query_dict["BU"],
                "Super-Category": query_dict["Super-Category"]
            }
            target = getTargetFor(user_id, password, new_query, query_date, retry)
        elif retry == 4:
            #ignore the super-category, Category, sub category and vertical and try again.
            new_query = {
                "Description Type": query_dict["Description Type"],
                "Source": query_dict["Source"],
                "BU": query_dict["BU"],
                "Super-Category": query_dict["Super-Category"]
            }
            target = getTargetFor(user_id, password, new_query, query_date, retry)
        else:
            target = 0
            #print "Failed in retrieving a target for the following query:"
            #print query_dict
            #print query_date
            #print "Carrying on...."
            #give up.
        #call the function again, without one key-value pair.
    elif len(entries) == 1:
        #print "Only one target for query_dict."
        target = entries[0]["Target"]
    else:
        #first check if it has multiple returns for one date.
            #of all the entries, get the closest data
        #Else, if it has only one date:
            #check all the probable targets and return the one with the highest frequency?
        target = -1
        #print "Found multiple targets, jack."

        possible_targets = []
        targets_data_frame = pd.DataFrame(entries)
        max_date = numpy.max(list(targets_data_frame["Revision Date"]))
        multi_target_on_single_date = False if list(targets_data_frame["Revision Date"]).count(max_date) == 1 else True
        if not multi_target_on_single_date:
            target = int(targets_data_frame.loc[targets_data_frame["Revision Date"] == max_date]["Target"])
        #print "Real Target", target, max_date
        else:
            for entry in entries:
                possible_targets.append(entry["Target"])
                try:
                    target = numpy.bincount(possible_targets).argmax() 
                except:
                    #print closest_date
                    #print entries
                    #print query_dict
                    target = -1
                    pass
        #print query_dict, target
    conn.commit()
    conn.close()
    return target

def getEventsForDate(user_id, password, query_date=None, query_dict=None):
    """Reads the eventcalendar and pulls up all events."""
    if query_date is None:
        query_date = datetime.date.today()

def addEvent(user_id, password, event_details):
    """Adds a new event to the event_calendar."""

def addUsersToEvent(user_id, password, event_details, query_users=None):
    """Add users to an event."""

def calculateRelaxationForEvent(user_id, password, event_details):
    """Given an event's details, this function calculates the reduction in efficiency."""

def getOldTargetFor(user_id, password, **query):
    #OLD METHOD. DO NOT USE.
    """Returns target for a combination of queries.
    If, for a combination of BUxTypexSourcexSupCatxCatxSubCatxVert, no target is defined,
    then, this method will keep eliminating one parameter after another to get a target.
    CHANGE PENDING: If it retrieves multiple targets, it should pick the one with the highest frequency.
"""
    #print "In getTargetFor"
    try:
        BUString = query["BU"]
        TypeString = query["DescriptionType"]
        SourceString = query["Source"]
        SupCatString = query["SuperCategory"]
    except:
        print "Error Message: BU, Super-Category, Source and Type are necessary!"
        raise
        return 0
    try:
        CatString = query["Category"]
    except:
        CatString = SupCatString
    try:
        SubCatString = query["SubCategory"]
    except:
        SubCatString = CatString
    try:
        VertString = query["Vertical"]
    except:
        VertString = SubCatString
    try:
        requestDate = query["QueryDate"] #Needs to be datetime.
        if type(requestDate) != type(datetime.date.today()):
            print "Error, date needs to be a datetime date. MOSES is resetting the date to TODAY NOW!"
            requestDate = datetime.date.today()
    except:
        print "No date provided. Fetching target for TODAY."
        requestDate = datetime.date.today() #Get today's date.
    #If I've got here, then I have what I need, mostly.
    connectdb = getOINKConnector(user_id, password)
    dbcursor=connectdb.cursor()
    sqlcmdstring = """SELECT `Target`, `Revision Date` FROM `categorytree` 
WHERE `BU`="%s" AND `Super-Category`="%s" AND `Category`="%s" 
AND `Sub-Category`="%s" AND `Vertical`="%s" 
AND `Description Type`="%s" AND `Source`="%s";""" % \
        (BUString,SupCatString,CatString,SubCatString,VertString,TypeString,SourceString)
    #print sqlcmdstring #debug
    try:
        dbcursor.execute(sqlcmdstring)
        data = dbcursor.fetchall()
    except Exception, e:
        print "Error getting target for %s." %query
        print repr(e)
        return 0
    #print data #debug
    connectdb.commit()
    connectdb.close()
    #Data is in a tuple containing dictionaries.
    #Separate the dates.
    entriesList = []
    for entry in data:
        entriesList.append(entry)
    #print entriesList #debug
    if len(entriesList)==1:
        #print "Only one target found." #debug
        result = entriesList[0]["Target"]
    elif len(entriesList) > 1:
        #print "Found multiple targets across separate dates." #debug
        #print entriesList
        result = None
        datesList = []
        for entry in entriesList:
            datesList.append(entry["Revision Date"])
        #print datesList #debug
        closestRevisionDate = getClosestDate(datesList,requestDate)
        #print "Closest revision date is %s." %closestRevisionDate #debug
        #print "Query Date is %s." %requestDate #debug
        entry_counter = 0
        for entry in entriesList:
            if entry["Revision Date"] == closestRevisionDate:
                result = entry["Target"]
                entry_counter +=1
        if entry_counter >1:
            print "*******************************************************"
            print "Trying to get a target for:"
            print "VertString:", VertString
            print "There seem to be multiple possible targets for separate dates."
            print entriesList
            print "*******************************************************"
    else:
        result = 0

    if int(result) == 0:
        try:
            retry = query["Retry"]
        except:
            retry = 0
        if retry == 0:
            #print "*****************************"
            #print "Got zero target. Trying again."
            #print "Date: %s, BU=%s, DescriptionType=%s, Source=%s, SuperCategory=%s, Category=%s, SubCategory=%s, Vertical=%s" %(requestDate, BUString, TypeString, SourceString, SupCatString, CatString, SubCatString, VertString)
            #print "*****************************"

            result = getTargetFor(user_id, password, BU=BUString, DescriptionType=TypeString, Source=SourceString, SuperCategory=SupCatString, Category=CatString, SubCategory=SubCatString, QueryDate = requestDate, Retry = 1)
        elif retry == 1:
            #print "*****************************"
            #print "Got zero target. Trying again."
            #print "Date: %s, BU=%s, DescriptionType=%s, Source=%s, SuperCategory=%s, Category=%s, SubCategory=%s, Vertical=%s" %(requestDate, BUString, TypeString, SourceString, SupCatString, CatString, SubCatString, VertString)
            #print "*****************************"
            result = getTargetFor(user_id, password, BU=BUString, DescriptionType=TypeString, Source=SourceString, SuperCategory=SupCatString, Category=CatString, QueryDate = requestDate, Retry = 2)
        elif retry == 2:
            #print "*****************************"
            #print "Got zero target. Trying again."
            #print "Date: %s, BU=%s, DescriptionType=%s, Source=%s, SuperCategory=%s, Category=%s, SubCategory=%s, Vertical=%s" %(requestDate, BUString, TypeString, SourceString, SupCatString, CatString, SubCatString, VertString)
            #print "*****************************"
            result = getTargetFor(user_id, password, BU=BUString, DescriptionType=TypeString, Source=SourceString, SuperCategory=SupCatString, QueryDate = requestDate, Retry = 3)
        else:
            #print "*****************************"
            #print "Got zero target. FAILED."
            #print "Date: %s, BU=%s, DescriptionType=%s, Source=%s, SuperCategory=%s, Category=%s, SubCategory=%s, Vertical=%s" %(requestDate, BUString, TypeString, SourceString, SupCatString, CatString, SubCatString, VertString)
            #print "*****************************"
            result = 0
    #print "Target is %r" %result #debug
    #print "Leaving getTargetFor"
    return int(result)

def getClosestDate(datesList, testDate):
    closestDate = None
    for oneDate in datesList:
        if oneDate == testDate:
            return testDate
        elif oneDate < testDate:
            try:
                if oneDate > closestDate:
                    closestDate = oneDate
            except:
                closestDate = oneDate
    return closestDate

def getMaxScoreForParameter(user_id, password, parameter, query_date=None):
    MaxScores = {
            "CFM01": 10.0, "CFM02": 10.0, "CFM03": 10.0, 
            "CFM04": 10.0, "CFM05": 10.0, "CFM06": 10.0, 
            "CFM07": 10.0, "CFM08":  5.0, "GSEO01": 5.0, 
            "GSEO02": 5.0, "GSEO03": 2.5, "GSEO04": 2.5, 
            "GSEO05": 2.5, "GSEO06": 2.5, "GSEO07": 5.0
            }
    return float(MaxScores[parameter])

def getWeightageForParameter(user_id, password, parameter, query_date=None):
    if ("CFM" in parameter):
        return float(getMaxScoreForParameter(user_id, password, parameter)/float(8))
    elif ("GSEO" in parameter):
        return float(getMaxScoreForParameter(user_id, password, parameter)/float(7))
    else:
        print "Error in getting weightage for %s" %parameter
        return 0

def getCFMFor(user_id, password, query_date, query_user=None):
    import numpy
    if query_user is None:
        query_user = user_id
    return getCFMBetweenDates(user_id, password, query_date, query_date, query_user)

def getAverageTeamCFMBetween(start_date, end_date, consider_fatal=None):
    """;"""
    if consider_fatal is None:
        consider_fatal = True
    import numpy
    user_id, password = getBigbrotherCredentials()
    raw_data_table, CFM_key_list, GSEO__key_list = getRawDataTableAndAuditParameters()
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """SELECT * FROM `%s` WHERE `Audit Date` BETWEEN '%s' AND '%s';""" %(raw_data_table, convertToMySQLDate(start_date), convertToMySQLDate(end_date))
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    conn.close()
    audits = len(data)
    #print "Found %d audited articles." % audits
    counter = 0
    fat_key_list = ["FAT01","FAT02","FAT03"]
    CFM_scores = []
    for each_entry in data:
        CFM_score = numpy.sum(list(each_entry[CFM_key] for CFM_key in CFM_key_list)) / float(75.0)
        fatals = list(each_entry[fat_key] for fat_key in fat_key_list)
        if consider_fatal:
            if "Yes" in fatals:
                CFM_score = 0.0
        counter += 1
        recorded_cfm = each_entry["CFM Quality"]
        CFM_score = numpy.around(CFM_score, decimals=3)
        #if CFM_score < recorded_cfm:
        #    sign = "<"
        #elif CFM_score > recorded_cfm:
        #    sign = ">"
        #else:
        #    sign = "=="
        #print "%f %s %f. Difference = %s" %(CFM_score, sign, recorded_cfm, CFM_score - recorded_cfm)
        CFM_scores.append(CFM_score) 
    if audits > 0:
        CFM_score_average = numpy.mean(CFM_scores)
        CFM_score_average = numpy.around(CFM_score_average, decimals=6)
    else:
        CFM_score_average = None
    #print CFM_scores
    return CFM_score_average

def getAverageTeamGSEOBetween(start_date, end_date, consider_fatal=None):
    """;"""
    import numpy
    if consider_fatal is None:
        consider_fatal = True
    user_id, password = getBigbrotherCredentials()
    raw_data_table, CFM_key_list, GSEO_key_list = getRawDataTableAndAuditParameters()
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """SELECT * FROM `%s` WHERE `Audit Date` BETWEEN '%s' AND '%s';""" %(raw_data_table, convertToMySQLDate(start_date), convertToMySQLDate(end_date))
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    conn.close()
    audits = len(data)
    #print "Found %d audited articles." % audits
    counter = 0
    fat_key_list = ["FAT01","FAT02","FAT03"]
    GSEO_scores = []
    for each_entry in data:
        GSEO_score = numpy.sum(list(each_entry[GSEO_key] for GSEO_key in GSEO_key_list)) / float(25.0)
        fatals = list(each_entry[fat_key] for fat_key in fat_key_list)
        if consider_fatal:
            if "Yes" in fatals:
                GSEO_score = 0.0
        counter += 1
        recorded_GSEO = each_entry["GSEO Quality"]
        GSEO_score = numpy.around(GSEO_score, decimals=4)
        #if GSEO_score < recorded_GSEO:
        #    sign = "<"
        #elif GSEO_score > recorded_GSEO:
        #    sign = ">"
        #else:
        #    sign = "=="
        #print "%f %s %f. Difference = %s" %(GSEO_score, sign, recorded_GSEO, GSEO_score - recorded_GSEO)
        GSEO_scores.append(GSEO_score)
    if audits > 0:
        GSEO_score_average = numpy.mean(GSEO_scores)
        GSEO_score_average = numpy.around(GSEO_score_average, decimals=6)
    else:
        GSEO_score_average = None
    #print GSEO_scores
    return GSEO_score_average

def getCFMBetweenDates(user_id, password, start_date, end_date, query_user=None):
    import numpy
    if query_user is None:
        query_user = user_id
    raw_data_table, CFM_key_list, GSEO__key_list = getRawDataTableAndAuditParameters()
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """SELECT * FROM `%s` WHERE `WriterID` = '%s' AND `Audit Date` BETWEEN '%s' AND '%s';""" %(raw_data_table, query_user, convertToMySQLDate(start_date), convertToMySQLDate(end_date))
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    conn.close()
    audits = len(data)
    #print "Found %d audited articles." % audits
    counter = 0
    fat_key_list = ["FAT01","FAT02","FAT03"]
    CFM_scores = []
    for each_entry in data:
        CFM_score = numpy.sum(list(each_entry[CFM_key] for CFM_key in CFM_key_list)) / float(75.0)
        fatals = list(each_entry[fat_key] for fat_key in fat_key_list)
        if "Yes" in fatals:
            CFM_score = 0.0
        counter += 1
        recorded_cfm = each_entry["CFM Quality"]
        CFM_score = numpy.around(CFM_score, decimals=3)
        #if CFM_score < recorded_cfm:
        #    sign = "<"
        #elif CFM_score > recorded_cfm:
        #    sign = ">"
        #else:
        #    sign = "=="
        #print "%f %s %f. Difference = %s" %(CFM_score, sign, recorded_cfm, CFM_score - recorded_cfm)
        CFM_scores.append(CFM_score) 
    if audits > 0:
        CFM_score_average = numpy.mean(CFM_scores)
        CFM_score_average = numpy.around(CFM_score_average, decimals=6)
    else:
        CFM_score_average = None
    #print CFM_scores
    return CFM_score_average

def getCFMForWeek(user_id, password, query_date, query_user=None):
    """Returns the average CFM for a query_user or the caller ID for the week in
    which the request date falls.
    It only considers those dates in the range which occur prior to the queryDate."""
    #Find out what day the given date falls on. 1 = Monday, 7 = Sunday.
    if query_user is None:
        query_user = user_id
    current_day = query_date.isocalendar()[2]
    #Get the date of the monday in that week. Week ends on Sunday.
    subtractor = current_day - 1
    first_day_of_the_week = query_date - datetime.timedelta(subtractor)
    CFM = getCFMBetweenDates(user_id, password, first_day_of_the_week, query_date, query_user)
    return CFM

def getCFMForMonth(user_id, password, query_date, query_user=None):
    """Returns the average CFM for a query_user or the caller ID for the month in
    which the request date falls.
    It only considers those dates in the range which occur prior to the queryDate."""
    
    if query_user is None:
        query_user = user_id
    first_day_of_the_month = datetime.date(query_date.year, query_date.month, 1)
    CFM = getCFMBetweenDates(user_id, password, first_day_of_the_month, query_date, query_user)
    return CFM

def getCFMForQuarter(user_id, password, query_date, query_user=None):
    """Returns the average CFM for a queryUser or the caller ID for the quarter in
    which the request date falls.
    It only considers those dates in the range which occur prior to the queryDate."""
    #JFM, AMJ, JAS, OND
    if query_user is None:
        query_user = user_id
    query_month = query_date.month

    #Create a dictionary which contains a 1:1 mapping for the first months of a quarter for any given month. 
    #If asked for the first month of JAS, it should return 7, i.e. July.

    quarter_first_month_mapped_dictionary = {
        1: 1, 2: 1, 3: 1,
        4: 4, 5: 4, 6: 4,
        7: 7, 8: 7, 9: 7,
        10: 10, 11: 10, 12: 10
    }
    first_month_of_the_quarter = quarter_first_month_mapped_dictionary[query_date.month]
    first_day_of_the_quarter = datetime.date(query_date.year, first_month_of_the_quarter, 1)
    CFM = getCFMBetweenDates(user_id, password, first_day_of_the_quarter, query_date, query_user)
    return CFM

def getCFMForHalfYear(user_id, password, query_date, query_user=None):
    if query_user is None:
        query_user = user_id
    half_year_start_date = getHalfYearStartDate(query_date)
    return getCFMBetweenDates(user_id, password, half_year_start_date, query_date, query_user)

def getGSEOFor(user_id, password, query_date, query_user=None):
    import numpy
    if query_user is None:
        query_user = user_id
    return getGSEOBetweenDates(user_id, password, query_date, query_date, query_user)

def getGSEOBetweenDates(user_id, password, start_date, end_date, query_user=None):
    import numpy
    if query_user is None:
        query_user = user_id
    raw_data_table, CFM_key_list, GSEO_key_list = getRawDataTableAndAuditParameters()
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """SELECT * FROM `%s` WHERE `WriterID` = '%s' AND `Audit Date` BETWEEN '%s' AND '%s';""" %(raw_data_table, query_user, convertToMySQLDate(start_date), convertToMySQLDate(end_date))
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    conn.close()
    audits = len(data)
    #print "Found %d audited articles." % audits
    counter = 0
    fat_key_list = ["FAT01","FAT02","FAT03"]
    GSEO_scores = []
    for each_entry in data:
        GSEO_score = numpy.sum(list(each_entry[GSEO_key] for GSEO_key in GSEO_key_list)) / float(25.0)
        fatals = list(each_entry[fat_key] for fat_key in fat_key_list)
        if "Yes" in fatals:
            GSEO_score = 0.0
        counter += 1
        recorded_GSEO = each_entry["GSEO Quality"]
        GSEO_score = numpy.around(GSEO_score, decimals=4)
        #if GSEO_score < recorded_GSEO:
        #    sign = "<"
        #elif GSEO_score > recorded_GSEO:
        #    sign = ">"
        #else:
        #    sign = "=="
        #print "%f %s %f. Difference = %s" %(GSEO_score, sign, recorded_GSEO, GSEO_score - recorded_GSEO)
        GSEO_scores.append(GSEO_score)
    if audits > 0:
        GSEO_score_average = numpy.mean(GSEO_scores)
        GSEO_score_average = numpy.around(GSEO_score_average, decimals=6)
    else:
        GSEO_score_average = None
    #print GSEO_scores
    return GSEO_score_average

def getGSEOForWeek(user_id, password, query_date, query_user=None):
    """Returns the average GSEO for a query_user or the caller ID for the week in
    which the request date falls.
    It only considers those dates in the range which occur prior to the queryDate."""
    #Find out what day the given date falls on. 1 = Monday, 7 = Sunday.
    if query_user is None:
        query_user = user_id
    current_day = query_date.isocalendar()[2]
    #Get the date of the monday in that week. Week ends on Sunday.
    subtractor = current_day - 1
    first_day_of_the_week = query_date - datetime.timedelta(subtractor)
    GSEO = getGSEOBetweenDates(user_id, password, first_day_of_the_week, query_date, query_user)
    return GSEO

def getGSEOForMonth(user_id, password, query_date, query_user=None):
    """Returns the average GSEO for a query_user or the caller ID for the month in
    which the request date falls.
    It only considers those dates in the range which occur prior to the queryDate."""
    if query_user is None:
        query_user = user_id
    first_day_of_the_month = datetime.date(query_date.year, query_date.month, 1)
    GSEO = getGSEOBetweenDates(user_id, password, first_day_of_the_month, query_date, query_user)
    return GSEO

def getGSEOForQuarter(user_id, password, query_date, query_user=None):
    """Returns the average GSEO for a queryUser or the caller ID for the quarter in
    which the request date falls.
    It only considers those dates in the range which occur prior to the queryDate."""
    #JFM, AMJ, JAS, OND
    if query_user is None:
        query_user = user_id
    query_month = query_date.month
    #Create a dictionary which contains a 1:1 mapping for the first months of a quarter for any given month. 
    #If asked for the first month of JAS, it should return 7, i.e. July.
    quarter_first_month_mapped_dictionary = {
        1: 1, 2: 1, 3: 1,
        4: 4, 5: 4, 6: 4,
        7: 7, 8: 7, 9: 7,
        10: 10, 11: 10, 12: 10
    }
    first_month_of_the_quarter = quarter_first_month_mapped_dictionary[query_date.month]
    first_day_of_the_quarter = datetime.date(query_date.year, first_month_of_the_quarter, 1)
    GSEO = getGSEOBetweenDates(user_id, password, first_day_of_the_quarter, query_date, query_user)
    return GSEO

def getGSEOForHalfYear(user_id, password, query_date, query_user=None):
    if query_user is None:
        query_user = user_id
    half_year_start_date = getHalfYearStartDate(query_date)
    return getGSEOBetweenDates(user_id, password, half_year_start_date, query_date, query_user)


def getDescriptionTypes(user_id, password):
    """Returns a list containing the entire list of values for Description Type."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor=connectdb.cursor()
    sqlcmdstring = "SELECT `Description Type` FROM `categorytree`;"""
    dbcursor.execute(sqlcmdstring)
    DTypeTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    #print len(BUTuple)
    #print BUList #Debug
    DTypeList=[DType["Description Type"] for DType in DTypeTuple]
#   BUList = [BU for BU in BUTuple]
    DTypeList= list(set(DTypeList))
    DTypeList.sort()
    return DTypeList

def getSources(user_id, password):
    """Returns a list containing the entire list of values for BU."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor=connectdb.cursor()
    sqlcmdstring = "SELECT `Source` FROM `categorytree`;"""
    dbcursor.execute(sqlcmdstring)
    SourceTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    #print len(BUTuple)
    #print BUList #Debug
    SourceList = [Source["Source"] for Source in SourceTuple]
#   BUList = [BU for BU in BUTuple]
    SourceList= list(set(SourceList))
    SourceList.sort()
    return SourceList

def getBUValues(user_id, password):
    """Returns a list containing the entire list of values for BU."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor=connectdb.cursor()
    sqlcmdstring = "SELECT `BU` FROM `categorytree`;"""
    dbcursor.execute(sqlcmdstring)
    BUTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    #print len(BUTuple)
    #print BUList #Debug
    BUList=[BU["BU"] for BU in BUTuple]
#   BUList = [BU for BU in BUTuple]
    BUList= list(set(BUList))
    BUList.sort()
    return BUList

def getSuperCategoryValues(user_id,password,BU=None):
    """Returns a list containing the appropriate list of values for Super-Category."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor=connectdb.cursor()
    if BU != None:
        sqlcmdstring = "SELECT `Super-Category` FROM `categorytree` WHERE `BU`= '%s';""" % BU
    else:
        sqlcmdstring = "SELECT `Super-Category` FROM `categorytree`;"""
    dbcursor.execute(sqlcmdstring)
    SupCTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    #print SupCTuple #Debug
    SupCList = [SC["Super-Category"] for SC in SupCTuple]
    SupCList = list(set(SupCList))
    SupCList.sort()
    return SupCList

def getCategoryValues(user_id, password, SupC=None):
    """Returns a list containing the appropriate list of values for Category."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor=connectdb.cursor()
    if SupC != None:
        sqlcmdstring = "SELECT `Category` FROM `categorytree` WHERE `Super-Category`= '%s';""" % SupC
    else:
        sqlcmdstring = "SELECT `Category` FROM `categorytree`;"""
    dbcursor.execute(sqlcmdstring)
    CTuple = dbcursor.fetchall()
    #print CTuple #debug
    connectdb.commit()
    connectdb.close()
    CList = [Cat["Category"] for Cat in CTuple]
    CList = list(set(CList))
    CList.sort()
    return CList

def getSubCategoryValues(user_id, password, Cat=None):
    """Returns a list containing the appropriate list of values for Sub-Category."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor=connectdb.cursor()
    if Cat != None:
        sqlcmdstring = "SELECT `Sub-Category` FROM `categorytree` WHERE `Category`= '%s';""" % Cat
    else:
        sqlcmdstring = "SELECT `Sub-Category` FROM `categorytree`;"""
    dbcursor.execute(sqlcmdstring)
    SubCTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    #print SubCTuple #debug
    SubCList = [SC["Sub-Category"] for SC in SubCTuple]
    SubCList = list(set(SubCList))
    SubCList.sort()
    return SubCList

def getBrandValues(user_id, password):
    """Returns a list containing the appropriate list of values for Sub-Category."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT `Brand` FROM `piggybank`;"
    dbcursor.execute(sqlcmdstring)
    brandTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    #print brandTuple #debug
    brandList = [brand["Brand"] for brand in brandTuple]
    brandList = list(set(brandList))
    brandList.sort()
    return brandList

def getCategoryTree(user_id, password):
    """Returns a list containing the appropriate list of values for Sub-Category."""
    import pandas
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT * FROM `categorytree`;"
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    data_frame = pandas.DataFrame(list(data))
    #print brandTuple #debug
    return data_frame

def checkDuplicacy(FSN, articleType, articleDate):
    """Working Principle:
    1. Check if the FSN has been entered in the piggybank on the same date. Return "Local" if found.
    2. Else, check if the FSN has been entered in the piggybank on some other date.
        (a) If the description  type is "Regular Description", also search for "Rich Product Description", "Rich Product Description Plan A" and "Rich Product Description Plan B".
        (b) If the description type is one of the RPD types, search for all RPD types.
        (c) If Found, return "Global".
    3. Else, check the fsndump using the same logic as step #2.
    4. Return False if not found.
    """
    wasWrittenBefore = False
    user_id, password = getBigbrotherCredentials()
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """SELECT * FROM `piggybank` WHERE `FSN` = '%s' and `Article Date` = '%s';""" % (FSN, articleDate)
    dbcursor.execute(sqlcmdstring)
    local_data = dbcursor.fetchall()
    if len(local_data) > 0: #If that FSN exists in the data for a given date.
        #print "Found FSN in local data."
        wasWrittenBefore = "Local"
    else: 
        #If not found in the given date
        #For RPD, it should search for RPD, RPD Plan A and RPD Plan B.
        #Check the first 24 letters as the type could be Plan A or Plan B as well.
        isRPD = False
        if articleType[:24] == "Rich Product Description":
            isRPD = True
            sqlcmdstring = """SELECT * FROM `piggybank` 
            WHERE `FSN` = '%s' AND (`Description Type`="Rich Product Description" OR 
                `Description Type`="Rich Product Description Plan A"
                OR `Description Type`="Rich Product Description Plan B");"""%FSN
        else:
            sqlcmdstring = """SELECT * from `piggybank` WHERE `FSN` = '%s' and 
                (`Description Type` = '%s' OR `Description Type`="Rich Product Description" 
                OR `Description Type`="Rich Product Description Plan A"
                OR `Description Type`="Rich Product Description Plan B");""" % (FSN, articleType)
        dbcursor.execute(sqlcmdstring)
        global_data = dbcursor.fetchall()
        if len(global_data) > 0: #If found for some date
            #print " Found FSN in global data."
            #print global_data
            wasWrittenBefore = "Global"
        else:
            if isRPD:
                sqlcmdstring = """SELECT * FROM `fsndump` 
                    WHERE `FSN` = '%s' AND (`Description Type`="Rich Product Description" OR 
                    `Description Type`="Rich Product Description Plan A"
                    OR `Description Type`="Rich Product Description Plan B");"""%FSN
            else:
                sqlcmdstring = """SELECT * from `fsndump` WHERE 
                `FSN` = '%s' and (`Description Type` = "%s" OR 
                    `Description Type`="Rich Product Description" OR 
                    `Description Type`="Rich Product Description Plan A"
                    OR `Description Type`="Rich Product Description Plan B");""" % (FSN, articleType)
            dbcursor.execute(sqlcmdstring)
            global_data = dbcursor.fetchall()
            if len(global_data) > 0: #If found in the fsndump
                #print "Found in the dump!"
                wasWrittenBefore = "Global"
    connectdb.commit()
    connectdb.close()   
    return wasWrittenBefore

def getVerticalValues(user_id, password, SubC=None):
    """Returns a list containing the appropriate list of values for Verticals."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor=connectdb.cursor()
    if SubC != None:
        sqlcmdstring = "SELECT `Vertical` FROM `categorytree` WHERE `Sub-Category`= '%s';""" % SubC
    else:
        sqlcmdstring = "SELECT `Vertical` FROM `categorytree`;"""
    dbcursor.execute(sqlcmdstring)
    VertTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    #print VertTuple #debug
    VertList=[Vert["Vertical"] for Vert in VertTuple]
    VertList=list(set(VertList))
    VertList.sort()
    return VertList

def modWorkingStatus(user_id, password, querydate, status, relaxation, comment, approval = "\\N",rejectionComment = "\\N", targetuser = None):
    """Method to modify the working status/relaxation of an employee.
    If no record exists, then the method creates an entry for it."""
    if targetuser == None:
        targetuser = user_id
    
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT 1 FROM `workcalendar` WHERE `Employee ID` = '%s' AND  `Date` = '%s';" \
    % (targetuser, convertToMySQLDate(querydate))
    #print sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()
    #print data #debug
    if len(data) == 0:
        #print "No data available."
        if getUserRole(user_id) == "Content Writer":
            sqlcmdstring = "INSERT INTO `workcalendar` (`Employee ID`, `Date`, `Status`, `Relaxation`, `Comment`, `Entered By`) VALUES ('%s','%s','%s','%s','%s', '%s')" %(targetuser, convertToMySQLDate(querydate), status, relaxation, comment, getUserRole(targetuser))
        elif getUserRole(user_id) == "Team Lead":
            #print "Team Lead!"
            sqlcmdstring = "INSERT INTO `workcalendar` (`Employee ID`, `Date`, `Status`, `Relaxation`, `Entered By`, `Comment`, `Approval`,`Rejection Comment`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %(targetuser, convertToMySQLDate(querydate), status, relaxation, getUserRole(targetuser), comment, approval, rejectionComment)
    else:
        #print "Data available. Updating entry."
        if getUserRole(user_id) == "Content Writer":
            sqlcmdstring = "UPDATE `workcalendar` SET `Status` = '%s', `Relaxation` = '%s', `Entered By` = '%s', `Comment` = '%s' WHERE `Employee ID` = '%s' AND `Date` = '%s';" \
            %(status, relaxation, getUserRole(targetuser), comment, targetuser, convertToMySQLDate(querydate))
        elif getUserRole(user_id) == "Team Lead":
            print "Team Lead!"
            sqlcmdstring = "UPDATE `workcalendar` SET `Status` = '%s', `Relaxation` = '%s', `Entered By` = '%s', `comment` = '%s', `Approval` = '%s', `Rejection Comment` = '%s' WHERE `Employee ID` = '%s' AND `Date` = '%s';" \
            %(status, relaxation, getUserRole(targetuser), comment, approval, rejectionComment, targetuser, convertToMySQLDate(querydate))
    #print sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def getUserRole(user_id, password=None, targetuser=None):
    """Returns the role of the user or of a targetuser."""
    if password == None and user_id != getBigbrotherCredentials()[0]:
        if targetuser == None:
            targetuser = user_id
        user_id, password = getBigbrotherCredentials()
    elif targetuser == None and user_id == getBigbrotherCredentials()[0]:
        return "Big Brother"
    elif targetuser == None:
        targetuser = user_id
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT `Role` FROM `employees` WHERE `Employee ID` = '%s';" % targetuser
    #print sqlcmdstring #debug 
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()
    #print "Printing Role information", data
    role = data[0]["Role"]
    #print role #debug
    connectdb.commit()
    connectdb.close()
    return role

def getHostID():
    hostid_file = OINKM.getLatestFile("hostid.txt","Data")
    #hostID = "localhost"
    #print hostid_file
    hostID = open(hostid_file).read()
    return hostID

def getDBName():
    dbName = "oink"
    return dbName

def detectChangeInHost(newHostID):
    oldHostID = getHostID()
    changedStatus = False
    if newHostID != oldHostID:
        if checkHostID(newHostID):
            changeHostID(newHostID)
            changedStatus = True
        else:
            print "Error, host ID is not valid."
    return changedStatus

def checkHostID(hostID):
    user_id, password = getBigbrotherCredentials()
    try:
        connectdb = getOINKConnector(user_id, password)
        dbcursor = connectdb.cursor()
        sqlcmdstring = "SHOW TABLES;"
        dbcursor.execute(sqlcmdstring)
        a = dbcursor.fetchall()
        #print a
        connectdb.commit()
        connectdb.close()
        success = True
    except:
        success = False
    return success

def changeHostID(hostID):
    """Changes the host id in the hostid file."""
    try:
        hostid_filename = OINKM.getLatestFile("hostid.txt","Data")
        hostid_file = open(hostid_filename, "w")
        hostid_file.write(hostID)
        hostid_file.close()
        success = True
    except:
        success = False
    return success

def addOverride(FSN, override_date, user_id, password):
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "INSERT INTO `overriderecord` (`FSN`, `Override Date`, `Overridden By`) VALUES ('%s', '%s', '%s');" %(FSN, convertToMySQLDate(override_date), user_id)
    #print sqlcmdstring
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def checkForOverride(FSN, query_date, user_id, password):
    """Checks if an override has been scheduled for a specific FSN and date by the TL.
    It returns True if there's an override for a particular date, and it returns the number of overrides for this FSN so far."""

    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT * FROM `overriderecord` WHERE `FSN` = '%s' AND `Override Date` = '%s';" %(FSN, convertToMySQLDate(query_date))
    dbcursor.execute(sqlcmdstring)
    retrieved_data = dbcursor.fetchall()
    #print "Found %d entries." % len(retrieved_data)
    sqlcmdstring = "SELECT * FROM `overriderecord` WHERE `FSN` = '%s';" %(FSN)
    dbcursor.execute(sqlcmdstring)
    overall_retrieved_data = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    return (len(retrieved_data) > 0), len(overall_retrieved_data)

def getLastWorkingDate(user_id, password, queryDate = None, queryUser = None):
    """Returns the last working date for the requested user."""
    #Testing pending: need to check if it recursively picks out leaves and holidays as well.
    if queryDate is None:
        queryDate = datetime.date.today()
    if queryUser is None:
        queryUser = user_id
    #print queryDate
    stopthis = False
    previousDate = queryDate - datetime.timedelta(1)
    while not stopthis:
        if not isWorkingDay(user_id, password, previousDate):
            #print previousDate, " is a holiday or a weekend!"
            previousDate -= datetime.timedelta(1)
        else:
            status = getWorkingStatus(user_id, password, previousDate)[0]
            if status == "Working":
                stopthis = True
            elif status in ["Leave", "Holiday", "Special Holiday"]:
                #print "Not working on ", previousDate
                previousDate -= datetime.timedelta(1)
            else:
                stopthis = True
    return previousDate

######################################################################
#Test methods#
#These are development methods that aren't called by the users.
######################################################################

def testmethods():
    print "Test methods."

def gettrialpiggydict():
    return  {
    "FSN": "123456789",
    "WriterID": 62487,
    "Article Date" : "2015-02-01",
    "Source" : "Inhouse",
    "Description Type" : "Rich Product Description",
    "BU" : "FMCGAndOthers",
    "Super-Category" : "Book",
    "Category" : "Book",
    "Sub-Category" : "Books-Fiction",
    "Vertical" : "Horror and Ghost Stories",
    "Brand" : "Penguin Books LTD",
    "Word Count" : 42,
    "Upload Link" : "www.flipkart.com\\book",
    "Reference Link" : "www.reflink.com",
    "Rewrite Ticket" : "No"
    }
    

def getSQLErrorType(errorString):
    error = "Unknown. Printing verbatim: %s" % errorString
    if "2003" in errorString:
        error = "Cannot connect to server. Check server IP."
    elif "1045" in errorString:
        error = "Login failure."
    return error


def pendingmethods():
    """Pending methods."""
    print "Pending methods."

def getOneToOneStringFromDict(query_dict, joiner = None):
    """Takes a dictionary and returns a string where each key is mapped to its value. Example:
    a = {"Name" : "Vinay", "Age" : "27"}
    returns 
    "'Name' = 'Vinay', 'Age' = '27'"
    The joiner is either None, AND or OR.
    """
    keys_list = query_dict.keys()

    result_string = ""
    if joiner == None:
        joiner = " AND "
    elif joiner.lower() == "and":
        joiner = " AND "
    elif joiner.lower() == "or":
        joiner = " OR "
    else:
        joiner = " OR "
    for key in keys_list:
        if len(result_string) != 0:
            result_string = result_string + "%s" % joiner
        result_string = result_string + "`" + key + "`" + " = " + '"' + query_dict[key] + '"'
    return result_string

def checkAuditStatus(user_id, password, articleDict):
    """Checks if an article has been audited before."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """SELECT * FROM `rawdata` WHERE %s;""" % getOneToOneStringFromDict(articleDict)
    print "Printing Command:\n", sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()
    audit_count = len(data)
    print "This query has %s entries." % audit_count #debug
    connectdb.commit()
    connectdb.close()
    return audit_count

def getQuality(user_id, password, queryDict):
    """Takes one rawdata row and returns the quality."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """"""
    print "Printing Command: \n", sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    return CFM, GSEO

def getRawDataColumnsInOrder(user_id, password):
    """Returns a list of raw data column headers in order."""
    rawDataColumns = [
        "WriterID", 
        "Category", 
        "Sub-Category", 
        "QAID", 
        "Article Date", 
        "WS Name", 
        "Word Count", 
        "FSN", 
        "Introduction", 
        "Product Theme", 
        "Flow of Article", 
        "Explain Features [in simple terms]", 
        "Practical Application of Features", 
        "Neutral Content", 
        "USP", 
        "Priority of Features", 
        "Sentence Construction", 
        "Sub-verb agreement", 
        "Missing/ additional/ repeated words", 
        "Spelling/ Typo", 
        "Punctuation", 
        "Formatting Errors", 
        "Keyword Variation", 
        "Keyword Density", 
        "Plagiarism", 
        "Mismatch in Specs", 
        "CFM Quality", 
        "GSEO Quality", 
        "Overall Quality", 
        "Fatals Count", 
        "Non Fatals Count", 
        "Introduction comment", 
        "Product Theme comment", 
        "Flow of Article comment", 
        "Explain Features [in simple terms] comment", 
        "Practical Application of Features comment",
        "Neutral Content comment",
        "USP comment",
        "Priority of Features comment",
        "Sentence Construction", 
        "Sub-verb agreement comment", 
        "Missing/ additional/ repeated words comment", 
        "Spelling/Typo comment", 
        "Punctuation comment", 
        "Formatting Errors comment", 
        "Keyword Variation comment", 
        "Keyword Density comment", 
        "Plagiarism comment", 
        "Mismatch in Specs comment", 
        "AuditCount"
        ]
    return rawDataColumns


def addClarification(user_id, password, FSN, postingDate, clarificationCode, clarificationComment = "NA"):
    """Adds a new clarification to the clarification tracker."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """INSERT INTO `clarifications` (`FSN`, `Posting Date`, `Poster ID`, `Poster Name`, `Poster Email ID`, `Code`, `Comments`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');""" %(FSN, convertToMySQLDate(postingDate), user_id, getEmpName(user_id), getEmpEmailID(user_id), clarificationCode, clarificationComment)
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def checkClarification(user_id, password, FSN, postingDate, postinguser_id, checkStatus, checkDate):
    """This method is used to modify the update the check status of a clarification."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """UPDATE `clarifications` SET `Checked By` = '%s', `Check Date` = '%s', `Check Status` = '%s' WHERE `FSN` = '%s' AND `Posting Date` = '%s' AND `Poster ID` = '%s';""" %(user_id, convertToMySQLDate(checkDate), checkStatus, FSN, convertToMySQLDate(postingDate), user_id)
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def updateClarification(user_id, password, FSN, postingDate, postinguser_id, newcode, newcomment):
    """This method allows users to change the clarification code and comments."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """UPDATE `clarifications` SET `Code` = '%s', `Comments` = '%s' WHERE 
    `FSN` = '%s' AND `Posting Date` = '%s' AND `Poster ID` = '%s';
    """ %(newcode, newcomment, FSN, convertToMySQLDate(checkDate), user_id)
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def checkIfClarificationPosted(user_id, password, FSN, code):
    """This method checks if a clarification code has already been posted for an FSN.
    Returns the date if that issue has been brought up before, else it returns false."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """SELECT * FROM `clarifications` WHERE `FSN` = '%s' AND `Code` = '%s';""" % (FSN, code)
    dbcursor.execute(sqlcmdstring)
    clarifications = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    if (len(clarifications) > 0):
        try:
            return clarification[0]["Posting Date"]
        except KeyError:
            return "Key Error. Check the clarifications table manually."
            pass
        except Exception, e:
            raise
    else:
        return False

def version():
    return "1.5"

def getAuditParameterName(query_parameter):
    user_id, password = getBigbrotherCredentials()
    param_class = "CFM" if "CFM" in query_parameter else "GSEO"
    param_class_index = query_parameter[-1:]
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """SELECT * FROM auditscoresheet WHERE `Parameter Class`="%s" AND `Parameter Class Index`="%s";""" %(param_class, param_class_index)
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    data = data[0]["Column Descriptions"]
    conn.close()
    return data

def getUniqueBUsBetweenDates(oinkdb, start_date, end_date = None, description_type = None):
    import numpy
    import pandas
    oinkcursor = oinkdb.cursor()
    if end_date is None:
        end_date = start_date
    if description_type is None:
        description_type = "All"
    sqlcmdstring = """SELECT * FROM `piggybank` WHERE `Article Date` BETWEEN '%s' AND '%s';""" % (start_date, end_date)
    oinkcursor.execute(sqlcmdstring)
    piggy_data = oinkcursor.fetchall()
    print "Found %d entries." % len(piggy_data)
    print "Extracting all the BU types written in between these dates."
    BUs =[]
    for piggy_entry in piggy_data:
        piggy_BU = piggy_entry["BU"]
        if piggy_BU not in BUs:
            BUs.append(piggy_BU)
    print "Retrieved %d unique BUs." %len(BUs)
    print "Counting articles at the BU level."
    BU_article_counter = []
    for BU in BUs:
        counter = 0
        for piggy_entry in piggy_data:
            if piggy_entry["BU"] == BU:
                counter+=1
        BU_article_counter.append(counter)
        print "The %s BU has %d articles." %(BU, counter)
    print "There are an average of %f articles per BU." % (numpy.mean(BU_article_counter))
    print "The median number of articles at the BU Edit Coverage Level is %f." %(numpy.median(BU_article_counter))
    no_of_editors = 4
    no_of_days = (end_date - start_date).days + 1
#    no_of_days = 1 if no_of_days == 1 else no_of_days
    max_edits_per_editor = 30
    print "Given %d editors for the time period of %d days, calculating the number of articles that can be edited at the BU level." % (no_of_editors, no_of_days)
    edit_percentage = 0.0
    empty_list = [0.0 for x in BU_article_counter]
    data_dict = {"BU": BUs, "Articles": BU_article_counter, "Audits": empty_list, "Audit_Percentage": empty_list}
    data_frame = pandas.DataFrame(data_dict)
    data_keys =list(data_frame.keys())
    total_no_of_edits = no_of_days * no_of_editors * max_edits_per_editor
    current_data_frame = data_frame
    while True:
        new_data = current_data_frame
        
        #increase the audit of each row by 1.
        #calculate audit percentage.
        #quit when the total audits are nearly or equal to the required number.
        #Quit when the audit percentages are equal, or later, as required, 
        #Only if increasing by 1 again will increase total to beyond the possible amount.
        furtherAuditsNecessary = (current_total_edits <= total_no_of_edits) and (new_total_edits > total_no_of_edits)
        quit = areAuditPercentagesEqual and furtherAuditsNecessary
        if quit:
            break
            current_data_frame = new_data
    return data_frame

def getRawDataFrame():
    import csv
    import pandas
    #raw_data_dump = open("Data\\RawDataTrial.csv", "r")
    #raw_data = csv.DictReader(raw_data_dump)
    data_frame = pandas.DataFrame.from_csv("Data\\RawDataTrial.csv")
    return data_frame

#############################################################
#############################################################
#Algorithm to generate an audit queue based on the usual method.
#
#1. The Piggy Bank table has the following columns:
#   [Usual Columns][Published by TL][Audit Status][Raw Data Columns*][Audit Revision Tag]
#   * SEO Articles use "SEO" as the FSN. The article topic is used as the "WSName".
#   * Remove unnecessary titles.
#2. The program picks a random article wherein:
#   * The writer who wrote it has the least audit coverage, AND
#   * The category identifying columns have the least audit coverage.
#   * If the audit percentages are equal, then it picks a random category and writer.
#############################################################
#############################################################

#def getCFMForDate():
#def getGSEOForDate():
#def getCFMForMultiQuery():
#def getGSEOForMultiQuery():
#def 
#def getCategories()
#    """Returns all the categories that have been worked on in a particular time-frame."""
#def getCategoryCoverage():
#    """Returns the audit percentage of the categories"""
#def buildAuditQueue():
#def buildRCAQueue():
#def 
def addSubha():
    u, p = getBigbrotherCredentials()
    emp = {
    "Employee ID": "78468",
    "Name": "Subha Nair",
    "Role": "Content Writer",
    "DOJ": "2015-04-06",
    "Email ID": "subha.nair@flipkart.com"
    }
    addEmployee(emp, u, p)

def convertAttendanceTrackerToWorkCalendar():
    user_id, password = getBigbrotherCredentials()
    if not os.path.isfile("Archive\\AttendanceCalendar.csv"):
        print "Ensure you're running this method from the OINKModule folder."
    else:
        print "Rebuilding Work Calendar"
        rebuildWorkCalendar(user_id, password)
        start_time = datetime.datetime.now()
        print "Initiating conversion of AttendanceCalendar to WorkCalendar."
        attendance_calendar_file = open("Archive\\AttendanceCalendar.csv")
        attendance_calendar_headers = attendance_calendar_file.read().split("\n")[0].split(",")
        attendance_calendar_file = open("Archive\\AttendanceCalendar.csv")
        
        attendance_calendar = csv.DictReader(attendance_calendar_file)
        employee_ids = attendance_calendar_headers[2:]
        print employee_ids
        print "Trying to loop through ", attendance_calendar
        for entry in attendance_calendar:
            print "looping!"
            #print entry
            #For each row, which corresponds to a date, get data for each writer, corresponding to columns,
            #and then post that data to the work calendar.
            for employee_id in employee_ids:
                print "Looping for ", employee_id
                status = entry[employee_id].upper()
                calendar_date = entry["Date"]
                relaxation = 0
                if status.upper() not in ["WOFF", "HOL", "HOLIDAY", "ATT", "NA"]:
                    if status == "P":
                        status = "Working"
                    elif status in ["CL", "LOP", "SL", "EL", "UL", "PL"]:
                        status = "Leave"
                    relaxation = 0
                    comment = "NA"
                    reviewed_by = "bigbrother"
                    approval="Approved"
                    rejection_comment="NA"
                    try:
                        updateWorkCalendar(user_id, password, calendar_date, status, relaxation, comment, employee_id, approval, rejection_comment, reviewed_by)
                    except MySQLdb.IntegrityError:
                        updateWorkCalendar(user_id, password, calendar_date, status, relaxation, comment, employee_id, approval, rejection_comment, reviewed_by, mode="Updation")
        print "Completed."

def updateWorkCalendar(user_id, password, calendar_date, status, relaxation=None, comment=None, employee_id=None, approval=None, rejection_comment=None, reviewed_by=None, mode=None):
    """Method used to add or modify an entry in the workcalendar."""
    if relaxation is None:
        relaxation = 0.0
    if comment is None:
        comment = "NA"
    if (mode is None) or (mode not in ["Addition", "Updation"]):
        mode = "Addition"
    if (approval is None) or (mode not in ["Approved","Pending","Rejected"]):
        approval = "Approved" 
    if employee_id is None:
        employee_id = user_id
    if reviewed_by is None:
        reviewed_by = "NA"
    if rejection_comment is None:
        rejection_comment = "NA"
    entered_by = user_id

    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    if mode == "Addition":
        sqlcmdstring = """INSERT INTO `workcalendar` (`Date`, `Employee ID`,  `Status`, `Relaxation`, `Entered By`, `Comment`, `Approval`, `Reviewed By`, `Rejection Comment`) VALUES ("%s", "%s", "%s", "%.2f", "%s", "%s", "%s", "%s", "%s")""" % (calendar_date, employee_id, status, relaxation, entered_by, comment, approval, reviewed_by, rejection_comment)
    elif mode =="Updation":
        sqlcmdstring = """UPDATE `workcalendar` SET `Status` = "%s", `Relaxation`="%.2f", `Entered By`="%s", `Comment`="%s", `Approval`="%s", `Reviewed By`="%s", `Rejection Comment`="%s" WHERE `Employee ID`="%s" AND `Date` = "%s";""" %(status, relaxation, user_id, comment, approval, reviewed_by, rejection_comment, employee_id, calendar_date)
    else:
        print "Mode error. %r is not a preset mode." % mode

    try:
        dbcursor.execute(sqlcmdstring)
    except MySQLdb.IntegrityError:
        raise
        print "Error. An entry already exists for %s on %s. Please change the mode to updation and try again." %(employee_id, calendar_date)
    except:
        print "Unaccounted error encountered in MOSES.addToWorkCalendar() while trying to process an %s for %s on %s." %(mode, employee_id, calendar_date)
        print "Printing the sqlcmdstring."
        print sqlcmdstring
        raise
    connectdb.commit()
    connectdb.close()

def rebuildLoginRecord(user_id, password):
    """Rebuilds the loginrecord table."""

    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """CREATE TABLE `loginrecord` (
`Date` Date Not Null,
`Employee ID` VARCHAR(20) NOT NULL,
`Login Time` DATETIME NOT NULL,
`Logout Time` DATETIME
);"""
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()


def createLoginStamp(user_id, password, login_date=None, login_time=None):
    """Makes a login entry in the loginrecord table."""
    if login_time is None:
        login_time = datetime.datetime.now()
    if login_date is None:
        login_date = datetime.date.today()
    status, relaxation = getWorkingStatus(user_id, password, login_date)
    if status == False:
        updateWorkCalendar(user_id, password, login_date, status="Working")

    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """INSERT INTO `loginrecord` (`Date`, `Employee ID`, `Login Time`) VALUES ("%s", "%s", "%s");"""%(convertToMySQLDate(login_date), user_id, login_time)
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def createLogoutStamp(user_id, password, logout_date=None, logout_time=None):
    """
    Records the logout time in the loginrecord table.
"""
    if logout_time is None:
        logout_time = datetime.datetime.now()
    if logout_date is None:
        logout_date = datetime.date.today()
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """UPDATE `loginrecord` SET `logout Time` = "%s" WHERE `Date` = "%s" AND `Employee ID` = "%s" AND `Logout Time` IS NULL;""" %(logout_time, logout_date, user_id)
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def isIdle(time_to_wait=None):
    import time
    import win32api
    if time_to_wait is None:
        time_to_wait = 60
    time.sleep(1) #Wait for a while.
    state_1 = win32api.GetLastInputInfo()
    time.sleep(time_to_wait)
    state_2 = win32api.GetLastInputInfo()
    return state_1 == state_2

def updateEmployeesTable(user_id, password):
    """Eventually, this method is going to be used to send a dictionary related to the employee table.
    For now, it's to update the DOL for certain employees."""
    connectdb = getOINKConnector(user_id, password)
    dbcursor = connectdb.cursor()
    employees_dict = [
        {"Employee ID": 54660, "DOL": datetime.date(2015,3,27)},
        {"Employee ID": 55863, "DOL": datetime.date(2015,3,4)},
        {"Employee ID": 56035, "DOL": datetime.date(2015,4,1)},
        {"Employee ID": 60877, "DOL": datetime.date(2015,3,19)},
        {"Employee ID": 61454, "DOL": datetime.date(2015,1,15)},
        {"Employee ID": 61949, "DOL": datetime.date(2015,3,5)},
        {"Employee ID": 62182, "DOL": datetime.date(2015,3,2)},
        {"Employee ID": 61904, "DOL": datetime.date(2015,3,11)}
        ]
    for employee in employees_dict:
        sqlcmdstring = "UPDATE `employees` SET `DOL` = '%s' WHERE `Employee ID`='%s'" % (convertToMySQLDate(employee["DOL"]), employee["Employee ID"])
        dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def populateStatsInWorkCalendar():
    import MySQLdb
    import MySQLdb.cursors
    import datetime
    import itertools
    print "Starting the process."
    start_time = datetime.datetime.now()
    u, p = getBigbrotherCredentials()
    conn = getOINKConnector(u, p)
    cursor = conn.cursor()
    print "Fetching all required rows of the work calendar."
    sqlcmdstring = """SELECT `Employee ID`, `Date` from `Workcalendar` where `Articles` is Null or `Audits` is Null OR `CFM` is Null OR `GSEO` is Null or `Efficiency` is Null;"""
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    counter = 1
    passed = 0
    total = len(data)
    print "Retrieved %d rows. Process starting now." %total
    last_update_time = datetime.datetime.now()   
    for row in data:
        query_date = row["Date"]
        query_id = row["Employee ID"]
        if getUserRole(u, p, query_id) == "Content Writer":
            try:
                articles = getArticleCount(u, p, query_date, query_id)
                audits = getAuditCount(u, p, query_date, query_id)
                efficiency = getEfficiencyFor(u, p, query_date, query_id)
                cfm = getCFMFor(u, p, query_date, query_id)
                gseo = getGSEOFor(u, p, query_date, query_id)
                if articles is None:
                    articles = '\N'
                if cfm is None:
                    cfm = "\N"
                if efficiency is None:
                    efficiency = "\N"
                if gseo is None:
                    gseo = '\N'
                sqlcmdstring = """UPDATE `workcalendar` SET `efficiency`="%s"  WHERE `Employee ID` = "%s" and `Date`="%s";""" %(efficiency, query_id, convertToMySQLDate(query_date))
                cursor.execute(sqlcmdstring)
                conn.commit()
                sqlcmdstring = """UPDATE `workcalendar` SET `CFM`="%s" WHERE `Employee ID` = "%s" and `Date`="%s";""" %(cfm, query_id, convertToMySQLDate(query_date))
                try:
                    cursor.execute(sqlcmdstring)
                except:
                    print sqlcmdstring
                conn.commit()
                sqlcmdstring = """UPDATE `workcalendar` SET `GSEO`="%s" WHERE `Employee ID` = "%s" and `Date`="%s";""" %(gseo, query_id, convertToMySQLDate(query_date))
                try:
                    cursor.execute(sqlcmdstring)
                except:
                    print sqlcmdstring
                conn.commit()
                sqlcmdstring = """UPDATE `workcalendar` SET `Articles`="%s" WHERE `Employee ID` = "%s" and `Date`="%s";""" %(articles, audits, query_id, convertToMySQLDate(query_date))
                try:
                    cursor.execute(sqlcmdstring)
                except:
                    print sqlcmdstring
                conn.commit()
                sqlcmdstring = """UPDATE `workcalendar` SET `Audits`="%s" WHERE `Employee ID` = "%s" and `Date`="%s";""" %(audits, query_id, convertToMySQLDate(query_date))
                try:
                    cursor.execute(sqlcmdstring)
                except:
                    print sqlcmdstring
                conn.commit()
                passed += 1
                print "Success."
                print "%d completed of %d. ETA: %s" %(counter, total, getETA(start_time, counter, total))
            except Exception, e:
                print sqlcmdstring
                raise
                print "*"*25
                #print repr(e)
                print "Writer ID: %s, Date= %s" %(query_id, query_date)
                if (datetime.datetime.now()-last_update_time)>datetime.timedelta(seconds=60):
                    print "%d completed of %d. ETA: %s" %(counter, total, getETA(start_time, counter, total))
                    last_update_time = datetime.datetime.now()
                print "*"*25
            counter += 1
    print "Passed: %d, total: %d, failed: %d" %(passed, total, total-passed)
    print "Time taken: %s" %(datetime.datetime.now()-start_time)
    conn.close()

def getReportingManager(user_id, password,  query_date=None, query_user=None):
    if query_user is None:
        query_user = user_id
    if query_date is None:
        query_date = datetime.date.today()
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """SELECT * from managermapping WHERE 
        `Employee ID`="%s" AND `Revision Date` = (
        SELECT MAX(`Revision Date`) FROM managermapping WHERE
        `Employee ID`="%s" AND `Revision Date`<="%s");""" %(query_user, query_user, convertToMySQLDate(query_date))
    #print sqlcmdstring
    cursor.execute(sqlcmdstring)
    manager_data = cursor.fetchall()
    conn.close()
    return manager_data[0]

def getRawDataParameterPercentagesBetween(user_id, password, start_date, end_date, query_user=None):
    import numpy
    if query_user is None:
        query_user = user_id
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    if query_user=="All":
        sqlcmdstring = """SELECT * FROM rawdata WHERE 
            `Audit Date` BETWEEN "%s" AND "%s";"""%(convertToMySQLDate(start_date), convertToMySQLDate(end_date))
    else:
        sqlcmdstring = """SELECT * FROM rawdata WHERE 
                `WriterID`="%s" 
                AND `Audit Date` BETWEEN "%s" AND "%s";"""%(query_user, 
                                        convertToMySQLDate(start_date), convertToMySQLDate(end_date))
    #print sqlcmdstring
    cursor.execute(sqlcmdstring)
    raw_data = cursor.fetchall()
    conn.close()
    cfm_score_lists = []
    gseo_score_lists = []
    #print len(raw_data)
    for entry in raw_data:
        cfm_scores, gseo_scores = getRawDataParameterPercentagesForRow(entry)
        cfm_score_lists.append(cfm_scores)
        gseo_score_lists.append(gseo_scores)

    cfm_list = getColumnAverages(cfm_score_lists)
    gseo_list = getColumnAverages(gseo_score_lists)
    return cfm_list, gseo_list

def getRawDataParameterPercentagesForRow(raw_data_row):
    max_scores = {
            "CFM01": 10.0,
            "CFM02": 10.0,
            "CFM03": 10.0,
            "CFM04": 10.0,
            "CFM05": 10.0,
            "CFM06": 10.0,
            "CFM07": 10.0,
            "CFM08": 5.0,
            "GSEO01": 5.0,
            "GSEO02": 5.0,
            "GSEO03": 2.5,
            "GSEO04": 2.5,
            "GSEO05": 2.5,
            "GSEO06": 2.5,
            "GSEO07": 5.0
    }
    process_dict = dict((key, raw_data_row[key]) for key in max_scores.keys())
    #print process_dict
    if raw_data_row["FAT01"] == "Yes" and raw_data_row["FAT01"] == "Yes" or raw_data_row["FAT03"] == "Yes":
        #print "Found fatal?"
        cfm_percentages_list = numpy.zeros(8)
        gseo_percentages_list = numpy.zeros(7)
    #if True:
    else:
        #print "No fatal."
        cfm_keys = [key for key in max_scores.keys() if "CFM" in key]
        cfm_keys.sort()
        #print cfm_keys
        gseo_keys = [key for key in max_scores.keys() if "GSEO" in key]
        gseo_keys.sort()
        #print gseo_keys
        cfm_percentages_list = [(process_dict[key]/max_scores[key]) for key in cfm_keys]
        gseo_percentages_list = [(process_dict[key]/max_scores[key]) for key in gseo_keys]
    return cfm_percentages_list, gseo_percentages_list

def getAuditPercentageBetween(query_user, start_date, end_date):
    user_id, password = getbbc()
    article_count = getArticleCountBetween(user_id, password, start_date-datetime.timedelta(days=1), end_date-datetime.timedelta(days=2), query_user)
    audit_count = getAuditCountBetween(user_id, password, start_date, end_date-datetime.timedelta(days=1), query_user)
    return audit_count/article_count

def showWriterAuditPercentages():
    start_date = datetime.date(2015,5,1)
    end_date = datetime.date.today()
    user_id, password = getbbc()
    writer_data_list = getWritersList(user_id, password, start_date)
    for writer in writer_data_list:
        writer_id = writer["Employee ID"]
        writer_name = writer["Name"]
        audit_percentage = getAuditPercentageBetween(writer_id, start_date, end_date)
        print writer_name, audit_percentage*100
    print "Done."

def getColumnAverages(data_list):
    import numpy
    data_array = numpy.array(data_list)
    #print data_array
    #given an array, this should return the average of all columns.
    averages_list = [numpy.mean(data_array[:,column_index]) for column_index in range(data_array.shape[1])]
    return averages_list

def getLastWorkingDayOfWeek(query_date):
    user_id, password = getBigbrotherCredentials()
    current_day = query_date.isocalendar()[2]
    day_difference = 5 - current_day
    while True:
        possible_last_date = query_date + datetime.timedelta(days=day_difference)
        if isWorkingDay(user_id, password, possible_last_date):
            break
        else:
            day_difference -= 1
    return possible_last_date

def dumpFSNsIntoFile(description_type = None):
    import pandas as pd
    user_id, password = getBigbrotherCredentials()
    start_time = datetime.datetime.now()
    last_update_time = datetime.datetime.now()
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    print "Trying to fetch data from fsn dump and the piggybank.\nThis step could take a while."
    if description_type is None:
        sqlcmdstring = """(SELECT `FSN`,`Item ID`, `Description Type` from `fsndump` WHERE 
            `Item ID` IS NOT NULL) UNION 
            (SELECT `FSN`,`Item ID`, `Description Type` from `piggybank` WHERE 
            `Item ID` IS NOT NULL);"""
    else:
        sqlcmdstring = """(SELECT `FSN`,`Item ID`, `Description Type` from `fsndump` WHERE 
            `Item ID` IS NOT NULL AND `Description Type` = "%s") UNION 
            (SELECT `FSN`,`Item ID`, `Description Type` from `piggybank` WHERE 
            `Item ID` IS NOT NULL AND `Description Type` = "%s");"""%(description_type, description_type)
    cursor.execute(sqlcmdstring)
    data_piggybank = cursor.fetchall()
    conn.close()
    print "Retrieved %d values." %len(data_piggybank)
    #print type(data_piggybank[0])
    #print type(data_piggybank[1000])
    #print type(data_piggybank)
    print "Writing to file."
    #print "Generating dataframe."
    data_frame = pd.DataFrame.from_records(data_piggybank)    
    #print data_frame.shape
    data_frame.to_csv("[%s]_FSN Dump.csv"%start_time.strftime("%Y%m%d"), sep=",")
    print "Successfully wrote to file."
    raw_input("Hit enter to exit.")
    #return data_piggybank, data_frame

def computeAuditAssignmentBetween(start_date, end_date=None, min_audit_percentage=None):
    """
    This function returns 4 dictionaries of dictionaries.
    1. writer_type_category_dictionary: A cross-table that counts 
        the "Article Count", "Audit Count" and "Audit Percentage"
        for each writer, giving the metrics at the type x category level.
        For example, for an employee (72062): this might return, for a particular date range,
        "72062": { 
                "Rich Product Description Plan A": 
                                {
                                    Watches":
                                        {
                                            "Article Count": 10,
                                            "Audit Count": 3,
                                            "Audit Percentage: 0.3 #This is >= the min_audit_percentage
                                            "Audits Picked": 3 #This number is for processing.
                                        }
                                }
    2. writer_dictionary: This table just contains the overall article count, 
        article count and audit percentage for a writer.
    3. category_type_dictionary: This table contains a similar method to #1. 
        Watches:{
            "Rich Product Description":
                {
                    "Article Count": 10,
                    "Audit Count": 3,
                    "Audit Percentage: 0.3 #This is >= the min_audit_percentage
                    "Audits Picked": 3 #This number is for processing.
                }
        }
    4. category_type_writer_dictionary: This table contains the inverse of #1, where the categories, 
        description types counts are mapped to writer_ids.

    First, these four are built using the piggybank data.
    Then, table #3 is constantly looped through.
    For each categoryxtype, the audit count is increased till the % hits min.
    While this is done, the same process is done for tables #4 and #1. 
    Here, the numbers are constantly monitored, so that the article count is exceeded.
    """
    import pandas as pd
    import numpy as np
    if end_date is None:
        end_date = start_date
    if min_audit_percentage is None:
        min_audit_percentage = 0.3
    user_id, password = getBigbrotherCredentials()
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    sqlcmdstring = """SELECT `Description Type`, `Category`, `WriterID`, `Writer Name` FROM `piggybank` WHERE `Article Date` BETWEEN "%s" AND "%s";""" %(start_date, end_date)
    #print sqlcmdstring
    cursor.execute(sqlcmdstring)
    data = cursor.fetchall()
    conn.close()
    #print data
    #Create a dataframe that contains the piggybank.
    piggy_bank_data_frame = pd.DataFrame.from_records(data)
    #print piggy_bank_data_frame
    #Create dictionaries to monitor writer audit % and writer category numbers.
    print "Computing the writer x type x category data set and the writer data set."
    writers_list = list(set(list(piggy_bank_data_frame["WriterID"])))
    writer_type_category_dictionary = dict((writer, {}) for writer in writers_list)
    writer_dictionary = dict((writer, {}) for writer in writers_list)
    for writer in writers_list:
        location_1 = (piggy_bank_data_frame["WriterID"] == writer)
        description_types =  list(set(list(description_type for description_type in list(piggy_bank_data_frame.loc[location_1,"Description Type"]))))
        articles_count = len(piggy_bank_data_frame.loc[location_1, "Description Type"].values)
        writer_dictionary[writer] = {"Article Count": articles_count, "Audit Count": 0, "Audit Percentage": 0.0, "Audits Picked": 0}
        writer_type_category_dictionary[writer] = dict((description_type,{}) for description_type in description_types)
        for description_type in description_types:
            location_2 = (piggy_bank_data_frame["WriterID"] == writer) & (piggy_bank_data_frame["Description Type"] == description_type)
            categories =  list(set(list(category for category in list(piggy_bank_data_frame.loc[location_2,"Category"]))))
            writer_type_category_dictionary[writer][description_type] = dict((category,{}) for category in categories)
            for category in categories:
                location_3 = (piggy_bank_data_frame["WriterID"] == writer) & (piggy_bank_data_frame["Description Type"] == description_type) &(piggy_bank_data_frame["Category"] == category)
                count_articles = len(piggy_bank_data_frame.loc[location_3, "Category"].values)
                writer_type_category_dictionary[writer][description_type][category] = {"Article Count": count_articles, "Audit Count": 0, "Audit Percentage": 0.0, "Audits Picked": 0}
    print "Computing the category x type data set and the category x type x writer data set."
    categories_list = list(piggy_bank_data_frame["Category"])
    category_type_writer_dictionary = dict((category, {}) for category in categories_list)
    category_type_dictionary = dict((category, {}) for category in categories_list)
    for category in categories_list:
        location_1 = (piggy_bank_data_frame["Category"] == category)
        description_types = list(description_type for description_type in list(piggy_bank_data_frame.loc[location_1,"Description Type"]))
        #print description_type
        category_type_dictionary[category] = dict((description_type,{}) for description_type in description_types)
        category_type_writer_dictionary[category] = dict((description_type,{}) for description_type in description_types)
        for description_type in description_types:
            location_2 = (piggy_bank_data_frame["Category"] == category) & (piggy_bank_data_frame["Description Type"] == description_type)
            article_count = len(piggy_bank_data_frame.loc[location_2, "Description Type"].values)
            category_type_dictionary[category][description_type] = {"Article Count":article_count, "Audit Count": 0, "Audit Percentage": 0, "Audits Picked": 0}
            writers = list(set(list(piggy_bank_data_frame.loc[location_2, "WriterID"])))
            category_type_writer_dictionary[category][description_type] = dict((writer,{}) for writer in writers)

            for writer in writers:
                location_3 = (piggy_bank_data_frame["Category"] == category) & (piggy_bank_data_frame["Description Type"] == description_type) & (piggy_bank_data_frame["WriterID"] == writer)
                article_count = len(piggy_bank_data_frame.loc[location_2, "WriterID"].values)
                #print category, description_type, writer
                #print category_type_writer_dictionary[category]
                category_type_writer_dictionary[category][description_type][writer] = {"Article Count": article_count, "Audit Count": 0, "Audit Percentage": 0.0, "Audits Picked": 0}
            #Give 1 audit to all category x types.
    print "Completed building the data sets."
    print "Starting the process loop. Minimum Audit Percentage is %.2f" %min_audit_percentage
    #loop through category_type_dictionary and pick out those which are zero.
    categories_list = list(piggy_bank_data_frame["Category"]) #I can remove this, probably.
    for category in categories_list:
       #location_1 = (piggy_bank_data_frame["Category"] == category)
        description_types = category_type_dictionary[category].keys()
        for description_type in description_types:
            audit_percentage = category_type_dictionary[category][description_type]["Audit Percentage"]
            article_count =  category_type_dictionary[category][description_type]["Article Count"]
            audit_count = category_type_dictionary[category][description_type]["Audit Count"]
            #While the audit percentage is below the minimum, increase the audit count by 1 and recalculate the aud_%.
            while audit_percentage < min_audit_percentage:
                    audit_count = category_type_dictionary[category][description_type]["Audit Count"]
                    audit_count +=1
                    category_type_dictionary[category][description_type]["Audit Count"] = audit_count
                    audit_percentage = audit_count/article_count
                    category_type_dictionary[category][description_type]["Audit Percentage"] = audit_percentage
            audit_count = category_type_dictionary[category][description_type]["Audit Count"]        
    writers_list = list(set(list(piggy_bank_data_frame["WriterID"])))
    for writer in writers_list:
        audit_percentage = writer_dictionary[writer]["Audit Percentage"]
        article_count = writer_dictionary[writer]["Article Count"]
        while audit_percentage < min_audit_percentage:
            audit_count = writer_dictionary[writer]["Audit Count"]
            audit_count += 1
            writer_dictionary[writer]["Audit Count"] = audit_count
            audit_percentage = audit_count/article_count
            writer_dictionary[writer]["Audit Percentage"] = audit_percentage
    print "Completed."
    #Write a segment that checks if the total audit count is constant. If not, it should raise a ValueError.
    total_writer_audits = sum([writer_dictionary[writer]["Audit Count"] for writer in writers_list])
    writer_audit_percentages = [writer_dictionary[writer]["Audit Percentage"] for writer in writers_list]
    total_category_audits = 0
    category_audit_percentages = []
    for category in category_type_dictionary.keys():
        for d_type in category_type_dictionary[category].keys():
            total_category_audits += category_type_dictionary[category][d_type]["Audit Count"]
            category_audit_percentages.append(category_type_dictionary[category][d_type]["Audit Percentage"])
    print "%d audits required to satisfy writer percentages. %d required for category audit percentage coverage." %(total_writer_audits, total_category_audits)
    category_audit_percentages.sort()
    writer_audit_percentages.sort()
    min_writer_audit_percentage = min(writer_audit_percentages)
    min_category_audit_percentage = min(category_audit_percentages)
    #print "Minimum Audit Percentage: %.4f (Writers); %.4f (Category Level);" %(min_writer_audit_percentage, min_category_audit_percentage)
    #print "Writer Percentages:", writer_audit_percentages
    #print "Category Percentages:", category_audit_percentages
    if total_writer_audits > total_category_audits:
        required_audit_count = total_writer_audits
        print "The deciding data set should be the writer cross tabulation. Thus, a total %d audits is required." %required_audit_count
    else:
        required_audit_count = total_category_audits
        print "The deciding data set should be the category cross tabulation. Total %d audits required." %required_audit_count
    #    for category in category_type_dictionary.keys():
    #        for description_type in category_type_dictionary[category].keys():

    return writer_dictionary, writer_type_category_dictionary, category_type_dictionary, category_type_writer_dictionary


def getAllTeamWorkingDays():
    user_id, password = getBigbrotherCredentials()
    start_date = datetime.date(2015,1,1)
    end_date = datetime.date.today()
    dates_list = []
    conn = getOINKConnector(user_id, password)
    cursor = conn.cursor()
    working_dates = getWorkingDatesBetween(user_id, password, start_date, end_date, mode="All")
    for date_ in working_dates:
        sqlcmdstring = """SELECT count(*) from workcalendar WHERE `Status`="Leave" and `Date`="%s";""" %date_
        cursor.execute(sqlcmdstring)
        data = cursor.fetchall()
        #print data
        if data[0]['count(*)'] == 0:
            dates_list.append(date_)
    conn.close()
    return len(dates_list), len(working_dates)

if __name__ == "__main__":
    print "Never call Moses mainly."