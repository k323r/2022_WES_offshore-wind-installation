#%%
# load dependecies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from glob import glob
from os import path
from mpl_toolkits.basemap import Basemap
from config import VESSEL_NAMES
from plot_mtdata import plot_track

from collections import defaultdict

from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))


# make plots interactive
# %matplotlib notebook
%matplotlib widget

%reload_ext autoreload
%autoreload 2

# %%
# read in wind farm data
wind_farms = pd.read_csv('../../data/wind-farms/wind-farms-2.txt')
wind_farms.insert(loc=0, column='key_name', value=wind_farms.windfarm_name.apply(lambda x: x.lower().replace('&', '_').replace(' ', '_').replace('/', '_')))
wind_farms.set_index('key_name', inplace=True)
wind_farms.construction_begin = pd.to_datetime(wind_farms.construction_begin, utc=True)
wind_farms.construction_end = pd.to_datetime(wind_farms.construction_end, utc=True)

#%%
# read in sea challenger data
sea_challenger = pd.read_csv('../../data/marine-traffic/sanitized/219019002_sea-challenger.csv')
sea_challenger.epoch = pd.to_datetime(sea_challenger.epoch, utc=True)
sea_challenger.set_index('epoch', inplace=True)

# %%
# 1. select only data points where vessel speed == 0
sea_challenger_select = sea_challenger.loc[sea_challenger.speed == 0]

# 2. select only data points in Europe
sea_challenger_select = sea_challenger_select.loc[
    # (sea_challenger_select.latitude > 0) & 
    #(sea_challenger_select.latitude < 8) & 
    (sea_challenger_select.latitude > 50) & 
    (sea_challenger_select.latitude < 56)    
]
plot_track(sea_challenger_select, wind_farms=wind_farms, figsize=(8,4))

#%%
sea_challenger_lat_lon = np.transpose(
    np.array(
        [sea_challenger_select.longitude, sea_challenger_select.latitude]
    )
)

#%%
scaler = StandardScaler()
X = scaler.fit_transform(sea_challenger_lat_lon)
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))

#%%
plt.figure()
unique_labels = set(labels)
print(f'{unique_labels}')

colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    print(k, col)
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = labels == k

    # xy = X[class_member_mask & core_samples_mask]
    xy = scaler.inverse_transform(X[class_member_mask & core_samples_mask])
    print(xy)
    plt.plot(
        xy[:, 0],
        xy[:, 1],
        "o",
        markerfacecolor=tuple(col),
        markeredgecolor="k",
        markersize=3,
    )

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(
        xy[:, 0],
        xy[:, 1],
        "o",
        markerfacecolor=tuple(col),
        markeredgecolor="k",
        markersize=6,
    )

plt.title("Estimated number of clusters: %d" % n_clusters_)
plt.show()


# %%
