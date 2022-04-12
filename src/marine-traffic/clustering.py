import numpy as np
import os
import pandas as pd
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def normalize_lat_lon(vesseltracks : pd.DataFrame) -> np.array:
    lat_lon = np.transpose(
        np.array([vesseltracks.latitude, vesseltracks.longitude])
    )
    # normalize data by applying the standard scaler
    scaler = StandardScaler()
    return scaler.fit_transform(lat_lon)


def find_clusters(lat_lon_norm : np.array, eps : float = 0.05, min_num_samples : int = 200, n_cores = 4, verbose : bool = True):
    # apply clustering algorithm
    db_fit= DBSCAN(eps=eps, min_samples=min_num_samples, n_jobs=n_cores).fit(lat_lon_norm)
    # Number of clusters in labels, ignoring noise if present.
    if verbose:
        n_clusters_ = len(set(db_fit.labels_)) - (1 if -1 in db_fit.labels_ else 0)
        n_noise_ = list(db_fit.labels_).count(-1)
        print("Estimated number of clusters: %d" % n_clusters_)
        print("Estimated number of noise points: %d" % n_noise_)
#         print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(lat_lon_norm, db_fit.labels_))
    return db_fit

def extract_clusters(db_fit, raw_data : pd.DataFrame, verbose=True, drop_noise=False) -> dict:
    clusters = dict()
    labels = db_fit.labels_
    unique_labels = set(labels)
    core_samples_mask = np.zeros_like(db_fit.labels_, dtype=bool)
    core_samples_mask[db_fit.core_sample_indices_] = True
    for label in unique_labels:
        # create a mask for the current label
        class_member_mask = labels == label
        if label == -1:  # noise data
            if verbose:
                print("extracting noise")
            if not drop_noise:
                clusters[label] = raw_data[class_member_mask & ~core_samples_mask]
        else:
            if verbose:
                print(f'extracting cluster {label+1}')
            clusters[label] = raw_data[class_member_mask & core_samples_mask]
    return clusters

def export_cluster(cluster : pd.DataFrame, fpath : str):
    assert os.path.isdir(os.path.dirname(fpath)), 'please provide a valid output directory'
    cluster.to_csv(fpath)


