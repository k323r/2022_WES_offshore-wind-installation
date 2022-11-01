import argparse
from bs4 import BeautifulSoup
from lat_lon_parser import parse
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import requests
import sys

from plot import plot_windfarms_cartopy
from wikitable import (get_table, clean_table)

if 'fivethirtyeight' in plt.style.available:
    plt.style.use('fivethirtyeight')

URL_de = "https://de.wikipedia.org/wiki/Liste_der_Offshore-Windparks"
URL_en = "https://en.wikipedia.org/wiki/List_of_offshore_wind_farms"

def parse_args()-> dict:
    argp = argparse.ArgumentParser()
    argp.add_argument('-o', '--output-dir', default=".", help="output dir for csv and plots")
    argp.add_argument('-p', '--plot', action="store_true", help="flag to plot wind farm data")
    argp.add_argument('-i', '--interactive', action="store_true", help="flag to keep plots open as interactive plots")
    argp.add_argument('-v', '--verbose', action="store_true", help="verbose flag")
    config = argp.parse_args().__dict__
    assert os.path.isdir(config['output_dir']), f"no such file or directory: {config['output_dir']}"
    assert not (config['interactive'] and not config['plot']), f"please provide the --plot switch with the --interactive switch"
    return config

def get_windfarms_wikipedia(URL):
    return data

if __name__ == "__main__":
    config = parse_args()
    data = clean_table(get_table(URL_de, verbose=config["verbose"]), verbose=config["verbose"])
    data.index.name = 'index'
    if config['plot']:
        output_fpath_png = os.path.join(config["output_dir"], "windfarms.png")
        plot_windfarms_cartopy(data, save_fig=output_fpath_png, verbose=config["verbose"])
        if config['interactive']:
            plt.show()
    output_fpath_csv = os.path.join(config["output_dir"], "windfarms.csv")
    data.to_csv(output_fpath_csv)


