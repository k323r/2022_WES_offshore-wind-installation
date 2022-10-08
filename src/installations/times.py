import numpy as np
import pandas as pd
from turbines import get_turbine_data
from config import installation_times_columns

def extract_installation_time(turbine : pd.DataFrame):
    return [
        turbine.index[0],
        turbine.index[-1],
        (turbine.index[-1] - turbine.index[0]).total_seconds(),
        turbine.latitude.mean(),
        turbine.longitude.mean(),
        len(turbine.index),
    ]

def get_installation_times(config : dict):
    installation_times = list()
    for turbine_name, turbine in get_turbine_data(config['turbines_dir'], config['turbines_file_pattern']):
        installation_times.append(
            [
                turbine_name,
                *extract_installation_time(turbine),
            ]
        )
    installation_times = pd.DataFrame(
        data=np.array(installation_times),
        columns=installation_times_columns
    )

    return sanitize_installation_times(installation_times)

def sanitize_installation_times(installation_times : pd.DataFrame, installation_time_limit = 12) -> pd.DataFrame():
    installation_times.sort_values('begin', inplace=True)
    installation_times.reset_index(inplace=True)
    installation_times.drop(columns=['index'], inplace=True)
    installation_times = installation_times[installation_times.duration > installation_time_limit*3600]  
    return installation_times
