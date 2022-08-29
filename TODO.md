# Infer duration of turbine installations from GPS data

# Data acquisition

## Tasks
### Wind farms
- implement a script that downloads the wind farm tables available [here](https://de.wikipedia.org/wiki/Liste_der_Offshore-Windparks)
  and converts the tables into a sqlite data base.

### Marine traffic
- Scale up
    - Get AIS data per farm
    - Extract turbine locations and installation intervals
    - Get ERA5 data per turbine and installation interval
    - Apply code

#### Clustering
- Set up data processing pipeline by using Trianel Windpark Borkum II as an example (verified installation 
  durations are available here from a previous project).

### Metocean data (ERA5)
- implement `fetch_era5.py` to retrieve metocean data for a given wind farm and time window. 



# Data processing

## Metadata

- Vessel (MMSI?)
    - ID (Name)
    - Timestamp -> (Position, is_jacked (aka State of vessel, Manoeuverability))
- [Offshore Wind] Farm
    - ID (Name)
    - Area
    - List of Turbines
        - Position <------------------ TO BE INFERRED FROM VESSEL POSITIONS / OOOOR: Open access data from "emergency flight corridors"
        - Timestamp -> State of installation  <---- TO BE INFERRED FROM VESSEL POSITIONS AND is_jacked FLAGS
- Environment
    - Wave direction
    - Wave height
    - Wave period
    - Wind direction
    - Wind speed
    - ignore: Temperature, Precipitation, Season

## Tasks

- Determine installation intervals for all turbines in a given farm
    - Localize individual turbines (either from open access data or from AIS)
    - Infer state of installation per turbine
    - Infer installation interval per turbine
- Correlate installation with environment
    - Acquire environment parameters during installation (because limited volume)
    - Scatter plots, Correlation matrices, etc.
        - Find correlations of individual parameters with installation duration
- Prediction model: Estimate net installation duration from "known parameters"


# Conditions

- Always jacked during installation. (Contraposition: Not jacked $implies$ no installation in progress)
- Min 500m(?) distance between wind turbines


# Useful info

- [List of offshore wind farms (wikipedia)](https://en.wikipedia.org/wiki/List_of_offshore_wind_farms)
- [Wind turbine installation vessel (wikipedia)](https://en.wikipedia.org/wiki/Wind_turbine_installation_vessel)
- [Construction and heavy maintenance database](https://www.4coffshore.com/vessels/construction-and-heavy-maintenance.html)
