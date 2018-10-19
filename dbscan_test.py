from geopy.distance import great_circle
from shapely.geometry import MultiPoint
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import pandas as pd
import statistics

def get_centermost_point(cluster):
    lon_sum=0
    lat_sum=0
    for coor in cluster:
        lon_sum = lon_sum+coor[0]
        lat_sum = lat_sum+coor[1]
    return (lon_sum/len(cluster),lat_sum/len(cluster))

centers =np.array( [[40.430023, -86.909103], [40.422363, -86.876688], [40.422363, -86.876668], [40.425368, -86.895309], [40.366318, -86.752251]])
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.3,
                            random_state=0)

X = StandardScaler().fit_transform(X)

# #############################################################################
# Compute DBSCAN
eps=1.5/6371.0088
db = DBSCAN(eps=eps, min_samples=1).fit(centers)
print(db.labels_)

labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
c = Counter(labels)
print(n_clusters_)
largest_cluster_index = (c.most_common(1))[0][0]

largest_cluster = []
for i in range(len(centers)):
    if labels[i] == largest_cluster_index:
        largest_cluster.append(centers[i].tolist())

print(largest_cluster)

print(get_centermost_point(largest_cluster))

print('Estimated number of clusters: %d' % n_clusters_)



