#!/bin/env python
import argparse
import cdsapi
import glob
import json
import matplotlib.pyplot as plt
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
        "--matching-windfarms",
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
        "--overwrite",
        action="store_true",
        help="overwrite existing era5 data"
    )
    arg_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="simulates data retrieval from the Copernicus Data Storage"
    )
    arg_parser.add_argument("--verbose", action="store_true", help="debugging info")
    args = arg_parser.parse_args().__dict__
    assert os.path.isfile(
        args["matching_windfarms"]
    ), f'not a file: {args["matching_windfarms"]}'
    assert os.path.isdir(args["output_dir"]), f"not a directory: {args['output_dir']}"
    return args

if __name__ == "__main__":
    config = parse_cmdline_args()
    printv("command line configuration")
    printv(f"{json.dumps(config, indent=4)}")
    printv(f"reading in known wind farms file {config['matching_windfarms']}")
    matching_windfarms = pd.read_csv(config["matching_windfarms"])
    matching_windfarms.set_index('index', inplace=True)
    print(matching_windfarms.columns)
    for windfarm in matching_windfarms.itertuples():
        begin = pd.to_datetime(windfarm.begin)
        begin_str = begin.strftime("%Y-%m-%d")
        end = pd.to_datetime(windfarm.end)
        end_str = end.strftime("%Y-%m-%d")

        if end.year > begin.year:
            printv(f"requested time period ({begin_str} -> {end_str}) spans several years, splitting into single years")

        output_fname = f"{windfarm.Index}_{windfarm.windfarm_name.replace(' ', '-').lower()}_{windfarm.vessel_name}_{windfarm.cluster_name}_{begin}_{end}.nc"
        output_fpath = os.path.join(config['output_dir'], output_fname)
        if os.path.isfile(output_fpath) and not config['overwrite']:
            printv("file {output_fpath} already exists, skipping. If you want to redownload the data, use the --overwrite option.")
            continue
        if config['dry_run']:
            print(f'retrieveing data for {windfarm.windfarm_name} begin: {windfarm.begin} end: {windfarm.end} latitude: {windfarm.latitude} longitude: {windfarm.longitude}')
            print(f"exporting weather data to: {output_fpath}")
        else:
            try:
                printv(f"requesting data for {windfarm.windfarm_name} {begin} -> {end}")
                get_era5_data_from_datespan_and_position(
                    start_date=begin, 
                    end_date=end,
                    target_file=output_fpath,
                    latitude=windfarm.latitude,
                    longitude=windfarm.longitude
                )
            except Exception as e:
                print(f"failed to fetch era5 data: {e}")
                continue

    # print(matching_windfarms.columns)
    # get_era5_data_from_datespan_and_position('2020-01-01', '2020-01-02', '/tmp/test.nc', latitude=54, longitude=8.5)
    # for windfarm in matching_windfarms.itertuples():
    #    pass
    
