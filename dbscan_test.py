from math import sqrt
from sklearn.cluster import DBSCAN
import numpy as np
from collections import Counter
from sklearn.cluster import KMeans
from shapely.geometry import MultiPoint
from geopy.distance import great_circle

def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return centermost_point


def get_center_in_cluster(coordinates_list):
    centers = np.array(coordinates_list)
    eps = 1.5/6371.0088

    # need to change min_samples size to get rid of outlier
    # otherwise each outlier could be a cluster
    db = DBSCAN(eps=eps, min_samples=1).fit(centers)
    labels = db.labels_

    # get the cluster number
    # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    # find the largest cluster
    c = Counter(labels)
    # cluster index of the largest one (not the coord index)
    largest_cluster_index = (c.most_common(1))[0][0]
    #print(largest_cluster_index)

    # the coordinates that in the largest cluster
    largest_cluster = []
    for i in range(len(centers)):
        if labels[i] == largest_cluster_index:
            largest_cluster.append(centers[i].tolist())

    print(largest_cluster)

    return get_centermost_point(largest_cluster)

    #
    # lon_sum = 0
    # lat_sum = 0
    # for coor in largest_cluster:
    #     lon_sum = lon_sum + coor[0]
    #     lat_sum = lat_sum + coor[1]
    #
    # avg = [lon_sum / len(largest_cluster), lat_sum / len(largest_cluster)]
    # #print(avg)
    #
    # # i'm trying to calculate the difference between all the points in largest cluster with the average
    # # to find the closest point
    # # and return that point!
    #
    # distances_list = []
    # # finding the distances of each point from average and returning the point with
    # # which the distance is shortest
    # # for short distances, distance formula is accurate
    #
    # for i in range(0, len(largest_cluster)):
    #     x = pow(abs(largest_cluster[i][0]-avg[0]), 2)
    #     y = pow(abs(largest_cluster[i][1]-avg[1]), 2)
    #     dist = sqrt(x+y)
    #     distances_list.append(dist)
    #
    # val, idx = min((val, idx) for (idx, val) in enumerate(distances_list))
    #
    # pt = largest_cluster[idx]
    # return pt


result = get_center_in_cluster([[40.430023, -86.909103], [40.422363, -86.876788], [40.422363, -86.876683],
                                [40.425368, -86.895309], [40.366318, -86.752251]])
print result



