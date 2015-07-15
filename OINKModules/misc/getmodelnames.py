import sys, time
import datetime
import os
import csv
import urllib2
from bs4 import BeautifulSoup


def getETA(start_time, counter, total):
    #from __future__ import division
    now = datetime.datetime.now()
    time_spent = now - start_time
    mean_time = time_spent.total_seconds()/counter
    ETA = start_time + datetime.timedelta(seconds=(mean_time*total))
    return ETA
    
def getFlipkartSearchString(FSN):
    "Returns the search query url for Flipkart, given an FSN or ISBN."
    return "http://www.flipkart.com/search?q=" + FSN

def getModelName(fsn):
    #get fk url
    #open fk page
    fk_html = urllib2.urlopen(getFlipkartSearchString(fsn),timeout=60)
    #check fsn page
    soup_object = BeautifulSoup(fk_html)

    #find the section in this thing.
    spec_section_area = soup_object.find(class_ = "productSpecs specSection")
    #get model name
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
    #return model name
    return specifications["Style Code"]

if __name__ == """__main__""":
    #open the file, read all fsns.
    fsns = open("getmodelnames.csv","r").read().split("\n")
    fsn_dict = dict((fsn,None) for fsn in fsns)
    start_time = datetime.datetime.now()
    last_update_time = datetime.datetime.now()
    counter = 1
    total = len(fsns)
    output_file = open("output_with_model_names.csv","w")
    output_csv = csv.DictWriter(output_file,fieldnames=["FSN","Model Name"])
    output_csv.writeheader()
    for fsn in fsns:
        try:
            fsn_dict[fsn] = getModelName(fsn)
            eta = getETA(start_time, counter, total)
            print fsn_dict[fsn], fsn
            output_csv.writerow({"FSN":fsn,"Model Name":fsn_dict[fsn]})
            print "%d of %d completed. ETA: %s" %(counter, total, datetime.datetime.strftime(eta,"%H:%M:%S"))
            #if (datetime.datetime.now()-last_update_time)>datetime.timedelta(seconds=60):
            #    last_update_time = datetime.datetime.now()
        except:
            print "Skipped", fsn
        counter+=1
    output_file.close()
    raw_input("Completed! Hit enter to continue.")

