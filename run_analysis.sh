#!/bin/bash

# set -e

WINDFARM_EPSILON=0.0225
WINDFARM_N_SAMPLES=200
TURBINE_EPSILON=0.025
TURBINE_N_SAMPLES=2


### run_analysis.sh

# Executing this script will run the data processing pipeline, 
# render plots and compile the paper "I spy with my little eye, or: 
# utilizing satellite data to estimate offshore wind farm installation
# performance" by Sander et al (2022). 

# 0. Setup
# 0.1 install python dependencies

# 1. AIS vessel tracks
# 1.1 Sanitize vessel tracks and split yearly mixed data into 
#     csv files, where each csv file corresponds to the AIS tracks
#     of a single vessel as definded by its mmsi ID. Sanitized vessel
#     tracks will be stored in data/marine-traffic/clean/MMSI_vessel-name.csv
function clean_marinetraffic() {
  mkdir -p data/marinetraffic/clean    # create output data directory
  python src/marinetraffic/sanitize_marinetraffic.py  --input-dir data/marinetraffic/raw --input-pattern '*.csv' --output-dir data/marinetraffic/clean --verbose
}
# 1.2 Plot vessel tracks
function plot_vesseltracks() {
  for vesselfile in data/marinetraffic/clean/*.csv
  do
    # plot sanitized vessel tracks
    python src/marinetraffic/plot_vesseltracks.py "${vesselfile}" --output-dir data/marinetraffic/clean
  done
}

# 1.3 Cluster vessel tracks using scipy's DBSCAN, a density based clustering algorithm
#     to extract wind farms. 
function cluster_vesseltracks() {
  mkdir -p data/marinetraffic/clustered
  for vesselfile in data/marinetraffic/clean/*.csv
  do
    echo "processing ${vesselfile}"
    vesselname=$(basename "${vesselfile}" .csv)
    outputdir="data/marinetraffic/clustered/${vesselname}"
    mkdir -p "${outputdir}"
    python src/marinetraffic/cluster_vesseltracks2.py --vesseltracks "${vesselfile}" --dbscan-epsilon "${WINDFARM_EPSILON}" --dbscan-num-samples "${WINDFARM_N_SAMPLES}" --output-dir "${outputdir}" --output-prefix "${vesselname}" --verbose
    if [[ -z $(ls $outputdir) ]]
    then
      echo "could not find any clusters, skipping"
      continue
    fi
    for clusterfile in "${outputdir}"/*_cluster_*.csv
    do
      clusterN=$(basename $clusterfile .csv | cut -d"_" -f3-4)
      mkdir -p "${outputdir}/${clusterN}"
      mv "${clusterfile}" "${outputdir}/${clusterN}"
    done
  done
}

function cluster_cluster() {
  for vesseldir in data/marinetraffic/clustered/*
  do
    echo "processing ${vesseldir}"
    vesselname=$(basename "${vesseldir}")
    echo "${vesselname}"
    if [[ -z $(ls "${vesseldir}") ]]
    then
      echo "could not find any clusters in ${vesseldir}, skipping"
      continue
    fi
    for clusterdir in "${vesseldir}"/cluster_*
    do 
      clusterN=$(basename $clusterdir)
      echo "clustering cluster ${clusterN}"
      clusterfile="${clusterdir}/${vesselname}_${clusterN}.csv"
      if ! [[ -e $clusterfile ]]
      then
        echo "no such file: ${clusterfile}, skipping"
        continue
      fi
      python src/marinetraffic/cluster_vesseltracks2.py --vesseltracks "${clusterfile}" --dbscan-epsilon "${TURBINE_EPSILON}" --dbscan-num-samples "${TURBINE_N_SAMPLES}" --output-dir "${clusterdir}" --output-prefix "${vesselname}_${clusterN}" --cluster-name location --verbose
      if [[ -z $(ls $outputdir) ]]
      then
        echo "could not find any clusters, skipping"
        continue
      fi
    done
  done
}

# 1.4 plot clusters
function plot_clusters() {
  for vessel in data/marinetraffic/clustered/*
  do
    if [[ -z $(ls "${vessel}") ]]
    then
      echo "no clusters available, skipping ${vessel}"
      continue
    fi
    for clusterdir in "${vessel}"/cluster_*
    do
      python src/marinetraffic/plot_vesseltracks.py "${clusterdir}"/*.csv --output-dir "${clusterdir}"
    done
  done
}

function build_report() {
  echo "# data processing report" >> report.md
  for vesseltrack in data/marinetraffic/clean/*.png
  do
    vesselname=$(basename "${vesseltrack}" .png)
    echo "## ${vesselname}" >> report.md
    echo "![${vesselname}](${vesseltrack})" >> report.md
    echo "" >> report.md
    echo "### clusters" >> report.md
    n_clusters=$(ls data/marinetraffic/clustered/"${vesselname}" | grep png | wc -l)
    if [[ $n_clusters -eq 0 ]]
    then
      echo "no clusters available" >> report.md
      continue
    fi
    echo "**found ${n_clusters} clusters for record ${vesselname}**" >> report.md
    for clusterdir in data/marinetraffic/clustered/"${vesselname}"/cluster_*
    do
      clusterN=$(basename $clusterdir)
      clusterplot="${clusterdir}/${vesselname}_${clusterN}.png"
      clusterplotname=$(basedir clusterplot .png)
      echo "#### ${clusterplotname}" >> report.md
      echo "![${clusterplotname}](${clusterplot})" >> report.md
    done
    echo "" >> report.md
  done
}

function run_analysis(){
  #clean_marinetraffic
  #plot_vesseltracks
  cluster_vesseltracks
  plot_clusters
  cluster_cluster
  #build_report
}

run_analysis
