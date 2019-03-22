import pyodbc

from sklearn.cluster import DBSCAN
import numpy as np
from collections import Counter
from shapely.geometry import MultiPoint
from geopy.distance import great_circle


def connect_database(server, username, password, database, driver):
    cnxn = pyodbc.connect(
        'DRIVER={' + driver + '};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return cnxn


def find_time_period_of_cluster(coordinates, user_id, data_table):
    cnxn = connect_database('128.46.137.96', 'localityteam', '123456', 'locality', 'PostgreSQL Unicode(x64)')
    cursor = cnxn.cursor()

    earliest = [99999999, 999999]
    latest = [00000000, 000000]
    for coordinate in coordinates:
        # Write query and execute
        query = "SELECT created_at FROM " + data_table + " where user_id = '" + str(user_id) + "' and geo_lat = " + \
                str(coordinate[0]) + " and geo_long = " + str(coordinate[1])

        cursor.execute(query)
        row = cursor.fetchone()

        # Parsing each row
        while row:
            date = int(row[0].strftime('%Y%m%d'))
            time = int(row[0].strftime('%H%M%S'))
            if earliest[0] > date or (earliest[0] == date and earliest[1] > time):
                earliest = [date, time]
            if latest[0] < date or (latest[0] == date and latest[1] < time):
                latest = [date, time]
            row = cursor.fetchone()

    return [latest[0] - earliest[0], latest[1] - earliest[1]]


# Function to get the centermost point in a list of points
# Argument cluster is a list of pair of coordinates, eg: [[lat1, lon1],[lat2, lon2], ...]
# Return value as the center most point in a tuple format in the list

def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return centermost_point


def get_center_in_cluster(coordinates_list, user_id, data_table):
    centers = np.array(coordinates_list)
    # eps = 1.5/6371.0088
    eps = 0.0004

    # Calling DBScan to build cluster and get the centers
    db = DBSCAN(eps=eps, min_samples=3).fit(centers)

    # Get the list of clusters
    labels = db.labels_

    filtered_labels = np.delete(labels, np.argwhere(labels == -1))

    # print the center index of each points
    n_clusters = len(set(filtered_labels))
    # print("cluster number: "+str(n_clusters))
    if n_clusters == 0:
        return None

    # find the largest cluster
    cluster_counter = Counter(filtered_labels)
    # cluster index of the largest one (not the coord index)
    # largest_cluster_index = (cluster_counter.most_common(1))[0][0]
    largest_cluster_number = cluster_counter.most_common()[0][1]

    largest_clusters = []
    for counter in cluster_counter.most_common():
        if counter[1] < largest_cluster_number:
            break
        largest_clusters.append(counter[0])

    # for cluster in cluster_counter:
    #     print cluster_counter[0]
    #     print cluster
    #     if cluster < largest_cluster_number:
    #         break
    #     largest_clusters.append(cluster)

    largest_cluster_index = -1

    if len(largest_clusters) == 1:
        largest_cluster_index = largest_clusters[0]

    else:
        longest_period = [0, 0]
        for cluster_index in largest_clusters:
            temp_cluster = []

            for i in range(len(centers)):
                if labels[i] == cluster_index:
                    temp_cluster.append(centers[i].tolist())

            print(temp_cluster)
            period = find_time_period_of_cluster(temp_cluster, user_id, data_table)
            if longest_period[0] < period[0] or (longest_period[0] == period[0] and longest_period[1] < period[1]):
                longest_period = period
                largest_cluster_index = cluster_index

    largest_cluster = []
    for i in range(len(centers)):
        if labels[i] == largest_cluster_index:
            largest_cluster.append(centers[i].tolist())

    # print(largest_cluster)
    return get_centermost_point(largest_cluster)
