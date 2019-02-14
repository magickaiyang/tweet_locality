import pyodbc
import datetime
import re

from sklearn.cluster import DBSCAN
import numpy as np
from collections import Counter
from shapely.geometry import MultiPoint
from geopy.distance import great_circle


def find_time_period_of_cluster(coordinates, screenname, data_table):
    # Specify config
    server = '128.46.137.201'
    database = 'LOCALITY1'
    username = 'localityedit'
    password = 'Edit123'
    # Connect to database
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    earliest = [99999999, 999999]
    latest = [00000000, 000000]
    for coordinate in coordinates:
    # Write query and execute
        query = "SELECT [created_at] FROM " + data_table + "where screenname = '" + screenname + "' and where geo_lat = " + coordinate[0] + " and where geo_lon = " + coordinate[1]

        cursor.execute(query)
        row = cursor.fetchone()

        # Parsing each row
        while row:
            t = re.split("\W", row[1])  # split time string with regular expression, condition: non alphanumeric
            date = int(t[0]+t[1]+t[2])
            time = int(t[3]+t[4]+t[5][:-3])
            if earliest[0] > date or (earliest[0] == date and earliest[1] > time):
                earliest = [date, time]
            if latest[0] < date or (latest[0] == date and latest[1] < time):
                latest = [date, time]

    return [latest[0]-earliest[0], latest[1]-earliest[1]]


# Function to get the centermost point in a list of points
# Argument cluster is a list of pair of coordinates, eg: [[lat1, lon1],[lat2, lon2], ...]
# Return value as the center most point in a tuple format in the list

def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return centermost_point


def get_center_in_cluster(coordinates_list, screenname, data_table):
    centers = np.array(coordinates_list)
    # eps = 1.5/6371.0088
    eps = 0.0004

    # Calling DBScan to build cluster and get the centers
    # Note: need to change min_samples size to get rid of outlier
    # otherwise each outlier could be a cluster
    db = DBSCAN(eps=eps, min_samples=3).fit(centers)

    # Get the list of clusters
    labels = db.labels_

    # print the center index of each points
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    # print("cluster number: "+str(n_clusters))
    if n_clusters == 0:
        return None

    # find the largest cluster
    cluster_counter = Counter(labels)
    # cluster index of the largest one (not the coord index)
    # largest_cluster_index = (cluster_counter.most_common(1))[0][0]

    largest_cluster_number = cluster_counter[0][1]
    largest_clusters = []
    for cluster in cluster_counter:
        if cluster[1] < largest_cluster_number:
            break
        largest_clusters.append(cluster[0])

    largest_cluster_index = -1

    if len(largest_clusters) == 1:
        largest_cluster_index = largest_clusters[0]

    else:
        longest_period = [0,0]
        for cluster_index in largest_clusters:
            temp_cluster = []

            for i in range(len(centers)):
                if labels[i] == cluster_index:
                    temp_cluster.append(centers[i].tolist())
            period = find_time_period_of_cluster(list(set(temp_cluster)), screenname, data_table)
            if longest_period[0] < period[0] or (longest_period[0] == period[0] and longest_period[1] < period[1]):
                longest_period = period
                largest_cluster_index = cluster_index

    largest_cluster = []
    for i in range(len(centers)):
        if labels[i] == largest_cluster_index:
            largest_cluster.append(centers[i].tolist())

    # print(largest_cluster)
    return get_centermost_point(largest_cluster)


# Test the old method to get the center most point
#result = get_center_in_cluster([[40.430023, -86.909103], [40.422363, -86.876788], [40.422363, -86.876683],
#                                [40.425368, -86.895309], [40.366318, -86.752251]])
#print result


# result = get_center_in_cluster([[40.430023, -86.909103], [40.422363, -86.876788], [40.422363, -86.876683],
#                                 [40.425368, -86.895309], [40.366318, -86.752251]])
# print result

a = [1,2,3,1,2,3,1,1,2,2]



def most_common(lst):
    data = Counter(lst)
    return max(lst, key=data.get)

print most_common(a)