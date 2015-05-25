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

    writer_1_cfm, writer_1_gseo = MOSES.getRawDataParameterPercentagesBetween(u, p, d1, d2, "73957")
    team_cfm, team_gseo = MOSES.getRawDataParameterPercentagesBetween(u, p, d1, d2, "All")
    writer_2_cfm, writer_2_gseo = MOSES.getRawDataParameterPercentagesBetween(u, p, d1, d2, "72062")

    writer_quality = writer_1_cfm + writer_1_gseo
    team_quality = team_cfm + team_gseo
    quality_headers = ["CFM00%s"%(x+1) for x in range(len(writer_1_cfm))]+["GSEO00%s"%(x+1) for x in range(len(writer_1_gseo))]

    writer_quality = 100*np.array(writer_quality)
    team_quality = 100*np.array(team_quality)

    #writer_quality = np.array([90,95,98,100])
    #team_quality = np.array([80,100,98,99])
    x = np.arange(len(writer_quality))+0.75
    x1 = np.arange(len(writer_quality))+0.75

    plt.xlabel("Quality Parameters")
    plt.ylabel("Average %% Between %s and %s" %(d1,d2))

    layout_grid_size = (1,2)

    plt.bar(x, writer_quality, width=0.5, alpha=0.45, color="blue", linestyle='solid', label="Writer")
    plt.bar(x+0.5, team_quality, width=0.25, color="green", linestyle='solid', hatch="-", label="Team")

    plt.title("Comparison of Quality of Writer and Team")
    plt.grid(True, lw=0.5, ls="--", c="0.05")
    plt.legend(loc="lower right", fancybox=True, shadow=True)

    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.FixedLocator(x+0.25))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter((quality_headers)))

    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=30.)
    plt.show()

