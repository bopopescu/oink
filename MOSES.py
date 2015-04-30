#!usr/bin/python2
# -*- coding: utf-8 -*-
#Modular OINK SQL Engagement Service
"""
Includes all the methods relevant to using MySQL-Python.
"""
import datetime
import csv
import os
import MySQLdb
import MySQLdb.cursors
import codecs
import OINKMethods as OINKM


#########################################################################
#Set up methods. These methods help set up the server for the first time.
#Be very careful while using these since they will delete all existing data.
#########################################################################

def rebuildRawData(userid, password):
    """This method deletes the current raw data and redefines it."""
    rawdatadb = MySQLdb.connect(host=getHostID(), \
            user=userid,passwd=password,db=getDBName(),\
            cursorclass=MySQLdb.cursors.DictCursor)
    rawdatadbcursor = rawdatadb.cursor()
    rawdatadbcursor.execute("DROP TABLE IF EXISTS `rawdata`")
    sqlcmdstring = """CREATE TABLE `rawdata` (
`WriterID` int(10) NOT NULL,
`Category` varchar(50),
`Sub-Category` varchar(50),
`QAID` varchar(10),
`AuditDate` DATE,
`WS Name` varchar(450) DEFAULT 'NA',
`WC` varchar(50),
`FSN` varchar(50) NOT NULL,
`Introduction` FLOAT(5,3),
`Product Theme` FLOAT(5,3),
`Flow of Article` FLOAT(5,3),
`Explain Features [in simple terms]` FLOAT(5,3),
`Practical Application of Features` FLOAT(5,3),
`Neutral Content` FLOAT(5,3),
`USP` FLOAT(5,3),
`Priority of Features` FLOAT(5,3),
`Sentence Construction` FLOAT(5,3),
`Sub-verb agreement` FLOAT(5,3),
`Missing/ additional/ repeated words` FLOAT(5,3),
`Spelling/ Typo` FLOAT(5,3),
`Punctuation` FLOAT(5,3),
`Formatting Errors` FLOAT(5,3),
`Keyword Variation` FLOAT(5,3),
`Keyword Density` ENUM('YES','NO') DEFAULT 'NO',
`Plagiarism` ENUM('YES','NO') DEFAULT 'NO',
`Mismatch in Specs` ENUM('YES','NO') DEFAULT 'NO',
`CFM Quality` FLOAT(5,4),
`GSEO Quality` FLOAT(5,4),
`Overall Quality` FLOAT(5,4),
`Fatals Count` INT(2) DEFAULT '0',
`Non Fatals Count` INT(2) DEFAULT '0',
`Introduction comments` VARCHAR(500) DEFAULT 'NA',
`Product Theme comments` VARCHAR(500) DEFAULT 'NA',
`Flow of Article comments` VARCHAR(500) DEFAULT 'NA',
`Explain Features [in simple terms] comments` VARCHAR(500) DEFAULT 'NA',
`Practical Application of Features comments` VARCHAR(500) DEFAULT 'NA',
`Neutral Content comments` VARCHAR(500) DEFAULT 'NA',
`USP comments` VARCHAR(500) DEFAULT 'NA',
`Priority of Features comments` VARCHAR(500) DEFAULT 'NA',
`Sentence Construction comments` VARCHAR(500) DEFAULT 'NA',
`Sub-verb agreement comments` VARCHAR(500) DEFAULT 'NA',
`Missing/ additional/ repeated words comments` VARCHAR(500) DEFAULT 'NA',
`Spelling/ Typo comments` VARCHAR(500) DEFAULT 'NA',
`Punctuation comments` VARCHAR(500) DEFAULT 'NA',
`Formatting Errors comments` VARCHAR(500) DEFAULT 'NA',
`Keyword Variation comments` VARCHAR(500) DEFAULT 'NA',
`Keyword Density comments` VARCHAR(500) DEFAULT 'NA',
`Plagiarism comments` VARCHAR(500) DEFAULT 'NA',
`Mismatch in Specs comments` VARCHAR(500) DEFAULT 'NA',
`Audit Count` INT(2) Default '1'
)"""
    rawdatadbcursor = rawdatadb.cursor()
    #print sqlcmdstring #debug
    rawdatadbcursor.execute(sqlcmdstring)
    rawdatadb.commit()
    rawdatadb.close()
    return True

def uploadRawData(userid,password):
    """Method to bulk upload raw data from a CSV file to MySQL.
    Notes to self:
    1. The writer name column in the csv file should be replaced with their employee Ids.
    2. The Audit Date should be reformatted into the YYYY-MM-DD format.
    """
    rawdatadb = MySQLdb.connect(host=getHostID(), \
            user=userid,passwd=password,db=getDBName(),\
            cursorclass=MySQLdb.cursors.DictCursor)
    rawdatadbcursor = rawdatadb.cursor()
    #delete all data in the current Raw Data field.
    rebuildRawData(userid,password) 
    sqlcmdstring = "LOAD DATA LOCAL INFILE 'Database/rawdata.csv' INTO TABLE oink.rawdata FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    rawdatadbcursor.execute(sqlcmdstring)
    rawdatadb.commit()
    rawdatadb.close()
    #print sqlcmdstring
    return True

def rebuildPiggyBank(userid,password):
    """Deletes the current piggy bank and redefines it."""
    piggybankdb = MySQLdb.connect(host=getHostID(),user=userid,passwd=password,db=getDBName(),cursorclass = MySQLdb.cursors.DictCursor)
    piggycursor = piggybankdb.cursor()
    sqlcmdstring = "DROP TABLE IF EXISTS `piggybank`;"
    piggycursor.execute(sqlcmdstring)
    sqlcmdstring = """CREATE TABLE `piggybank` (
`FSN` VARCHAR(150) NOT NULL,
`WriterID` VARCHAR(20),
`Article Date` DATE,
`Source` ENUM('Inhouse','Crowdsourced') DEFAULT "Inhouse",
`Description Type` ENUM('Regular Description','Rich Product Description','Rich Product Description Plan A', 'Rich Product Description Plan B','SEO Big', 'SEO Small', 'SEO Project','RPD Updation','RPD Variant') NOT NULL DEFAULT "Regular Description",
`BU` VARCHAR(50),
`Super-Category` VARCHAR(50),
`Category` VARCHAR(50),
`Sub-Category` VARCHAR(50),
`Vertical` VARCHAR(50),
`Brand` VARCHAR(50),
`Word Count` INT(5) DEFAULT '0',
`Upload Link` VARCHAR(500),
`Reference Link` VARCHAR(500),
`Rewrite Ticket` ENUM('No','First Instance','Second Instance','Third Instance','Fourth Instance') NOT NULL DEFAULT 'No',
PRIMARY KEY (`FSN`,`Description Type`,`Rewrite Ticket`)
)"""
    piggycursor.execute(sqlcmdstring)
    piggybankdb.commit()
    piggybankdb.close()
    return True

def uploadPiggyBank(userid,password):
    """Method to bulk upload piggy bank data from a CSV file to MySQL."""
    piggybankdb = MySQLdb.connect(host=getHostID(), user=userid, passwd=password, db=getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
    piggycursor = piggybankdb.cursor()
    rebuildPiggyBank(userid,password)
    #Write the code to read and upload all the data in a piggybank.csv 
    #file to the MySQL database.
    sqlcmdstring = "LOAD DATA LOCAL INFILE 'Database/piggybank.csv' INTO TABLE oink.piggybank FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    piggycursor.execute(sqlcmdstring)
    piggybankdb.commit()
    piggybankdb.close()
    return True

def rebuildEmployeesTable(userid,password):
    """Rebuilds the employee table in the database."""
    employeedb = MySQLdb.connect(host = getHostID(), user = userid, passwd = password, db = getDBName(),cursorclass = MySQLdb.cursors.DictCursor)
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
    
def uploadEmployeesTable(userid, password):
    """Uploads the employees table from a csv file into the server."""
    rebuildEmployeesTable(userid, password)
    employeedb = MySQLdb.connect(host = getHostID(), user = userid, passwd = password, db = getDBName(),cursorclass = MySQLdb.cursors.DictCursor)
    empcursor = employeedb.cursor()
    sqlcmdstring = """LOAD DATA LOCAL INFILE 
'Database/employeetable.csv' INTO TABLE %s.employees FIELDS 
TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;""" %getDBName()
    #print sqlcmdstring #debug
    empcursor.execute(sqlcmdstring)
    employeedb.commit()
    employeedb.close()
    

def rebuildClarifications(userID,password):
    """This method drops the current Clarifications table and redefines it."""
    "Creating a new clarifications table."
    connectdb = MySQLdb.connect(host = getHostID(), user = userID, passwd = password, db =getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "DROP TABLE IF EXISTS `clarifications`;"
    dbcursor.execute(sqlcmdstring)
    sqlcmdstring = "CREATE TABLE `clarifications` (`Code` VARCHAR(10) NOT NULL, `Description` VARCHAR(500), PRIMARY KEY (`Code`));"
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def uploadClarifications(userID,password):
    """This method uploads the data in the clarifications csv file into the database. Run from the VINDALOO folder only."""
    print "Uploading new clarifications table."
    connectdb = MySQLdb.connect(host = getHostID(), user = userID, passwd = password, db =getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "LOAD DATA LOCAL INFILE 'Database/clarifications.csv' INTO TABLE `clarifications` FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()


def uploadFSNDump(userid,password):
    """Creates the fsndata table, and loads all the data into it."""
    fsndumpdb = MySQLdb.connect(host=getHostID(),user=userid,passwd=password,db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
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

def rebuildCategoryTree(userID,password):
    """This method drops the current Category Tree and redefines it."""
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
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

def uploadCategoryTree(userID,password):
    rebuildCategoryTree(userID,password)
    connectdb=MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
    dbcursor=connectdb.cursor()
    sqlcmdstring="""LOAD DATA LOCAL INFILE 'Database/categorytree.csv' INTO 
TABLE `categorytree` FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES"""
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def rebuildCosting(userID,password):
    """This method drops the current Category Tree and redefines it."""
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
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

def initUsers(userID, password):
    """Loops through the employees table and creates a userid for each of the
    users listed."""
    for employee in getEmployeesList(userID, password):
        createUser(employee["Employee ID"],employee["Role"],userID,password)
        resetPassword(employee["Employee ID"], userID, password)
    return True

def rebuildWorkCalendar(userID,password):
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
    dbcursor=connectdb.cursor()
    sqlcmdstring="DROP TABLE IF EXISTS `workcalendar`;"
    dbcursor.execute(sqlcmdstring)
    sqlcmdstring ="""CREATE TABLE `workcalendar` (
`Date` DATE NOT NULL,
`Employee ID` INT(10) NOT NULL DEFAULT '0',
`Status` ENUM('Working','Leave','Planned Leave','Sick Leave', 'Emergency Leave','Company Holiday') DEFAULT 'Working',
`Relaxation` float(3,2) DEFAULT '0.00',
`Entered By` ENUM('Writer','Team Lead','Copy Editor','Assistant Manager','Manager','Big Brother'),
`Comment` VARCHAR(500),
`Approval` ENUM('Approved','Rejected'),
`Rejection Comment` VARCHAR(500),
PRIMARY KEY (`Date`,`Employee ID`)
);"""
#    print sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def uploadWorkCalendar(userid,password):
    """Uploads all the data in the work calendar csv file into the database."""
    connectdb = MySQLdb.connect(host = getHostID(), user = userid, passwd = password, db = getDBName())
    dbcursor = connectdb.cursor()
    sqlcmdstring = "LOAD DATA LOCAL INFILE 'Database/workcalendar.csv' INTO TABLE oink.workcalendar FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES;"
#    print sqlcmdstring
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def initiateDatabase():
    """This module initializes the server for use."""
    #if "V.I.N.D.A.L.O.O" in os.getcwd():
    if True:
        userID, password = getBigbrotherCredentials()
        print "Creating a new Raw Data table and uploading new data."
        uploadRawData(userID,password)
        print "Creating a new piggy bank dump and uploading new data."
        uploadPiggyBank(userID,password)
        print "Creating a new FSN Dump and uploading the new data."
        uploadFSNDump(userID, password)
        print "Creating a new employee table and uploading the new data."
        uploadEmployeesTable(userID,password)
        print "Creating a new category tree and uploading the new data."
        uploadCategoryTree(userID,password)
        print "Creating the costing table."
        rebuildCosting(userID,password)
        print "Creating the Work Calendar table."
        rebuildWorkCalendar(userID,password)
        print "Uploading the Work Calendar table."
        uploadWorkCalendar(userID,password)
        print "Creating a new clarifications table and uploading the table."
        rebuildClarifications(userID,password)
        uploadClarifications(userID,password)
        print "Creating the required users."
        initUsers(userID,password)
    else:
        print "Run this from the V.I.N.D.A.L.O.O folder."

def rebuildAuditParametersTable():
    """Deletes any existing audit parameters table in the MySQL database and redefines it."""

def uploadAuditParametersTable():
    """Uploads all data in auditparameters.csv file into the MySQL database."""

def makePORKChops():
    """Combines the Piggy Bank and the Raw Data tables into a PORKChops table."""

def rebuildFSNInformationTable():
    """Deletes any exisitng FSNInformation table and recreates it."""

def uploadFSNInformationTable():
    """Uploads data into the table from a csv file."""

def rebuildOverideRecord(userID, password):
    """Rebuilds the overriderecord table in the database"""
    connectdb = MySQLdb.connect(host = getHostID(), user = userID, passwd = password, db = getDBName())
    dbcursor = connectdb.cursor()
    sqlcmdstring = "DROP TABLE IF EXISTS `overiderecord`;"
    dbcursor.execute(sqlcmdstring)
    sqlcmdstring = """CREATE TABLE `overiderecord` (
`FSN` VARCHAR(30) NOT NULL,
`Overide Date` DATE NOT NULL,
`Overidden By` VARCHAR(100) NOT NULL,
PRIMARY KEY (`FSN`, `Overide Date`, `Overidden By`)
);"""
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()
 
#########################################################################
#Regular methods
#These methods are regularly used while running the application.
#########################################################################

def getWorkingStatus(userid, password, querydate, lookupuser=None):
    """Method to fetch the status for a writer on any particular date.
    Returns "Working" if the employee is delivering 100%.
    Returns "Leave" if the employee is on leave.
    Returns n/10 if the employee is granted a relaxation of n%
    Returns "Holiday" if the company has granted a holiday on a particular date.
    If lookupuser isn't specified, it'll just pull the status for the current user.
    """
    status = "Working"
    connectdb = MySQLdb.connect(host = getHostID(), user = userid, 
                        passwd = password, db = getDBName(),
                        cursorclass = MySQLdb.cursors.DictCursor)
    dbcursor = connectdb.cursor()
    if lookupuser == None:
        lookupuser = userid
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


def updatePiggyBankEntry(entryDict, userid, password):
    """Method to update the values in an entry in the piggybank. This cross-checks the FSN with the date. 
    possible bugs: 1. It will not allow updation of date, writerID or FSN.
    """
    connectdb = MySQLdb.connect(host = getHostID(), user = userid, 
                    passwd = password, db = getDBName(), 
                    cursorclass = MySQLdb.cursors.DictCursor)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """UPDATE `piggybank` SET `Source` = '%(Source)s', 
`Description Type` = '%(Description Type)s', `BU` = '%(BU)s', `Super-Category` = '%(Super-Category)s', 
`Category` = '%(Category)s', `Sub-Category` = '%(Sub-Category)s', `Vertical` = '%(Vertical)s', 
`Brand` = '%(Brand)s', `Word Count` = '%(Word Count)s', `Upload Link` = '%(Upload Link)s', 
`Reference Link` = '%(Reference Link)s', `Rewrite Ticket` = '%(Rewrite Ticket)s'
where `FSN` = '%(FSN)s' AND `Article Date` = '%(Article Date)s' 
AND `WriterID` = '%(WriterID)s';""" % entryDict
    try:
        dbcursor.execute(sqlcmdstring)
    except Exception, e:
        print "Unknown error while trying to upload piggybank."
        print "The command string is:\n%s" % sqlcmdstring
        print "The error is: ", repr(e)
    connectdb.commit()
    connectdb.close()


def addToPorkChops(porkChopsDict, userid, password):
    """Method to send a single entry to Pork Chops from a 
    python dictionary"""
    return True

def addToPiggyBank(piggyBankDict, userid, password):
    """Method to send a single entry to Piggy Bank from a
    python Dictionary"""
    #test dictionary
    #merge all keys and values names into one string, separated by commas.
    columnsList, valuesList = getDictStrings(piggyBankDict)
    #rebuildPiggyBank(userid, password)
    piggybankdb = MySQLdb.connect(host = getHostID(), user = userid, passwd = password, db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
    piggycursor = piggybankdb.cursor()
    sqlcmdstring = "INSERT INTO `piggybank` (%s) VALUES (%s);" % (columnsList, valuesList)
    #print sqlcmdstring #debug
    try:
        piggycursor.execute(sqlcmdstring)
        returnValue = "True"
    except MySQLdb.IntegrityError:
        error = "Duplicate entry not possible. Request repeat instance approval."
        print error
        returnValue = error
    except Exception, e:
        error = repr(e)
        print error
        returnValue = error 
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
            valuesString = "'" + value + "'"
        else:
            valuesString = valuesString + ", '" + str(value) + "'"
    return keysString, valuesString

def markCalendar(calendarEntryDict):
    """Method to mark an entry into the work calendar from a 
    python dictionary."""
    return True

def readFromPorkChops(queryDict,userid,password):
    """Method to read data from Pork Chops and return all data for
    a query."""
    return True

def readFromPiggyBank(queryDict, userid, password):
    """Method to read data from Piggy Bank and return all data for
    a query."""

    piggybankdb = MySQLdb.connect(host=getHostID(), user=userid, passwd=password, db=getDBName(), cursorclass=MySQLdb.cursors.DictCursor)
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
    keys_list = ["Article Date", "WriterID", "FSN", "Source", "Description Type", "BU", "Super-Category", "Category", "Sub-Category", "Vertical", "Brand", "Word Count", "Upload Link", "Reference Link", "Rewrite Ticket"]
    return keys_list

def writePorkChopsDictToFile(porkChopsDict):
    """Method to bulk export Pork Chops data to a file for a query."""
    return True

def writePiggyBankDictToFile(queryDict):
    """Method to bulk export Piggy Bank data to a file for a query."""
    return True

def getPiggyBankDataBetweenDates(startDate, endDate, queryDict, userid, password):
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
    #feed the dictionary to the getPiggyBankMultiQuery()
    return getPiggyBankMultiQuery(multiQueryDict, userid, password)

def convertToMySQLDate(queryDate):
    """Takes a python datetime and changes it to the YYYY-MM-DD format 
    for MySQL. 
    Uses the OINKModule2 module's changeDatesToStrings method."""
    dateString = OINKM.changeDatesToStrings(queryDate,"YYYY-MM-DD")
    return dateString[0]

def getPiggyBankMultiQuery(queryDictList, userid, password):
    """Method to extract Piggy Bank data from the database corresponding
    to multiple queries."""
    #Breaks down the list into separate dictionaries, and then feeds each 
    #query dictionary to the appropriate method, collects the answers and 
    #returns that.
    resultList = []
    for query in queryDictList:
        if type(query) == type({}):
            #print query #debug
            resultList.append(readFromPiggyBank(query,userid,password))
        else:
            print "Unknown query, printing verbatim.\n%s" % query
    return resultList

def createUser(newUserID,userClass,userid,password):
    """This method creates a new user with appropriate permissions 
    according to the userClass."""
    dbname = getDBName()
    connecteddb = MySQLdb.connect(host = getHostID(), user = userid, passwd = password, db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
    dbcursor = connecteddb.cursor()
    sqlcmdstring = "CREATE USER '%s' IDENTIFIED BY 'password'" %newUserID
    try:
        dbcursor.execute(sqlcmdstring)
    except MySQLdb.OperationalError, e:
        if newUserID in getUsersList(userid, password):
            print "There is already a user defined by %s, please contact bigbrother." %newUserID
        else:
            print "Unknown Error!"
            error = repr(e)
            print error

    if userClass=="Content Writer":
        sqlcmdstring = "GRANT SELECT on %s.* TO '%s';" % (dbname, newUserID)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT ON %s.workcalendar To '%s';" %(dbname, newUserID)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT, DELETE ON %s.piggybank To '%s';" %(dbname, newUserID)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
    elif userClass == "Copy Editor":
        sqlcmdstring = "GRANT SELECT on %s.* TO '%s';" % (dbname, newUserID)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT, DELETE ON %s.rawdata To '%s';" %(dbname, newUserID)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
    elif userClass == "Team Lead":
        sqlcmdstring = "GRANT SELECT on %s.* TO '%s';" % (dbname, newUserID)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)
        sqlcmdstring = "GRANT SELECT, UPDATE, INSERT, DELETE ON %s.workcalendar To '%s';" %(dbname, newUserID)
        #print sqlcmdstring #debug
        dbcursor.execute(sqlcmdstring)      
    elif userClass == "Super":
        #print sqlcmdstring #debug
        sqlcmdstring = "GRANT ALL PRIVILEGES ON %s.* To '%s' WITH GRANT OPTION;" %(dbname, newUserID)
    else:
        print "Wrong user class. Cannot set privileges for %s." % userClass
    connecteddb.commit()
    connecteddb.close()

def getUsersList(userid,password):
    superdb = MySQLdb.connect(host = getHostID(), user = userid, passwd = password,\
                    db = "mysql",cursorclass = MySQLdb.cursors.DictCursor)
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

def getClarifications(userID,password):
    """Returns a list of all the clarifications."""
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,db=getDBName(),cursorclass = MySQLdb.cursors.DictCursor)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT `Code` FROM clarifications"
    dbcursor.execute(sqlcmdstring)
    clarTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    clarList = [clar["Code"] for clar in clarTuple]
    return clarList


def addEmployee(employeeDict,userid,password):
    """Takes a dictionary with employee data. The fields are Employee ID, Name, Email-ID, DOJ and Current Class"""
    employeesdb = MySQLdb.connect(host=getHostID(),user=userid,passwd=password,db=getDBName(),cursorclass = MySQLdb.cursors.DictCursor)
    empcursor = employeesdb.cursor()
    keysString, valuesString = getDictStrings(employeeDict)
    sqlcmdstring = "INSERT INTO `employees` (%s) VALUES (%s);" % (keysString,valuesString)
    try:
        empcursor.execute(sqlcmdstring)
        createUser(employeeDict["employee id"],employeeDict["current class"],userid,password)
    except MySQLdb.ProgrammingError, e:
        if employeeDict["employee id"] in getEmployeesList(userid,password):
            print "There is already an employee with that name."
        else:
            error = repr(e)
            print error
    except Exception, e:
        error = repr(e)
        print error
    employeedb.commit()
    employeedb.close()
    return True

def getEmployeesList(userid,password):
    """Returns a list of all the employees IDs currently in the table."""
    employeesdb = MySQLdb.connect(host=getHostID(),user=userid,passwd=password,db=getDBName(),cursorclass = MySQLdb.cursors.DictCursor)
    empcursor = employeedb.cursor()
    sqlcmdstring = "SELECT `Employee ID` FROM employees"
    empcursor.execute(sqlcmdstring)
    employeesTuple = empcursor.fetchall()
    employeesList = []
    for employeeTuple in employeeTuples:
            employeesList.append(employeesTuple["employee id"])
    employeesdb.commit()
    employeesdb.close()
    return employeesList

def checkUserID(userID):
    superID, superPassword = getBigbrotherCredentials()
    return userID in getUsersList(superID, superPassword)

def checkPassword(userID,password):
    success,error = False,"Unchecked"
    if checkUserID(userID):
        try:
            oinkdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
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
    userID = "bigbrother"
    password = str(codecs.decode('bejryy',"rot_13")) #using the rot_13 encryption method to hide password.
    #print password #debug
    return userID, password

def getEmpName(employeeID):
    userID, password = getBigbrotherCredentials()
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT `Name` FROM `employees` WHERE `Employee ID` = '%s'" %employeeID
    dbcursor.execute(sqlcmdstring)
    nameTuple = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    name = nameTuple[0]["Name"]
    return name

def resetOwnPassword(userID,password,newpassword):
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,db=getDBName())
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SET PASSWORD = PASSWORD('%s');" %newpassword
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()
    return True

def getEmployeesList(userID,password):
    """Returns a list of employees' IDs"""
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
    dbcursor=connectdb.cursor()
    sqlcmdstring="""SELECT `Employee ID`, `Role` from `employees`;
"""
    dbcursor.execute(sqlcmdstring)
    employeesData=dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    return employeesData

def resetPassword(user_To_Reset, userID, password):
    """Resets the password of user_To_Reset to 'password'."""
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
    dbcursor=connectdb.cursor()
    sqlcmdstring="SET PASSWORD FOR `%s` = PASSWORD('password');" %user_To_Reset
    print "Resetting password for ", user_To_Reset
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def getPiggyBankDataForDate(queryDate,userid,password):
    return getPiggyBankDataBetweenDates(queryDate,queryDate,{},userid,password)

def getUserPiggyBankData(queryDate,userid,password,queryUser=None):
    #print "In getUserPiggyBankData"
    if queryUser == None:
        queryUser = userid
    queryDict = {"WriterID" : queryUser}
    return getPiggyBankDataBetweenDates(queryDate,\
                queryDate,queryDict,userid,password)[0]

def checkWorkStatus(queryDate, userid, password,targetUser = None):
    """This method checks the work calendar in the database and checks whether the employee is working or not on that particular date."""
    #print "In checkWorkStatus"
    if targetUser == None:
        targetUser = userid
    connectdb = MySQLdb.connect(host = getHostID(), user = userid, passwd = password, db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
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
        print "Unknown error in MOSES.checkWorkStatus.\nPrinting verbatim:\n%s" % repr(e)
    #print status, relaxation, approval
    #print "Leaving checkWorkStatus"
    return status, relaxation, approval

def getEfficiencyForDateRange(userID,password,startDate,endDate,queryUser=None):
    """Returns the efficiency for an employee for all dates between two dates."""
    #print "In getEfficiencyForDateRange"
    if queryUser == None:
        queryUser = userID
    datesList = OINKM.getDatesBetween(startDate,endDate)
    efficiency = 0.0
    days = 0
    for queryDate in datesList:
        efficiency += getEfficiencyFor(userID, password, queryDate, queryUser)
        days += 1   
    #print "Total efficiency: %f for %d days." % ((efficiency / days), days)
    #print "Leaving getEfficiencyForDateRange"
    return efficiency

def getEfficiencyFor(userID, password, queryDate, queryUser = None):
    """Returns the total efficiency for a user for a particular date."""
    #print "In getEfficiencyFor"
    if queryUser == None:
        queryUser = userID
    requestedData = getUserPiggyBankData(queryDate, userID, password, queryUser)
    #print "Received a %s of %d length." %(type(requestedData),len(requestedData))
    efficiency = 0.0
    status, relaxation, approval = checkWorkStatus(queryDate, userID, password,queryUser)
    if (status == "Working") or (approval != "Approved"):
        #Calculate only for working days
        if relaxation > 0.0:
            efficiencyDivisor = 1.0/relaxation
        else:
            efficiencyDivisor = 1.0
        #This doesn't account for negative relaxation, scenarios where a writer must make up. Does it need to? I don't really think so.
        for entry in requestedData:
            #pass the classification identifiers to the method.
            target = getTargetFor(userID, password, BU = entry["BU"], DescriptionType = entry["Description Type"], Source = entry["Source"], SuperCategory = entry["Super-Category"], Category = entry["Category"], SubCategory = entry["Sub-Category"], Vertical = entry["Vertical"], QueryDate = queryDate)
            if target == 0.0:
                efficiency += 0.0
            else:
                efficiency += 1.0/target
    elif status == "Leave" or status == "Company Holiday":
        effiency = 1.0
    #print efficiency
    #print "Leaving getEfficiencyFor"
    return efficiency

def getTargetFor(userID,password,**query):
    """Returns target for a combination of queries."""
    #print "In getTargetFor"
    try:
        BUString = query["BU"]
        TypeString = query["DescriptionType"]
        SourceString = query["Source"]
        SupCatString = query["SuperCategory"]
    except:
        print "Error Message: BU, Super-Category, Source and Type are necessary!"
        return "Error. BU, Super-Category, Source and Type are necessary!"
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
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)  
    dbcursor=connectdb.cursor()
    sqlcmdstring = """SELECT `Target`, `Revision Date` FROM `categorytree` 
WHERE `BU`='%s' AND `Super-Category`='%s' AND `Category`='%s' 
AND `Sub-Category`='%s' AND `Vertical`='%s' 
AND `Description Type`='%s' AND `Source`='%s';""" % \
        (BUString,SupCatString,CatString,SubCatString,VertString,TypeString,SourceString)
    #print sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()
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
        result = None
        datesList = []

        for entry in entriesList:
            datesList.append(entry["Revision Date"])
        #print datesList #debug
        closestRevisionDate = getClosestDate(datesList,requestDate)
        #print "Closest revision date is %s." %closestRevisionDate #debug
        #print "Query Date is %s." %requestDate #debug
        for entry in entriesList:
            if entry["Revision Date"] == closestRevisionDate:
                result = entry["Target"]
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

def getDescriptionTypes(userID, password):
    """Returns a list containing the entire list of values for Description Type."""
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
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

def getSources(userID,password):
    """Returns a list containing the entire list of values for BU."""
    connectdb = MySQLdb.connect(host = getHostID(),user = userID,passwd = password,\
        db = getDBName(),cursorclass = MySQLdb.cursors.DictCursor)
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

def getBUValues(userID, password):
    """Returns a list containing the entire list of values for BU."""
    connectdb = MySQLdb.connect(host = getHostID(), user = userID, passwd = password,\
        db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
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

def getSuperCategoryValues(userID,password,BU=None):
    """Returns a list containing the appropriate list of values for Super-Category."""
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
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

def getCategoryValues(userID,password,SupC=None):
    """Returns a list containing the appropriate list of values for Category."""
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
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

def getSubCategoryValues(userID, password, Cat=None):
    """Returns a list containing the appropriate list of values for Sub-Category."""
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
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

def checkDuplicacy(FSN, articleType, articleDate):
    """Returns true if it finds this FSN written before in the same type."""
    #First check if that FSN was written in this date.
    #Look for that data in `piggybank`.
    #If found, return "Local"
    #Else, look in `piggybank` without the date and in the FSN Dump.
    #If found, return "Global"
    #Else return False
    wasWrittenBefore = False
    userID, password = getBigbrotherCredentials()
    connectdb = MySQLdb.connect(host = getHostID(), user = userID, passwd = password, db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """SELECT * FROM `piggybank` WHERE `FSN` = '%s' and `Article Date` = '%s';""" % (FSN, articleDate)
    dbcursor.execute(sqlcmdstring)
    local_data = dbcursor.fetchall()
    if len(local_data) > 0: #If that FSN exists in the data for a given date.
        wasWrittenBefore = "Local"
    else: #If not found in the given date
        sqlcmdstring = """SELECT * from `piggybank` WHERE `FSN` = '%s' and `Description Type` = '%s';""" % (FSN, articleType)
        dbcursor.execute(sqlcmdstring)
        global_data = dbcursor.fetchall()
        if len(global_data) > 0: #If found for some date
            wasWrittenBefore = "Global"
        else: #If not found
            sqlcmdstring = """SELECT * from `fsndump` WHERE `FSN` = '%s' and `Description Type` = '%s';""" % (FSN, articleType)
            dbcursor.execute(sqlcmdstring)
            global_data = dbcursor.fetchall()
            if len(global_data) > 0: #If found in the fsndump
                wasWrittenBefore = "Global"
    connectdb.commit()
    connectdb.close()   
    return wasWrittenBefore

def getVerticalValues(userID, password, SubC=None):
    """Returns a list containing the appropriate list of values for Verticals."""
    connectdb = MySQLdb.connect(host = getHostID(), user = userID,passwd = password,\
        db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
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

def modWorkingStatus(userid, password, querydate, status, relaxation, comment, approval = "\\N",rejectionComment = "\\N", targetuser = None):
    """Method to modify the working status/relaxation of an employee.
    If no record exists, then the method creates an entry for it."""
    if targetuser == None:
        targetuser = userid
    
    connectdb = MySQLdb.connect(host = getHostID(), user = userid, 
                            passwd = password, db = getDBName())
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT 1 FROM `workcalendar` WHERE `Employee ID` = '%s' AND  `Date` = '%s';" \
    % (targetuser, convertToMySQLDate(querydate))
    #print sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()
    #print data #debug
    if len(data) == 0:
        #print "No data available."
        if getUserRole(userid) == "Content Writer":
            sqlcmdstring = "INSERT INTO `workcalendar` (`Employee ID`, `Date`, `Status`, `Relaxation`, `Comment`, `Entered By`) VALUES ('%s','%s','%s','%s','%s', '%s')" %(targetuser, convertToMySQLDate(querydate), status, relaxation, comment, getUserRole(targetuser))
        elif getUserRole(userID) == "Team Lead":
            #print "Team Lead!"
            sqlcmdstring = "INSERT INTO `workcalendar` (`Employee ID`, `Date`, `Status`, `Relaxation`, `Entered By`, `Comment`, `Approval`,`Rejection Comment`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %(targetuser, convertToMySQLDate(querydate), status, relaxation, getUserRole(targetuser), comment, approval, rejectionComment)
    else:
        #print "Data available. Updating entry."
        if getUserRole(userid) == "Content Writer":
            sqlcmdstring = "UPDATE `workcalendar` SET `Status` = '%s', `Relaxation` = '%s', `Entered By` = '%s', `Comment` = '%s' WHERE `Employee ID` = '%s' AND `Date` = '%s';" \
            %(status, relaxation, getUserRole(targetuser), comment, targetuser, convertToMySQLDate(querydate))
        elif getUserRole(userid) == "Team Lead":
            print "Team Lead!"
            sqlcmdstring = "UPDATE `workcalendar` SET `Status` = '%s', `Relaxation` = '%s', `Entered By` = '%s', `comment` = '%s', `Approval` = '%s', `Rejection Comment` = '%s' WHERE `Employee ID` = '%s' AND `Date` = '%s';" \
            %(status, relaxation, getUserRole(targetuser), comment, approval, rejectionComment, targetuser, convertToMySQLDate(querydate))
    #print sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def getUserRole(userid, password=None, targetuser=None):
    """Returns the role of the user or of a targetuser."""
    if password == None and userid != getBigbrotherCredentials()[0]:
        if targetuser == None:
            targetuser = userid
        userid, password = getBigbrotherCredentials()
    elif targetuser == None and userid == getBigbrotherCredentials()[0]:
        return "Big Brother"
    elif targetuser == None:
        targetuser = userid
    connectdb = MySQLdb.connect(host = getHostID(), user = userid, 
                            passwd = password, db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
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
    userID, password = getBigbrotherCredentials()
    try:
        connectdb = MySQLdb.connect(host = hostID, user = userID, passwd = password, db = getDBName())
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

def addOveride(FSN, overide_date, userID, password):
    connectdb = MySQLdb.connect(host = getHostID(), user = userID, passwd = password, db = getDBName())
    dbcursor = connectdb.cursor()
    sqlcmdstring = "INSERT INTO `overiderecord` (`FSN`, `Overide Date`, `Overidden By`) VALUES ('%s', '%s', '%s');" %(FSN, convertToMySQLDate(overide_date), userID)
    print sqlcmdstring
    dbcursor.execute(sqlcmdstring)

    connectdb.commit()
    connectdb.close()

def checkForOveride(FSN, query_date, userID, password):
    """Checks if an overide has been scheduled for a specific FSN and date by the TL."""
    connectdb = MySQLdb.connect(host = getHostID(), user = userID, passwd = password, db = getDBName())
    dbcursor = connectdb.cursor()
    sqlcmdstring = "SELECT * FROM `overiderecord` WHERE `FSN` = '%s' AND `Overide Date` = '%s';" %(FSN, convertToMySQLDate(query_date))
    dbcursor.execute(sqlcmdstring)
    retrieved_data = dbcursor.fetchall()
    #print "Found %d entries." % len(retrieved_data)
    connectdb.commit()
    connectdb.close()
    return (len(retrieved_data) > 0)
  
######################################################################
#Test methods#
#These are development methods that aren't called by the users.
######################################################################

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
    
def dummyFunction(userID,password):
    """Use when needed."""
    connectdb = MySQLdb.connect(host=getHostID(),user=userID,passwd=password,\
        db=getDBName(),cursorclass=MySQLdb.cursors.DictCursor)
    dbcursor=connectdb.cursor()
    sqlcmdstring="""
"""
    dbcursor.execute(sqlcmdstring)
    connectdb.commit()
    connectdb.close()

def getSQLErrorType(errorString):
    error = "Unknown. Printing verbatim: %s" % errorString
    if "2003" in errorString:
        error = "Cannot connect to server. Check server IP."
    elif "1045" in errorString:
        error = "Login failure."
    return error


#queryDict = {"BU":"FMCGAndOthers","Super-Category":"Book","Category":"Book","Sub-Category":"Books-Fiction","Vertical":"Yearbooks & Annuals1","Source":"Inhouse","Description Type":"Regular Description"} #debug
#queryDict = {"BU":"Lifestyle","Super-Category":"LifestyleAccessory","Category":"LifestyleAccessory","Sub-Category":"LifestyleAccessory","Category":"LifestyleAccessory","Vertical":"LifestyleAccessory","Source":"Inhouse","Description Type":"Regular Description"}

def test():
    startDate = datetime.date(2015,01,20)
    endDate = datetime.date(2015,01,21)
    queryDict = {"WriterID":75027}
    userid,password = getBigbrotherCredentials()
    answer = getPiggyBankDataBetweenDates(startDate,endDate,queryDict,userid,password)
    #print "Welcome back to the Main function!" #debug
    counter = 0
    days = 0
    for eachtuple in answer:
        if len(eachtuple)>0:
            days += 1
            for row in eachtuple:
                counter += 1
                #print counter #debug 
                #print row #debug
    #print answer
    print "%d entries found for %d days when looking for %d days!" % (counter, days, len(answer))




#######################################################################################
####################################Pending methods.###################################
#######################################################################################

def getLastWorkingDate(userID, password, queryDate = None, queryUser = None):
    """Returns the last working date for the requested user."""
    #Testing pending: need to check if it recursively picks out leaves and holidays as well.
    if queryDate == None:
        queryDate = datetime.date.today()
    if queryUser == None:
        queryUser = userID
    #print queryDate
    stopthis = False
    previousDate = queryDate - datetime.timedelta(1)
    while not stopthis:
        if not OINKM.isWeekend(queryDate):
            status = getWorkingStatus(userID, password, previousDate)[0]
            if status == "Working":
                stopthis = True
            else:
                previousDate -= datetime.timedelta(1)
        else:
            previousDate -= datetime.timedelta(1)
    return previousDate
    
def getRawDataMultiQuery(userID, password, multiQueryDict):
    """Returns a list of raw data rows corresponding to a list of query dictionaries."""
    return rawDataRows

def getRawDataBetweenDates(userID, password, startDate, endDate):
    """Builds a multiquerydict and calls getRawDataMultiQuery to fetch all raw data rows between dates."""
    return rawDataRow

def readFromRawData(userID, password, queryDict):
    """Reads a single entry from the raw data, based on a query."""
    connectdb = MySQLdb.connect(host = getHostID(), user = userID, passwd = password, db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """SELECT %s FROM rawdata WHERE %s;""" % (", ".join(getRawDataScoreHeaders()), )
    print "Printing Command: \n ", sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    return rawData

def getOneToOneStringFromDict(queryDict, joiner = None):
    """Takes a dictionary and returns a string where each key is mapped to its value. Example:
    a = {"Name" : "Vinay", "Age" : "27"}
    returns 
    "'Name' = 'Vinay', 'Age' = '27'"
    The joiner is either None, AND or OR.
    """
    keys_list = queryDict.keys()
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
        result_string = result_string + "`" + key + "`" + " = " + "'" + queryDict[key] + "'"
    return result_string

def checkAuditStatus(userID, password, articleDict):
    """Checks if an article has been audited before."""
    connectdb = MySQLdb.connect(host = getHostID(), user = userID, passwd = password, db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
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

def getQuality(userID, password, queryDict):
    """Takes one rawdata row and returns the quality."""
    connectdb = MySQLdb.connect(host = getHostID(), user = userID, passwd = password, db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """"""
    print "Printing Command: \n", sqlcmdstring #debug
    dbcursor.execute(sqlcmdstring)
    data = dbcursor.fetchall()
    connectdb.commit()
    connectdb.close()
    return CFM, GSEO

def getRawDataColumnsInOrder(userID, password):
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


def getQualityForDate(userID, password, queryDate):
    """Returns the CFM and GSEO quality for a date."""
    return CFM, GSEO

def getQualityBetweenDates(userID, password, startDate, endDate):
    """Returns the CFM and GSEO quality between a date range."""
    return avg_CFM, avg_GSEO

def getManDaysBetween(userID, password, startDate, endDate, queryUser = None):
    """Returns the total man days for a user between two dates."""
    return man_days

def getWTDQualityFor(userID, password, queryDate, queryUser = None):
    """Returns the WTD Quality as CFM and GSEO for the days in a particular week, upto a particular date.
Given a thursday, it'll return data for M-Th, including Th. So use this with the 'Last Working Day' date instead of the current date."""
    return CFM, GSEO

def getWTDEfficiencyFor(userID, password, queryDate, queryUser = None):
    """Returns the WTD efficiency for a user for the days in a particular week, upto a particular date.
Given a thursday, it'll return data for M-Th, including Th. So use this with the 'Last Working Day' date instead of the current date."""
    return avgEfficiency

def getMTDQualityFor(userID, password, queryDate, queryUser = None):
    """Returns MTD quality for a user for all the days in a month, upto and including a given date. Given the 15th, it will fetch data for 1-15 of a month."""
    return CFM, GSEO

def getMTDEfficiencyFor(userID, password, queryDate, queryUser = None):
    """Returns MTD efficiency for a user for all the days in a month, upto and including a given date. Given the 15th, it will fetch data for 1-15 of a month."""
    return avgEfficiency

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

if __name__ == "__main__":
    print "Starting Code."
    print "Doing nothing!"
    print "Code completed."