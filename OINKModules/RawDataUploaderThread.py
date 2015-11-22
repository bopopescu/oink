from __future__ import division
import datetime
import os
import sys
import math
import unidecode
from PyQt4 import QtGui, QtCore
import pandas as pd
import xlrd
import MOSES
import MySQLdb

class RawDataUploaderThread(QtCore.QThread):
    sendActivity = QtCore.pyqtSignal(int, datetime.datetime, int, int, int, int) 
    #progress, eta, accepted, rejected, failed, pending
    sendMessage = QtCore.pyqtSignal(str)
    def __init__(self, user_id, password):
        super(RawDataUploaderThread, self).__init__()
        self.user_id, self.password = user_id, password
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.data_frame = None
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def run(self):
        while True:
            self.mutex.unlock()
            if self.data_frame is not None:
                self.processDataFrame()
            self.mutex.lock()

    def processDataFrame(self):
        start_time = datetime.datetime.now()
        total = self.data_frame.shape[0]
        self.sendMessage.emit("%d rows loaded from the file."%total)
        unfiltered_raw_data = self.data_frame
        unfiltered_raw_data.columns = MOSES.getRawDataKeys()
        raw_data = unfiltered_raw_data[[not(match) for match in list(pd.isnull(unfiltered_raw_data["WriterID"]))]]
        raw_data[["WriterID"]] = raw_data[["WriterID"]].astype(int)
        raw_data[["Editor ID"]] = raw_data[["Editor ID"]].astype(int)
        #print raw_data.columns
        rejected_data_frame = raw_data[raw_data["Overall Quality"] == "-"]
        rejected_rows = rejected_data_frame.shape[0]
        tentatively_accepted_rows = raw_data[raw_data["Overall Quality"] != "-"]
        raw_data_as_dicts = tentatively_accepted_rows.to_dict("records")
        conn = MOSES.getOINKConnector(self.user_id, self.password)
        cursor = conn.cursor()
        accepted_total = len(tentatively_accepted_rows)
        self.sendMessage.emit("%d accepted rows loaded."%accepted_total)
        progress = 0
        eta = datetime.datetime.now()
        accepted = 0
        rejected = 0
        failed = 0
        pending = total
        self.sendActivity.emit(progress, eta, accepted, rejected, failed, pending)
        primary_key_columns = ["Audit Date","Editor ID","WriterID", "FSN"]
        for each_row in raw_data_as_dicts:
            for key in each_row.keys():
                if type(each_row[key]) == unicode:
                    try:
                        each_row[key]= str(unidecode.unidecode(each_row[key])).replace('"',"'")
                    except:
                        each_row[key]= str("Failed Loading %s from the Raw Data"%key)
            success = False
            columns, values = MOSES.getDictStrings(each_row)
            sqlcmdstring = "INSERT INTO `rawdata` (%s) VALUES (%s);" % (columns, values)
            try:
                cursor.execute(sqlcmdstring)
                conn.commit()
                success = True
            except MySQLdb.IntegrityError:
                #print "Integrity Error!"
                try:
                    updation_columns = [x for x in each_row.keys() if x not in primary_key_columns]
                    update_field_list = ['`%s` = "%s"'%(column, str(each_row[column]).replace('"',"'")) for column in updation_columns]
                except:
                    print each_row
                    print sqlcmdstring
                    raise
                update_query = ", ".join(update_field_list)

                primary_key_field_list = ['`%s` = "%s"'%(column, str(each_row[column]).replace('"',"'")) for column in primary_key_columns]
                primary_key_query = " AND ".join(primary_key_field_list)
                sqlcmdstring = "UPDATE `rawdata` SET %s WHERE %s;" % (update_query, primary_key_query)
                try:
                    cursor.execute(sqlcmdstring)
                    conn.commit()
                    success = True
                except Exception, err:
                    print repr(err)
                    print sqlcmdstring
                    success = False
            except Exception, e:
                print repr(e)
                print sqlcmdstring
                success = False
            if success:
                accepted += 1
            else:
                failed += 1
            counter = accepted + rejected + failed
            progress = int(math.floor(counter/total*100))
            eta = MOSES.getETA(start_time, counter, total)
            pending = total-counter
            self.sendActivity.emit(progress, eta, accepted, rejected, failed, pending)

        self.sendMessage.emit("Uploading %d rejected Audits."%rejected_rows)
        for each_row in rejected_data_frame.to_dict("records"):
            for key in each_row.keys():
                if type(each_row[key]) == unicode:
                    try:
                        each_row[key]= str(unidecode.unidecode(each_row[key])).replace('"',"'")
                    except:
                        each_row[key]= str("Failed Loading %s from the Raw Data"%key)
            success = False
            columns, values = MOSES.getDictStrings(each_row)
            sqlcmdstring = "INSERT INTO `rejected_rawdata` (%s) VALUES (%s);" % (columns, values)
            try:
                cursor.execute(sqlcmdstring)
                conn.commit()
                success = True
            except MySQLdb.IntegrityError:
                #print "Integrity Error!"
                primary_key_columns = ["Audit Date","Editor ID","WriterID", "FSN"]
                updation_columns = [x for x in each_row.keys() if x not in primary_key_columns]
                update_field_list = ['`%s` = "%s"'%(column, str(each_row[column]).replace('"',"'")) for column in updation_columns]
                update_query = ", ".join(update_field_list)

                primary_key_field_list = ['`%s` = "%s"'%(column, str(each_row[column]).replace('"',"'")) for column in primary_key_columns]
                primary_key_query = " AND ".join(primary_key_field_list)
                sqlcmdstring = "UPDATE `rejected_rawdata` SET %s WHERE %s;" % (update_query, primary_key_query)
                try:
                    cursor.execute(sqlcmdstring)
                    conn.commit()
                    success = True
                except Exception, err:
                    print repr(err)
                    print sqlcmdstring
                    success = False
            except Exception, e:
                print repr(e)
                print sqlcmdstring
                success = False
            if success:
                rejected += 1
            else:
                failed += 1
            counter = accepted + rejected + failed
            progress = int(math.floor(counter/total*100))
            eta = MOSES.getETA(start_time, counter, total)
            pending = total - counter
            self.sendActivity.emit(progress, eta, accepted, rejected, failed, pending)
        conn.close()
        self.sendMessage.emit("Completed at %s. Accepted: %d, Rejected: %d, Failed: %d. Pending: %d."%(datetime.datetime.now(), accepted, rejected, failed, pending))
        self.data_frame = None

    def setDataFrame(self, data_frame):
        self.data_frame = data_frame