#!/usr/bin/env python3

import datetime
import os
import xml.etree.cElementTree as ET

from config import DIR_DATA_AIS

PATHS_FETCH_TEST = [
    os.path.join(DIR_DATA_AIS, 'test_raw', fname)
    for fname in [
        'utc_2021-05-11-20-38-00.xml',
        'utc_2021-05-12-13-53-00.xml']]

def get_epoch_fetch(path):
    '''
    utc_2021-05-11-20-38-00.xml
    '''
    fname = os.path.basename(path)
    epoch_fetch = int(
        datetime.datetime.strptime(
            fname, 'utc_%Y-%m-%d-%H-%M-%S.xml').replace(
            tzinfo=datetime.timezone.utc).timestamp())
    return epoch_fetch

def test_get_epoch_fetch():
    path_fetch = 'utc_2021-05-11-20-38-00.xml'
    epoch_fetch = get_epoch_fetch(path_fetch)
    utc_fetch = datetime.datetime.utcfromtimestamp(epoch_fetch)
    print(path_fetch)
    print(utc_fetch)
    print(epoch_fetch)

def get_records_raw(path):
    tree = ET.ElementTree(file=path)
    records_raw = [r for r in tree.iter() if r.tag == 'V_POS']
    return records_raw

def test_get_records_raw():
    print(get_records_raw(PATHS_FETCH_TEST[0]))

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
    for path_fetch in PATHS_FETCH_TEST:
        records_raw = get_records_raw(path_fetch)
        for record_raw in records_raw:
            print(parse_record(record_raw))

if __name__ == '__main__':
#    test_get_epoch_fetch()
#    test_get_records_raw()
    test_parse_record()
