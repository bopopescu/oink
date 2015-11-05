#!usr/bin/python2
# -*- coding: utf-8 -*-
"""Includes custom methods which help with the old system of using Google Drive."""

import sys
import os
import csv
import datetime
from glob import glob as getFileList

def getFilteredList(prefixFile, column, criteria="All"):
    """
    Example of usage:
    ListofSubCategoriesInBGM = getList("Prefix.csv",Column = "Category", criteria = "BGM")
"""
    
    rowData = open(prefixFile,"r").read().split("\n")
    BUColumn = []
    superColumn = []
    catColumn = []
    subCatColumn = []
    verticalColumn = []
    for row in range(len(rowData)):
        if row > 0: #ignore the title headers? Why am I not using dicts?
            thisRow = rowData[row].split(",")
            BUColumn.append(thisRow[0])
            superColumn.append(thisRow[1])
            catColumn.append(thisRow[2])
            subCatColumn.append(thisRow[3])
            verticalColumn.append(thisRow[4])
    
    if column == "BU":
        return filterList(BUColumn,criteria,[]) 
    elif column == "Super-Category":
        return filterList(superColumn,criteria,BUColumn)
    elif column == "Category":
        return filterList(catColumn,criteria,superColumn)
    elif column == "Sub-Category":
        return filterList(subCatColumn,criteria,catColumn)
    elif column == "Vertical":
        return filterList(verticalColumn,criteria,subCatColumn)
            
def filterList(listToFilter,criteria,criteriaList):
    filteredList = []
    if criteria == "All":
        return sortAndCleanList(listToFilter)
    else:
        for row in range(len(listToFilter)):
            if criteriaList[row] == criteria :
                filteredList.append(listToFilter[row])
        return sortAndCleanList(filteredList)
    
def sortAndCleanList(listToClean):
    listToClean = list(set(listToClean))
    listToClean.sort()
    return listToClean

def getLatestFile(fileName,path):
    
    #log("Program Run","Recieved a request for %s in directory %s." % (fileName,path))
    #print "Recieved a request for %s in directory %s." % (fileName,path)
    
    fileNames = getAllPossibleFiles(fileName,path)
    fileNameTimeDict = {}
    #Create a dictionary with the modification times mapped against the file names.
    if (fileNames == fileName) or type(fileNames) == type(""):
        #log("Program Run", "Returning %s" % os.path.join(path,fileName))
        #print "Returning %s" % os.path.join(path,fileName) 
        return os.path.join(path,fileName)
    else:
        for fileName in fileNames:
            #print fileName
            fileNameTimeDict.update({fileName:os.path.getmtime(fileName)})
        #find the latest file by using the key parameter of the max() function.
        latestFile = max(fileNameTimeDict,key=fileNameTimeDict.get)
        #log("Program Run","Found multiple files. Using %s" % latestFile)
        #return only the file's name. glob.glob returns a merged list.
        #return latestFile[latestFile.rfind("\\")+1:] 
        return latestFile

def getAllPossibleFiles(fileName,path):
    fileAndPath = os.path.join(path,"*.*")
    allPossibleFiles = getFileList(fileAndPath)
    fileNameList = []
    if fileName.find(".") > -1:
        fileNameWithoutExtension = fileName[:fileName.rfind(".")] #remove the extension.
    for name in allPossibleFiles:
        if name.find(fileNameWithoutExtension)>-1:
            fileNameList.append(name)
    if len(fileNameList) > 1:
        return fileNameList
    else:
        return os.path.join(path,fileName)
        
def getEfficiencyFor(effIdentifier=[]):
    targetColumn = -1
    numberOfIdentifyingColumns = 5 #number of the type columns in the Cat Tree.
    #print "Received: %s" % effIdentifier
    if effIdentifier[0] == "Regular Description":
        if effIdentifier[1] == "Inhouse":
            targetColumn = numberOfIdentifyingColumns
        else:
            targetColumn = numberOfIdentifyingColumns + 7

    elif effIdentifier[0] == "Rich Product Description":
        if effIdentifier[1] == "Inhouse":
            targetColumn = numberOfIdentifyingColumns + 1 
        else:
            targetColumn = numberOfIdentifyingColumns + 8 
    elif effIdentifier[0] == "RPD Updation":
        if effIdentifier[1] == "Inhouse":
            targetColumn = numberOfIdentifyingColumns + 2
        else:
            targetColumn = numberOfIdentifyingColumns + 9
    
    elif effIdentifier[0] == "RPD Variant":
        if effIdentifier[1] == "Inhouse":
            targetColumn = numberOfIdentifyingColumns + 3
        else:
            targetColumn = numberOfIdentifyingColumns + 10
    elif effIdentifier[0] == "SEO Big":
        if effIdentifier[1] == "Inhouse":
            targetColumn = numberOfIdentifyingColumns + 4
        else:
            targetColumn = numberOfIdentifyingColumns + 11
    elif effIdentifier[0] == "SEO Project":
        if effIdentifier[1] == "Inhouse":
            targetColumn = numberOfIdentifyingColumns + 5
        else:
            targetColumn = numberOfIdentifyingColumns + 12
    elif effIdentifier[0] == "SEO Small":
        if effIdentifier[1] == "Inhouse":
            targetColumn = numberOfIdentifyingColumns + 6
        else:
            targetColumn = numberOfIdentifyingColumns + 13
    
    #targetsFileName = getLatestFile("Vertical-Category Mapping.csv","Lists\\")
    #columnLabels = open(columnLabelsFile,"r").read().split("\n")
    targetsFile = open(getTargetFileName(),"rt")
    targetsArray = csv.reader(targetsFile)
    target = "Undefined"
    rowCounter = 0
    foundSuperCategory = False
    foundCategory = False
    foundSubCategory = False
    foundVertical = False
    for row in targetsArray:
        #if rowCounter == 0:
            #log("Program Run","Looking in %s for efficiency." %row[targetColumn]   )
        rowCounter += 1
        if (row[0] == effIdentifier[2]):
            if not foundSuperCategory:
                target = row[targetColumn]
                foundSuperCategory = True
                
            if (row[1] == effIdentifier[3]):
                if not foundCategory:
                    target = row[targetColumn]
                    foundCategory = True
                    
                if (row[2] == effIdentifier[4]):
                    if not foundSubCategory:
                        target = row[targetColumn]
                        foundSubCategory = True
                        
                    if (row[3] == effIdentifier[5]):
                        if not foundVertical:
                            target = row[targetColumn]
                            foundVertical = True
                            
    targetsFile.close()
    if target == "Undefined":
        #notify("No Target","The target for that type of article has yet to be defined. Please contact your TL.")
        return target
    elif target == "0":
        return 0.00
    else:
        return (1.00/float(target))*100


def getTargetFileName():
    #return getLatestFile("Vertical-Category Mapping.csv","Lists\\")
    return getLatestFile("CatTreeWithTargets.csv","Lists\\")


def log(messagetype,activity):
    timestamp = datetime.datetime.now()
    logFileName = "CSVs\Log.txt"
    if os.path.isfile(logFileName):
        logFile = open(logFileName,"a")
    else:
        logFile = open(logFileName,"w")
    logFile.write("\n[time]%s[/time] - [messagetype]%s[/messagetype] - [activity]%s[/activity]" % (timestamp,messagetype,activity))
    logFile.close()
    return

def isWeekend(queryDate):
    #pending
    is_weekend = False
    #print "In isWeekend!"
    #print getWeekDay(queryDate)
    if getWeekDay(queryDate) == 6 or getWeekDay(queryDate) == 7:
        is_weekend = True
    return is_weekend

def getDatesInMonthOf(inputDate):
    """Returns all the dates in a month containing a particular date."""
    #pending
    if type(inputDate) == type(datetime.date.today()):
        counter = 1
        stopthis = False
        dates = [inputDate]
        while not stopthis:
            previousDate = inputDate - datetime.timedelta(days = counter)
            print previousDate
            todayMonth = getMonth(inputDate)
            previousDateMonth = getMonth(inputDate)
            if todayMonth == previousDateMonth:
                dates.append(previousDate)
            else:
                stopthis = True
            counter += 1
        return dates
    else:
        return "Error, please input a python datetime object to getDatesInMonthOf."

def getDatesInWeekOf(inputDate):
    """Returns all the dates in the week containing a particular date."""
    if type(inputDate) == type(datetime.date.today()):
        #inputDate
        counter = 1
        stopthis = False
        dates=[inputDate]
        while not stopthis:
            previousDate = inputDate - datetime.timedelta(days = counter)
            todayWeek = getWeekNum(inputDate)
            previousDateWeek = getWeekNum(previousDate)
            if todayWeek == previousDateWeek:
                dates.append(previousDate)
            else:
                stopthis = True
            counter += 1
        return dates
    else:
        return "Error, please input a python datetime object to getDatesInWeekOf."

def getMonth(inputDate):
    if type(inputDate) == type(datetime.date.today()):
        return inputDate.month

def getYear(inputDate):
    if type(inputDate) == type(datetime.date.today()):
        return inputDate.isocalendar()[0]

def getWeekDay(inputDate):
    if type(inputDate) == type(datetime.date.today()):
        return inputDate.isocalendar()[2]

def getWeekNum(inputDate):
    if type(inputDate) == type(datetime.date.today()):
        return inputDate.isocalendar()[1]

def getQuarter(inputDate):
    month = getMonth(inputDate)
    month_quarter_mapping = {
        1: "JFM", 2: "JFM", 3: "JFM", 4: "AMJ", 5: "AMJ", 6: "AMJ", 
        7: "JAS", 8: "JAS", 9: "JAS", 10: "OND", 11: "OND", 12: "OND"
    }
    return month_quarter_mapping[month]
    
def changeDatesToStrings(inputDates,format="YYYYMMDD"):
    format.upper()
    if type(inputDates) == type([]):
        dateStringList = []
        for dates in inputDates:
            dateString = format
            dateString = dateString.replace("YYYY",str(dates.year))
            dateString = dateString.replace("MM",str(dates.month))
            dateString = dateString.replace("DD",str(dates.day))
            dateStringList.append(dateString)
        return dateStringList
    elif type(inputDates) == type(datetime.date.today()):
        return changeDatesToStrings([inputDates],format)
    else:
        return "Error String"


def getDatesStringInWeekOf(inputDate):
    inputWeekDateList = getDatesInWeekOf(inputDate)
    inputWeekDateListStrings = changeDatesToStrings(inputWeekDateList)
    return inputWeekDateListStrings

def getDateFromString(inputDate,format="YYYYMMDD"):
    format.upper()
    yearPosition = format.find("YYYY")
    monthPosition = format.find("MM")
    dayPosition = format.find("DD")
    year = int(inputDate[yearPosition:yearPosition+4])
    month = int(inputDate[monthPosition:monthPosition+2])
    day = int(inputDate[dayPosition:dayPosition+2])
    return datetime.date(year,month,day)

def getDatesBetween(startDate,endDate):
    #print "Here!"
    currentDate = startDate
    dateList = []
    while currentDate <= endDate:
        dateList.append(currentDate)
        currentDate += datetime.timedelta(days=1)
    #print dateList
    return dateList

def getWriterList():
    #returns a list of dictionaries containing writers' names and Email-IDs.
    writerDataFileName = "writerList.csv"
    writerDataFileName = getLatestFile(writerDataFileName,"Lists")
    writerDataFile = open(writerDataFileName,"rt")
    writerDataArray = csv.DictReader(writerDataFile)
    dataList = []
    #writerCounter = 0
    for writer in writerDataArray:
        #if writerCounter >0:
        dataList.append(writer)
        #writerInfo = {"Name":writer[0],"Email-ID":writer[1]}
        #dataList.append([writerInfo])
        #writerCounter += 1
    #print dataList
    return dataList

def compileDataForDates(startdate="Null",enddate="Null",\
            writers="All",types="All",supercategories="All",\
            categories="All",verticals="All",brands="All"):
    """Returns piggy bank data for requested filter"""
#1. Type check: startdate, enddate should be datetime.date types.
#   writers, types, supercategories, categories, verticals and 
#   brands should be a list, or a string.
#2. Validity check:
#   Check if dates are valid.
    startDateIsDate = False
    endDateIsDate = False
    writersIsValid = False
    typesIsValid = False
    supercategoriesIsValid = False
    categoriesIsValid = False
    verticalsIsValid = False
    brandsIsValid = False
    if startdate != "Null":
        startDateIsDate = (type(startdate) == type(datetime.date.today()))
        if enddate == "Null":
            enddate = startdate
            endDateisDate = True
        else:
            endDateIsDate = (type(enddate) == type(datetime.date.today()))
            
    errorLog = []
    getSingleWriterData = (type(writers) == type("")) and (writers != "All")

    if writers == "All":
        writersFileName = getLatestFile("writerList.csv","Lists")
        writersFile = open(writersFileName,"rb")
        writersData = csv.DictReader(writersFile)
        writers = []
        for writer in writersData:
             writers.append(writer["Writer Name (Shortened)"])
        writersFile.close()
    elif getSingleWriterData:
        writers = [writers]
    resultData = []
    datesAreOK = startDateIsDate and endDateIsDate
    if datesAreOK:
        for writer in writers:
            dates = getDatesBetween(startdate, enddate)
            for oneday in dates:
                piggyFileName = getPiggyBankFileName(writer,oneday)
                if os.path.isfile(piggyFileName):
                    piggyFile = open(piggyFileName,"rb")
                    piggyFileData = csv.DictReader(piggyFile)
                    rowKeys = getDumpHeaders()
                    for row in piggyFileData:
                        rowData = {}
                        for key in rowKeys:
                            try:
                                rowData.update({key:row[key]})
                            except KeyError:
                                if key == "Date":
                                    rowData.update({key:oneday})
                                elif key == "Name":
                                    rowData.update({key:writer})
                                elif key == "Email-ID":
                                    rowData.update({key:getEmailID(writer)})
                                else:
                                    errorLog.append(["%s is not a recognized key for the dictionary. It was requested for %s on %s." % (key,writer,oneday)])
                        resultData.append(rowData)
                    piggyFile.close()
                else:
                    errorLog.append(["There is no data for %s on %s." % (writer,oneday)])
        return resultData, errorLog
    else:
        #returns this if there is an error with the dates, or if no dates are provided.
        errString = "Dates are invalid. %s or %s is not a valid start date." % (startdate, enddate)
        return errString

def getPiggyPathFromVindaloo(writername):
    """for the given writer, this returns the path to the csvs folder of their PORK installation."""
    piggyPath = os.path.join("..\\..\\Writers", writername)
    piggyPath = os.path.join(piggyPath, "P.O.R.K\\CSVs")
    return piggyPath

def getEmailID(writerName):
    writersFileName = getLatestFile("writerList.csv","Lists")
    writersFile = open(writersFileName,"rb")
    writersData = csv.DictReader(writersFile)
    writersDict = {}
    for writer in writersData:
        writersDict.update({writer["Writer Name (Shortened)"]:writer["Email-ID"]})
    writersFile.close()
    return writersDict[writerName]

def getDateString(requiredDate,format="YYYYMMDD"):
    """
    getDateString takes a datetime date and 
    returns a datestring in a particular format.
    """
    requiredDay = requiredDate.day
    requiredMonth = requiredDate.month
    requiredYear = requiredDate.yearString
    year = str(requiredYear)
    dayString = str(requiredDay)
    if len(dayString) == 1:
        dayString = "0" + dayString
    monthString = str(requiredMonth)
    if len(monthString) == 1:
        monthString = "0" + monthString
    dateString = format.replace("YYYY",yearString).replace("MM",\
            monthString).replace("DD",dayString)
    return dateString

def getPiggyBankFileName(writer,requiredDate):
    """returns the complete path+file name for the latest piggy bank corresponding to a particular date."""
    piggyBankFileString = "%s.pork" % getDateString(requiredDate)
    piggyPathFromVindaloo = getPiggyPathFromVindaloo(writer)
    return getLatestFile(piggyBankFileString,piggyPathFromVindaloo)

def getDumpHeaders():
    #Read the list of writers' names and email-IDs.
    #writerInfoFile = open("Lists\writerList.csv", "rt")
    #writerInfo = csv.reader(writerInfoFile)
    #Read the list of labels in PORK files.
    labelsInPorkFile = open("Lists\columnLabels.csv","rt")
    labelsInPork = labelsInPorkFile.read().split("\n")
    labelsInPorkFile.close()
    #create a list containing the labels in the Piggy Bank Dump.
    labelsInPiggyBankDump = ["Date","Name","Email-ID"]
    for label in labelsInPork:
            labelsInPiggyBankDump.append(label)
    return labelsInPiggyBankDump

def getQuality(writers,inputDate):
    #writer is a list
    #date is a datetime date.
    #returns Overall quality as a floating point?
    TOTALCFMSCORE = 75.00
    TOTALGSEOSCORE = 25.00
    if type(writers) == type(""):
        writers = [writers]
    writersQuality = (dict((writer,"Null") for writer in writers))
    for writer in writers:
        gseo_breakup = getGSEO(writer,inputDate)
        cfm_breakup = getCFM(writer,inputDate)
        fatals_breakup, fatalCount = getFatals(writer,inputDate)
        if fatalCount == 0:
            #GSEOQualityTotal, CFMQualityTotal = [0.0, 0.0]
            GSEOQuality = 0.0
            entries = len(gseo_breakup)
            if entries == 0:
                return "No Audits"
            else:
                GSEOScore = 0.0
                CFMScore = 0.0
                for row in gseo_breakup:
                    GSEOScore += getGSEOTotalScore(row)
                #CFMQuality /= entries
                #print "CFM for %d entries is %f" %(entries,CFMQuality)
                for row in cfm_breakup:
                    CFMScore += getCFMTotalScore(row)
                quality = (GSEOScore + CFMScore) / entries / 100
                CFMQuality = CFMScore / entries / TOTALCFMSCORE
                GSEOQuality = GSEOScore / entries / TOTALGSEOSCORE
                #print "CFM = %f, GSEO = %f, Overall = %s" % (CFMQuality, GSEOQuality, quality)
        else:
            #print "Fatal!"
            quality = 0.0
            CFMQuality = 0.0
            GSEOQuality = 0.0
        writersQuality[writer]  = {"CFM Quality": CFMQuality, "Overall Quality": quality,"GSEO Quality": GSEOQuality}
    return writersQuality


#def getNFABreakup(writer,date):
    #writer is a list
    #date is a datetime date.
    #returns a dictionary(?) of scores?/percentages?

def getGSEO(writers,inputDate):
    #writer is a list
    #date is a datetime date.
    #returns GSEO NFAs and quality as a dictionary
    #print "Getting GSEO Parameters..."
    if type(writers) == type(""):
        writers = [writers]
    GSEOQuality = []
    rawData = readQualityRawData()
    GSEOData = []
    for writer in writers:
        dataCounter = 0
        for row in rawData:
            if row["Writer"] == writer:
                if getDate(row["Date"]) == inputDate:
                    dataCounter +=1
                    GSEORow = (dict((parameter,row[parameter]) \
                        for parameter in getGSEOParams() ))
                    GSEORow.update({"Writer":writer})
                    GSEOData.append(GSEORow)
        #print "Found %d entries for %s." % (dataCounter, writer)
    return GSEOData

def getCFM(writers,inputDate):
    #writer is a list
    #date is a datetime date.
    #returns CFM NFAs and quality as a dictionary
    #print "Getting CFM parameters..."
    if type(writers) == type(""):
        writers = [writers]
    CFMQuality = []
    rawData = readQualityRawData()
    CFMData = []
    for writer in writers:
        dataCounter = 0
        for row in rawData:
            if row["Writer"] == writer:
                if getDate(row["Date"]) == inputDate:
                    dataCounter +=1
                    CFMRow = (dict((parameter,row[parameter]) \
                        for parameter in getCFMParams() ))
                    CFMRow.update({"Writer":writer})
                    CFMData.append(CFMRow)
        #print "Found %d entries for %s." % (dataCounter, writer)
    return CFMData

def getFatals(writers,inputDate):
    #writer is a string
    #date is a datetime date.
    #returns Fatal parameter scores as a dictionary and 
    #returns a boolean True if there are no fatals.
    #print "Getting Fatal Parameters..."
    if type(writers) == type(""):
        writers = [writers]
    FatalQuality = []
    rawData = readQualityRawData()
    FatalData = []
    FatalCounter = 0
    for writer in writers:
        dataCounter = 0
        for row in rawData:
            if row["Writer"] == writer:
                if getDate(row["Date"]) == inputDate:
                    dataCounter +=1
                    FatalRow = (dict((parameter,row[parameter]) \
                        for parameter in getFatalParams() ))
                    for parameter in getFatalParams():
                        if FatalRow[parameter] == "Yes":
                            FatalCounter += 1
                    FatalRow.update({"Writer":writer})
                    FatalData.append(FatalRow)
        #print "Found %d entries for %s." % (dataCounter, writer)
    return FatalData, FatalCounter

def getCFMTotalScore(CFMDict):
    total = 0.0
    for parameter in getCFMParams():
        if "Quality" not in parameter:
            total += float(CFMDict[parameter])
    return total

def getGSEOTotalScore(GSEODict):
    total = 0.0
    for parameter in getGSEOParams():
        if "Quality" not in parameter:
            total += float(GSEODict[parameter])
    return total

def getPercentageFromScore(parameter,score):
    scoreDict = {
        "Introduction": 10.0,
        "Product Theme": 10.0,
        "Flow of Article": 10.0,
        "Explain Features [in simple terms]": 10.0,
        "Practical Application of Features": 10.0,
        "Neutral Content": 10.0,
        "USP": 10.0,
        "Priority of Features": 5.0,
        "Sentence Construction": 5.0,
        "Sub-verb agreement": 5.0,
        "Missing/ additional/ repeated words": 2.5,
        "Spelling/ Typo": 2.5,
        "Punctuation": 2.5,
        "Formatting Errors": 2.5,
        "Keyword Variation": 5.0,
        }

    #print score, parameter

    try:
        percentage = float(score)/float(scoreDict[parameter])
        return percentage
    except:
        if parameter in ["GSEO Quality","CFM Quality"]:
            #print "Is this it?"
            return float(score)
        else:
            #print "No such parameter %s"% parameter
            return 0.0

def getDate(inputDate,format="DD/MM/YYYY"):
    format.upper()
    yearPosition = format.find("YYYY")
    monthPosition = format.find("MM")
    dayPosition = format.find("DD")
    year = int(inputDate[inputDate.rfind("/")+1:yearPosition+4])
    month = int(inputDate[inputDate.find("/")+1:inputDate.rfind("/")])
    day = int(inputDate[:inputDate.find("/")])
    return datetime.date(year,month,day)

def readQualityRawData():
    rawData = getLatestFile("QualityRawData.csv","Reports\\")
    rawDataFile = open(rawData,"r")
    rawDataArray = csv.DictReader(rawDataFile)
    rawDataList = []
    for row in rawDataArray:
        rawDataDict = getEmptyRawDataDict()
        for key in getRawDataHeaders():
            rawDataDict[key] = row[key]
        rawDataList.append(rawDataDict)
    rawDataFile.close()
    return rawDataList

def getQualityParams():
    qualityParams= [
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
        "Overall Quality"
        ]
    return qualityParams

def getEmptyQualityDict():
    qualityDict = (dict((key,"NULL") for key in getQualityParams()))
    return qualityDict

def getRawDataHeaders():
    rawDataHeaders = [
        "Writer",
        "Category",
        "Sub-Category",
        "QA",
        "Date",
        "Week",
        "Month",
        "WS Name",
        "WC",
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
        "Introduction comments",
        "Product Theme comments",
        "Flow of Article comments",
        "Explain Features [in simple terms] comments",
        "Practical Application of Features comments",
        "Neutral Content comments",
        "USP comments",
        "Priority of Features comments",
        "Sentence Construction comments",
        "Sub-verb agreement comments",
        "Missing/ additional/ repeated words comments",
        "Spelling/ Typo comments",
        "Punctuation comments",
        "Formatting Errors comments",
        "Keyword Variation comments",
        "Keyword Density comments",
        "Plagiarism comments",
        "Mismatch in Specs comments"
        ]
    return rawDataHeaders

def getEmptyRawDataDict():
    rawDataDict = (dict((key,"NULL") for key in getRawDataHeaders()))
    return rawDataDict

def getQualityParameterClass(qualityParameter):
    if qualityParameter in getCFMParams():
        return "CFM"
    elif qualityParameter in getGSEOParams():
        return "GSEO"
    elif qualityParameter in getFatalParams():
        return "FATAL"
    else:
        return "Unknown Parameter"

def getCFMParams():
    return [
        "Introduction",
        "Product Theme",
        "Flow of Article",
        "Explain Features [in simple terms]",
        "Practical Application of Features",
        "Neutral Content",
        "USP",
        "Priority of Features",
        "CFM Quality"
        ]

def getGSEOParams():
    return [
        "Sentence Construction",
        "Sub-verb agreement",
        "Missing/ additional/ repeated words",
        "Spelling/ Typo",
        "Punctuation",
        "Formatting Errors",
        "Keyword Variation",
        "GSEO Quality"
        ]   

def getFatalParams():
    return [
        "Keyword Density",
        "Plagiarism",
        "Mismatch in Specs"
    ]

def checkIfISBN(querystring):
    """Checks if the FSN is an ISBN."""
    isISBN = False
    if check_if_FSN(querystring):
        isISBNLength = (len(querystring) == 13)
        isAllNumber = querystring.isdigit()
        hasXAtEnd = (querystring[:len(querystring)-1].isdigit()) and (querystring[len(querystring)-1:] == "X")
        hasNoSpaces = (querystring.find(" ") == -1)
        isISBN = isISBNLength and (isAllNumber or hasXAtEnd) and hasNoSpaces
    return isISBN

def checkIfFSN(querystring):
    """Checks if an input is an FSN or not."""
    isFSN = False
    isFSNLength = (len(querystring) == 16)
    isISBNLength = (len(querystring) == 13)
    isAllUpper = querystring.isupper()
    isAllNumber = querystring.isdigit()
    hasXAtEnd = (querystring[:len(querystring)-1].isdigit()) and (querystring[len(querystring)-1:] == "X")
    hasNoSpaces = (querystring.find(" ") == -1)
    isFSN = ((isFSNLength and isAllUpper) or (isISBNLength and (isAllNumber or hasXAtEnd)) and hasNoSpaces)
    return isFSN

def version():
    return "1.1"

def getMonday(query_date):
    day = query_date.isocalendar()[2]
    monday = query_date - datetime.timedelta(day - 1)
    return monday

def getHalfYear(query_date):
    if query_date.month <= 6:
        return "Jan-June"
    else:
        return ("Jul-Dec")