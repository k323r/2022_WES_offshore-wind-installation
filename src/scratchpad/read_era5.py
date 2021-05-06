import cfgrib
import xarray
from os import path

datafile = '../../data/era5/twbii/twbii_era5.grib'

with xarray.open_dataset(datafile, engine='cfgrib') as ds:
    
    # convert to pandas dataframe
    df = ds.to_dataframe()

    # describe the data
    print(df.describe())
