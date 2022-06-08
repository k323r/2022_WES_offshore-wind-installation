import argparse
import os.path
import pandas as pd
import pygrib as grib
import sys


def parse_args() -> dict:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "input", nargs="+", default=(None if sys.stdin.isatty() else sys.stdin)
    )
    arg_parser.add_argument("--verbose", action="store_true", help="debug flag")

    return arg_parser.parse_args().__dict__


def get_columns(filehandle) -> set:
    columns = set([m.name for m in filehandle])
    filehandle.seek(0)
    return columns


def get_data_by_column(filehandle, column):
    data = list()
    for m in filehandle.select(name=column):
        data.append([m.analDate, m.values])
    return pd.DataFrame(columns=["timestamp", column], data=data)


def grib2csv(config: dict):
    for input_filepath in config["input"]:
        if config["verbose"]:
            print(f"processing {input_filepath}")
        if not os.path.isfile(input_filepath):
            print(f"no a file: {input_filepath}. skipping.")
            continue
        filename = ".".join(os.path.basename(input_filepath).split(".")[:-1])
        target_filepath = os.path.abspath(
            os.path.join(os.path.curdir, f"{filename}.csv")
        )
        if config["verbose"]:
            print(f"output file path: {target_filepath}")
        with grib.open(input_filepath) as input_filehandle:
            joined_data = pd.DataFrame()
            for column in get_columns(input_filehandle):
                if config["verbose"]:
                    print(f"processing {column}")
                data_by_column = get_data_by_column(input_filehandle, column)
                data_by_column.timestamp = pd.to_datetime(
                    data_by_column.timestamp, utc=True
                )
                data_by_column.set_index("timestamp", inplace=True)
                if joined_data.empty:
                    joined_data = data_by_column.copy(deep=True)
                else:
                    joined_data = joined_data.join(data_by_column)
            # joined_data.drop_duplicates('timestamp', keep='first', inplace=True)
            joined_data = joined_data[~joined_data.index.duplicated(keep='first')]
            joined_data.to_csv(target_filepath)
        
if __name__ == "__main__":
    grib2csv(parse_args())
