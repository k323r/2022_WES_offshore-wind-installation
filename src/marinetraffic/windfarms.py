#!/bin/env python

import os
import pandas as pd


def read_windfarms_file(windfarms_fpath: str) -> pd.DataFrame:
    assert os.path.isfile(windfarms_fpath), f"no such file: {windfarms_fpath}"
    windfarms = pd.read_csv(windfarms_fpath)
    windfarms.insert(
        loc=0,
        column="key_name",
        value=windfarms.windfarm_name.apply(
            lambda x: x.lower().replace("&", "_").replace(" ", "_").replace("/", "_")
        ),
    )
    windfarms.set_index("key_name", inplace=True)
    windfarms.construction_begin = pd.to_datetime(
        windfarms.construction_begin, utc=True
    )
    windfarms.construction_end = pd.to_datetime(windfarms.construction_end, utc=True)
    return windfarms


def match_windfarms_cluster(
    windfarms: pd.DataFrame, cluster: pd.DataFrame, bounding_box_edgelength: float = 0.25, verbose=True,
):
    potential_windfarms = list()
    cluster_lat_mean = cluster.latitude.mean()
    cluster_lon_mean = cluster.longitude.mean()
    for windfarm in windfarms.itertuples():
        if (
            windfarm.latitude - bounding_box_edgelength
            < cluster_lat_mean
            < windfarm.latitude + bounding_box_edgelength
            and windfarm.longitude - bounding_box_edgelength
            < cluster_lon_mean
            < windfarm.longitude + bounding_box_edgelength
        ):
            if verbose:
                print(f"found potential wind farm: {windfarm.windfarm_name}")
            potential_windfarms.append(windfarm.Index)
    return potential_windfarms
        
