import argparse
from glob import glob
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from plot import plot_durations, plot_gantt

from times import get_installation_times

def printv(message, end="\n"):
    global config
    if config["verbose"]:
        print(message, end=end)

def parse_cmdline_args() -> dict:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "input",
        nargs="+",
        default=[],
        help="input csv files for each matching wind farm",
    )
    arg_parser.add_argument(
        "--output-dir",
        default=None,
        type=str,
        help="output directory to store sanitized installations to",
    )
    arg_parser.add_argument(
        "--max-distance-centroid-sigma",
        default=0,
        type=float,
        help="maximum allowable distance of turbine location from cluster centroid. calculated as max_distance = mean_distance + distance_centroid_sigma * standard_deviation(distances)",
    )
    arg_parser.add_argument(
        "--max-duration",
        default=0,
        type=float,
        help="maximum allowed duration at single turbine location, defaults to 30 days.",
    )
    arg_parser.add_argument(
        "--plot-durations",
        default=False,
        action="store_true",
    )
    arg_parser.add_argument(
        "--plot-gantt",
        default=False,
        action="store_true",
    )
    arg_parser.add_argument(
        "--verbose",
        default=False,
        help="verbose output, useful for debugging",
        action="store_true",
    )
    arg_parser.add_argument(
        "--interactive",
        action="store_true",
        help="keep generated figures open"
    )
    arg_parser.add_argument(
        "--installations-whitelist",
        type=str,
        default="",
        help="whitelist of installations to sanitize"
    )
    args = arg_parser.parse_args().__dict__
    assert os.path.isdir(args["output_dir"]), f'not a directory: {args["output_dir"]}'
    assert len(args["input"]) > 0, "please provide at least one input file"
    for ffile in args["input"]:
        assert os.path.isfile(ffile), f"no such file: {ffile}"
    assert (
        args["max_distance_centroid_sigma"] >= 0
    ), f"--max-distance-centroid-sigma must be greater than 0"
    assert args["max_duration"] >= 0, f"--max-duration must be > 0"
    return args

def get_matching_windfarm(fpath: str):
    df = pd.read_csv(fpath)
    df.set_index("index", inplace=True)
    df.begin = pd.to_datetime(df.begin)
    df.end = pd.to_datetime(df.end)
    df.duration = pd.to_timedelta(df.duration)
    df.duration = df.duration.apply(lambda x: x.total_seconds() / 3600)
    df.sort_values("begin", inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.index.name="index"
    # df.reindex(inplace=True)
    return df

def get_whitelist(fpath : str) -> pd.DataFrame:
    df = pd.read_excel(fpath, engine="odf")
    return df


if __name__ == "__main__":
    config = parse_cmdline_args()
    printv("commandline configuration:")
    printv(f"{json.dumps(config, indent=4)}")
    printv("parsing installations whitelist")
    whitelist = get_whitelist(config["installations_whitelist"])
    for matching_windfarm_file in config["input"]:
        print(matching_windfarm_file)
        windfarm = get_matching_windfarm(matching_windfarm_file)
        windfarm_key = f"{os.path.basename(matching_windfarm_file).split('.')[0]}"
        windfarm_name = windfarm_key.split("_")[1]
        if whitelist[whitelist.windfarm_name == windfarm_name].include.any():
            printv(f"in whitelist: {windfarm_name}")
        else:
            printv(f"skipping {windfarm_name} due to whitelist")
            continue
        #    if whitelist[whitelist.windfarm_name == 
        printv(f"processing {windfarm_key}")
        n_locations = len(windfarm)
        if config["max_duration"]:
            max_duration = config["max_duration"] * 24
            printv(f"max. allowed duration: {max_duration}", end=" ")
            windfarm = windfarm[windfarm.duration < max_duration]
            printv(f"removed {n_locations - len(windfarm)} due to duration restriction")
            n_locations = len(windfarm)
        if config["max_distance_centroid_sigma"]:
            max_location_distance = windfarm.distance_centroid.mean() + (config["max_distance_centroid_sigma"]*windfarm.distance_centroid.std())
            printv(f"max location distance: {max_location_distance}", end=" ")
            windfarm = windfarm[windfarm.distance_centroid < max_location_distance ]
            printv(
                f"removed {n_locations - len(windfarm)} due to distance to centroid restriction"
            )
            n_locations = len(windfarm)
        if n_locations == 0:
            print(f"no suitable turbine locations availabel")
            continue
        output_fname = f"{windfarm_key}_sanitized.csv"
        windfarm.to_csv(os.path.join(config["output_dir"], output_fname))
        if config["plot_durations"]:
            plot_durations(
                windfarm,
                title=windfarm_key,
                save_fig=os.path.join(config["output_dir"], f"{windfarm_key}_sanitized_durations.png")
            )
        if config["plot_gantt"]:
            plot_gantt(
                windfarm,
                title=windfarm_key,
                save_fig=os.path.join(config["output_dir"], f"{windfarm_key}_sanitized_gantt.png")
            )
    if config["interactive"]:
        plt.show()
