#!/bin/bash

set -o nounset -o pipefail -o errexit

update_crontab () {
    echo "
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * command-to-be-executed

# every 5 minutes, fetch ais data
*/5 * * * * python3 ~/2021_WES_offshore-wind-installation/src/fetch_ais.py

# MAYBE: every day at midnight, report yesterday's data per email
#@midnight ...

# MAYBE: 30 mins after midnight, compress acquired data files.
#30 0 * * * ...
" | crontab -
}

update_crontab
