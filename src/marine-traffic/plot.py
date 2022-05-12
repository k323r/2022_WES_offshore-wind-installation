import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd


def plot_vesseltracks(
    vesseltracks: pd.DataFrame,
    margin=1,
    figsize=(9, 9),
    save_fig=None,
    verbose=False,
    transparent=True,
    show_fig=False,
):
    # create new figure, axes instances.
    fig = plt.figure(figsize=figsize)
    if transparent:
        fig.patch.set_alpha(0)
    min_lat = vesseltracks.latitude.min() - margin
    max_lat = vesseltracks.latitude.max() + margin
    min_lon = vesseltracks.longitude.min() - margin
    max_lon = vesseltracks.longitude.max() + margin
    if verbose:
        print(
            f"min_lat: {min_lat} min_lon: {min_lon} max_lat: {max_lat} max_lon: {max_lon}"
        )
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

    m.drawcoastlines()
    m.fillcontinents()
    # m.drawcountries()
    # m.drawstates()
    m.drawmapboundary(fill_color="#46bcec")
    m.fillcontinents(color="white", lake_color="#46bcec")
    m.drawparallels(np.arange(-90, 90, 2), labels=[1, 1, 1, 1])
    m.drawmeridians(np.arange(-180, 180, 2), labels=[1, 1, 1, 1])
    lons, lats = m(vesseltracks.longitude, vesseltracks.latitude)
    m.scatter(lons, lats, marker="o", color="tab:red", zorder=5, s=2)
    fig.tight_layout()
    if save_fig:
        plt.savefig(save_fig, dpi=300)
    if show_fig:
        plt.show(block=False)


def plot_clusters(
    clusters,
    raw_data,
    figsize=(9, 9),
    save_fig=None,
    show_fig=True,
    margin=1,
    legend=True,
    title=None,
    annotate_clusters=False,
    verbose=False,
):
    fig = plt.figure(figsize=figsize)
    min_lat = raw_data.latitude.min() - margin
    max_lat = raw_data.latitude.max() + margin
    min_lon = raw_data.longitude.min() - margin
    max_lon = raw_data.longitude.max() + margin
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
    m.drawcoastlines()
    m.fillcontinents()
    m.drawmapboundary(fill_color="#46bcec")
    m.fillcontinents(color="white", lake_color="#46bcec")
    m.drawparallels(np.arange(-90, 90, 2), labels=[1, 1, 1, 1])
    m.drawmeridians(np.arange(-180, 180, 2), labels=[1, 1, 1, 1])
    m.scatter(
        *m(raw_data.longitude, raw_data.latitude),
        marker="s",
        color="grey",
        zorder=3,
        #alpha=0.5,
        s=40,
        label="raw data",
    )
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(clusters))]
    for (label, cluster), color in zip(clusters.items(), colors):
        lons, lats = m(cluster.longitude, cluster.latitude)
        m.scatter(
            lons, lats, marker="o", zorder=5, s=20, color=color, label=f"cluster_{label+1}"
        )
        # annotate('0', xy=(x, y), xycoords='data', xytext=(x, y), textcoords='data')
        plt.text(np.mean(lons) + 0.2, np.mean(lats) + 0.2, f'{label+1}', zorder=7)
    if legend:
        plt.legend(loc="upper right")
    if title:
        plt.title(title)
    fig.tight_layout()
    if save_fig:
        if verbose:
            print(f'saving figure to {save_fig}')
        plt.savefig(save_fig, dpi=300)
    if show_fig:
        plt.show(block=False)


def plot_cluster_windfarms(
    cluster: pd.DataFrame,
    windfarms,
    figsize=(9, 9),
    save_fig=None,
    show_fig=True,
    margin=1,
):
    fig = plt.figure(figsize=figsize)
    min_lat = cluster.latitude.min() - margin
    max_lat = cluster.latitude.max() + margin
    min_lon = cluster.longitude.min() - margin
    max_lon = cluster.longitude.max() + margin
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
    m.drawcoastlines()
    m.fillcontinents()
    m.drawmapboundary(fill_color="#46bcec")
    m.fillcontinents(color="white", lake_color="#46bcec")
    m.drawparallels(np.arange(-90, 90, 2), labels=[1, 1, 1, 1])
    m.drawmeridians(np.arange(-180, 180, 2), labels=[1, 1, 1, 1])
    m.scatter(
        *m(cluster.longitude, cluster.latitude),
        marker="s",
        color="tab:red",
        zorder=3,
        s=40,
        label="cluster",
    )
    for windfarm in windfarms.itertuples():
        m.scatter(
            *m(windfarm.longitude, windfarm.latitude),
            marker="s",
            color="c",
            zorder=5,
            s=75,
            label=windfarm.windfarm_name,
        )
    plt.legend(loc="upper right")
    fig.tight_layout()
    if save_fig:
        plt.savefig(save_fig, dpi=300)
    if show_fig:
        plt.show(block=False)
