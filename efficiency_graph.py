#from __future__ import division
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from OINKModules import MOSES

def getData(query_date=None):
    #Set the date.
    if query_date is None:
        query_date = datetime.date.today()
    
    user_id, password = MOSES.getbbc()

    #Get a list of dictionaries pertaining to writers' data.
    writers_data_list = MOSES.getWritersList(user_id, password, query_date)

    #get a sorted list of writers' employee IDs.
    writers_ids = [writer["Employee ID"] for writer in writers_data_list]
    writers_ids.sort()

    writer_count = len(writers_ids)

    #For each writer, get the efficiency, work status, cfm and gseo.
    writer_data_frame = pd.DataFrame(columns=["Employee ID","Employee Name","Status","Efficiency","CFM","GSEO","Efficiency Color","CFM Color", "GSEO Color"]                                    )

    #create a pandas dataframe with the following columns:
    #writerid, writer_name, work_status, efficiency, cfm, gseo, stack_rank_index

    red = "#FF3325"
    green = "#43AD38"
    blue = "#027CD5"
    bright_blue = "#027CD5"
    grey = "0.75"
    writer_counter = 0
    for writer in writers_data_list:
        writer_id = writer["Employee ID"]
        writer_name = "%s" %writer["Name"][:writer["Name"].find(" ")]
        status, relaxation, approval = MOSES.checkWorkStatus(user_id, password, query_date, writer_id)
        if status == "Working":
            efficiency = MOSES.getEfficiencyFor(user_id, password, query_date, writer_id)
        else:
            efficiency = 100.00
        cfm = MOSES.getCFMFor(user_id, password, query_date, writer_id)
        gseo = MOSES.getGSEOFor(user_id, password, query_date, writer_id)
        if status == "Working":
            efficiency *= 100.000
            efficiency = np.around(efficiency,3)
            if efficiency < 100.000:
                efficiency_color = red
            elif 100.000 <= efficiency < 105.000:
                efficiency_color = green
            elif 105.000 <= efficiency < 110.000:
                efficiency_color = blue
            else:
                efficiency_color = bright_blue
        else:
            efficiency_color = grey
        #print efficiency, efficiency_color
        if cfm < 95.000:
            cfm_color = red
        elif 95.000 <= cfm < 97.000:
            cfm_color = green
        elif 97.000 <= cfm < 99.000:
            cfm_color = blue
        else:
            cfm_color = bright_blue
        if gseo < 95.000:
            gseo_color = red
        elif 95.000 <= gseo < 97.000:
            gseo_color = green
        elif 97.000 <= gseo < 99.000:
            gseo_color = blue
        else:
            gseo_color = bright_blue
        writer_array = [writer_id, writer_name, status, efficiency, 
                    cfm, gseo, efficiency_color, cfm_color, gseo_color]
        #print writer_array
        writer_data_frame.loc[writer_counter] = writer_array
        writer_counter+=1
    writer_data_frame.sort(["Efficiency","CFM","GSEO"], ascending = [0,0,0], inplace = True)
    return writer_data_frame
    
if __name__ == "__main__":
    query_date = datetime.date(2015, 5, 13)
    data_set = getData(query_date)
    print data_set
    #first plot the efficiency
    data_set.sort(["Efficiency", "Status"],ascending=[0,0],inplace = True)
    #data_set.sort(["Status"],ascending=[0],inplace = True)

    efficiency_writers_order = list(data_set["Employee Name"])
    efficiency_list = list(data_set["Efficiency"])
    efficiency_colors = list(data_set["Efficiency Color"])
    efficiency_width = 0.5
    data_length = len(data_set.index)
    positions = np.arange(data_length)+0.5

    #start plotting
    plt.xlabel("Writers")
    plt.ylabel("Efficiency")
    #print efficiency_writers_order, efficiency_list, efficiency_colors
    for counter in range(data_length):
        bar_set = plt.bar(positions[counter], efficiency_list[counter], width=efficiency_width, color = efficiency_colors[counter])
    plt.grid(True, lw=0.5, ls="--", c="0.05")
    plt.title("Efficiency Graph For %s" % query_date)

    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.FixedLocator(positions))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter((efficiency_writers_order)))
    y_axis_tickers = np.arange(40)*2.5
    plt.yticks(np.arange(min(efficiency_list), max(efficiency_list)+1, max(efficiency_list)/20))
    locs, labels = plt.xticks()
    plt.setp(labels, rotation = 90.0)
    plt.subplots_adjust(bottom=0.2)
    plt.ylim(min(efficiency_list))
#    ax = plt.axes()
#    ax.xaxis.set_major_locator(ticker.FixedLocator(positions))
#    ax.xaxis.set_major_locator(ticker.FixedFormatter(efficiency_writers_order))
#    ax.xaxis.set_major_locator(ticker.FixedFormatter(efficiency_writers_order))
   # plt.setp(labels)
    plt.show()
    