# I spy with my little eye, or: using satellite data to investigate performance of offshore wind farm installation campaigns

Offshore wind is rapidly becoming a major source of energy. With more than 5700 offshore wind turbines currently
operational, a significant amount of experience has been gathered by industries and nations alike. The wind turbines
currently being operated in the world's seas are, however, far from homogenous 

## [Data](data.md)

## How to use this repository

To run the analysis from start (cleaning raw data) to building end (compiling the paper pdf), please run the followin
command in the base of this repository. Beware: this may take a considerable amount of time.

```bash
./run_analysis.sh --clean --analyse --paper
```

### Folder Structure

```
data
  installations
    installations.sqlite    # sqlite data base containing all successfully identified installations
    windfarm-name_vessel_start_end.csv    # installation data as csv
    ...
  marine-traffic  # contains AIS vessel tracks
    raw           # raw AIS data
      2010.csv
      2011.csv
      ...
    clean         # clean AIS data decomposed into per vessel time series
      215644000_blue-tern.csv
      218389000_thor.csv
      ...
    clustered     # clustered AIS vessel tracks
      215644000_blue-tern    # folder per vessel
        windfarm_1           # folder per wind farm candidate AIS vessel tracks
          windfarm_1.csv     # AIS vessel tracks of the wind farm candidate 1
          windfarm_1_turbine_1.csv    # AIS vessel tracks of single turbine 1
          windfarm_1_turbine_2.csv    # AIS vessel tracks of single turbine 2
          ...
        windfarm_2    # wind farm candidate 2
          windfarm_2.csv
          windfarm_2_turbine_1.csv
          windfarm_2_turbine_2.csv
          ...
        ...
      218389000_thor
        windfarm_1
        windfarm_2
    marine-traffic_clusters.sqlite    # sqlite database containing all clustered AIS vessel tracks
  metocean        # metocean data
    metocean-data.sqlite    # sqlite database listing available metocean data
    windfarm-name_coord-lat_coor-lon_start_end  # metocean record per wind farm 
  wind-farms      # wind farm data
    raw           # raw wind farm data from e.g. wikipedia
    clean         # clean wind farm data as csvs
    wind-farms.sqlite    # sqlite database containing all wind farm data
```

# Acknowledgements



