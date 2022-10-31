#!/bin/env python
import argparse
import cdsapi
import glob
import json
import matplotlib.pyplot as plt
from multiprocessing import Pool
import numpy as np
import os
import pandas as pd
import sys

sys.path.append("../../modules/feedinlib/src")
from era5 import get_era5_data_from_datespan_and_position


def printv(message: str):
    global config
    if config["verbose"]:
        print(message)


def parse_cmdline_args() -> dict:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--installation",
        help="csv file containing a list of offshore wind farms extracted from vessel tracks and validated against known windfarms",
    )
    arg_parser.add_argument(
        "--output-dir",
        default="",
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
        "--overwrite", action="store_true", help="overwrite existing era5 data"
    )
    arg_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="simulates data retrieval from the Copernicus Data Storage",
    )
    arg_parser.add_argument("--verbose", action="store_true", help="debugging info")
    args = arg_parser.parse_args().__dict__
    assert os.path.isfile(args["installation"]), f'not a file: {args["installation"]}'
    assert os.path.isdir(args["output_dir"]), f"not a directory: {args['output_dir']}"
    return args


if __name__ == "__main__":
    config = parse_cmdline_args()
    printv("command line configuration")
    printv(f"{json.dumps(config, indent=4)}")
    printv(f"reading in known wind farms file {config['installation']}")
    installation = pd.read_csv(config["installation"])
    installation.set_index("index", inplace=True)
    cluster_key = "_".join(
        os.path.basename(config["installation"]).split(".")[0].split("_")[0:3]
    )
    for location in installation.itertuples():
        begin_str = pd.to_datetime(location.begin).strftime("%Y-%m-%d")
        end_str = pd.to_datetime(location.end).strftime("%Y-%m-%d")
        output_fname = f"{cluster_key}_{location.location_key}_{begin_str}_{end_str}.nc"
        output_fpath = os.path.join(config["output_dir"], output_fname)
        if os.path.isfile(output_fpath) and not config["overwrite"]:
            printv(
                f"file {output_fpath} already exists, skipping. If you want to redownload the data, use the --overwrite option."
            )
            continue
        if config["dry_run"]:
            print(f"{begin_str} {end_str}")
            print(f"exporting weather data to: {output_fpath}")
        else:
            printv(f"queueing request for {output_fname}")
            try:
                get_era5_data_from_datespan_and_position(
                    start_date=begin_str,
                    end_date=end_str,
                    target_file=output_fpath,
                    latitude=location.latitude,
                    longitude=location.longitude,
                )
            except Exception as e:
                print(f"failed to fetch era5 data: {e}")
                continue
