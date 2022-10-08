#!/bin/bash

### run_analysis.sh

# Executing this script will run the data processing pipeline, 
# render plots and compile the paper "I spy with my little eye, or: 
# utilizing satellite data to estimate offshore wind farm installation
# performance" by Sander et al (2022). 

# 1. AIS vessel tracks
#
# 1.1 Sanitize vessel tracks and split yearly mixed data into 
#     csv files, where each csv file corresponds to the AIS tracks
#     of a single vessel as definded by its mmsi ID. Sanitized vessel
#     tracks will be stored in data/marine-traffic/sanitized/MMSI_vessel-name.csv
#
# 1.2 Cluster vessel tracks using scipy's DBSCAN, a density based clustering algorithm
#     to extract wind farms. 
#     
#           
