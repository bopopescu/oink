import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from OINKModules import MOSES


def getQualityData(query_date = None):
    if query_date is None:
        query_date = datetime.date.today()
    #Get a list of lists containing group of working dates.
    dates_lists = MOSES.getWorkingDatesLists(query_date, group_size=5, quantity=20)
    #create two lists of average cfm and average gseo for all writers for these groups of dates.
    #print dates_lists
    cfm_average_list, gseo_average_list = [], []
    end_dates = []
    for date_set in dates_lists:
        start_date = min(date_set)
        end_date = max(date_set)
        end_dates.append(end_date)
        #print start_date, end_date
        cfm_average = 100.00*MOSES.getAverageTeamCFMBetween(start_date, end_date)
        gseo_average = 100.00*MOSES.getAverageTeamGSEOBetween(start_date, end_date)
        #print cfm_average, gseo_average
        cfm_average_list.append(cfm_average)
        gseo_average_list.append(gseo_average)
    #print cfm_average_list, gseo_average_list
    return end_dates, cfm_average_list, gseo_average_list

if __name__ == "__main__":
    query_date = datetime.date(2015, 5, 22)
    end_dates, cfm_quality_data, gseo_quality_data = getQualityData(query_date)

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
    plt.show()
    



