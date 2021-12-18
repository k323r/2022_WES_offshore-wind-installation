import pandas as pd
import numpy as np
import logging
from glob import glob
from matplotlib import pyplot as plt
from os import path
from datetime import datetime

try:
    from config import (COLUMN_NAMES, SHIP_NAMES, parse_args)
except ImportError as e:
    logging.fatal(f'failed to import from config.py: {e}')

def convert2datetime(dt, encoding='utf-8') -> datetime:
    try:
        return datetime.fromisoformat(dt).timestamp()
    except Exception as e:
        logging.warning(f'failed to convert to datetime: {dt} type {type(dt)}: {e} skipping')
        return np.nan

def read_file(file_path : str, skip_lines=1, delimiter=';', converter={0:int, 7: convert2datetime}) -> list:
    """
    read_file() -> list

    reads in a csv file, skips the provided number of lines 
    and splits each line by the provided delimiter

    returns a list of lists containing the data from the csv file
    """

    data = np.genfromtxt(
        fname=file_path,
        skip_header=skip_lines,
        delimiter=delimiter,
        # converters=converter,
    )

    return data

def read_file_pandas(file_path : str, column_names : list, delimiter=';', skip_lines=1) -> pd.DataFrame:
    data = pd.read_csv(
        file_path,
        names=column_names,
        delimiter=delimiter,
        converters={
            7 : convert2datetime
        },
        skiprows=skip_lines,
    )

    logging.debug(data.info())
    return data

def parse_ship_data(data : pd.DataFrame) -> pd.DataFrame:
    """
    parse_ship_data -> pandas.DataFrame

    parses raw data from a csv file contained in a DataFrame
    """

    available_ships = data.mmsi.unique()
    logging.debug(f'found {len(available_ships)} unique ships: {available_ships}')

    ships= {mmsi : 0 for mmsi in available_ships}

    for ship in available_ships:
        logging.debug(f'parsing data for {ship} -> {SHIP_NAMES[ship]}')
        ships[ship] = data[data['mmsi'] == ship]

    

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

    logging.debug(f'found {len(input_files)} input files: {input_files}')

    frames = list()

    for data_file in input_files:
        # read in all available data files
        frames.append(read_file_pandas(data_file, column_names=COLUMN_NAMES))
        # merge data frames into one large data frame
    frames = pd.concat(frames)
    parse_ship_data(frames)


#################################################

if __name__ == "__main__":
    main()
