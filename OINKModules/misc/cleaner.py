import MySQLdb
import datetime
import csv

import time


def getFSNsfromFile():
	fsns_file = "fsns.csv"
	return open(fsns_file).read().split("\n")

def isNotDuplicate(fsn):
    wasWrittenBefore = False
    userID, password = getBigbrotherCredentials()
    connectdb = MySQLdb.connect(host = getHostID(), user = userID, passwd = password, db = getDBName(), cursorclass = MySQLdb.cursors.DictCursor)
    dbcursor = connectdb.cursor()
    sqlcmdstring = """SELECT * FROM `piggybank` WHERE `FSN` = '%s';""" % (fsn)
    dbcursor.execute(sqlcmdstring)
    local_data = dbcursor.fetchall()
    if len(local_data) > 0: #If that FSN exists in the data for a given date.
        wasWrittenBefore = True
    else: #If not found in the given date    
        sqlcmdstring = """SELECT * from `fsndump` WHERE `FSN` = '%s' and `Description Type` = '%s';""" % (FSN, articleType)
        dbcursor.execute(sqlcmdstring)
        global_data = dbcursor.fetchall()
        if len(global_data) > 0: #If found in the fsndump
            wasWrittenBefore = True      
    connectdb.commit()
    connectdb.close()   
    return wasWrittenBefore

def getETA(start_time, counter, total):
    now = datetime.datetime.now()
    time_spent = now - start_time
    mean_time = time_spent/counter
    ETA = start_time + (mean_time*total)
    return ETA

if __name__ == "__main__":
	fsns = getFSNsfromFile()
	output_file_name = "new_fsns.csv"
	output_file = open(output_file_name,"w")
	output_file.truncate()
	start_time = datetime.datetime.now()
	print "Starting operation."
	total = len(fsns)
	counter = 1
	uniques = 0
	for fsn in fsns:
		if isNotDuplicate(fsn):
			uniques+=1
			output_file_csv.writerow([fsn])
		counter += 1
		if counter == 1 or (counter % (total\10) == 0):
			print "Completed %d FSNs. Found %d uniques." %(counter, uniques)
			print "Operation will possibly complete by: %s." % getETA(start_time, counter, total)
	
	output_file.close()
	
	print "Completed! Please check %s" %output_file_name

