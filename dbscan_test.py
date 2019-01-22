from sklearn.cluster import DBSCAN
import numpy as np
from collections import Counter
from shapely.geometry import MultiPoint
from geopy.distance import great_circle


# Function to get the centermost point in a list of points
# Argument cluster is a list of pair of coordinates, eg: [[lat1, lon1],[lat2, lon2], ...]
# Return value as the center most point in a tuple format in the list

def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return centermost_point


def get_center_in_cluster(coordinates_list):
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
    c = Counter(labels)
    # cluster index of the largest one (not the coord index)
    largest_cluster_index = (c.most_common(1))[0][0]
    # print(largest_cluster_index)

    # the coordinates that in the largest cluster
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