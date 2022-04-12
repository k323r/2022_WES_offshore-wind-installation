import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from plot_mtdata import plot_track

from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from IPython.core.display import display, HTML

display(HTML("<style>.container { width:100% !important; }</style>"))

margin = 0.1
wind_farms = pd.read_csv("../../data/wind-farms/wind-farms-2.txt")
wind_farms.insert(
    loc=0,
    column="key_name",
    value=wind_farms.windfarm_name.apply(
        lambda x: x.lower().replace("&", "_").replace(" ", "_").replace("/", "_")
    ),
)
wind_farms.set_index("key_name", inplace=True)
wind_farms.construction_begin = pd.to_datetime(wind_farms.construction_begin, utc=True)
wind_farms.construction_end = pd.to_datetime(wind_farms.construction_end, utc=True)

sea_challenger = pd.read_csv(
    "../../data/marine-traffic/sanitized/219019002_sea-challenger.csv"
)
sea_challenger.epoch = pd.to_datetime(sea_challenger.epoch, utc=True)
sea_challenger.set_index("epoch", inplace=True)

sea_challenger_select = sea_challenger.loc[sea_challenger.speed == 0]

sea_challenger_select = sea_challenger_select.loc[
    # (sea_challenger_select.latitude > 0) &
    # (sea_challenger_select.latitude < 8) &
    (sea_challenger_select.latitude > 50)
    & (sea_challenger_select.latitude < 56)
]
plot_track(sea_challenger_select, wind_farms=wind_farms, figsize=(12, 6))

# create a 2D numpy array with only longitude and latitude
sea_challenger_lat_lon = np.transpose(
    np.array([sea_challenger_select.longitude, sea_challenger_select.latitude])
)

# normalize data by applying the standard scaler
scaler = StandardScaler()
X = scaler.fit_transform(sea_challenger_lat_lon)

# apply clustering algorithm
db = DBSCAN(eps=0.05, min_samples=200).fit(X)

core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

#%%

# Number of clusters in labels, ignoring noise if present.
# the number of clusters equals the number of unique labels. 
# converting labels to a set will result in a unique set of these labels
# so that the number of clusters becomes the length of the set of labels
# noise points receive the label -1, so if -1 is present in labels,
# the actual number of clusters is that of the unique set of labels -1
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))

#%%
unique_labels = set(labels)
print(f"found {len(unique_labels)} unique labels: {unique_labels}")

clusters = dict()

fig = plt.figure(figsize=(8, 4))

plt.title("Estimated number of wind farms: %d" % n_clusters_)
min_lat = sea_challenger_select.latitude.min() - margin
max_lat = sea_challenger_select.latitude.max() + margin
min_lon = sea_challenger_select.longitude.min() - margin
max_lon = sea_challenger_select.longitude.max() + margin
print(f"min_lat: {min_lat} min_lon: {min_lon} max_lat: {max_lat} max_lon: {max_lon}")

m = Basemap(
    llcrnrlon=min_lon,
    llcrnrlat=min_lat,
    urcrnrlon=max_lon,
    urcrnrlat=max_lat,
    resolution="h",
    projection="merc",
    lat_0=(max_lat - min_lat) / 2,
    lon_0=(max_lon - min_lon) / 2,
)
=======
print(f'min_lat: {min_lat} min_lon: {min_lon} max_lat: {max_lat} max_lon: {max_lon}')

m = Basemap(llcrnrlon=min_lon,
            llcrnrlat=min_lat,
            urcrnrlon=max_lon,
            urcrnrlat=max_lat,
            resolution='h',
            projection='merc',
            lat_0=(max_lat - min_lat)/2,
            lon_0=(max_lon - min_lon)/2,
            )
>>>>>>> 80de633613b81bebec25d26c38829b28588349b1

m.drawcoastlines()
m.fillcontinents()
# m.drawcountries()
m.drawstates()
<<<<<<< HEAD
m.drawmapboundary(fill_color="#46bcec")
m.fillcontinents(color="white", lake_color="#46bcec")
# draw parallels
m.drawparallels(np.arange(-90, 90, 2), labels=[1, 1, 1, 1])
# draw meridians
m.drawmeridians(np.arange(-180, 180, 2), labels=[1, 1, 1, 1])
=======
m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color = 'white',lake_color='#46bcec')
# draw parallels
m.drawparallels(np.arange(-90,90,2),labels=[1,1,1,1])
# draw meridians
m.drawmeridians(np.arange(-180,180,2),labels=[1,1,1,1])
>>>>>>> 80de633613b81bebec25d26c38829b28588349b1

# lons, lats = m(vessel_track.longitude, vessel_track.latitude)
# m.scatter(lons, lats, marker = 'o', color='tab:red', zorder=5, s=2)

colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

for label, color in zip(unique_labels, colors):

    # create a mask for the current label
    class_member_mask = labels == label

<<<<<<< HEAD
    if label == -1:  # noise data
        print("plotting noise")
        color = [0, 0, 0, 1]  # black
        xy = scaler.inverse_transform(X[class_member_mask & ~core_samples_mask])
    else:
        xy = scaler.inverse_transform(X[class_member_mask & core_samples_mask])

    print(f"found {len(xy)} data points for cluster {label}")

    # xy = X[class_member_mask & core_samples_mask]

    clusters[f"cluster_{label}"] = xy

    lons, lats = m(xy[:, 0], xy[:, 1])
    m.scatter(lons, lats, marker="o", color=tuple(color), zorder=5, s=5)
=======
    if label == -1:
        print('plotting noise')
        color = [0, 0, 0, 1]
        xy = scaler.inverse_transform(X[class_member_mask & ~ core_samples_mask])
    else:
        xy = scaler.inverse_transform(X[class_member_mask &  core_samples_mask])

    print(f'found {len(xy)} data points for cluster {label}')

    # xy = X[class_member_mask & core_samples_mask]
    
    clusters[f'cluster_{label}'] = xy

    lons, lats = m(xy[:, 0], xy[:,1])
    m.scatter(lons, lats, marker = 'o', color=tuple(color), zorder=5, s=5)
>>>>>>> 80de633613b81bebec25d26c38829b28588349b1

plt.tight_layout()
plt.show()

# %%
