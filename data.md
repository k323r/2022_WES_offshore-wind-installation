# Project Data

This document describes the types of data this project is concerned with, the structure of the data and the
relationships between the different data types. After a short overview, each data set is described in depth. 

Central to the project is the Vessel data. Automatic Identification System (AIS) tracks of nine offshore wind farm
installation vessels have been procured from a data broker [marinetraffic.com](https://marinetraffic.com). The vessel
AIS tracks contain the port calls, sailing legs and of course offshore wind farm installation campaigns, 
which this project aims at investigating.

Each offshore wind farm is in itself a data set (albeit small), as each offshore wind farm contains of a different
type of turbine, has a different location, has a different number of turbines and a different layout.

Finally, for each offshore wind farm installation campaign, metocean data, such as wind speed and direction, wave 
height, wave direction and wave period, is required.

# Vessel Data

A total of nine offshore wind farm installation vessels have been 

## ERA5 Data

ERA5 Data are data sets provided by ECWMF, containing hourly estimates of a vast number of atmospheric and oceaning parameters. A short description can be found [here](https://confluence.ecmwf.int/display/CKB/The+family+of+ERA5+datasets) (ECMWF -> European Center for Medium-range Weather Forecasts). 

The Data mostly stems from ESA's Copernicus program and access is possible through a web interface or the Climate Data Store (CDS) API.
CDS provides a [python package](https://cds.climate.copernicus.eu/api-how-to) that can be used to request data. More information on how to access ERA5 data can be found [here](https://confluence.ecmwf.int/display/CKB/How+to+download+ERA5)


