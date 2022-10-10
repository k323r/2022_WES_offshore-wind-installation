# from mpl_toolkits.basemap import Basemap
import argparse
import cartopy.crs as ccrs
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sys

from plot import plot_vesseltracks_cartopy

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
        "input", nargs="+", default=(None if sys.stdin.isatty() else sys.stdin)
    )

    arg_parser.add_argument("-v", "--verbose", action="store_true", help="debug flag")

    return arg_parser


def parse_cmdline_args(arg_parser: argparse.ArgumentParser) -> dict:
    """
    parse_cmdline_args(arg_parser  : argparse.ArgumentParser) -> dict:

    Parses command line arguments provided by the user using the given argparse.ArgumentParser object

        Parameters:
            arg_parser : argparse.ArgumentParser object

        Returns:
            dictionary containing all valid command line arguments
    """
    try:
        args = arg_parser.parse_args().__dict__
    except Exception as e:
        print(f"failed to parse command line arguments: {e}")
        sys.exit()
    assert len(args["input"]) > 0, f"please provide at least one vessel track file"
    assert type(args["input"]) in [
        type(list()),
        type(sys.stdin),
    ], f'Not a valid input type: {type(args["input"])}'
    if args["output_dir"]:
        assert os.path.isdir(
            args["output_dir"]
        ), f'Not a directory: {args["output_dir"]}'
    if not args["output_dir"] and not args["interactive"]:
        print(
            "please either supply an output directory or set the interactive commandline flag"
        )
        sys.exit()
    return args

def plot_vesseltracks():

    config = parse_cmdline_args(define_cmdline_args())
    vessels = dict()

    for v_file in config["input"]:
        print(f"processing {v_file}")
        vessel = ".".join(os.path.basename(v_file).split(".")[:-1])
        vessels[vessel] = pd.read_csv(v_file)
        vessels[vessel].epoch = pd.to_datetime(vessels[vessel].epoch, unit="s", utc=True)
        vessels[vessel].set_index("epoch", inplace=True)

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

if __name__ == "__main__":
    plot_vesseltracks()
