import argparse
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from plot import plot_durations, plot_gantt
from times import get_installation_times

def parse_cmdline_args() -> dict:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--clusters-dir",
        default=None,
        help="directory containing clusters in directories",
    )
    arg_parser.add_argument(
        "--output-dir",
        default="",
        help="output directory"
    )
    arg_parser.add_argument(
        "--verbose",
        default=False,
        help="verbose output, useful for debugging",
        action="store_true",
    )
    args = arg_parser.parse_args().__dict__
    assert os.path.isdir(args["turbines_dir"]), f'not a directory: {args["turbines_dir"]}'
    assert args['export_installation_times_fpath'], 'please provide an output file path'
    return args

if __name__ == "__main__":
    config = parse_cmdline_args()
    if config["verbose"]:
        print(f"{config}")

    installation_times = get_installation_times(config) 
    if config['plot_durations']:
        plot_durations(installation_times, save_fig=os.path.join(os.path.dirname(config['export_installation_times_fpath']), 'durations.png'))

    if config['plot_gantt']:
        plot_gantt(installation_times, save_fig=os.path.join(os.path.dirname(config['export_installation_times_fpath']), 'timeline.png'))

    installation_times.to_csv(config['export_installation_times_fpath'])
    plt.show()

