#!/bin/bash

set -e

TRUE=1
FALSE=0

WINDFARM_EPSILON=0.015
WINDFARM_N_SAMPLES=100
TURBINE_EPSILON=0.1
TURBINE_N_SAMPLES=3

SHORT=s,c,l,m,pv,pc,pm,h,M,e,a
LONG=sanitize,clusters,locations,match-windfarms,plot-vesseltracks,plot-clusters,plot-matching-windfarms,help,manuscript,era5,all
OPTS=$(getopt -a -n run_analysis --options $SHORT --longoptions $LONG -- "$@")

VALID_ARGUMENTS=$# # Returns the count of arguments that are in short or long options

if [ "$VALID_ARGUMENTS" -eq 0 ]; then
  help
fi

eval set -- "$OPTS"

while :
do
  case "$1" in
    --sanitize )
      sanitize=$TRUE
      shift 1
      ;;
    --clusters )
      clusters=$TRUE
      shift 1
      ;;
    --locations )
      locations=$TRUE
      shift 1
      ;;
    --match-windfarms )
      match_windfarms=$TRUE
      shift 1
      ;;
    --plot-vesseltracks )
      plot_vesseltracks=$TRUE
      shift 1
      ;;
    --plot-clusters )
      plot_clusters=$TRUE
      shift 1
      ;;
    --plot-matching-windfarms )
      plot_matching_windfarms=$TRUE
      shift 1
      ;;
    --era5 )
      era5=$TRUE
      shift 1
      ;;
    --manuscript )
      manuscript=$TRUE
      shift 1
      ;;
    --all )
      sanitize=$TRUE
      clusters=$TRUE
      locations=$TRUE
      match=$TRUE
      plot_vesseltracks=$TRUE
      plot_clusters=$TRUE
      plot_matching_windfarms=$TRUE
      era5=$TRUE
      manuscript=$TRUE
      shift 1
      ;;
    --help)
      help
      ;;
    --)
      shift;
      break
      ;;
    *)
      echo "Unexpected option: $1"
      help
      ;;
  esac
done

function help() {
    echo "Usage: run_analysis.sh [ -s | --sanitize ][ -c | --clusters ][ -l | --locations ][ -m | --match ][ -p | --plot ][ -M | --manuscript ][ -e | --era5 ]"
    exit 2
}

function error() {
  echo "an unexpected error occured: $@"
  return -1
}

function sanitize_marinetraffic() {
  mkdir -p data/marinetraffic/clean    # create output data directory
  python bin/sanitize_marinetraffic.py  \
    --input-dir data/marinetraffic/raw \
    --input-pattern '*.csv' \
    --output-dir data/marinetraffic/clean \
    --verbose
}

function plot_vesseltracks() {
  for vesselfile in data/marinetraffic/clean/*.csv
  do
    # plot sanitized vessel tracks
    python bin/plot_vesseltracks.py "${vesselfile}" \
      --output-dir data/marinetraffic/clean
  done
}

function cluster_vesseltracks() {
  mkdir -p data/marinetraffic/clustered
  vesselfiles=$(find data/marinetraffic/clean -iname "*.csv")
  if [[ -z $vesselfiles ]]
  then
    echo "no sanitized vessel data available, please add the --sanitize flag"
    exit 2
  fi
  for vesselfile in data/marinetraffic/clean/*.csv
  do
    echo "processing ${vesselfile}"
    local vesselkey=$(basename "${vesselfile}" .csv)
    local outputdir="data/marinetraffic/clustered/${vesselkey}"
    mkdir -p "${outputdir}"
    python src/marinetraffic/cluster_vesseltracks2.py \
      --vesseltracks "${vesselfile}" \
      --dbscan-epsilon "${WINDFARM_EPSILON}" \
      --dbscan-num-samples "${WINDFARM_N_SAMPLES}" \
      --output-dir "${outputdir}" \
      --output-prefix "${vesselkey}" \
      --verbose
    # check if any clusters were found
    local n_clusters=$(ls "${outputdir}"/ | grep csv | wc -l)
    if [[ $n_clusters -eq 0 ]] # if no clusters are available, skip
    then
      echo "no clusters available for ${vesselkey}.. skipping"
      rm -r "${outputdir}"
      continue
    fi
    #move clusters into dedicated directories
    for clusterfile in "${outputdir}"/"${vesselkey}"_cluster-*.csv
    do
      # get the name of the cluster (eg cluster_13)
      local clustername=$(basename "${clusterfile}" .csv | cut -d "_" -f 2)
      local clusterdir="${outputdir}/${clustername}"
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
    local vesselkey=$(basename "${vesseldir}")
    local n_clusters=$(ls "${vesseldir}" | grep cluster | wc -l)
    echo "number of clusters: ${n_clusters}"
    if [[ "${n_clusters}" -eq 0 ]]
    then
      echo "${vesseldir}: no cluster available, skipping"
      continue
    fi
    for clusterdir in "${vesseldir}"/cluster-*
    do
      clustername=$(basename "${clusterdir}")
      clusterfile="${clusterdir}/${vesselkey}_${clustername}.csv"
      python bin/cluster_vesseltracks2.py \
        --vesseltracks "${clusterfile}" \
        --dbscan-epsilon "${TURBINE_EPSILON}" \
        --dbscan-num-samples "${TURBINE_N_SAMPLES}" \
        --output-dir "${clusterdir}" \
        --output-prefix "${vesselkey}_${clustername}" \
        --cluster-name location \
        --verbose
    done
  done
}

function match_windfarms() {
    mkdir -p data/windfarms/matching_windfarms
    python bin/match_windfarms.py \
      --known-windfarms data/windfarms/windfarms-complete_turbines.ods \
      --cluster-dir data/marinetraffic/clustered \
      --output-dir data/windfarms/matching_windfarms \
      --match-tolerance 0.09 \
      --max-distance-centroid-sigma 3 \
      --max-duration 30 \
      --min-duration 0.5 \
      --verbose
}

function plot_clusters() {
  for vessel in data/marinetraffic/clustered/*
  do
    python bin/plot_vesseltracks.py \
      $(find "${vessel}" -iname "*cluster-*.csv" | grep -v location | grep -v noise) \
      --output-dir "${vessel}"
  done
}

function plot_matching_windfarms() {
  for vesselfile in data/marinetraffic/clean/*.csv
  do
    local vesselkey=$(basename "${vesselfile}" .csv)
    local windfarm_locations=$(find data/windfarms/matching_windfarms -iname "*_${vesselkey}_cluster-*.csv" | tr '\n' ' ')
    if [[ -z $windfarm_locations ]]
    then
      echo "no matching windfarms available for ${vesselkey}, skipping"
      continue
    else
      echo "plotting ${windfarm_locations}"
    fi
    python bin/plot_vesseltracks_clusters_locations.py \
      --vesseltracks "${vesselfile}" \
      --windfarm-locations data/windfarms/matching_windfarms/*_"${vesselkey}"_cluster-*.csv \
      --known-windfarms data/windfarms/windfarms-complete_turbines.ods \
      --matching-windfarms data/windfarms/matching_windfarms/matching_windfarms.csv \
      --output-dir data/windfarms/matching_windfarms \
      --verbose \
      --interactive
  done
}

function fetch_era5() {
    for installation in data/installations/*cluster-*.csv
    do
        python3 bin/fetch_era5.py --installation $installation --output-dir data/metocean --verbose
    done
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
  if [[ $sanitize == $TRUE ]]
  then
    echo "sanitizing raw data"
    (find data/marinetraffic/clean -name "*.csv" -delete && sanitize_marinetraffic) || error "failed to sanitize raw data"
  fi

  if [[ $clusters == $TRUE ]]
  then 
    echo "clustering vesseltracks"
    (find data/marinetraffic/clustered -name "*cluster*.csv" -delete && cluster_vesseltracks) || error "failed to cluster vesseltracks"
  fi

  if [[ $locations == $TRUE ]]
  then
    echo "clustering locations"
    (find data/marinetraffic/clustered -name "*location*.csv" -delete && cluster_locations) || error "failed to cluster locations"
  fi

  if [[ $match_windfarms == $TRUE ]]
  then
    echo "matching windfarms"
    (find data/windfarms/matching_windfarms -type f -delete && match_windfarms) || error "failed to match windfarms"
  fi

  if [[ $era5 == $TRUE ]]
  then
      fetch_era5
  fi

  if [[ $manuscript == $TRUE ]]
  then
    echo "building manuscript"
    # build_report
  fi

  if [[ $plot_vesseltracks == $TRUE ]]
  then
    echo "plotting vesseltracks"
    plot_vesseltracks

  fi

  if [[ $plot_clusters == $TRUE ]]
  then
    echo "plotting clusters"
    plot_clusters
  fi
 
  if [[ $plot_matching_windfarms == $TRUE ]]
  then
    plot_matching_windfarms
  fi

}

run_analysis
