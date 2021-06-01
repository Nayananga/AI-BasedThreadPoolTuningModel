import csv
import os

import numpy as np
import pandas as pd
from flask import request
from matplotlib import pyplot as plt

import config


def plot_data(threadpool_data, throughput_data, latency_data, pause_time=config.PAUSE_TIME, save=False):
    folder_name = config.RESULT_DATA_PATH

    plt.plot(threadpool_data, label='thread pool size')
    plt.plot(latency_data, label='latency (ms)')

    plt.title("thread pool size vs latency")
    plt.xlabel("Time (Minutes)")

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    if save:
        if os.path.exists(folder_name + "Latency and Threadpool size.png"):
            os.remove(folder_name + "Latency and Threadpool size.png")

        plt.savefig(folder_name + "Latency and Threadpool size.png", bbox_inches="tight")

    # Show the plot
    plt.show(block=False)
    plt.pause(pause_time)
    plt.close()


def write_into_file(plot_data_1, folder_name=config.RESULT_DATA_PATH):
    if os.path.exists(folder_name + "result_data.csv"):
        os.remove(folder_name + "result_data.csv")

    pd.DataFrame(plot_data_1).to_csv('result_data.csv', index=True)


def create_folder(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print("requested directory already exists")


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
