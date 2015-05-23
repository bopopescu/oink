import MySQLdb
import datetime
import time
import urllib2

def getItemID(html_object):
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

def getFSNsForItemIDs(query_date=None):
	import itertools	
	u = "bigbrother"
	p = "orwell"
	if query_date is None:
		sqlcmdstring = "SELECT `FSN` FROM `fsndump` WHERE `Item ID` IS NULL;"
#	else:
#		sqlcmdstring = """SELECT `FSN` FROM `PiggyBank` WHERE `Item ID` IS NULL AND `Description Type` NOT LIKE 'SEO%' AND `Article Date`="%s";""" %convertToMySQLDate(query_date)
#		sqlcmdstring = """SELECT `FSN` FROM `PiggyBank` WHERE `Item ID` IS NULL AND `Description Type` NOT LIKE 'SEO%'`Article Date`="%s";""" %convertToMySQLDate(query_date)
	conn = getOINKConnector()
	cursor = conn.cursor()
	cursor.execute(sqlcmdstring)
	data = cursor.fetchall()
	conn.commit()
	conn.close()
	return list(itertools.chain.from_iterable(data))

def getOINKConnector():
	import MySQLdb
	import MySQLdb.cursors
	conn = MySQLdb.connect(host = "172.17.188.139", user = "bigbrother", passwd = "orwell", db = "oink")
	return conn

def convertToMySQLDate(queryDate):
    """Takes a python datetime and changes it to the YYYY-MM-DD format 
    for MySQL. 
    Uses the OINKModule2 module's changeDatesToStrings method."""
    dateString = changeDatesToStrings(queryDate,"YYYY-MM-DD")
    return dateString[0]

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
        return "Error in changeDatesToStrings"

def getETA(start_time, counter, total):
    now = datetime.datetime.now()
    time_spent = now - start_time
    mean_time = time_spent/counter
    ETA = start_time + (mean_time*total)
    return ETA

def populatePiggyBankWithItemID(fsn, item_id):
	sqlcmdstring = """UPDATE fsndump set `Item ID`="%s" WHERE `FSN`="%s";""" %(item_id, fsn)
	conn = getOINKConnector()
	cursor = conn.cursor()
	cursor.execute(sqlcmdstring)
	conn.commit()
	conn.close()

if __name__ == "__main__":
	import datetime
	import time
	import random
	fsns = getFSNsForItemIDs()
	random.shuffle(fsns)
	counter = 1
	passed = 0
	total = len(fsns)
	start_time = datetime.datetime.now()
	for fsn in fsns:
		url = "http://www.flipkart.com/search?q=" + fsn
		try:
			html_object = urllib2.urlopen(url, timeout=10)
			item_id = getItemID(html_object)
			if counter == 1 or counter%10 == 0:
				print "Processing FSN#%d. Process started at %s, current time is %s." %(counter, start_time, datetime.datetime.now())
			if item_id is not None:
				populatePiggyBankWithItemID(fsn, item_id)
				passed +=1
				if counter == 1 or counter%10 == 0:
					print "Processed %d FSNs successfully.\n%d failed, %d remaining.\nPossible ETA: %s" % (passed, (counter-passed), total, getETA(start_time, counter, total))
		except Exception, e:
			print "*"*10
			print "Error with url:"
			print repr(e)
			print "*"*10
			if counter == 1 or counter%10 == 0:
				print "Processed %d FSNs successfully.\n%d failed, %d remaining.\nPossible ETA: %s" % (passed, (counter-passed), total, getETA(start_time, counter, total))
			pass
		time.sleep(2)
		counter +=1

