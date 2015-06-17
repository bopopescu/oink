import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import datetime
import MOSES
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

def plotTeamScatter(query_date=None):
    if query_date is None:
        query_date = datetime.date.today()
    user_id, password = MOSES.getBigbrotherCredentials()
    writers_data = MOSES.getWritersList(user_id, password, query_date)
    writers_list = [writer["Employee ID"] for writer in writers_data]
    #X is efficiency
    #Y is an average of CFM and GSEO
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    counter = 1
    total = len(writers_list)
    start_time = datetime.datetime.now()
    for writer in writers_list:
        print "Getting Data for %s." %MOSES.getEmpName(writer)
        xs = MOSES.getEfficiencyForQuarter(user_id, password, query_date, writer)
        ys = MOSES.getCFMForQuarter(user_id, password, query_date, writer)
        zs = MOSES.getGSEOForQuarter(user_id, password, query_date, writer)
        ax.scatter(xs, ys, zs, c='b', marker='o')
        print "Completed %d of %d. ETA: %s" %(counter, total, MOSES.getETA(start_time, counter, total))
        counter += 1
        ax.annotate(
            label, 
            xy = (x, y), xytext = (-20, 20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    ax.set_xlabel('Efficiency')
    ax.set_ylabel('CFM')
    ax.set_zlabel('GSEO')

    plt.show()

def plot3DScatter(query_date=None):
    if query_date is None:
        query_date = datetime.date.today()-datetime.timedelta(days=1)
    user_id, password = MOSES.getBigbrotherCredentials()
    writers_data = MOSES.getWritersList(user_id, password, query_date)
    writers_list = [writer["Employee ID"] for writer in writers_data]
    writer_names = []
    for writer in writers_list:
        writer_name = MOSES.getEmpName(writer)
        writer_name = writer_name[:writer_name.find(" ")]
        writer_names.append(writer_name)
    print "Getting Writers' data. This will take a while."
    points_list = []
    counter = 1
    total = len(writer_names)
    start_time = datetime.datetime.now()
    for writer in writers_list:
        print "Processing for %s. ETA: %s" %(writer, MOSES.getETA(start_time, counter, total))
        eff = MOSES.getEfficiencyForHalfYear(user_id, password, query_date, writer)
        cfm = MOSES.getCFMForHalfYear(user_id, password, query_date, writer)
        gseo = MOSES.getGSEOForHalfYear(user_id, password, query_date, writer)
        points_list.append((eff, cfm, gseo))
        counter += 1
    print "Completed."
    print "Going to plot the scatter chart now."
    points = np.array(points_list)
    labels = writer_names

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    xs, ys, zs = np.split(points, 3, axis=1)
    sc = ax.scatter(xs,ys,zs)

    # if this code is placed inside a function, then
    # we must use a predefined global variable so that
    # the update function has access to it. I'm not
    # sure why update_positions() doesn't get access
    # to its enclosing scope in this case.
    global labels_and_points
    labels_and_points = []
    ax.set_xlabel('Efficiency')
    ax.set_ylabel('CFM')
    ax.set_zlabel('GSEO')
    for txt, x, y, z in zip(labels, xs, ys, zs):
        x2, y2, _ = proj3d.proj_transform(x,y,z, ax.get_proj())
        label = plt.annotate(
            txt, xy = (x2, y2), xytext = (-20, 20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
        labels_and_points.append((label, x, y, z))
    def update_position(e):
        for label, x, y, z in labels_and_points:
            x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
            label.xy = x2,y2
            label.update_positions(fig.canvas.renderer)
        fig.canvas.draw()

    fig.canvas.mpl_connect('motion_notify_event', update_position)

    plt.show()


if __name__ == "__main__":
    #plotTeamScatter()
    plot3DScatter()