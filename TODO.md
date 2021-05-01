# Infer duration of turbine installations from GPS data

# Data acquisition

## Sources

- [AIS (wikipedia)](https://en.wikipedia.org/wiki/Automatic_identification_system)
    - GPS from vessel tracking
    - Multiple commercial data brokers $\implies$ spend some money
- [ERA5](https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5)
    - Hindcast of meteorological data, i.a. wind, waves, inferred from radar et al.
    - API with volume restriction $\implies$ **Request incrementally per turbine (location and installation interval)**

## Tasks

- Set up data processing pipeline
    - Get AIS data for Trianel farm
    - Share ERA5 data for Trianel farm
    - Write code
- Scale up
    - [Choose additional wind farms from wikipedia list](https://en.wikipedia.org/wiki/List_of_offshore_wind_farms)
    - Get AIS data per farm
    - Extract turbine locations and installation intervals
    - Get ERA5 data per turbine and installation interval
    - Apply code


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
