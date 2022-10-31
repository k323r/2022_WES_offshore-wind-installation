import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

def plot_durations(installation_times : pd.DataFrame, figsize=(16,9), title="", save_fig=None, show_fig=False):
    plt.figure(figsize=figsize)
    plt.bar(installation_times.index, height=installation_times.duration)
    plt.grid()
    plt.xlabel('turbine no.')
    plt.ylabel('installation duration (h)')
    if title:
        plt.title(title)
    plt.tight_layout()
    if show_fig:
        plt.show(block=False)
    if save_fig:
        plt.savefig(save_fig, dpi=300)

def plot_gantt(installation_times : pd.DataFrame, figsize=(16,9), title="", save_fig=None, show_fig=False):
    plt.figure(figsize=figsize)
    for turbine in installation_times.itertuples():
        begin = mdates.date2num(turbine.begin)
        end = mdates.date2num(turbine.end)
        plt.barh(turbine.Index, width=end-begin, left=begin)
    plt.gca().xaxis_date()
    plt.grid()
    plt.ylabel('turbine no.')
    plt.xlabel('timeline')
    if title:
        plt.title(title)
    plt.tight_layout()
    if show_fig:
        plt.show(block=False)
    if save_fig:
        plt.savefig(save_fig, dpi=300)

