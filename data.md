# Project Data

This document describes the types of data this project is concerned with, the structure of the data and the
relationships between the different data types. After a short overview, each data set is described in depth. 

Central to the project are tracks of offshore installation vessels, spanning several years, covering more than a
dozen offshore wind farm installations. These wind farms in turn form a second (meta) data set, as each offshore
wind farm consists of a different type of turbine, has a different location, a different number of turbines and 
a different layout. Finally, for each offshore wind farm installation campaign, metocean data, such as wind speed
and direction, wave height, wave direction and wave period, are compiled.

# Vessel Tracks
Automatic Identification System (AIS) tracks of nine offshore wind farm installation vessels have been procured
from a data broker ([marinetraffic.com](https://marinetraffic.com)). 
A track refers to a collection of unique AIS records. Each record contains a unique time stamp and the vessels 
ID as well as latitude, longitude, speed, heading and the vessel's status. 
The vessel AIS tracks spread over several years and thus contain the port calls, sailing legs and of course 
offshore wind farm installation campaigns. 
Each vessel is identified by it's unique ID. There are several types of IDs available: IMO, MMSI, the vessels 
call sign and it's name. In this project, we use the MMSI ID in conjunction with the vessel's name to uniquely identify a vessel. 
Note, that the MMSI can change, if the  vessel is reflagged and that there several vessels can carry the same name. 

The following vessels and their respective tracks are available

| MMSI      | Name           | data availability |
| --------- | -------------- | ----------------- |
| 218389000 | Thor           | 2010 - 2021       |
| 218657000 | Vole au Vent   | 2013 - 2021       |
| 253355000 | Vole au Vent   | 2013 - 2021       |
| 219019002 | Sea Challenger | 2013 - 2021       |
| 229044000 | Brave Tern     | 2012 - 2021       |
| 229080000 | Bold Tern      | 2013 - 2021       |
| 235090598 | Blue Tern      | 2015 - 2021       |
| 215655000 | Blue Tern      | 2015 - 2021       |
| 245179000 | Aeolus         | 2010 - 2021       |
| 245924000 | MPI Adventure  | 2010 - 2021       |
| 246777000 | MPI Resolution | 2010 - 2021       |
| 253609000 | Taillevent     | 2010 - 2021       |
 
The raw vessel data as delivered by the data broker has been split into at least one csv file per year, 
e.g.: `2010.csv`. For some years, however, the data has been split into two files per year, e.g. `2012A.csv` and `2012B.csv`. 
The data files are structured into eight columns and as an example, the first three lines from the file `2010.csv` are shown:

```
MMSI;LAT;LON;SPEED;HEADING;COURSE;STATUS;TIMESTAMP
245924000;53.53467;0.284;81;511;303;0;2010-01-01 06:54:38.000
245924000;53.5505;0.1855;61;511;258;0;2010-01-01 07:25:38.000
```

`MMSI` is the ID of the vessel, `LAT` and `LON` correspond to the vessel's latitude and longitude, 
`SPEED` is the vessel speed in knots, `HEADING` the orientation of the vessel with respect to due North,
`COURSE` the vessels current planned direction of motion. `STATUS` is unknown and `TIMESTAMP` corresponds to the
date and time of the record in UTC.

The raw data can be found in the [data/marine-traffic/raw](data/marine-traffic/raw) directory.
[Data/marine-traffic/sanitized](data/marine-traffic/sanitized) contains the sanitized AIS tracks per vessel as 
csv files. These files span all available years for a given vessel and are organized into 7 columns. As an 
example the first three lines from `data/marine-traffic/sanitized/215644000_blue-tern.csv` are shown:

```
datetime,latitude,longitude,speed,heading,course,status,epoch
2020-06-15 13:52:10+00:00,53.45238,6.81926,0.0,287.0,132.0,5,1592229130
2020-06-15 14:13:11+00:00,53.45235,6.819262,0.0,287.0,132.0,5,1592230391
```


## ERA5 Data

ERA5 Data are data sets provided by ECWMF, containing hourly estimates of a vast number of atmospheric and oceaning parameters. A short description can be found [here](https://confluence.ecmwf.int/display/CKB/The+family+of+ERA5+datasets) (ECMWF -> European Center for Medium-range Weather Forecasts). 

The Data mostly stems from ESA's Copernicus program and access is possible through a web interface or the Climate Data Store (CDS) API.
CDS provides a [python package](https://cds.climate.copernicus.eu/api-how-to) that can be used to request data. More information on how to access ERA5 data can be found [here](https://confluence.ecmwf.int/display/CKB/How+to+download+ERA5)


