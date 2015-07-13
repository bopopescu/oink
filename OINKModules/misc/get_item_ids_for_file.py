import datetime
import time
import urllib2
import pandas as pd
def getETA(start_time, counter, total):
    now = datetime.datetime.now()
    time_spent = now - start_time
    mean_time = time_spent/counter
    ETA = start_time + (mean_time*total)
    return ETA


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

def main():
    fsns_list = open("check_these.csv").read().split("\n")
    total = len(fsns_list)
    output_data = dict((fsn, {}) for fsn in fsns_list)
    start_time = datetime.datetime.now()
    last_update_time = datetime.datetime.now()
    print "Got %d fsns. Starting at %s." %(total, start_time)
    counter = 1
    for fsn in fsns_list:
        url = "http://www.flipkart.com/search?q=" + fsn
        try:
            html_object = urllib2.urlopen(url, timeout=60)
            item_id = getItemID(html_object)
            output_data[fsn] = {
                    "Item ID":item_id, "Status": "Found on FK Site"
                    }
        except:
            output_data[fsn] = {
                            "Item ID": None, 
                            "Status": "Possibly not featuring on FK site."
                        }
        if datetime.datetime.now() - last_update_time > datetime.timedelta(seconds=60):
            print "%d/%d. ETA: %s" %(counter, total, getETA(start_time, counter, total))
            last_update_time = datetime.datetime.now()
        output_data_frame = pd.DataFrame.from_dict(output_data, )
        output_data_frame.transpose().to_csv("Checked_FSNs.csv", sep=",")
        counter += 1
    print "Completed."
if __name__ == "__main__":
    main()