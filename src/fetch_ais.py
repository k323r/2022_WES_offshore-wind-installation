#!/usr/bin/env python3

import datetime
import os

import requests

from config import DIR_DATA_AIS

# https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
'''
<html><body>
<h1>Access Denied</h1><br/>
You don't have permission to access MarineTraffic.<br/>
This might be due to system abuse and/or violation of the Terms of Service.<br/>
If you believe this is an error, please contact us via <a href="http://help.marinetraffic.com" class="external-link" rel="nofollow" title="Follow link">http://help.marinetraffic.com</a>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"rayId":"64de13902ea70487","version":"2021.4.0","si":10}'></script>
</body></html>
'''
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
#URL = 'https://www.marinetraffic.com/legacy/getxml_i?sw_x=7.93&sw_y=52.07&ne_x=10.69&ne_y=53.83&zoom=14'
URL_PREFIX = 'https://www.marinetraffic.com/legacy/getxml_i?'
ZOOM = '&zoom=14'

def fetch_ais(sw_lon=7.93, sw_lat=52.07, ne_lon=10.69, ne_lat=53.83):
    fmt = f'utc_%Y-%m-%d-%H-%M-%S_pos_{sw_lon}-{sw_lat}-{ne_lon}-{ne_lat}.xml'
    position = f'sw_x={sw_lon}&sw_y={sw_lat}&ne_x={ne_lon}&ne_y={ne_lat}'
    url = f'{URL_PREFIX}{position}{ZOOM}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        utcnow = datetime.datetime.utcnow()
        dir_data = os.path.join(
            DIR_DATA_AIS, 'raw', utcnow.strftime('utc_%Y-%m-%d'))
        os.makedirs(dir_data, exist_ok=True)
        path_data = os.path.join(dir_data, utcnow.strftime(fmt))
        with open(path_data, 'w') as f:
            print(response.text, file=f)

if __name__ == '__main__':
    fetch_ais()
