from math import sqrt
from sklearn.cluster import DBSCAN
import numpy as np
from collections import Counter
from shapely.geometry import MultiPoint
from geopy.distance import great_circle
import matplotlib.pyplot as plt

from sklearn.datasets.samples_generator import make_blobs
from sklearn import metrics
from sklearn.preprocessing import StandardScaler



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

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print("cluster number: "+str(n_clusters))


    # # Testing, plot the graph
    # core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    # core_samples_mask[db.core_sample_indices_] = True
    #
    # unique_labels = set(labels)
    # colors = [plt.cm.Spectral(each)
    #             for each in np.linspace(0, 1, len(unique_labels))]
    #
    # for k, col in zip(unique_labels, colors):
    #     if k == -1:
    #         col = [0, 0, 0, 1]
    #     class_member_mask = (labels == k)
    #
    #     xy = centers[class_member_mask & core_samples_mask]
    #     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
    #                            markeredgecolor = 'k', markersize = 14)
    #
    #     xy = centers[class_member_mask & ~core_samples_mask]
    #     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
    #                            markeredgecolor = 'k', markersize = 6)
    #
    # plt.title('Estimated number of clusters: %d' % n_clusters)
    # plt.show()

    # end of testing


    # get the cluster number


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


#result = get_center_in_cluster([[40.430023, -86.909103], [40.422363, -86.876788], [40.422363, -86.876683],
#                                [40.425368, -86.895309], [40.366318, -86.752251]])
#print result

def test_cluster():
    centers = [[40, -86], [41, -87]]
    X, labels_true = make_blobs(n_samples = [8,6],centers=centers, cluster_std = 0.00001,
                                random_state=0)
    print X
    print("======")
    print(get_center_in_cluster(X))



test_cluster()

# result = get_center_in_cluster([[40.430023, -86.909103], [40.422363, -86.876788], [40.422363, -86.876683],
#                                 [40.425368, -86.895309], [40.366318, -86.752251]])
# print result