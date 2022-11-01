import cartopy
import matplotlib.pyplot as plt
import pandas as pd
import sys

def plot_windfarms_cartopy(
    data: pd.DataFrame,
    label = "",
    color = "",
    fig = None,
    axis = None,
    margin : float = 1.0,
    figsize : tuple =(16, 9),
    save_fig="",
    verbose=False,
    transparent=True,
):

    if label:
        l = label
    else:
        l = ""
    if fig and not axis:
        print(f"please provide both figure and axis objects")
        sys.exit()
    if fig:
        figure = fig
    else:
        figure = plt.figure(figsize=figsize)
    if transparent:
        figure.patch.set_alpha(0)
    min_lat = data.latitude.min() - margin
    max_lat = data.latitude.max() + margin
    min_lon = data.longitude.min() - margin
    max_lon = data.longitude.max() + margin
    if verbose:
        print(
            f"min_lat: {min_lat} min_lon: {min_lon} max_lat: {max_lat} max_lon: {max_lon}"
        )
    if axis:
        ax = axis
    else:
        ax = figure.add_subplot(1,1,1, projection=cartopy.crs.Mercator())
    ax.set_extent([min_lon, max_lon, min_lat, max_lat])
    ax.add_feature(cartopy.feature.BORDERS)
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    ax.coastlines(resolution='10m')
    plt.scatter(data['longitude'], data['latitude'], transform=cartopy.crs.PlateCarree(), label=l)
    if label:
        plt.legend()
    plt.tight_layout()
    if save_fig:
        if verbose:
            print(f"exporting figure as {save_fig}")
        plt.savefig(save_fig, dpi=300)
    #plt.show()
    return figure
