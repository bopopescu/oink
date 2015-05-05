#MOSES v2.0, the Prophet update.

import datetime
import sys
import MySQLdb
from PyQt4 import QtCore
import pandas

import OINKMethods as OINKM


class Prophet(QtCore.QThread):
    """

    The Prophet class allows for communication with the MySQL server.
    The Prophet is also a slave of Jehovah, 
    and thou shalt not have any other god before him.

    This class overrides the MOSES method collection in that 
    it provides a completely threaded solution to the same methods.
    It also uses DataFrames instead of dictionaries whereever possible."""

    #Define the signals this class emits.
    got_piggybank = QtCore.pyqtSignal(pandas.DataFrame)
    got_stats_data = QtCore.pyqtSignal(pandas.DataFrame)
    got_calendar_data = QtCore.pyqtSignal(pandas.DataFrame)

    def __init__(self, user_id, password, active_date=None, start_date=None, end_date=None, mode=None):
        """This class controls all communication
        with the OINK server.
        As opposed to using the methods directly, This
        class opens a single MySQLdb connector and uses it throughout the run.
        Upon deletion, it closes the connection.
        This class is also instantiated for PORK. For VINDALOO, BACON and Napoleon,
        it might be better to have their own classes with limited line of sight.
        For now, I'm merging these classes into one.
        active_date is the current date that is displayed in PORK.
        start_date, end_date is the date range that is displayed in VINDALOO.
        mode decides how this class runs. 1 is PORK, 2 is VINDALOO and 3 is BACON.
        """

        QtCore.QThread.__init__(self)
        #Thread stuff
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.user_id = user_id
        self.password = password

        if active_date is None:
            self.active_date = datetime.date.today()
        else:
            self.active_date = active_date
        print type(self.active_date)
        print self.active_date
        if start_date is None:
            self.start_date = self.getFirstDisplayedDateFor(self.active_date)
        else:
            self.start_date = start_date
        
        if end_date is None:
            self.end_date = self.getLastDisplayedDateFor(self.start_date)
        else:
            self.end_date = end_date
        
        if mode not in [1,2,3]:
            self.mode = 1
        else:
            self.mode = mode    

        #Instantiate two connections to the server.
        self.reader_conn = MySQLdb.connect(host = self.getHostID(), \
                            user = self.user_id, passwd = self.password, \
                            db = self.getDBName(), \
                            cursorclass = MySQLdb.cursors.DictCursor)
        self.writer_conn = MySQLdb.connect(host = self.getHostID(), \
                            user = self.user_id, passwd = self.password, \
                            db = self.getDBName(), \
                            cursorclass = MySQLdb.cursors.DictCursor)
        
        #Instantiate one cursor for each of the connections.
        self.reading_cursor = self.reader_conn.cursor()
        self.writing_cursor = self.writer_conn.cursor()

        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def closeConnections(self):
        """This method commits and closes both the MySQLdb connections this 
        class created originally."""
        self.reader_conn.commit()
        self.reader_conn.close()
        self.writer_conn.commit()
        self.writer_conn.close()

    def __del__(self):
        """"""
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def run(self):
        """
        This method transmits regular information.
        1. The writer statistics for each date that is displayed in the weekcalendar,
        defined by start_date and end_date.
        2. The active date's piggybank entries.

        The date range is controlled through the setCalendarVisibleDateRange method
        and the current page for transmission is controlled through the setActiveDate
        method.
        
        The run method constantly emits a dictionary in which dates are the keys 
        and the values are dictionaries corresponding to the writer statistics for 
        each date.

        This method also uses a separate cursor, in order to keep it separate 
        from the rest of the functions, should they require it.
        """
        self.previous_piggybank = None
        self.previous_stats_data = None
        self.previous_calendar_data = None
        while True:
            #Run forever.
            self.broadcastPiggyBank()
            self.broadcastStatsData()
            if mode == 1:
                self.broadcastCalendarData()

    def broadcastPiggyBank(self):
        """This method emits the piggybank for the current user for a given
        date.
        Later, if this class needs to be called by VINDALOO, I need to make 
        this change depending on the mode.
        """
        self.current_piggybank = self.getPiggyBankFor(self.active_date)
        if self.current_piggybank != self.previous_piggybank:
            self.got_piggybank.emit(self.current_piggybank)
            self.previous_piggybank = self.current_piggybank

    def broadcastStatsData(self):
        self.current_stats_data = self.getStatsData()
        if self.current_stats_data != self.previous_stats_data:
            self.got_stats_data.emit(self.current_stats_data)
            self.previous_stats_data = self.current_stats_data

    def broadcastCalendarData(self):
        import calendar
        self.current_calendar_data = {}
        self.month_first = self.getFirstDisplayedDateFor(self.active_date)
        self.month_last = self.getLastDisplayedDateFor(self.active_date)
        self.dates_list = OINKM.getDatesBetween(self.month_first, self.month_last)
        for each_date in self.dates_list:
            if self.isWorkingDay(each_date):
                status, relaxation, approval = MOSES.checkWorkStatus(each_date)
                if status == "Working" and relaxation >= 0.0:
                    efficiency = self.getEfficiencyFor(each_date)
                else:
                    efficiency = 0.0
            else:
                status = "Holiday"
                relaxation = "NA"
                efficiency = 0.0
            self.current_calendar_data.update({each_date:[status, relaxation, efficiency]})
        if self.current_calendar_data != self.previous_calendar_data:
            self.got_calendar_data.emit(self.current_calendar_data)
            self.previous_calendar_data = self.current_calendar_data


    def setActiveDate(self, new_date):
        """self method controls the current date.
        It is the date that is active in the WeekCalendar class in PORK.
        Changing this affects several emissions, including the getLastWorkingDate value
        and the piggybank data."""
        self.active_date = new_date

    def setCalendarVisibleDateRange(self, start_date=None, end_date=None):
        """This method controls the data for the visible date range.
        """
        if (start_date is not None) and (end_date is not None):
            self.start_date = start_date
            self.end_date = end_date
        else:
            start_date = getFirstDisplayedDateFor(self.active_date)
            end_date = getLastDisplayedDateFor(self.active_date)

    def changeMyPassword(self, new_password):
        """Method to reset own password."""
        sqlcmdstring = """SET PASSWORD = password("%s");""" % new_password
        self.reading_cursor.execute(sqlcmdstring)

    def resetUserPassword(self, user_to_reset, new_password=None):
        """Method to reset another user's password."""
        if new_password is None:
            new_password = "password"
        sqlcmdstring = """SET PASSWORD FOR `%s` = PASSWORD("%s");""" % (user_to_reset, new_password)
        self.reading_cursor.execute(sqlcmdstring)

    def isWorkingDay(self, query_date):
        """Checks if the company is operating on a 
        particular date, irrespective of 
        leaves etc. Only checks weekends and company
        holidays."""
        isWeekend = (query_date.isocalendar()[2] in [6,7])
        isCompanyHoliday = self.isFKHoliday(query_date)[0]
        return not (isWeekend or isCompanyHoliday)

    def isFKHoliday(self, query_date):
        """Check the teamcalendar table
        and return the status and comment.
        If there is no entry, assume it is not 
        a holiday as per the list of holidays. 
        Else, return True and the reason 
        for the holiday."""
        
        sqlcmdstring = """Select * from `teamcalendar` WHERE 
            `Record Date` = '%s'""" % MOSES.convertToMySQLDate(query_date)
        
        self.reading_cursor.execute(sqlcmdstring)
        
        query_date_in_holidays_table = self.reading_cursor.fetchall()
        if len(query_date_in_holidays_table) == 0:
            status = False
            comment = "NA"
        else:
            status = True
            comment = query_date_in_holidays_table[0]["Comments"]
        return status, comment

    def getWorkingStatus(self, query_date, lookupuser=None):
        """Method to fetch the status for a writer on any particular date.
        Returns "Working" if the employee is delivering 100%.
        Returns "Leave" if the employee is on leave.
        Returns n/10 if the employee is granted a relaxation of n%
        If lookupuser isn't specified, it'll just pull the status for the current user.
        NOTE:
        This method had a conflicting method called checkWorkStatus.
        Also, this method doesn't account for company holidays.
        Use along with the isCompanyHoliday function.
    """
        status = False
        relaxation = 0
        approval = False
        if lookupuser is None:
            lookupuser = self.user_id
        sqlcmdstring = """SELECT * FROM `workcalendar` WHERE `Date` = '%s' AND `Employee ID` = '%s';""" % (self.convertToMySQLDate(query_date),lookupuser)
        self.reading_cursor.execute(sqlcmdstring)
        work_data_for_user = self.reading_cursor.fetchall() 
        entries = len(work_data_for_user)
        if entries != 0:
            status = work_data_for_user[0]["Status"]
            relaxation = work_data_for_user[0]["Relaxation"]
            approval = work_data_for_user[0]["Approval"]
        
        return status, relaxation, approval

    def updateWorkCalendar(self, start_date, end_date=None, query_user=None, status=None, relaxation=None, entered_by=None, comment=None, approval=None, reviewed_by=None, rejection_comment=None):
        """Given a start_date, this method checks if there's an entry for a given date.
        If there is: it UPDATEs the entry with the given parameters.
        ELSE: it INSERTS and new entry for the given parameters.
        """
        if end_date is None:
            end_date = start_date
        if query_user is None:
            query_user = self.user_id
        if status is None:
            status = "Working"        
        if relaxation is None:
            relaxation = 0.0
        if comment is None:
            comment = "NA"
        if entered_by is None:
            entered_by = self.user_id
        if approval is None:
            approval = "Pending"
        if rejection_comment is None:
            rejection_comment = "NA"
        #get all the company working dates between the start date and end date
        for each_date in working_dates:
            status, relaxation, approval = self.getWorkingStatus(each_date)
            if status == False:
                sqlcmdstring = """INSERT INTO `workcalendar` (`date`,`employee id`,`status`,`relaxation`,`entered by`, `comment`, `approval`,`rejection comment`) VALUES ("%s","%s","%s","%s","%s","%s","%s");"""%(self.convertToMySQLDate(each_date), query_user, status, relaxation, comment, entered_by, approval, rejection_comment)
            else:
                sqlcmdstring = """UPDATE `workcalendar` SET `Status`="%s", `Relaxation`="%s", `Comment`="%s", `entered by`="%s", `approval`="%s", `rejection comment`="%s" WHERE `Date`="%s" AND `Employee ID`="%s";"""%(status, relaxation, comment, entered_by, approval, rejection_comment, self.convertToMySQLDate(eachDate), query_user)
            try_to_write = self.writeToOINK(sqlcmdstring)
            if not try_to_write:
                print "Failed while trying to write for %s." %each_date


    def addToPiggyBank(self, entry_dict):
        """Given a dictionary, this method enters 
        that information
        into the piggybank table."""
        #The entry dictionary should contain:
        #
        entry_dict.update({"End Time": datetime.datetime.now()})
        columns, values = self.getColValuesForSQL(entry_dict)
        sqlcmdstring = """INSERT INTO `piggybank` (%s) VALUES (%s);""" %(columns, values)
        try:
            self.writing_cursor.execute(sqlcmdstring)
            status = "Success"
            error_message = None
        except MySQLdb.IntegrityError:
            #Ideally, this should check for overrides itself and increment rewrite_ticket.
            status = "Failure"
            error_message = "Override"
        except Exception, e:
            status = "Failure"
            error_message = "Caught %s in addToPiggyBank method in Prophet Class." %repr(e)
        return status, error_message

    def updatePiggyBankEntry(self):
        """"""
    def getPiggyBankKeysInOrder(self):
        return MOSES.getPiggyBankKeysInOrder()
    def getPiggyBankFor(self, query_date):
        """Retrieves all piggy bank data for a logged-in user for a given date."""
        return self.getPiggyBankBetween(query_date, query_date, {})

    def getPiggyBankBetween(self, start_date, end_date, query_dict):
        """Retrieves all piggy bank data between two dates, given a dictionary
        of queries."""
        #first get a list of all dates between the two given dates.
        dates_list = OINKM.getDatesBetween(start_date, end_date)
        #Build a list of query dictionaries.
        multi_query = []
        counter = 0
        for each_date in dates_list:
            if counter == 0:
                query_dict.update({"Article Date": self.convertToMySQLDate(eachDate)})
            else:
                query_dict["Article Date"] = self.convertToMySQLDate(eachDate)
            counter += 1
            multi_query.append(query_dict)
        return self.getPiggyBankMultiQuery(multi_query)
    
    def convertToMySQLDate(self, query_date):
        """Takes a python datetime and changes it to the YYYY-MM-DD format 
        for MySQL. 
        Uses the OINKModule2 module's changeDatesToStrings method."""
        date_as_string = OINKM.changeDatesToStrings(query_date,"YYYY-MM-DD")
        return date_as_string[0]

    def getPiggyBankMultiQuery(self, multi_query):
        """Given a list of dictionaries, this method pulls data for each
        dictionary and then compiles them together as one list.
        """
        results = []
        for query in multi_query:
            if type(query) == type([]):
                results.append(self.readFromPiggyBank(query))
            else:
                print "*********************"
                print "Error in Prophet. Function name %s." %sys._getframe().f_code.co_name
                print "Time: %s" %datetime.datetime.now()
                print "User: %s\nMultiQuery:%s" %(self.user_id, multi_query)
                print "*********************"
        return results
    
    def readFromPiggyBank(self, query):
        """Given a single query dictionary, this method pulls piggybank
        records."""
        no_of_conditions = len(query)
        counter = 0
        sqlcmdstring = "SELECT * FROM piggybank WHERE "
        for key in query:
            sqlcmdstring = sqlcmdstring + ("""`%s` = "%s" """ % (key, query[key]))
            if counter < numberOfConditions-1:
                sqlcmdstring += " AND "
            else:
                sqlcmdstring += ";"
            counter +=1
        results = self.readFromOINK(sqlcmdstring, sys._getframe().f_code.co_name)
        results_as_one_list = []
        for row in results:
            results_as_one_list.append(row)
        return results_as_one_list

    def readFromOINK(self, sqlcmdstring, function_name):
        """Tries to read from the OINK server using the reading_cursor."""
        trial = 0
        try_again = True
        results = None
        while (trial < 3) and (try_again):
            try:
                self.reading_cursor.execute(sqlcmdstring)
                results = self.reading_cursor.fetchall()
                try_again = False
            except MySQLdb.Error, e:
                print "*********************"
                print "Error in Prophet. Function name %s." %sys._getframe().f_code.co_name
                print "Time: %s" % datetime.datetime.now()
                print "User: %s" %(self.user_id)
                print "Possible loss of connection to the server."
                print "Trying to fetch data again. Current trial no: %d" %trial 
                print "*********************"
                trial += 1
                results = None
            except:
                print "*********************"
                print "Error in Prophet. Function name %s." %sys._getframe().f_code.co_name
                print "Time: %s" % datetime.datetime.now()
                print "User: %s" %(self.user_id)
                print "Printing the sqlcmdstring:\n*\n%s\n*" %sqlcmdstring
                print "This is not a connection failure error. Current trial no: %d" %trial 
                print "Raising the error."
                print "*********************"
                raise
        return results

    def getStatsData(self):
        """This method returns the stats data for the active date.
        Use with PORK for the writer stats table."""
        last_working_date = self.getLastWorkingDate(self.active_date)
        current_week = OINKM.getWeekNum(last_working_date)
        current_month = OINKM.getMonth(last_working_date)
        current_quarter = OINKM.getQuarter(last_working_date)
        stats_data = {
        "LWD": last_working_date,
        "Current Week": current_week,
        "Current Month": current_month,
        "Current Quarter": current_quarter,
        "LWD Efficiency": 100.00*self.getEfficiencyFor(
                        last_working_date),
        "LWD GSEO": 100.00*self.getGSEOFor(last_working_date),
        "LWD CFM": 100.00*self.getCFMFor(last_working_date),
        "CW Efficiency": 100.00*self.getEfficiencyForWeek(last_working_date),
        "CW GSEO": 100.00*self.getGSEOForWeek(last_working_date),
        "CW CFM": 100.00*self.getCFMForWeek(last_working_date),
        "CM Efficiency": 100.00*self.getEfficiencyForMonth(last_working_date),
        "CM GSEO": 100.00*self.getGSEOForMonth(last_working_date),
        "CM CFM": 100.00*self.getCFMForMonth(last_working_date),
        "CQ Efficiency": 100.00*self.getEfficiencyForQuarter(last_working_date),
        "CQ GSEO": 100.00*self.getGSEOForQuarter(last_working_date),
        "CQ CFM": 100.00*self.getCFMForQuarter(last_working_date)
        }
        return stats_data

    def checkDuplicacy(self):
        """"""
    def checkForOverride(self):
        """"""
    def getLastWorkingDate(self, query_date):
        """Returns the last working date for the requested user."""
        #Testing pending: need to check if it recursively picks out leaves and holidays as well.
        if query_date is None:
            query_date = datetime.date.today()
        #print query_date
        stopthis = False
        previous_date = query_date - datetime.timedelta(1)
        while not stopthis:
            if not self.isWorkingDay(userID, password, previous_date):
                #print previous_date, " is a holiday or a weekend!"
                previous_date -= datetime.timedelta(1)
            else:
                status = self.getWorkingStatus(previous_date)[0]
                if status == "Working":
                    stopthis = True
                elif status in ["Leave", "Holiday", "Special Holiday"]:
                    #print "Not working on ", previous_date
                    previous_date -= datetime.timedelta(1)
                else:
                    stopthis = True
        return previous_date

    def getClosestDate(self, dates, query_date):
        """"Given a list of dates and a query date, this method returns the
        closest date that occurs on or before the query date."""

        closest_date = None
        for each_date in dates:
            if each_date == query_date:
                return query_date
            elif each_date < query_date:
                try:
                    if each_date > closest_date:
                        closest_date = each_date
                except:
                    closest_date = each_date
        return closest_date

    def getTargetFor(self, **query):
        """
        NOTE: This function is used with a multiple length query list. Oddly,
        this isn't the best way to go about things.
        """
        try:
            BUString = query["BU"]
            TypeString = query["DescriptionType"]
            SourceString = query["Source"]
            SupCatString = query["SuperCategory"]
        except:
            print "Error Message: BU, Super-Category, Source and Type are necessary!"
            raise
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
            requestDate = datetime.date.today()
        sqlcmdstring = """SELECT `Target`, `Revision Date` FROM `categorytree` 
    WHERE `BU`="%s" AND `Super-Category`="%s" AND `Category`="%s" 
    AND `Sub-Category`="%s" AND `Vertical`="%s" 
    AND `Description Type`="%s" AND `Source`="%s";""" % \
            (BUString,SupCatString,CatString,SubCatString,VertString,TypeString,SourceString)
        #print sqlcmdstring #debug
        results = self.readFromOINK(sqlcmdstring, sys._getframe().f_code.co_name)
        #print data #debug
        #Data is in a tuple containing dictionaries.
        #Separate the dates.
        entries = []
        for entry in results:
            entries.append(entry)
        #print entries #debug
        """This portion needs rework.
        If it finds multiple targets in one date, 
        then it needs to short list a target.
        Wait, does this ever happen?
        """
        if len(entries)==1:
            #print "Only one target found." #debug
            result = entries[0]["Target"]
        elif len(entries) > 1:
            #print "Found multiple targets across separate dates." #debug
            #print entries
            result = None
            datesList = []
            for entry in entries:
                datesList.append(entry["Revision Date"])
            #print datesList #debug
            closestRevisionDate = self.getClosestDate(datesList,requestDate)
            #print "Closest revision date is %s." %closestRevisionDate #debug
            #print "Query Date is %s." %requestDate #debug
            for entry in entries:
                if entry["Revision Date"] == closestRevisionDate:
                    result = entry["Target"]
        else:
            result = 0

        if int(result) == 0:
            try:
                retry = query["Retry"]
            except:
                retry = 0
            if retry == 0:
                result = self.getTargetFor(BU=BUString, DescriptionType=TypeString, Source=SourceString, SuperCategory=SupCatString, Category=CatString, SubCategory=SubCatString, QueryDate = requestDate, Retry = 1)
            elif retry == 1:
                result = self.getTargetFor(BU=BUString, DescriptionType=TypeString, Source=SourceString, SuperCategory=SupCatString, Category=CatString, QueryDate = requestDate, Retry = 2)
            elif retry == 2:
                result = self.getTargetFor(BU=BUString, DescriptionType=TypeString, Source=SourceString, SuperCategory=SupCatString, QueryDate = requestDate, Retry = 3)
            else:
                result = 0
        #print "Target is %r" %result #debug
        return int(result)

    def getWorkingDatesBetween(self, start_date, end_date, mode=None):
        """Given two dates, it returns the working dates between two given dates for the requesting user. 
        If the mode is set to "All", it will procure a list of non-working days for the company."""
        if mode is None:
            mode = "Self"
        date_range = OINKM.getDatesBetween(start_date, end_date)
        #print date_range
        working_dates = []
        for each_date in date_range:
            if self.isWorkingDay(each_date):
                if mode == "All":
                    working_dates.append(each_date)
                elif mode == "Self":
                    status = self.checkWorkStatus(each_date)
                    if status[0] == "Working":
                        working_dates.append(each_date)
        return working_dates

    def getEfficiencyFor(self, query_date):
        """Returns the current user_id's efficiency for a given date.
        NOTE: If calculating efficiency between a range of dates, do not consider
        dates on which a writer is given a leave.
        """
        requested_data = self.getPiggyBankFor(query_date)
        efficiency = 0.0
        status, relaxation, approval = self.getWorkingStatus(query_date)
        if (status == "Working") or (approval != "Approved"):
            #Calculate only for working days
            if relaxation > 0.0:
                efficiency_divisor = (1-relaxation)
            else:
                efficiency_divisor = 1.0
            #This doesn't account for negative relaxation, scenarios where a writer must make up. 
            #Does it need to? I don't really think so.
            for entry in requestedData:
                #pass the classification identifiers to the method.
                target = self.getTargetFor(BU = entry["BU"], DescriptionType = entry["Description Type"], Source = entry["Source"], SuperCategory = entry["Super-Category"], Category = entry["Category"], SubCategory = entry["Sub-Category"], Vertical = entry["Vertical"], QueryDate = queryDate)
                if target == 0.0:
                    efficiency += 0.0
                else:
                    efficiency += 1/(efficiency_divisor*target)         
        #print efficiency
        #print "Leaving getEfficiencyFor"
        return efficiency
    
    def getEfficiencyBetween(self, start_date, end_date):
        """Returns the efficiency for an emplyoee for all dates between two dates."""
        dates_list = self.getWorkingDatesBetween(start_date, end_date)
        efficiency = 0.0
        days = 0.0
        for each_date in dates_list:
            efficiency += self.getEfficiencyFor(each_date)
            days += 1.0
        if days == 0:
            print "Zero day error for the following dates:", start_date, end_date
            return 0
        else:
            #print "Total efficiency: %f for %d days." % ((efficiency / days), days)
            return efficiency / days

    def getEfficiencyForWeek(self, query_date, query_user=None):
        """Returns the average efficiency for a query_user or the caller ID for the week in
        which the request date falls.
        It only considers those dates in the range which occur prior to the queryDate."""
        #Find out what day the given date falls on. 1 = Monday, 7 = Sunday.
        if query_user is None:
            query_user = self.user_id
        current_day = query_date.isocalendar()[2]
        #Get the date of the monday in that week. Week ends on Sunday.
        subtractor = current_day - 1
        first_day_of_the_week = query_date - datetime.timedelta(subtractor)
        efficiency = self.getEfficiencyBetween(user_id, password, first_day_of_the_week, query_date, query_user)
        return efficiency

    def getEfficiencyForMonth(self, query_date):
        """Returns the average efficiency for a query_user or the caller ID for the month in
        which the request date falls.
        It only considers those dates in the range which occur prior to the queryDate."""
        
        first_day_of_the_month = datetime.date(query_date.year, query_date.month, 1)
        efficiency = self.getEfficiencyBetween(first_day_of_the_month, query_date)
        return efficiency

    def getEfficiencyForQuarter(self, query_date):
        """Returns the average efficiency for a queryUser or the caller ID for the quarter in
        which the request date falls.
        It only considers those dates in the range which occur prior to the queryDate."""
        #JFM, AMJ, JAS, OND
        query_month = query_date.month
        #Create a dictionary which contains a 1:1 mapping for the first months
        #of a quarter for any given month. 
        #If asked for the first month of JAS, it should return 7, i.e. July.
        quarter_first_month_mapped_dictionary = {
            1: 1, 2: 1, 3: 1,
            4: 4, 5: 4, 6: 4,
            7: 7, 8: 7, 9: 7,
            10: 10, 11: 10, 12: 10
        }
        first_month_of_the_quarter = quarter_first_month_mapped_dictionary[query_date.month]
        first_day_of_the_quarter = datetime.date(query_date.year, first_month_of_the_quarter, 1)
        efficiency = self.getEfficiencybetween(first_day_of_the_quarter, query_date)
        return efficiency

    def getCFMFor(self, query_date):
        import numpy
        if query_user is None:
            query_user = user_id
        raw_data_table, CFM_Key_list, GSEO_list = self.getRawDataTableAndAuditParameters()
        sqlcmdstring = """SELECT * FROM `%s` WHERE `WriterID` = '%s' AND `Audit Date` = '%s';""" %(raw_data_table, query_user, self.convertToMySQLDate(query_date))
        #print sqlcmdstring
        data = self.readFromOINK(sqlcmdstring, sys._getframe().f_code.co_name)
        audits = len(data)
        #print "Found %d audited articles." % audits
        CFM_score_total = 0
        counter = 0
        for each_entry in data:
            CFM_score = numpy.sum(list(each_entry[CFM_Key] for CFM_Key in CFM_Key_list)) / float(75.0)
            counter += 1
            #print "Score for audit #%d = %f" %(counter, CFM_score) 
            #print "Recorded CFM Score = %f" %each_entry["CFM Quality"]
            CFM_score_total += CFM_score
        if audits > 0:
            CFM_score_average = CFM_score_total / audits
        else:
            CFM_score_average = None
        connectdb.commit()
        connectdb.close()
        return CFM_score_average

    def getCFMBetween(self, start_date, end_date):
        import numpy
        dates = OINKM.getDatesBetween(start_date, end_date)
        #print dates
        CFM_scores = []
        for query_date in dates:
            CFM = self.getCFMFor(query_date)
            if CFM is not None:
                CFM_scores.append(CFM)
        CFM_score_average = numpy.mean(CFM_scores)
        return CFM_score_average

    def getCFMForWeek(self, query_date):
        """Returns the average CFM for a query_user or the caller ID for the week in
        which the request date falls.
        It only considers those dates in the range which occur prior to the queryDate."""
        #Find out what day the given date falls on. 1 = Monday, 7 = Sunday.
        current_day = query_date.isocalendar()[2]
        #Get the date of the monday in that week. Week ends on Sunday.
        subtractor = current_day - 1
        first_day_of_the_week = query_date - datetime.timedelta(subtractor)
        CFM = self.getCFMBetween(first_day_of_the_week, query_date)
        return CFM

    def getCFMForMonth(self, query_date):
        """Returns the average CFM for a query_user or the caller ID for the month in
        which the request date falls.
        It only considers those dates in the range 
        which occur prior to the queryDate."""
        first_day_of_the_month = datetime.date(query_date.year, query_date.month, 1)
        CFM = self.getCFMBetween(first_day_of_the_month, query_date)
        return CFM

    def getCFMForQuarter(self, query_date):
        """Returns the average CFM for a queryUser or the caller ID for the quarter in
        which the request date falls.
        It only considers those dates in the range which occur prior to the queryDate."""
        #JFM, AMJ, JAS, OND
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
        CFM = self.getCFMBetween(first_day_of_the_quarter, query_date)
        return CFM

    def getGSEOFor(self, query_date):
        import numpy
        if query_user is None:
            query_user = user_id
        raw_data_table, CFM_Key_list, GSEO_Key_list = self.getRawDataTableAndAuditParameters()

        sqlcmdstring = """SELECT * FROM `%s` WHERE `WriterID` = '%s' AND `Audit Date` = '%s';""" %(raw_data_table, query_user, convertToMySQLDate(query_date))
        #print sqlcmdstring
        data = self.readFromOINK(sqlcmdstring, sys._getframe().f_code.co_name)
        #print "Found %d audited articles." % audits
        GSEO_score_total = 0
        counter = 0
        for each_entry in data:
            GSEO_score = numpy.sum(list(each_entry[GSEO_Key] for GSEO_Key in GSEO_Key_list)) / float(25)
            counter += 1
            #print "FSN or SEO Topic: ", each_entry["FSN"]
            #print "Score for audit #%d = %f" %(counter, GSEO_score) 
            #print "Recorded GSEO Score = %f" %each_entry["GSEO Quality"]
            GSEO_score_total += GSEO_score
        
        audits = len(data)
        if audits != 0:
            print "Found %d audits for %s on %s." %(audits, query_user, query_date)
            GSEO_score_average = GSEO_score_total / audits
        else:
            #print data
            GSEO_score_average = None    
        return GSEO_score_average

    def getGSEOBetween(self, start_date, end_date):
        import numpy
        dates = OINKM.getDatesBetween(start_date, end_date)
        #print dates
        GSEO_scores = []
        for query_date in dates:
            GSEO = self.getGSEOFor(query_date)
            if GSEO is not None:
                GSEO_scores.append(GSEO)
        #print GSEO_scores
        GSEO_score_average = numpy.mean(GSEO_scores)
        return GSEO_score_average

    def getGSEOForWeek(self, query_date):
        """Returns the average GSEO for a query_user or the caller ID for the week in
        which the request date falls.
        It only considers those dates in the range which occur prior to the queryDate."""
        #Find out what day the given date falls on. 1 = Monday, 7 = Sunday.
        current_day = query_date.isocalendar()[2]
        #Get the date of the monday in that week. Week ends on Sunday.
        subtractor = current_day - 1
        first_day_of_the_week = query_date - datetime.timedelta(subtractor)
        GSEO = self.getGSEOBetween(first_day_of_the_week, query_date)
        return GSEO

    def getGSEOForMonth(self, query_date):
        """Returns the average GSEO for a query_user or the caller ID for the month in
        which the request date falls.
        It only considers those dates in the range which occur prior to the queryDate."""
        first_day_of_the_month = datetime.date(query_date.year, query_date.month, 1)
        GSEO = self.getGSEOBetween(first_day_of_the_month, query_date)
        return GSEO

    def getGSEOForQuarter(self, query_date):
        """Returns the average GSEO for a queryUser or the caller ID for the quarter in
        which the request date falls.
        It only considers those dates in the range which occur prior to the queryDate."""
        #JFM, AMJ, JAS, OND
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
        GSEO = self.getGSEOBetween(first_day_of_the_quarter, query_date)
        return GSEO

    def getDescriptionTypes(self):
        """"""
    def getSources(self):
        """"""
    def getBUValues(self):
        """"""
    def getSuperCategoryValues(self):
        """"""
    def getCategoryValues(self):
        """"""
    def getSubCategoryValues(self):
        """"""
    def getBrandValues(self):
        """"""

    def getRawDataTableAndAuditParameters(self, query_date=None):
        raw_data_table = 'rawdata'
        CFM = ["CFM01","CFM02","CFM03","CFM04","CFM05","CFM06","CFM07","CFM08"]
        GSEO = ["GSEO01","GSEO02","GSEO03","GSEO04","GSEO05","GSEO06","GSEO07"]
        return raw_data_table, CFM, GSEO

    def getFirstDisplayedDateFor(self, query_date=None):
        """Returns the first monday of a month.
        Rather, it returns the first monday in a calendar page. 
        If the month starts on a saturday, it returns 
        the last monday of the previous month."""
        if query_date is None:
            query_date = self.active_date
        first_day_of_the_month = datetime.date(query_date.year, query_date.month, 1) 
        day_of_the_week = first_day_of_the_month.isocalendar()[2]
        return first_day_of_the_month - datetime.timedelta(day_of_the_week -1)

    def getLastDisplayedDateFor(self, query_date=None):
        """Returns a day 40 days after the current start_date."""
        if query_date is None:
            query_date = self.start_date
        return query_date + datetime.timedelta(40)

    def getHostID(self):
        hostid_file = OINKM.getLatestFile("hostid.txt","Data")
        return open(hostid_file).read()

    def getDBName(self):
        return "oink"

    def createLoginStamp(self):
        """This method does two things:
        1. It checks if a workcalendar entry exists for the present date. 
            If it does it, it goes ahead and adds it.
        2. It then builds an sqlcmdstring for inserting a time into the login record.
        """
        login_time = datetime.datetime.now()
        login_date = datetime.date.today()
        status, relaxation, approval = self.getWorkingStatus(login_date)
        if status == False:
            self.updateWorkCalendar(login_date, status="Working")

        sqlcmdstring = """INSERT INTO `loginrecord` (`Date`, `Employee ID`, `Login Time`) VALUES ("%s", "%s", "%s");"""%(convertToMySQLDate(login_date), self.user_id, login_time)
        try_to_write = self.writeToOINK(sqlcmdstring)
        if not try_to_write:
            print "Failed while trying to write this command."
    
    def writeToOINK(self, sqlcmdstring):
        """This method handles all the writing related queries.
        """
        self.writing_cursor.execute(sqlcmdstring)
        self.writer_conn.commit()
        trial = 0
        try_again = True
        isSuccess = False
        while (trial < 3) and (try_again):
            try:
                self.writing_cursor.execute(sqlcmdstring)
                self.writer_conn.commit()
                try_again = False
                is_success = True
            except MySQLdb.Error, e:
                print "*********************"
                print "Error in Prophet. Function name %s." %sys._getframe().f_code.co_name
                print "Time: %s" % datetime.datetime.now()
                print "User: %s" %(self.user_id)
                print "Possible loss of connection to the server."
                print "Trying to post data again. Current trial no: %d" %trial 
                print "*********************"
                trial += 1
                results = None
            except:
                print "*********************"
                print "Error in Prophet. Function name %s." %sys._getframe().f_code.co_name
                print "Time: %s" % datetime.datetime.now()
                print "User: %s" %(self.user_id)
                print "This is not a connection failure error. Current trial no: %d" %trial 
                print "Printing the sqlcmdstring:\n*\n%s\n*" %sqlcmdstring
                print "Raising the error."
                print "*********************"
                raise
        return results