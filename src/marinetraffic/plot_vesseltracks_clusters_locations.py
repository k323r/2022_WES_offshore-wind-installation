# from mpl_toolkits.basemap import Basemap
import argparse
import cartopy.crs as ccrs
import folium
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sys
import webbrowser

sys.path.append("./src")
if not os.path.isdir(sys.path[-1]):
    print(f"cwd: {os.path.abspath(os.path.curdir)}")
    print(f"not a directory: {sys.path[-1]}")

from marinetraffic.vesseltracks import read_vesseltracks_file
from marinetraffic.plot import get_bounding_box_latlon


def printv(message: str):
    global config
    if config["verbose"]:
        print(message)


def define_cmdline_args() -> argparse.ArgumentParser:
    """
    define_cmdline_args -> argparse.ArgumentParser object

    Instantiates an ArgumentParser object and adds valid command line arguments to it.

        Returns:
            argparse.ArgumentParser object
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="",
        help="If provided, figure will be saved to this directory. Default is None",
    )
    arg_parser.add_argument(
        "--matching-windfarms",
        type=str,
        default="",
        help="csv containing matching wind farm meta information",
    )
    arg_parser.add_argument(
        "--known-windfarms",
        type=str,
        default="",
        help="file containing a list of known offshore wind farms",
    )
    arg_parser.add_argument(
        "--vesseltracks", type=str, help="path to raw vessel tracks"
    )
    arg_parser.add_argument(
        "--windfarm-locations",
        default=[],
        nargs="+",
        help="windfarm location csv files",
    )
    arg_parser.add_argument(
        "--interactive",
        action="store_true",
        help="if set, an interactive map will be opened in a browser"
    )
    arg_parser.add_argument("-v", "--verbose", action="store_true", help="debug flag")
    try:
        args = arg_parser.parse_args().__dict__
    except Exception as e:
        print(f"failed to parse command line arguments: {e}")
        sys.exit()
    return args


def parse_cmdline_args(args: dict) -> dict:
    """
    parse_cmdline_args(arg_parser  : argparse.ArgumentParser) -> dict:

    Parses command line arguments provided by the user using the given argparse.ArgumentParser object

        Parameters:
            arg_parser : argparse.ArgumentParser object

        Returns:
            dictionary containing all valid command line arguments
    """

    def assert_filepaths(filepaths: list):
        for infile in filepaths:
            assert os.path.isfile(infile), f"no such file or directory: {infile}"

    assert os.path.isfile(args["vesseltracks"]), f"no such file: {args['vesseltracks']}"
    assert (
        len(args["windfarm_locations"]) > 0
    ), f"please provide at least one location file"
    assert_filepaths(args["windfarm_locations"])
    assert os.path.isfile(
        args["matching_windfarms"]
    ), f"not a file {args['matching_windfarms']}"
    assert os.path.isfile(
        args["known_windfarms"]
    ), f"not a file {args['known_windfarms']}"
    assert os.path.isdir(args["output_dir"]), f"not a directory: {args['output_dir']}"
    return args

def get_known_windfarms(fpath: str) -> pd.DataFrame:
    known_windfarms = pd.read_excel(fpath, engine="odf")
    known_windfarms.set_index("index", inplace=True)
    known_windfarms.turbine_installation_vessel = (
        known_windfarms.turbine_installation_vessel.apply(
            lambda x: [i.lower().lstrip().replace(" ", "-") for i in str(x).split(",")]
        )
    )
    return known_windfarms




def plot_vesseltracks_clusters_locations(config):
    matching_windfarms = pd.read_csv(config["matching_windfarms"])
    known_windfarms = get_known_windfarms(config["known_windfarms"])
    matching_windfarms.set_index("index", inplace=True)
    vesseltracks = read_vesseltracks_file(config["vesseltracks"])
    locations = dict()
    for windfarm_location_fpath in config["windfarm_locations"]:
        windfarm_location_key = os.path.basename(windfarm_location_fpath).split(".")[0]
        windfarm_key = int(windfarm_location_key.split("_")[0])
        locations[windfarm_key] = pd.read_csv(windfarm_location_fpath)

    min_lat, max_lat, min_lon, max_lon = get_bounding_box_latlon(
        vesseltracks, margin=0.1
    )
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # add vesseltracks
    folium.PolyLine(
        locations=vesseltracks[["latitude", "longitude"]].to_numpy(),
        color="#7e7e7e",
        weight=1,
        opacity=0.5,
    ).add_to(m)

    # add windfarm marker
    for windfarm_key, windfarm_location in locations.items():
        folium.CircleMarker(
            location=(windfarm_location.latitude.mean(), windfarm_location.longitude.mean()),
            popup=f"{matching_windfarms.iloc[windfarm_key].windfarm_name}",
            tooltip=f"{matching_windfarms.iloc[windfarm_key].windfarm_name}",
            radius=10,
            color="#00aa00"
        ).add_to(m)
        for location in windfarm_location.itertuples():
            folium.Circle(
                location=(location.latitude, location.longitude),
                popup=location.location_key,
                tooltip=location.location_key,
                radius=100,
                color='#ff0000'
            ).add_to(m)
    m.fit_bounds(bounds=[[min_lat, min_lon], [max_lat, max_lon]])
    output_fpath = os.path.join(config["output_dir"], f"{os.path.basename(config['vesseltracks']).split('.')[0]}.html")
    m.save(output_fpath)
    if config["interactive"]:
        webbrowser.open(output_fpath, new=2)


if __name__ == "__main__":
    config = parse_cmdline_args(define_cmdline_args())
    plot_vesseltracks_clusters_locations(config)
