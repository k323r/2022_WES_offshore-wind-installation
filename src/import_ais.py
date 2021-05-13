#!/usr/bin/env python3

import os
import sqlite3
import sys
import datetime
from glob import glob

from config import DIR_DATA_AIS
from parse_ais import (
    get_epoch_fetch,
    get_records_raw,
    parse_record)

PATH_DATABASE = os.path.join(DIR_DATA_AIS, 'db', 'ais.sqlite')

# TODO: 
#   - Check constraints on latitude and longitude.
#   - Maybe create index on positions.epoch_position?
SCHEMA = '''
    CREATE TABLE vessels (
        mmsi INT PRIMARY KEY,
        vessel_name TEXT NOT NULL,
        vessel_type TEXT NOT NULL,
        vessel_length TEXT);

    CREATE TABLE positions (
        mmsi INT NOT NULL,
        epoch_position INT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        heading_degrees REAL,
        speed_knots REAL,
        epoch_fetch INT NOT NULL,
        PRIMARY KEY (mmsi, epoch_position));'''

SQL_INSERT_VESSELS = '''
    INSERT OR IGNORE INTO vessels (
        mmsi,
        vessel_name,
        vessel_type,
        vessel_length)
    VALUES (?, ?, ?, ?);'''

SQL_INSERT_POSITIONS = '''
    INSERT OR IGNORE INTO positions (
        mmsi,
        epoch_position,
        latitude,
        longitude,
        heading_degrees,
        speed_knots,
        epoch_fetch)
    VALUES (?, ?, ?, ?, ?, ?, ?);'''

def init_database():
    connection = sqlite3.connect(PATH_DATABASE)
    connection.executescript(SCHEMA)
    connection.commit()
    connection.close()

def insert_many(sql_template, values):
    connection = sqlite3.connect(PATH_DATABASE)
    connection.executemany(sql_template, values)
    connection.commit()
    connection.close()

def import_ais():
    if not os.path.exists(PATH_DATABASE):
        init_database()
    try:
        start_date = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')    # -> maybe use argparse in the future?
    except IndexError:
        start_date = datetime.datetime.strptime('2021-05-11', '%Y-%m-%d')
        # start_date = datetime.datetime.strptime('2021-05-11', '%Y-%m-%d')

    #days = sorted([
    #    day for day in os.listdir(os.path.join(DIR_DATA_AIS, 'raw'))
    #    if day != '.gitkeep'
    #    and day >= start_date])   # -> utc_2021-05-13 > 2021-05-11
    
    # convert folder names into datetime objects to warant sane comparison
    days = sorted([
        datetime.datetime.strptime(day.split('_')[-1], '%Y-%m-%d') for day in glob(os.path.join(os.path.join(DIR_DATA_AIS, 'raw'), 'utc_*'))
    ])

    # remove all dates > start_date and convert back to folder name
    days = [f'utc_{datetime.datetime.strftime(day, "%Y-%m-%d")}' for day in days if day > start_date]

    for day in days:
        fnames = sorted(os.listdir(os.path.join(DIR_DATA_AIS, 'raw', day)))
        for fname in fnames:
            path_fetch = os.path.join(DIR_DATA_AIS, 'raw', day, fname)
            epoch_fetch = get_epoch_fetch(path_fetch)
            records_raw = get_records_raw(path_fetch)
            values_vessels = []
            values_positions = []
            for record_raw in records_raw:
                (mmsi,
                vessel_name,
                vessel_type,
                vessel_length,
                time_since_received_seconds,
                latitude,
                longitude,
                heading_degrees,
                speed_knots) = parse_record(record_raw)
                epoch_position = epoch_fetch - time_since_received_seconds
                values_vessels.append((
                    mmsi,
                    vessel_name,
                    vessel_type,
                    vessel_length))
                values_positions.append((
                    mmsi,
                    epoch_position,
                    latitude,
                    longitude,
                    heading_degrees,
                    speed_knots,
                    epoch_fetch))
            insert_many(SQL_INSERT_VESSELS, values_vessels)
            insert_many(SQL_INSERT_POSITIONS, values_positions)

if __name__ == '__main__':
    import_ais()
