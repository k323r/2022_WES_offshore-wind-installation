#!/bin/env python
import argparse
import json
import os
import sys

from clustering import (
    normalize_lat_lon,
    find_clusters,
    extract_clusters,
    export_cluster,
)
from vesseltracks import read_vesseltracks_file, extract_stationary_vesseltracks
from windfarms import read_windfarms_file, match_windfarms_cluster


def printv(message: str):
    global config
    if config["verbose"]:
        print(message)


def parse_cmdline_args() -> dict:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--vesseltracks",
        default="",
        help="csv file containing the tracks of an installation vessel.",
    )
    arg_parser.add_argument(
        "--dbscan-drop-noise",
        default=False,
        action="store_true",
        help="flag to drop noise during clustering",
    )
    arg_parser.add_argument(
        "--dbscan-epsilon",
        default=0.05,
        type=float,
        help="distance parameter to be used to identify clusters",
    )
    arg_parser.add_argument(
        "--dbscan-num-samples",
        default=200,
        type=int,
        help="minimum number of samples per cluster",
    )
    arg_parser.add_argument(
        "--dbscan-num-processors",
        default=4,
        type=int,
        help="number of processors to use when extracting clusters",
    )
    arg_parser.add_argument(
        "--latitude-min",
        default=-89,
        type=float,
        help="mimium latitude to be used in analysis. Default is -90 (south pole)",
    )
    arg_parser.add_argument(
        "--latitude-max",
        default=89,
        type=float,
        help="maximum latitude to be used in analysis. Default is 90 (south pole)",
    )
    arg_parser.add_argument(
        "--longitude-min",
        default=-179,
        type=float,
        help="mimium longitude to be used in analysis. Default is -180 (180 west)",
    )
    arg_parser.add_argument(
        "--longitude-max",
        default=179,
        type=float,
        help="maximum longitude to be used in analysis. Default is 180 (180 east)",
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
    arg_parser.add_argument("--verbose", action="store_true", help="debugging info")
    args = arg_parser.parse_args().__dict__
    assert os.path.isfile(args["vesseltracks"]), f'not a file: {args["vesseltracks"]}'
    assert (
        -90 < args["latitude_min"] < 90
    ), f'invalid value: {args["latitude_min"]}. Only values between -90 and 90 degrees latitude are valid'
    assert (
        -90 < args["latitude_max"] < 90
    ), f'invalid value: {args["latitude_max"]}. only values between -90 and 90 degrees latitude are valid'
    assert (
        -180 < args["longitude_min"] < 180
    ), f'invalid value: {args["longitude_min"]}. only values between -180 and 180 degrees longitude are valid'
    assert (
        -180 < args["longitude_max"] < 180
    ), f'invalid value: {args["longitude_max"]}. only values between -180 and 180 degrees longitude are valid'
    assert (
        args["latitude_min"] < args["latitude_max"]
    ), f"minumum latitude needs to be smaller than maximum latitude"
    assert (
        args["longitude_min"] < args["longitude_max"]
    ), f"minumum longitude needs to be smaller than maximum longitude"
    assert args["output_prefix"], f"please provide a prefix for exported csv files"
    return args


if __name__ == "__main__":
    config = parse_cmdline_args()
    printv("command line configuration")
    printv(f"{json.dumps(config, indent=4)}")
    printv(f"reading in vessel tracks file {config['vesseltracks']}")
    vesseltracks = extract_stationary_vesseltracks(
        read_vesseltracks_file(config["vesseltracks"]),
        lat_min=config["latitude_min"],
        lat_max=config["latitude_max"],
        lon_min=config["longitude_min"],
        lon_max=config["longitude_max"],
    )
    if vesseltracks.empty:
        print(f"no suitable ais vessel tracks for clustering available, quiting")
        sys.exit()
    if not os.path.isdir(config["output_dir"]):
        printv(f"output directory {config['output_dir']} does not exist, creating")
        try:
            os.makedirs(config["output_dir"], exist_ok=True)
        except Exception as e:
            print(f"failed to create output directory: {config['output_dir']}: {e}")
            sys.exit()
    printv("finding clusters")
    db_fit_windfarm_clusters = find_clusters(
        normalize_lat_lon(vesseltracks),
        eps=config["dbscan_epsilon"],
        min_num_samples=config["dbscan_num_samples"],
        n_cores=config["dbscan_num_processors"],
    )
    printv("extractinv clusters")
    clusters = extract_clusters(
        db_fit=db_fit_windfarm_clusters,
        raw_data=vesseltracks,
        drop_noise=config["dbscan_drop_noise"],
    )
    printv(f"found {len(clusters)} clusters")
    printv(f"exporting clusters to {config['output_dir']}")
    for cluster_label, cluster in clusters.items():
        if cluster_label == -1:
            output_fpath = os.path.join(
                config["output_dir"], f"{config['output_prefix']}_noise.csv"
            )
        else:
            output_fpath = os.path.join(
                config["output_dir"],
                f"{config['output_prefix']}_cluster_{cluster_label}.csv",
            )
        printv(f"exporting cluster_{cluster_label} to {output_fpath}")
        export_cluster(cluster, output_fpath)
