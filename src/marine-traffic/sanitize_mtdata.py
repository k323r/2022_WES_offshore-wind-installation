import pandas as pd
import numpy as np
import logging
import sys
from glob import glob
from matplotlib import pyplot as plt
from os import path
from datetime import datetime

try:
    from config import (COLUMN_NAMES, VESSEL_NAMES, parse_args)
except ImportError as e:
    logging.fatal(f'failed to import from config.py: {e}')

def convert_to_timestamp(dt, encoding='utf-8') -> int:
    try:
        return int(datetime.fromisoformat(dt).timestamp())
    except Exception as e:
        logging.warning(f'failed to convert to datetime: {dt} type {type(dt)}: {e} skipping')
        return 0

def read_file(file_path : str, column_names : list, delimiter=';', skip_lines=1) -> pd.DataFrame:
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
        converters={
            7 : convert_to_timestamp
        },
        skiprows=skip_lines,
    )

    logging.debug(data.info())

    return data

def parse_ship_data(data : pd.DataFrame) -> dict:
    """
    parse_ship_data -> pandas.DataFrame

    parses raw data from a csv file contained in a DataFrame
    and returns a dictionary containing dataframes for each individual vessel.
    """

    available_mmsi = data.mmsi.unique()
    logging.debug(f'found {len(available_mmsi)} unique ships: {available_mmsi}')

    # create an empty dictionary to store data for individual vessels
    vessels = {mmsi : 0 for mmsi in available_mmsi}

    for mmsi in available_mmsi:
        logging.debug(f'processing {mmsi}')
        if mmsi in VESSEL_NAMES:
            logging.debug(f'parsing data for {mmsi} -> {VESSEL_NAMES[mmsi]}')
        else:
            logging.debug(f'did not find mmsi {mmsi} in VESSEL_NAMES')

        # leverage the awesome power of pandas and selecet only data where
        # the mmsi equals the current mmsi
        vessels[mmsi] = data[data['mmsi'] == mmsi]

        # convert timestamps to pd.DateTime objects
        vessels[mmsi].insert(
            loc=len(vessels[mmsi].columns),
            value=pd.to_datetime(vessels[mmsi]['timestamp'], unit='s', utc=True),
            column='epoch',
        )

        # make the newly create epoch the index of the DataFrame
        vessels[mmsi].set_index('epoch', inplace=True)

        # drop the mmsi data column as it is constant for the whole dataframe
        vessels[mmsi].drop('mmsi', axis=1, inplace=True)

    return vessels
    

def main():

    config = parse_args()

    logging.basicConfig(
        filename=config['logfile'],
        level=logging.DEBUG if config['verbose'] else logging.WARNING,
        format='%(levelname)s: %(asctime)s %(message)s',
        datefmt='%Y%m%dT%H%M%S%z',
    )

    logging.debug('done parsing commmand line arguments')

    # build a list of available files using the provided input directory, the glob matching pattern
    # and the glob function
    input_files = sorted(
        glob(
            path.join(config['input_dir'], config['input_pattern'])
        )
    )

    if not len(input_files) > 0:
        logging.fatal(f'did not find any input files. exit.')
        sys.exit()

    logging.debug(f'found {len(input_files)} input files: {input_files}')

    frames = list()

    for data_file in input_files:
        # read in all available data files
        frames.append(read_file(data_file, column_names=COLUMN_NAMES))

    # merge data frames into one large data frame
    try:
        frames = pd.concat(frames)
    except Exception as e:
        logging.fatal(f'failed to concatenate DataFrames: {e}')
        sys.exit()

    # sanitize data and extract data frames for individual ships 
    vessels = parse_ship_data(frames)

    for mmsi, data in vessels.items():
        export_path = path.join(config['output_dir'], f'{mmsi}_{VESSEL_NAMES[mmsi].lower().replace(" ", "-")}.csv')
        logging.debug(f'exporting vessel data to {export_path}')
        try:
            data.to_csv(export_path)
        except Exception as e:
            logging.error(f'failed to export pandas dataframe: {e}')


#################################################

if __name__ == "__main__":
    main()
