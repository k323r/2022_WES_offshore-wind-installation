# 2022 WES Offshore Wind Farm Installations - ToDo

# Marine Traffic
- [x] cleaning script to extract per vessel time series from yearly marine traffic data: [sanitize_mtdata.py](src/marine-traffic/sanitize_mtdata.py) 
- [x] clustering script to extract track clusters: [decomposed_vesseltracks.py](src/marine-traffic/decompose_vesseltracks.py)
- [x] clustering script to extract single turbines from track clusters: [decompose_vesseltracks](sr/marine-traffic/decompose_vesseltracks)
  this should be refactored into two different scripts

# Wind Farms
- [ ] script to download/update offshore wind farm data from wikipedia and store in a SQLite-database

# MetOcean data
- [ ] script to download ERA5 data for given coordinates, a start and a stop date
- [ ] script to download NewEuropeanWindAtlas data for given coordinates, a start and a stop date

# Installation Analysis
- [ ] script to match vessel track clusters with wind farm installation data and metocean data and export all data into a single data set (directory)
- [ ] 
