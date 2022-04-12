#!/usr/bin/env python3

import os
import sqlite3
import sys

from config import DIR_DATA_AIS

PATH_DATABASE = os.path.join(DIR_DATA_AIS, 'db', 'ais.sqlite')

def fetchall(sql, params=()):
    connection = sqlite3.connect(PATH_DATABASE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    connection.close()
    return result

def get_positions(mmsi, utc_start='', utc_stop=''):
    '''
    Return the positions of the vessel identified by mmsi between utc_start
    (including) and utc_stop (excluding). 

    utc_{start,stop} must be RFC 3339 formatted datetime strings. The time part
    may be omitted. If there is a time part, it must be separated from the date
    part by a space (' ') character. (RFC 3339 allows a space for date and time
    separation, while ISO 8601 requires the character 'T'. The space is
    necessary here for compatibility with sqlite3.) Valid examples are:

        2021
        2021-05
        2021-05-11
        2021-05-11 20
        2021-05-11 20:37
        2021-05-11 20:37:00

    If utc_{start,stop} is an empty string, the respective side of the
    interval is unlimited.
    '''
    utc_stop = utc_stop or '9999'
    sql = '''
        SELECT
            mmsi,
            epoch_position,
            datetime(epoch_position, 'unixepoch') as utc_position,
            latitude,
            longitude,
            heading_degrees,
            speed_knots,
            epoch_fetch
        FROM
            positions
        WHERE
            mmsi = ?
            AND utc_position >= ?
            AND utc_position < ?
        ORDER BY
            epoch_position ASC;'''
    positions = fetchall(sql, params=(mmsi, utc_start, utc_stop))
    return positions

def test_get_positions():
    print()
    print('Both unlimited')
    for row in get_positions(992111847):
        print(dict(row))
    print()
    print('Start unlimited')
    for row in get_positions(992111847, utc_stop='2021-05-12'):
        print(dict(row))
    print()
    print('Stop unlimited')
    for row in get_positions(992111847, utc_start='2021-05-12'):
        print(dict(row))
    print()
    print('Both limited')
    for row in get_positions(
            992111847, utc_start='2021-05-12', utc_stop='2021-06'):
        print(dict(row))

if __name__ == '__main__':
    test_get_positions()
