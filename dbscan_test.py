from sklearn.cluster import DBSCAN
import numpy as np
from collections import Counter


# def get_centermost_point(cluster):
#     lon_sum=0
#     lat_sum=0
#     for coor in cluster:
#         lon_sum = lon_sum+coor[0]
#         lat_sum = lat_sum+coor[1]
#     return (lon_sum/len(cluster),lat_sum/len(cluster))

def get_center_in_cluster(coordinates_list):
    centers = np.array(coordinates_list)
    eps = 1.5/6371.0088

    # need to change min_samples size to get rid of outlier
    # otherwise each outlier could be a cluster
    db = DBSCAN(eps=eps, min_samples=1).fit(centers)
    labels = db.labels_

    # get the cluster number
    #n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    #find the largest cluster
    c = Counter(labels)
    # cluster index of the largest one (not the coord index)
    largest_cluster_index = (c.most_common(1))[0][0]
    print(largest_cluster_index)

    # the coordinates that in the largest cluster
    largest_cluster = []
    for i in range(len(centers)):
        if labels[i] == largest_cluster_index:
            largest_cluster.append(centers[i].tolist())

    print(largest_cluster)

    lon_sum = 0
    lat_sum = 0
    for coor in largest_cluster:
        lon_sum = lon_sum + coor[0]
        lat_sum = lat_sum + coor[1]

    avg = [lon_sum / len(largest_cluster), lat_sum / len(largest_cluster)]
    print(avg)
    difference_list = {}

    # i'm trying to calculate the difference between all the points in largest cluster with the average
    # to find the closest point
    # and return that point!
    for i in range(0, len(largest_cluster)):
        difference_list.update(i: ([abs(coor[0]-avg[0]),abs(coor[1]-avg[1])]))

    print difference_list




    return ()



result = get_center_in_cluster([[40.430023, -86.909103], [40.422363, -86.876788], [40.422363, -86.876668], [40.425368, -86.895309], [40.366318, -86.752251]])
print result


#
# centers =np.array( [[40.430023, -86.909103], [40.422363, -86.876688], [40.422363, -86.876668], [40.425368, -86.895309], [40.366318, -86.752251]])
# X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.3,
#                             random_state=0)
#
# X = StandardScaler().fit_transform(X)
#
# # #############################################################################
# # Compute DBSCAN
# eps=1.5/6371.0088
# db = DBSCAN(eps=eps, min_samples=1).fit(centers)
# print(db.labels_)
#
# labels = db.labels_
#
# # Number of clusters in labels, ignoring noise if present.
# n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
# c = Counter(labels)
# print(n_clusters_)
# largest_cluster_index = (c.most_common(1))[0][0]
#
# largest_cluster = []
# for i in range(len(centers)):
#     if labels[i] == largest_cluster_index:
#         largest_cluster.append(centers[i].tolist())
#
# print(largest_cluster)
#
# print(get_centermost_point(largest_cluster))
#
# print('Estimated number of clusters: %d' % n_clusters_)



