import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from OINKModules import MOSES
import datetime

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from OINKModules import MOSES
    import datetime
    u, p = MOSES.getBigbrotherCredentials()
    d1 = datetime.date(2015,1,1)
    d2 = datetime.date.today()
    query_user = "72891"
    writer_1_cfm, writer_1_gseo = MOSES.getRawDataParameterPercentagesBetween(u, p, d1, d2, query_user)
    team_cfm, team_gseo = MOSES.getRawDataParameterPercentagesBetween(u, p, d1, d2, "All")
    quality_header_codes = ["CFM0%d"%(x+1) for x in range(len(writer_1_cfm))]+["GSEO0%d"%(x+1) for x in range(len(writer_1_gseo))]
    #print quality_header_codes
    #print writer_1_gseo, team_gseo
    writer_quality = writer_1_cfm + writer_1_gseo
    #print writer_quality
    team_quality = team_cfm + team_gseo
    quality_headers = [MOSES.getAuditParameterName(parameter_code) for parameter_code in quality_header_codes]
    writer_quality = 100*np.array(writer_quality)
    team_quality = 100*np.array(team_quality)

    #writer_quality = np.array([90,95,98,100])
    #team_quality = np.array([80,100,98,99])
    x = np.array([y+1 for y in np.arange(len(writer_quality))])
    #print x
    x1 = np.arange(len(writer_quality))


    plt.xlabel("Quality Parameters")
    plt.ylabel("Average %")
    layout_grid_size = (1,2)
    writer_name = MOSES.getEmpName(query_user)
    plt.barh(x, writer_quality, height=0.5, alpha=0.45, color="blue", linestyle='solid', label="%s"%writer_name[:writer_name.find(" ")])
    plt.barh(x+0.5, team_quality, height=0.25, color="green", linestyle='solid', label="Team")

    plt.title("Comparison of %s's quality with the team between %s and %s" %(MOSES.getEmpName(query_user), d1, d2))
    plt.grid(True, lw=0.5, ls="--", c="0.05")
    plt.legend(loc="upper center", fancybox=True, shadow=True, fontsize=9)

    ax = plt.axes()
    ax.yaxis.set_major_locator(ticker.FixedLocator(x+0.125))
    ax.yaxis.set_major_formatter(ticker.FixedFormatter((quality_headers)))
    #ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    x_min = np.min([np.min(writer_quality), np.min(team_quality)])

    #print x_min
    ax.set_xlim([x_min-2,100])
    steps = (100 - x_min)/12

    ax.xaxis.set_major_locator(ticker.MultipleLocator(steps))

    labels = ax.get_xticklabels()
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(9)
        #label.set_bbox(dict(facecolor='white',edgecolor='None', alpha=0.65))
    plt.setp(labels)

    #plt.style.use('dark_background')
    plt.subplots_adjust(left=0.2)

    file_name = "Quality_Comparision_Graph_%s_%d%d%d.png" %(query_user,d1.year,d1.month, d1.day)

    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    #plt.show()
    print "Generated graph and wrote to file %s" %file_name
