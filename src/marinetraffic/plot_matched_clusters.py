# from mpl_toolkits.basemap import Basemap
import argparse
import cartopy.crs as ccrs
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sys

from plot import plot_cluster_locations
from match_windfarms import get_known_windfarms

if 'fivethirtyeight' in plt.style.available:
    plt.style.use('fivethirtyeight')

def define_cmdline_args() -> argparse.ArgumentParser:
    """
    define_cmdline_args -> argparse.ArgumentParser object

    Instantiates an ArgumentParser object and adds valid command line arguments to it.

        Returns:
            argparse.ArgumentParser object
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="keeps matplotlib figures open for interactive use",
    )
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
        help="csv containing matching wind farm meta information"
    )

    arg_parser.add_argument(
        "--known-windfarms",
        type=str,
        help="file containing a list of known offshore wind farms"
    )

    arg_parser.add_argument(
        "input", nargs="+", default=(None if sys.stdin.isatty() else sys.stdin)
    )

    arg_parser.add_argument("-v", "--verbose", action="store_true", help="debug flag")

    try:
        args = arg_parser.parse_args().__dict__
    except Exception as e:
        print(f"failed to parse command line arguments: {e}")
        sys.exit()
    return args


def parse_cmdline_args(args : dict) -> dict:
    """
    parse_cmdline_args(arg_parser  : argparse.ArgumentParser) -> dict:

    Parses command line arguments provided by the user using the given argparse.ArgumentParser object

        Parameters:
            arg_parser : argparse.ArgumentParser object

        Returns:
            dictionary containing all valid command line arguments
    """
    assert len(args["input"]) > 0, f"please provide at least one vessel track file"
    assert type(args["input"]) in [
        type(list()),
        type(sys.stdin),
    ], f'Not a valid input type: {type(args["input"])}'
    for infile in args['input']:
        assert os.path.isfile(infile), f"no such file: {infile}"
    if args["output_dir"]:
        assert os.path.isdir(
            args["output_dir"]
        ), f'Not a directory: {args["output_dir"]}'
    if not args["output_dir"] and not args["interactive"]:
        print(
            "please either supply an output directory or set the interactive commandline flag"
        )
        sys.exit()
    assert os.path.isfile(args['matching_windfarms']), f"not a file {args['matching_windfarms']}"
    assert os.path.isfile(args['known_windfarms']), f"not a file {args['known_windfarms']}"
    return args

def plot_matched_clusters():
    config = parse_cmdline_args(define_cmdline_args())
    matching_windfarms = pd.read_csv(config["matching_windfarms"])
    known_windfarms = get_known_windfarms(config['known_windfarms'])
    matching_windfarms.set_index('index', inplace=True)
    for windfarm_file in config["input"]:
        print(f"processing {windfarm_file}")
        windfarm_key = int(os.path.basename(windfarm_file).split("_")[0])
        if config['output_dir']:
            save_fig=os.path.join(config['output_dir'], f"{os.path.basename(windfarm_file).split('.')[0]}.png")
        else:
            save_fig = ""
        plot_cluster_locations(pd.read_csv(windfarm_file), matching_windfarms.loc[windfarm_key], known_windfarms, save_fig=save_fig)  
    if config['interactive']:
        plt.show()
    """
    for vessel_name, vessel_tracks in vessels.items():
        if config['verbose']:
            print(f'plotting {vessel_name}')
        if config["output_dir"]:
            plot_path = os.path.join(config["output_dir"], f"{vessel_name}.png")
            if config['verbose']:
                print(f"exporting figures to {plot_path}")
        else:
            plot_path = ""
        try:
            plot_vesseltracks_cartopy(vessel_tracks, vessel_name, save_fig=plot_path, verbose=config['verbose'])
        except Exception as e:
            print(f"failed to plot vessel tracks for {vessel_name}: {e}")
    if config['interactive']:
        plt.show()
    """

if __name__ == "__main__":
    plot_matched_clusters()
