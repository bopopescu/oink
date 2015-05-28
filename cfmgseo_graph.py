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
        writer_name = "%s..." %writer["Name"][:10]
        status, relaxation, approval = MOSES.checkWorkStatus(user_id, password, query_date, writer_id)
        if status == "Working":
            efficiency = MOSES.getEfficiencyFor(user_id, password, query_date, writer_id)
        else:
            efficiency = 100.00
        cfm = MOSES.getCFMFor(user_id, password, query_date, writer_id)
        gseo = MOSES.getGSEOFor(user_id, password, query_date, writer_id)
        if cfm is None or gseo is None:
            cfm = 0.0
            gseo = 0.0
        else:
            cfm *= 100.00
            gseo *= 100.00
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
    query_date = datetime.date(2015, 5, 20)
    data_set = getData(query_date)
    print data_set
    #first plot the efficiency
    data_set.sort(["CFM", "Status"],ascending=[0,1],inplace = True)
    writers_order = list(data_set["Employee Name"])
    cfm_list = list(data_set["CFM"])
    gseo_list = list(data_set["GSEO"])
    cfm_colors = list(data_set["CFM Color"])
    gseo_colors = list(data_set["GSEO Color"])
    bar_width = 0.25
    data_length = len(data_set.index)

    cfm_positions = np.arange(data_length)+0.5
    gseo_positions = cfm_positions+0.25
    #start plotting
    plt.xlabel("Writers")
    plt.ylabel("CFM & GSEO")
    #print efficiency_writers_order, efficiency_list, efficiency_colors
    for counter in range(data_length):
        bar_set = plt.bar(cfm_positions[counter], cfm_list[counter], width=bar_width, color = cfm_colors[counter])
        bar_set = plt.bar(gseo_positions[counter], gseo_list[counter], width=bar_width, color = gseo_colors[counter])
    plt.grid(True, lw=0.5, ls="--", c="0.05")
    plt.title("Quality Graph For %s" % query_date)

    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.FixedLocator(gseo_positions))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter((writers_order)))
    y_axis_tickers = np.arange(40)*2.5
    plt.yticks(np.arange(80.00, 100.00, 2))
    locs, labels = plt.xticks()
    plt.setp(labels, rotation = 90.0)
    plt.ylim(80.00)
    plt.subplots_adjust(bottom=0.2)
#    ax = plt.axes()
#    ax.xaxis.set_major_locator(ticker.FixedLocator(positions))
#    ax.xaxis.set_major_locator(ticker.FixedFormatter(efficiency_writers_order))
#    ax.xaxis.set_major_locator(ticker.FixedFormatter(efficiency_writers_order))
   # plt.setp(labels)
    plt.show()
    