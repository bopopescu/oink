#from __future__ import division
import datetime
import numpy as np
import pandas as pd
import MOSES

def getEfficiencyData(query_date=None):
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
    
def plotEfficiencyGraph(query_date = None):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    plt.clf()

    if query_date is None:
        query_date = datetime.date.today()
    data_set = getEfficiencyData(query_date)
    #print data_set
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
    min_efficiency = min(efficiency_list)
    min_y_value =  min_efficiency if min_efficiency <100.00 else 70.00
    plt.ylim(min_y_value)

    file_name = "%d%02d%02d_Efficiency_Graph.png" %(query_date.year,query_date.month, query_date.day)
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    print "Generated the efficiency graph. Check file: %s" %file_name

def getCFMGSEOData(query_date=None):
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
    
def plotCFMGSEOGraph(query_date=None):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    plt.clf()

    if query_date is None:
        query_date = datetime.date.today()
    data_set = getCFMGSEOData(query_date)
    #print data_set
    #first plot the efficiency
    data_set.sort(["GSEO", "CFM"],ascending=[0,0],inplace = True)
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
    file_name = "%d%02d%02d_CFM_GSEO_Graph.png" %(query_date.year,query_date.month, query_date.day)
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    #plt.show()
    print "Generated CFM and GSEO Graph. Check file %s" %file_name

def getQualityHistoricalData(query_date = None, period = None):
    if query_date is None:
        query_date = datetime.date.today()
    if period is None:
        period = 5
    group_size = 5
    quantity = int(period/group_size)
    #Get a list of lists containing group of working dates.
    dates_lists = MOSES.getWorkingDatesLists(query_date, group_size=group_size, quantity=quantity)
    #create two lists of average cfm and average gseo for all writers for these groups of dates.
    #print dates_lists
    cfm_average_list, gseo_average_list = [], []
    end_dates = []
    for date_set in dates_lists:
        start_date = min(date_set)
        end_date = max(date_set)
        end_dates.append(end_date)
        #print start_date, end_date
        cfm_average = 100.00*MOSES.getAverageTeamCFMBetween(start_date, end_date, True)
        gseo_average = 100.00*MOSES.getAverageTeamGSEOBetween(start_date, end_date, True)
        #print cfm_average, gseo_average
        cfm_average_list.append(cfm_average)
        gseo_average_list.append(gseo_average)
    #print cfm_average_list, gseo_average_list
    return end_dates, cfm_average_list, gseo_average_list

def plotQualityHistoricGraph(query_date, period=None):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    plt.clf()
    if query_date is None:
        query_date = datetime.date.today()
    if period is None:
        period = 15 # working days ago.
    #query_date = datetime.date(2015, 5, 28)
    end_dates, cfm_quality_data, gseo_quality_data = getQualityHistoricalData(query_date, period)

    week_names = ["Week of\n%s"%date_ for date_ in end_dates]
    #print cfm_quality_data, gseo_quality_data
    x_coordinates = np.arange(len(cfm_quality_data))+1
    #print x_coordinates
    cfm = plt.plot(x_coordinates, cfm_quality_data, "-bo",label="CFM")
    gseo = plt.plot(x_coordinates, gseo_quality_data, "-g^",label="GSEO")
    plt.setp(cfm, color='b', linewidth=2.0)
    plt.setp(gseo, color='g', linewidth=2.0)

    plt.title("Comparison of Team Quality for 15 days before %s" %query_date)
    min_value = min([min(cfm_quality_data),min(gseo_quality_data)])
    plt.ylim(min_value-2, 100.00)
    plt.legend(loc="upper center", fancybox=True, shadow=True, fontsize=12)
    plt.yticks(np.arange(min_value-2, 100.00, 0.25))
    plt.xticks(x_coordinates)
    plt.xlim(min(x_coordinates)-0.25,max(x_coordinates)+0.25)
    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.FixedLocator(x_coordinates))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter((week_names)))
    plt.grid(True, lw=0.5, ls="--", c="0.05")
    locs, labels = plt.xticks()
    plt.subplots_adjust(bottom=0.3)
    plt.setp(labels, rotation = 90.0)

    file_name = "%d%02d%02d_HistoricalQuality_Graph.png" %(query_date.year,query_date.month, query_date.day)
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    print "Generated the historical quality graph. Check file: %s" %file_name


def getQualityHistoricalDataMonth(query_date = None, months = None):
    import calendar
    if query_date is None:
        query_date = datetime.date.today()
    if months is None:
        months = 2
    months_list = [month for month in range(query_date.month+1)][1:][-months:]
    print months_list
    dates_lists = []
    end_dates = []
    cfm_average_list = []
    gseo_average_list = []
    user_id, password = MOSES.getBigbrotherCredentials()
    for month in months_list:
        year_ = query_date.year
        start_date = datetime.date(year_, month, 1)
        end_date = datetime.date(year_, month, calendar.monthrange(year_, month)[1])
        dates = MOSES.getWorkingDatesBetween(user_id, password, start_date, end_date, mode="All")
        dates.sort()
        start_date = min(dates)
        end_date = max(dates)
        cfm_average = 100.00*MOSES.getAverageTeamCFMBetween(start_date, end_date, True)
        gseo_average = 100.00*MOSES.getAverageTeamGSEOBetween(start_date, end_date, True)
        cfm_average_list.append(cfm_average)
        gseo_average_list.append(gseo_average)
        end_dates.append(end_date)
    return end_dates, cfm_average_list, gseo_average_list


def plotQualityHistoricGraphMonth(query_date, months=None):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    plt.clf()
    if query_date is None:
        query_date = datetime.date.today()
    if months is None:
        months = 2 # 2 months ago.
    #query_date = datetime.date(2015, 5, 28)
    end_dates, cfm_quality_data, gseo_quality_data = getQualityHistoricalDataMonth(query_date, months)

    week_names = ["Month #%02d"%date_.month for date_ in end_dates]
    #print cfm_quality_data, gseo_quality_data
    x_coordinates = np.arange(len(cfm_quality_data))+1
    #print x_coordinates
    cfm = plt.plot(x_coordinates, cfm_quality_data, "-bo",label="CFM")
    gseo = plt.plot(x_coordinates, gseo_quality_data, "-g^",label="GSEO")
    plt.setp(cfm, color='b', linewidth=2.0)
    plt.setp(gseo, color='g', linewidth=2.0)

    plt.title("Team Quality For %d months till %s." %(months, query_date))
    min_value = min([min(cfm_quality_data),min(gseo_quality_data)])
    plt.ylim(min_value-2, 100.00)
    plt.legend(loc="upper center", fancybox=True, shadow=True, fontsize=12)
    plt.yticks(np.arange(min_value-2, 100.00, 0.25))
    plt.xticks(x_coordinates)
    plt.xlim(min(x_coordinates)-0.25,max(x_coordinates)+0.25)
    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.FixedLocator(x_coordinates))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter((week_names)))
    plt.grid(True, lw=0.5, ls="--", c="0.05")
    locs, labels = plt.xticks()
    plt.subplots_adjust(bottom=0.3)
    plt.setp(labels, rotation = 90.0)

    file_name = "%d%02d%02d_HistoricalQuality_Graph_For_Months.png" %(query_date.year,query_date.month, query_date.day)
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    print "Generated the historical quality graph. Check file: %s" %file_name

def generateDailyGraphs(query_date):
    print "Generating the graphs for %s." %query_date
    print "Plotting the efficiency graph."
    plotEfficiencyGraph(query_date)
    print "Plotting CFM and GSEO graph."
    plotCFMGSEOGraph(query_date)
    period = 15
    print "Plotting team efficiency data for the last %d working days in groups of 5." %period
    plotQualityHistoricGraph(query_date, period)

if __name__ == "__main__":
    date_ = str(raw_input("Please enter the date in 'YYYY-MM-DD' format:"))
    try:
        query_date = datetime.datetime.strptime(date_, '%Y-%m-%d').date()
        generateDailyGraphs(query_date)
    except ValueError:
        print "Incorrect date format."

