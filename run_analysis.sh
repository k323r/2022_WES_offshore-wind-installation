#!/bin/bash

set -e

WINDFARM_EPSILON=0.03
WINDFARM_N_SAMPLES=500
TURBINE_EPSILON=0.1
TURBINE_N_SAMPLES=3


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
    n_clusters=$(ls "${outputdir}"/ | grep csv | wc -l)
    if [[ $n_clusters -eq 0 ]]
    then
      echo "no clusters available for ${vesselname}.. skipping"
      continue
    fi
    for clusterfile in "${outputdir}"/"${vesselname}"_cluster_*.csv
    do
      clusterN=$(basename "${clusterfile}" .csv | cut -d "_" -f 3-4)
      clusterdir="${outputdir}/${clusterN}"
      echo "moving ${clusterfile} to ${clusterdir}"
      mkdir -p "${clusterdir}"
      mv "${clusterfile}" "${clusterdir}"
    done
  done
}

function cluster_locations() {
  for vesseldir in data/marinetraffic/clustered/*
  do
    echo "processing ${vesseldir}"
    vesselname=$(basename "${vesseldir}")
    if [[ -z $(ls "${vesseldir}") ]]
    then
      echo "${vesseldir}: no cluster available, skipping"
      continue
    fi
    for clusterdir in "${vesseldir}"/cluster_*
    do
      clustername=$(basename "${clusterdir}")
      clusterfile="${clusterdir}/${vesselname}_${clustername}.csv"
      echo "${clusterfile}"
      if ! [[ -f "${clusterfile}" ]]
      then
        echo "no cluster available"
        continue
      fi
      #outputdir="data/marinetraffic/clustered/${vesselname}/clusters"
      #mkdir -p "${outputdir}"
      python src/marinetraffic/cluster_vesseltracks2.py --vesseltracks "${clusterfile}" --dbscan-epsilon "${TURBINE_EPSILON}" --dbscan-num-samples "${TURBINE_N_SAMPLES}" --output-dir "${clusterdir}" --output-prefix "${vesselname}_${clustername}" --cluster-name location --verbose
    done
  done
}

function match_windfarms() {
    mkdir -p data/marinetraffic/matching_windfarms
    python src/marinetraffic/match_windfarms.py --known-windfarms data/windfarms/windfarms-complete_turbines.ods --cluster-dir data/marinetraffic/clustered --output-dir data/marinetraffic/matching_windfarms --verbose
}

# 1.4 plot clusters
function plot_clusters() {
  for vessel in data/marinetraffic/clustered/*
  do
    python src/marinetraffic/plot_vesseltracks.py "${vessel}"/clusters/*.csv --output-dir "${vessel}/clusters"
  done
}

function plot_matched_windfarms() {
  python src/marinetraffic/plot_matched_clusters.py  data/marinetraffic/matching_windfarms/*_cluster-*.csv  --output-dir data/marinetraffic/matching_windfarms --matching-windfarms data/marinetraffic/matching_windfarms/matching_windfarms.csv --known-windfarms data/windfarms/windfarms-complete_turbines.ods
}

function build_report() {
 
  cat <<EOF > report.md
# data processing report
EOF

  for vesseltrack in data/marinetraffic/clean/*.png
  do
    vesselname=$(basename "${vesseltrack}" .png)
    echo "## ${vesselname}" >> report.md
    echo "![${vesselname}](${vesseltrack})" >> report.md
    echo "" >> report.md
    echo "### clusters" >> report.md
    n_clusters=$(ls data/marinetraffic/clustered/"${vesselname}"/ | grep csv | wc -l)
    if [[ $n_clusters -eq 0 ]]
    then
      echo "no clusters available" >> report.md
      continue
    fi
    echo "**found ${n_clusters} clusters for record ${vesselname}**" >> report.md
    for clusterplot in data/marinetraffic/clustered/"${vesselname}"/clusters/*.png
    do
      clustername=$(basename $clusterplot .png)
      echo "#### ${clustername}" >> report.md
      echo "![${clustername}](${clusterplot})" >> report.md
    done
    echo "" >> report.md
  done

}

function run_analysis(){
  rm -r data/marinetraffic/clean/*
  rm -r data/marinetraffic/clustered/*
  rm -r data/marinetraffic/matching_windfarms/*
  clean_marinetraffic
  plot_vesseltracks
  cluster_vesseltracks
  cluster_locations
  match_windfarms
  plot_matched_windfarms
  # build_report
}

run_analysis
