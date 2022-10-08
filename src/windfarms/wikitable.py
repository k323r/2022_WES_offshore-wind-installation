from bs4 import BeautifulSoup
from lat_lon_parser import parse
import numpy as np
import pandas as pd
import requests
import sys

from mappings import (labels_map, seas_map, countries_map, status_map)

def get_table(url, verbose=False):
    response=requests.get(url)
    if response.status_code != 200:
        print(f'failed to request data: {response.status_code}')
        sys.exit()
    if verbose:
        print("retrieving data from wikipedia")
    soup = BeautifulSoup(response.text, 'html.parser')
    windfarm_table=soup.find('table',{'class':"wikitable"})
    df = pd.read_html(str(windfarm_table).replace(",", "."))
    df = pd.DataFrame(df[0])
    return df

def find_headers(df, verbose=False):
    for i, row in df.iterrows():
        if row.Meer == row.Staat:
            if verbose:
                print(f'duplicate entries: {row.Meer}')
            yield i

def convert_lat_lon(df, coord_column_name="coordinates"):
    lats = list()
    lons = list()
    for coords in df[coord_column_name]:
        lat, lon = coords.replace("\xa0", "").split(".")
        lats.append(parse(lat))
        lons.append(parse(lon))
        
    df.insert(loc=len(df.columns), value=lats, column='latitude')
    df.insert(loc=len(df.columns), value=lons, column='longitude')
    #df.insert()

def replace_parenthesis(x):
    try:
        return x.replace("(", "").replace(")", "")
    except:
        return x
    
def replace_german_float(x, verbose=False):
    xr = x.replace(",", ".")
    print(f"replaced: {x} -> {xr}")
    try:
        return float(xr)
    except:
        if verbose:
            print(f"failed to convert from german float: {x} -> {xr}.. skipping")
        return np.nan
        
def estimate_power(df):
    try:
        return round(pd.to_numeric(df.capacity) / pd.to_numeric(df.number_of_turbines), 1)
    except Exception as e:
        if verbose:
            print(f"failed to parse capacity:{e}")

def to_numeric(x, verbose=False):
    try:
        return pd.to_numeric(x)
    except Exception as e:
        if verbose:
            print(f"failed to convert to numeric: {x} skipping")
        return np.nan

def clean_table(df, verbose=False):
    if verbose:
        print("dropping intermediate header")
    df.drop(find_headers(df), inplace=True)
    if verbose:
        print("renaming headers")
    df.rename(columns=labels_map, inplace=True, errors="raise")
    if verbose:
        print("converting columns to numeric values")
    df.capacity = df.capacity.apply(to_numeric)
    df.number_of_turbines = df.number_of_turbines.apply(to_numeric)
    if verbose:
        print("mapping sea names to machine readable format")
    df.sea = df.sea.apply(lambda x: seas_map[x])
    if verbose:
        print("mapping country names to machine readable format")
    df.country = df.country.apply(lambda x: countries_map[x])
    if verbose:
        print("replacing parenthesis")
    df.commissioning = df.commissioning.apply(replace_parenthesis)
    if verbose:
        print("mapping status to machine readable format")
    df.status = df.status.apply(lambda x: status_map[x])
    if verbose:
        print("estimating turbine capacity")
    df.insert(loc=len(df.columns), value=estimate_power(df), column="turbine_capacity")
    if verbose:
        print("converting latitude/longitude to a machine readable format")
    convert_lat_lon(df)
    return df
