import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

def plot_track(vessel_track : pd.DataFrame, vessel_id : str, margin = 1, figsize=(9,9), save_fig = None):
    # create new figure, axes instances.
    fig = plt.figure(figsize=figsize)

    min_lat = vessel_track.latitude.min() - margin
    max_lat = vessel_track.latitude.max() + margin
    min_lon = vessel_track.longitude.min() - margin
    max_lon = vessel_track.longitude.max() + margin

    m = Basemap(llcrnrlon=min_lon,
                llcrnrlat=min_lat,
                urcrnrlon=max_lon,
                urcrnrlat=max_lat,
                resolution='h',
                projection='merc',
                lat_0=(max_lat - min_lat)/2,
                lon_0=(max_lon - min_lon)/2,
               )

    m.drawcoastlines()
    m.fillcontinents()
    m.drawcountries()
    m.drawstates()
    m.drawmapboundary(fill_color='#46bcec')
    m.fillcontinents(color = 'white',lake_color='#46bcec')
    # draw parallels
    m.drawparallels(np.arange(10,90,2),labels=[1,1,1,1])
    # draw meridians
    m.drawmeridians(np.arange(-180,180,2),labels=[1,1,1,1])

    lons, lats = m(vessel_track.longitude, vessel_track.latitude)

    m.scatter(lons, lats, marker = 'o', color='r', zorder=5, s=2)

    #m.plot(vessel_track.latitude, vessel_track.longitude)

    fig.tight_layout()

    if save_fig:
        plt.savefig(save_fig, dpi=300)

    plt.show()