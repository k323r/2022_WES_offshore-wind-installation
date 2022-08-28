#!/usr/bin/env python3

import datetime
import glob
import os
import xml.etree.cElementTree as ET

from config import DIR_DATA_AIS

TEST_FETCH_PATHS = sorted(
    glob.glob(os.path.join(DIR_DATA_AIS, 'test_raw/utc_*/utc_*.xml')))

def get_epoch_fetch(path):
    '''
    utc_2021-05-11-20-38-00_pos_7.93-52.07-10.69-53.83.xml
    '''
    fname = os.path.basename(path)
    assert fname.startswith('utc_') and '_pos_' in fname
    epoch_fetch = int(
        datetime.datetime.strptime(
            fname.split('_pos_')[0],
            'utc_%Y-%m-%d-%H-%M-%S').replace(
                tzinfo=datetime.timezone.utc).timestamp())
    return epoch_fetch

def test_get_epoch_fetch():
    for fetch_path in TEST_FETCH_PATHS:
        epoch_fetch = get_epoch_fetch(fetch_path)
        utc_fetch = datetime.datetime.utcfromtimestamp(epoch_fetch)
        print()
        print(epoch_fetch)
        print(os.path.basename(fetch_path))
        print(utc_fetch)

def get_records_raw(path):
    tree = ET.ElementTree(file=path)
    records_raw = [r for r in tree.iter() if r.tag == 'V_POS']
    return records_raw

def test_get_records_raw():
    for fetch_path in TEST_FETCH_PATHS:
        print(get_records_raw(fetch_path))

def parse_record(record_raw):
    '''
    NOTE: A missing attribute will throw a KeyError.
    '''
    mmsi = int(record_raw.attrib['M'])
    vessel_name = record_raw.attrib['N']
    vessel_type = int(record_raw.attrib['T'])
    try:
        vessel_length = float(record_raw.attrib['L'])   # meters?
    except ValueError:
        vessel_length = None
    time_since_received_seconds = float(record_raw.attrib['E']) * 60
    latitude = float(record_raw.attrib['LAT'])
    longitude = float(record_raw.attrib['LON'])
    try:
        heading_degrees = float(record_raw.attrib['H'])
    except ValueError:
        heading_degrees = None
    try:
        speed_knots = float(record_raw.attrib['S']) / 10
    except ValueError:
        speed_knots = None
    record = (
        mmsi,
        vessel_name,
        vessel_type,
        vessel_length,
        time_since_received_seconds,
        latitude,
        longitude,
        heading_degrees,
        speed_knots)
    return record

def test_parse_record():
    for fetch_path in TEST_FETCH_PATHS:
        records_raw = get_records_raw(fetch_path)
        for record_raw in records_raw:
            print(parse_record(record_raw))

if __name__ == '__main__':
    test_get_epoch_fetch()
    test_get_records_raw()
    test_parse_record()
