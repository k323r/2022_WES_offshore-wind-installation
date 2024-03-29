import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
import cartopy
import numpy as np
import pandas as pd

def get_bounding_box_latlon(track: pd.DataFrame, margin: float = 1.0, verbose=False):
    min_lat = track.latitude.min() - margin
    max_lat = track.latitude.max() + margin
    min_lon = track.longitude.min() - margin
    max_lon = track.longitude.max() + margin
    if verbose:
        print(
            f"min_lat: {min_lat} min_lon: {min_lon} max_lat: {max_lat} max_lon: {max_lon}"
        )
    return (min_lat, max_lat, min_lon, max_lon)

def plot_cluster_locations(
    locations: pd.DataFrame,
    windfarm,
    known_windfarms,
    title : str = "",
    label : str = "",
    margin : float = 0.025,
    figsize : tuple =(9, 9),
    save_fig="",
    verbose=False,
    transparent=True,
    show_fig=False,
):
    figure = plt.figure(figsize=figsize)
    if transparent:
        figure.patch.set_alpha(0)
    min_lat = locations.latitude.min() - margin
    max_lat = locations.latitude.max() + margin
    min_lon = locations.longitude.min() - margin
    max_lon = locations.longitude.max() + margin
    if verbose:
        print(
            f"min_lat: {min_lat} min_lon: {min_lon} max_lat: {max_lat} max_lon: {max_lon}"
        )
    ax = figure.add_subplot(1,1,1, projection=cartopy.crs.Mercator())
    ax.set_extent([min_lon, max_lon, min_lat, max_lat])
    ax.add_feature(cartopy.feature.BORDERS)
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    ax.coastlines(resolution='10m')
    for _, loc in locations.iterrows():
        plt.scatter(loc.longitude, loc.latitude, transform=cartopy.crs.PlateCarree())
        plt.text(loc.longitude + 0.002, loc.latitude, f"{loc.location_key.split('_')[-1]}", zorder=7, transform=cartopy.crs.PlateCarree())
    plt.scatter(windfarm.longitude, windfarm.latitude, color='tab:red', transform=cartopy.crs.PlateCarree(), label="Cluster centroid", s=75)
    plt.scatter(known_windfarms.loc[windfarm.known_windfarms_index].longitude, known_windfarms.loc[windfarm.known_windfarms_index].latitude, color='tab:green', transform=cartopy.crs.PlateCarree(), label=f"Official location {windfarm.windfarm_name}", s=75)
    # plt.scatter(vessel_tracks.longitude.mean(), vessel_tracks.latitude.mean(), transform=cartopy.crs.PlateCarree(), label="vessel tracks centroid", color='tab:green')
    plt.legend()
    if title:
        plt.title(title)
    plt.tight_layout()
    if save_fig:
        plt.savefig(save_fig, dpi=300)
    if show_fig:
        plt.show()

def plot_vesseltracks_cartopy(
    vessel_tracks: pd.DataFrame,
    vessel_name : str = "", 
    ex_figure = None,
    margin : float = 0.1,
    figsize : tuple =(16, 9),
    save_fig="",
    verbose=False,
    transparent=True,
    new_fig = True,
):
    if not ex_figure:
        figure = plt.figure(figsize=figsize)
    else:
        figure = ex_figure
    if transparent:
        figure.patch.set_alpha(0)
    min_lat = vessel_tracks.latitude.min() - margin
    max_lat = vessel_tracks.latitude.max() + margin
    min_lon = vessel_tracks.longitude.min() - margin
    max_lon = vessel_tracks.longitude.max() + margin
    if verbose:
        print(
            f"min_lat: {min_lat} min_lon: {min_lon} max_lat: {max_lat} max_lon: {max_lon}"
        )
    ax = figure.add_subplot(1,1,1, projection=cartopy.crs.Mercator())
    ax.set_extent([min_lon, max_lon, min_lat, max_lat])
    ax.add_feature(cartopy.feature.BORDERS)
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    ax.coastlines(resolution='10m')
    plt.scatter(vessel_tracks['longitude'], vessel_tracks['latitude'], transform=cartopy.crs.PlateCarree())
    if vessel_name:
        plt.title(vessel_name)
    plt.tight_layout()
    if save_fig:
        plt.savefig(save_fig, dpi=300)
    #plt.show()

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
