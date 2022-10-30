import argparse
from datetime import datetime
from glob import glob
import json
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import sys

try:
    from config import OUTPUT_COLUMN_NAMES, COLUMN_NAMES, VESSEL_NAMES
except ImportError as e:
    print(f"failed to import from cmdline_args.py: {e}")


def convert_to_timestamp(dt, encoding="utf-8") -> int:
    try:
        return int(datetime.fromisoformat(dt).timestamp())
    except Exception as e:
        printv(f"failed to convert to datetime: {dt} type {type(dt)}: {e} skipping")
        return 0


def parse_args() -> dict:
    """
    parse_args -> dict

    instantiate an argument parser object
    to parse the command line argument supplied by the user

    returns a dictionary containing all parsed command line options

    """
    argp = argparse.ArgumentParser()

    argp.add_argument(
        "-i",
        "--input-dir",
        help="input directory containing data files",
        default=os.path.curdir,
    )
    argp.add_argument(
        "-p",
        "--input-pattern",
        help="input pattern used to glob data files",
        default="*.csv",
    )
    argp.add_argument(
        "-o",
        "--output-dir",
        help="output directory, defaults to the current working directory",
        default=os.path.curdir,
    )
    argp.add_argument(
        "-v",
        "--verbose",
        help="if provided, the logging level will be set to DEBUG",
        action="store_true",
        default=False,
    )
    cmdline_args = argp.parse_args().__dict__

    assert os.path.isdir(cmdline_args["input_dir"]), f"not a directory: {cmdline_args['input_dir']}"
    assert os.path.isdir(
        cmdline_args["output_dir"]
    ), f"not a directory: {cmdline_args['output_dir']}"

    return cmdline_args


def printv(message : str):
    global cmdline_args
    if cmdline_args["verbose"]:
        print(message)


def read_file(
    file_path: str, column_names: list, delimiter=";", skip_lines=1
) -> pd.DataFrame:
    """
    read_file() -> pd.DataFrame

    reads in a given csv file from marine traffic.

    returns a pandas DataFrame with the following columns
    mmsi | latitude | longitude | speed | heading | course | status | timestamp |
    """
    data = pd.read_csv(
        file_path,
        names=column_names,
        delimiter=delimiter,
        converters={7: convert_to_timestamp},
        skiprows=skip_lines,
    )
    data.rename(columns={"timestamp": "epoch"}, inplace=True)
    # reorder columns in table
    data = data.loc[:, OUTPUT_COLUMN_NAMES]
    return data


def parse_ship_data(data: pd.DataFrame) -> dict:
    """
    parse_ship_data -> pandas.DataFrame

    parses raw data from a csv file contained in a DataFrame
    and returns a dictionary containing dataframes for each individual vessel.
    """

    available_mmsi = data.mmsi.unique()
    printv(f"found {len(available_mmsi)} unique ships: {available_mmsi}")

    for mmsi in available_mmsi:
        printv(f"processing {mmsi}")
        if mmsi in VESSEL_NAMES:
            printv(f"parsing data for {mmsi} -> {VESSEL_NAMES[mmsi]}")
        else:
            printv(f"did not find mmsi {mmsi} in VESSEL_NAMES")
        # leverage the awesome power of pandas and selecet only data where
        # the mmsi equals the current mmsi
        vessel_data = data[data["mmsi"] == mmsi].copy()
        # convert timestamps to pd.DateTime objects
        vessel_data.insert(
            loc=0,
            value=pd.to_datetime(vessel_data["epoch"], unit="s", utc=True),
            column="timestamp",
        )
        # make the newly create epoch the index of the DataFrame
        vessel_data.set_index("timestamp", inplace=True)
        # drop the mmsi data column as it is constant for the whole dataframe
        vessel_data.drop("mmsi", axis=1, inplace=True)
        yield (mmsi, vessel_data)


def sanitize_marinetraffic(cmdline_args : dict):
    printv("done parsing commmand line arguments")
    printv(f"{json.dumps(cmdline_args, indent=4)}")
    # build a list of available files using the provided input directory, the glob matching pattern
    # and the glob function
    input_files = sorted(glob(os.path.join(cmdline_args["input_dir"], cmdline_args["input_pattern"])))
    if not len(input_files) > 0:
        print(f"did not find any input files. exit.")
        sys.exit()
    printv(f"found {len(input_files)} input files: {input_files}")
    frames = list()
    for data_file in input_files:
        # read in all available data files
        frames.append(read_file(data_file, column_names=COLUMN_NAMES))
    # merge data frames into one large data frame
    try:
        frames = pd.concat(frames)
    except Exception as e:
        print(f"failed to concatenate DataFrames: {e}")
        sys.exit()
    # sanitize data and extract data frames for individual ships
    for mmsi, vessel_data in parse_ship_data(frames):
        export_path = os.path.join(
            cmdline_args["output_dir"],
            f'{mmsi}-{VESSEL_NAMES[mmsi].lower().replace(" ", "-")}.csv',
        )
        printv(f"exporting vessel data to {export_path}")
        try:
            vessel_data.to_csv(export_path)
        except Exception as e:
            print(f"failed to export pandas dataframe: {e}")


#################################################

if __name__ == "__main__":
    cmdline_args = parse_args()
    sanitize_marinetraffic(cmdline_args)
