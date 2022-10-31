#!/bin/env python
import argparse
import glob
from haversine import haversine, Unit
from itertools import combinations
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sys

sys.path.append("src")
from marinetraffic.vesseltracks import read_vesseltracks_file

def printv(message: str):
    global config
    if config["verbose"]:
        print(message)

def parse_cmdline_args() -> dict:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--known-windfarms",
        help="ods file containing a list of knonw offshore wind farms",
    )
    arg_parser.add_argument(
        "--cluster-dir",
        help="directory containing the clustered vessel tracks",
    )
    arg_parser.add_argument(
        "--match-tolerance",
        default=0.075,
        type=float,
        help="tolerance in degrees for matching known wind farm locations with clustered vessel tracks",
    )
    arg_parser.add_argument(
        "--output-dir",
        default=".",
        type=str,
        help="default output directory for the extracted cluster",
    )
    arg_parser.add_argument(
        "--output-prefix",
        default="",
        type=str,
        help="string prefixed to exported csv files",
    )
    arg_parser.add_argument(
        "--cluster-name",
        default="cluster",
        type=str,
        help="Pattern to name clusters. Defaults to 'cluster'",
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
        "--min-duration",
        default=0,
        type=float,
        help="minimum allowed duration at single turbine location, defaults to 0.5 days.",
    )

    arg_parser.add_argument("--verbose", action="store_true", help="debugging info")
    args = arg_parser.parse_args().__dict__
    assert os.path.isfile(
        args["known_windfarms"]
    ), f'not a file: {args["known_windfarms"]}'
    assert args["match_tolerance"] > 0, f"match tolerance must be a positive float"
    assert os.path.isdir(args["cluster_dir"]), f"not a directory: {args['cluster_dir']}"
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


def get_cluster_coord(basedir, min_locations=6, verbose=False):
    for vesseldir in glob.glob(os.path.join(basedir, "*")):
        vesselkey = os.path.basename(vesseldir)
        for clusterdir in glob.glob(os.path.join(vesseldir, "cluster-*")):
            clustername = os.path.basename(clusterdir)
            if (
                n_locations := len(
                    glob.glob(os.path.join(clusterdir, "*location-*.csv"))
                )
            ) < 6:
                if verbose:
                    print(
                        f"only {n_locations} single locations available at {clusterdir}, skipping"
                    )
                continue
            if os.path.isfile(
                cluster_fpath := os.path.join(
                    clusterdir, f"{vesselkey}_{clustername}.csv"
                )
            ):
                cluster = read_vesseltracks_file(cluster_fpath)
                lat_mean = cluster.latitude.mean()
                lon_mean = cluster.longitude.mean()
                begin = cluster.index[0]
                end = cluster.index[-1]
                yield (vesselkey, clustername, lat_mean, lon_mean, begin, end, cluster_fpath)

def match_cluster_windfarm(
    clustered_vesseltracks_dir,
    windfarms,
    bound=0.08,
    verbose=False,
):
    match_n = 1
    for (
        vesselkey,
        clustername,
        cluster_lat,
        cluster_lon,
        cluster_begin,
        cluster_end,
        cluster_fpath,
    ) in get_cluster_coord(clustered_vesseltracks_dir, verbose=verbose):
        vesselname = "-".join(vesselkey.split("-")[1:])
        for windfarm in windfarms.itertuples():
            lat_lower = windfarm.latitude - bound
            lat_upper = windfarm.latitude + bound
            lon_lower = windfarm.longitude - bound
            lon_upper = windfarm.longitude + bound
            if (
                lat_lower < cluster_lat < lat_upper
                and lon_lower < cluster_lon < lon_upper
                and vesselname in windfarm.turbine_installation_vessel
            ):
                if verbose:
                    print(
                        f"found possible match {match_n}: {windfarm.Index} {windfarm.name}: {vesselkey}/{clustername}",
                        end=" ",
                    )
                    print(
                        f"vessel match: {vesselname} -> {windfarm.turbine_installation_vessel}"
                    )
                match_n += 1
                # build path to cluster
                yield (
                    windfarm.Index,
                    windfarm.name,
                    vesselkey,
                    clustername,
                    cluster_lat,
                    cluster_lon,
                    cluster_begin,
                    cluster_end,
                    cluster_fpath,
                )

def get_location_means(cluster_dir, location_pattern="*location-*.csv"):
    for location_fpath in sorted(
        glob.glob(os.path.join(cluster_dir, location_pattern))
    ):
        location_key = os.path.basename(location_fpath).split(".")[0]
        tmp = read_vesseltracks_file(location_fpath)
        # locations[location_key] = {"lat_mean" : tmp.latitude.mean(), "lon_mean" : tmp.longitude.mean(), "start" : tmp.index[0], "end" : tmp.index[-1], "duration" : (tmp.index[-1] - tmp.index[0])}
        yield (
            location_key,
            tmp.latitude.mean(),
            tmp.longitude.mean(),
            tmp.index[0],
            tmp.index[-1],
            (tmp.index[-1] - tmp.index[0]).total_seconds()/3600,
        )


def get_matching_windfarms(
    cluster_dir,
    known_windfarms,
    bound=0.05,
    verbose=True,
    columns=[
        "known_windfarms_index",
        "windfarm_name",
        "vessel_name",
        "cluster_name",
        "latitude",
        "longitude",
        "begin",
        "end",
        "cluster_fpath",
    ],
):
    matching_windfarms = pd.DataFrame(
        data=match_cluster_windfarm(
            cluster_dir, known_windfarms, verbose=verbose, bound=bound
        ),
        columns=columns,
    )
    # matching_windfarms.set_index("known_windfarms_index", inplace=True)
    matching_windfarms.index.name = "index"
    return matching_windfarms

def calc_distances_centroid(locations, centroid):
    distances = list()
    for _, loc in locations.iterrows():
        distances.append(
            haversine((loc.latitude, loc.longitude), centroid, Unit.METERS)
        )
    return distances

def get_windfarms_turbines(
    matching_windfarms, 
    columns=[
                "location_key",
                "latitude",
                "longitude",
                "begin",
                "end",
                "duration",
            ],):
    for matching_windfarm in matching_windfarms.itertuples():
        printv(f"{matching_windfarm.Index}, {matching_windfarm.windfarm_name}, {matching_windfarm.cluster_fpath}")
        windfarm_turbines = pd.DataFrame(
            data=get_location_means(os.path.dirname(matching_windfarm.cluster_fpath)),
            columns=columns,
        )
        windfarm_turbines.insert(
            value=calc_distances_centroid(
                windfarm_turbines,
                (matching_windfarm.latitude, matching_windfarm.longitude),
            ),
            column="distance_centroid",
            loc=len(windfarm_turbines.columns),
        )
        windfarm_turbines.index.name = 'index'
        yield (matching_windfarm.Index, windfarm_turbines)

if __name__ == "__main__":
    config = parse_cmdline_args()
    printv("command line configuration")
    printv(f"{json.dumps(config, indent=4)}")
    printv(f"reading in known wind farms file {config['known_windfarms']}")
    known_windfarms = get_known_windfarms(config["known_windfarms"])
    printv("matching known windfarms with vessel clusters")
    matching_windfarms = get_matching_windfarms(
        config["cluster_dir"],
        known_windfarms=known_windfarms,
        bound=config["match_tolerance"],
        verbose=config["verbose"],
    )
    for windfarm_key, windfarm in get_windfarms_turbines(matching_windfarms):
        vessel_name = matching_windfarms.loc[windfarm_key].vessel_name
        cluster_name = matching_windfarms.loc[windfarm_key].cluster_name.replace("_", "-")
        windfarm_name = matching_windfarms.loc[windfarm_key].windfarm_name.replace("/", "-")
        windfarm_name = "-".join(windfarm_name.split()).lower()
        printv(f"processing {windfarm_key}")
        n_locations = len(windfarm)
        if config["max_duration"]:
            max_duration = config["max_duration"] * 24
            windfarm = windfarm[windfarm.duration < max_duration]
            printv(f"removed {n_locations - len(windfarm)} due to maximum duration restriction")
            n_locations = len(windfarm)
        if config["min_duration"]:
            min_duration = config["min_duration"] * 24
            windfarm = windfarm[windfarm.duration > min_duration]
            printv(f"removed {n_locations - len(windfarm)} due to minimum duration restriction")
            n_locations = len(windfarm)
        if config["max_distance_centroid_sigma"]:
            max_location_distance = windfarm.distance_centroid.mean() + (config["max_distance_centroid_sigma"]*windfarm.distance_centroid.std())
            windfarm = windfarm[windfarm.distance_centroid < max_location_distance ]
            printv(
                f"removed {n_locations - len(windfarm)} due to distance to centroid restriction"
            )
            n_locations = len(windfarm)
        if n_locations == 0:
            print(f"no suitable turbine locations availabel")
            continue
        output_fname = f"{windfarm_key}_{windfarm_name}_{vessel_name}_{cluster_name}.csv"
        output_fpath = os.path.join(config['output_dir'], output_fname)
        printv(f"exporting identified wind farm to: {output_fpath}")
        windfarm.to_csv(output_fpath)
    matching_windfarms_fpath = os.path.join(config['output_dir'], "matching_windfarms.csv")
    printv(f"exporting matching windfarms to {matching_windfarms_fpath}")
    matching_windfarms.to_csv(os.path.join(config['output_dir'], "matching_windfarms.csv"))
