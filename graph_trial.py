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
    query_user = "62487"
    writer_1_cfm, writer_1_gseo = MOSES.getRawDataParameterPercentagesBetween(u, p, d1, d2, query_user)
    team_cfm, team_gseo = MOSES.getRawDataParameterPercentagesBetween(u, p, d1, d2, "All")

    writer_quality = writer_1_cfm + writer_1_gseo
    team_quality = team_cfm + team_gseo
    quality_header_codes = ["CFM0%s"%(x+1) for x in range(len(writer_1_cfm))]+["GSEO0%s"%(x+1) for x in range(len(writer_1_gseo))]
    quality_headers = [MOSES.getAuditParameterName(parameter_code) for parameter_code in quality_header_codes]
    writer_quality = 100*np.array(writer_quality)
    team_quality = 100*np.array(team_quality)

    #writer_quality = np.array([90,95,98,100])
    #team_quality = np.array([80,100,98,99])
    x = np.arange(len(writer_quality))+0.75
    x1 = np.arange(len(writer_quality))+0.75

    plt.xlabel("Quality Parameters")
    plt.ylabel("Average %")

    layout_grid_size = (1,2)

    plt.bar(x, writer_quality, width=0.5, alpha=0.45, color="blue", linestyle='solid', label="%s..."%MOSES.getEmpName(query_user)[:10])
    plt.bar(x+0.5, team_quality, width=0.25, color="green", linestyle='solid', label="Team")

    plt.title("Comparison of %s's quality with the team between %s and %s" %(MOSES.getEmpName(query_user), d1, d2))
    plt.grid(True, lw=0.5, ls="--", c="0.05")
    plt.legend(loc="lower right", fancybox=True, shadow=True, fontsize=9)

    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.FixedLocator(x+0.25))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter((quality_headers)))

    ax.yaxis.set_major_locator(ticker.MultipleLocator(1.0))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    ax.set_ylim([80,100])

    labels = ax.get_xticklabels()
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(9)
        #label.set_bbox(dict(facecolor='white',edgecolor='None', alpha=0.65))
    plt.setp(labels, rotation=90.)
    plt.style.use('dark_background')
    plt.subplots_adjust(bottom=0.4)
    plt.show()

