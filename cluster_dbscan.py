# TODO: define function which takes in data set of coordinates,
# makes clusters, finds largest cluster and prints its centroid
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np


def make_clusters(coords):
    X, labels_true = make_blobs()           # what do
    X = StandardScaler().fit_transform(X)   # these do
    kms_per_radian = 6371.0088
    epsilon = 0.056 / kms_per_radian
    db = DBSCAN(eps=epsilon, min_samples=3, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels))
    # found num_clusters now find biggest cluster


def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)

