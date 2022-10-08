from glob import glob
import os
import pandas as pd

def read_turbine_file(turbine_fpath : str) -> pd.DataFrame:
    turbine = pd.read_csv(turbine_fpath)
    turbine.epoch = pd.to_datetime(turbine.epoch)
    turbine.set_index('epoch', inplace=True)
    return turbine

def get_turbine_data(turbine_file_dir : str, turbine_file_pattern : str) -> dict:
    for turbine_fpath in sorted(glob(os.path.join(turbine_file_dir, turbine_file_pattern))):
        turbine_name = os.path.basename(turbine_fpath).split('.')[0]
        yield (turbine_name, read_turbine_file(turbine_fpath))

