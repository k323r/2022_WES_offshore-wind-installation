import pandas as pd
from global_land_mask import globe

def read_vesseltracks_file(vesseltracks_fpath: str) -> pd.DataFrame:
    """
    read_vesseltracks_file

    input:
        vesseltracks_fpath: file path to a csv file containing vessel tracks.

    returns:
        pandas DataFrame containing the sanitized vessel track
    """
    vesseltracks = pd.read_csv(vesseltracks_fpath)
    vesseltracks.timestamp = pd.to_datetime(vesseltracks.epoch, utc=True, unit='s')
    vesseltracks.set_index("timestamp", inplace=True)
    return vesseltracks

def extract_stationary_vesseltracks(
    vesseltracks: pd.DataFrame,
    lat_min : float = -70,
    lat_max : float = 70,
    lon_min : float = -179.9,
    lon_max : float = 179.9,
    speed_threshold : float =0,
) -> pd.DataFrame:
    if vesseltracks.empty:
        print(f"empty data frame, skipping!")
        return pd.DataFrame()
    vesseltracks = vesseltracks.loc[vesseltracks.speed == speed_threshold]
    vesseltracks = vesseltracks.loc[
        (vesseltracks.latitude > lat_min)
        & (vesseltracks.latitude < lat_max)
        & (vesseltracks.longitude > lon_min)
        & (vesseltracks.longitude < lon_max)
    ]
    # remove data points on land (port)
    vesseltracks = vesseltracks[globe.is_ocean(vesseltracks.latitude, vesseltracks.longitude)]
    return vesseltracks
