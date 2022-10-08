#!/bin/env python
import argparse
import matplotlib.pyplot as plt
import os
import sys

from clustering import (
    normalize_lat_lon,
    find_clusters,
    extract_clusters,
    export_cluster,
)
from config import WINDFARMS_FPATH
from plot import plot_vesseltracks, plot_clusters, plot_cluster_windfarms
from vesseltracks import read_vesseltracks_file, extract_stationary_vesseltracks
from windfarms import read_windfarms_file, match_windfarms_cluster

def parse_cmdline_args() -> dict:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--windfarms",
        default=None,
        help="csv file containing a list of wind farms. Used for cluster attribution. Defaults to WINDFARMS_FPATH as defined in config.py",
    )
    arg_parser.add_argument(
        "--windfarm-cluster-match-tolerance",
        default=0.1,
        type=float,
        help="match tolerance in degree lat/lon for matching a cluster to a wind farm",
    )
    arg_parser.add_argument(
        "--vesseltracks",
        default="",
        help="csv file containing the tracks of an installation vessel.",
    )
    arg_parser.add_argument(
        "--dbscan-drop-noise",
        default=False,
        action="store_true",
        help="distance parameter to be used to identify clusters",
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
        "--dbscan-epsilon-turbines",
        default=0.05,
        type=float,
        help="distance parameter to be used to identify single turbines in a turbine cluster",
    )
    arg_parser.add_argument(
        "--dbscan-num-samples-turbines",
        default=10,
        type=int,
        help="minimum number of samples per turbines when identifying turbines in a single cluster",
    )
    arg_parser.add_argument(
        "--min-num-turbines",
        default=25,
        type=int,
        help="minimum number of turbines in a wind farm",
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
        "--plot-vesseltracks",
        default=False,
        action="store_true",
        help="flag to plot vesssel tracks",
    )
    arg_parser.add_argument(
        "--plot-clusters",
        default=False,
        action="store_true",
        help="flag to plot vesssel tracks",
    )
    arg_parser.add_argument(
        "--plot-cluster-windfarms",
        default=False,
        help="plot single clusters with matching windfarms",
        action="store_true",
    )
    arg_parser.add_argument(
        "--plot-cluster-turbines",
        default=False,
        help="plot single clusters with matching windfarms",
        action="store_true",
    )
    arg_parser.add_argument(
        "--export-windfarms-dir",
        default="",
        type=str,
        help="directory to export wind successfully detected wind farms to",
    )
    arg_parser.add_argument(
        "--verbose",
        default=False,
        help="verbose output, useful for debugging",
        action="store_true",
    )
    args = arg_parser.parse_args().__dict__
    if not args["windfarms"]:
        args["windfarms"] = WINDFARMS_FPATH
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
    return args


if __name__ == "__main__":
    config = parse_cmdline_args()
    if config["verbose"]:
        print(f"{config}")
    windfarms_meta = read_windfarms_file(config["windfarms"])
    if config["verbose"]:
        print(f'read in wind farms file {config["windfarms"]}')
        print(f"{windfarms_meta}")
    vesseltracks = extract_stationary_vesseltracks(
        read_vesseltracks_file(config["vesseltracks"]),
        lat_min=config["latitude_min"],
        lat_max=config["latitude_max"],
        lon_min=config["longitude_min"],
        lon_max=config["longitude_max"],
    )
    if config["export_windfarms_dir"]:
        if not os.path.isdir(config["export_windfarms_dir"]):
            try:
                os.makedirs(config["export_windfarms_dir"], exist_ok=True)
            except Exception as e:
                print(f"failed to create output directory: {e}")

    if config["plot_vesseltracks"]:
        plot_vesseltracks(
            vesseltracks,
            show_fig=True,
            save_fig=os.path.join(config["export_windfarms_dir"], "vesseltracks.png")
            if config["export_windfarms_dir"]
            else False,
            verbose=True,
        )
    db_fit_windfarm_clusters = find_clusters(
        normalize_lat_lon(vesseltracks),
        eps=config["dbscan_epsilon"],
        min_num_samples=config["dbscan_num_samples"],
        n_cores=config["dbscan_num_processors"],
    )
    windfarm_clusters = extract_clusters(
        db_fit=db_fit_windfarm_clusters,
        raw_data=vesseltracks,
        drop_noise=config["dbscan_drop_noise"],
    )
    if config["plot_clusters"]:
        plot_clusters(
            windfarm_clusters,
            vesseltracks,
            save_fig=os.path.join(config["export_windfarms_dir"], "windfarms.png")
            if config["export_windfarms_dir"]
            else False,
        )
    for windfarm_cluster_label, windfarm_cluster in windfarm_clusters.items():
        export_windfarm_dir = None
        if config["export_windfarms_dir"]:
            export_windfarm_dir = os.path.join(
                config["export_windfarms_dir"],
                f"windfarm_cluster_{windfarm_cluster_label+1}",
            )
            os.makedirs(export_windfarm_dir, exist_ok=True)
            export_cluster(
                windfarm_cluster,
                os.path.join(
                    export_windfarm_dir, f"windfarm_cluster_{windfarm_cluster_label+1}.csv"
                ),
            )
        matching_windfarms = match_windfarms_cluster(
            windfarms_meta,
            windfarm_cluster,
            bounding_box_edgelength=config["windfarm_cluster_match_tolerance"],
        )
        if matching_windfarms and config["plot_cluster_windfarms"]:
            plot_cluster_windfarms(
                windfarm_cluster,
                windfarms_meta[windfarms_meta.index.isin(matching_windfarms)],
                show_fig=True,
                save_fig=os.path.join(
                    export_windfarm_dir,
                    f"windfarm_cluster_{windfarm_cluster_label+1}.png",
                )
                if export_windfarm_dir
                else False,
            )
        db_fit_turbine_clusters = find_clusters(
            normalize_lat_lon(windfarm_cluster),
            eps=config["dbscan_epsilon_turbines"],
            min_num_samples=config["dbscan_num_samples_turbines"],
            n_cores=config["dbscan_num_processors"],
        )
        turbine_clusters = extract_clusters(
            db_fit=db_fit_turbine_clusters,
            raw_data=windfarm_cluster,
            drop_noise=config["dbscan_drop_noise"],
        )
        if num_turbines := len(turbine_clusters) < config["min_num_turbines"]:
            if config["verbose"]:
                print(
                    f"skipping turbines cluster as too few turbines were found ({num_turbines})"
                )
            continue
        if config["plot_cluster_turbines"]:
            plot_clusters(
                clusters=turbine_clusters,
                raw_data=windfarm_cluster,
                margin=0.01,
                legend=False,
                title=" ".join(
                    [windfarms_meta.loc[i].windfarm_name for i in matching_windfarms]
                ),
                save_fig=os.path.join(export_windfarm_dir, "turbine_clusters.png")
                if export_windfarm_dir
                else None,
            )
        if export_windfarm_dir:
            for turbine_cluster_label, turbine_cluster in turbine_clusters.items():
                export_cluster(
                    turbine_cluster,
                    os.path.join(
                        export_windfarm_dir,
                        f"turbine_cluster_{turbine_cluster_label+1}.csv",
                    ),
                )
    plt.show()
