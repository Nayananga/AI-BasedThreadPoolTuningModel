import os

import pandas as pd
from flask import request
from matplotlib import pyplot as plt

import config


def plot_data(plot_data_1, pause_time=config.PAUSE_TIME, save=False):
    folder_name = config.RESULT_DATA_PATH

    plt.plot(plot_data_1["latency_data"], label='Actual')
    plt.plot(plot_data_1["model_predict_data"], label='predicted')

    plt.title("model performance")
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
    if os.path.exists(folder_name + "resultdata.csv"):
        os.remove(folder_name + "resultdata.csv")

    pd.DataFrame(plot_data_1).to_csv(folder_name + "resultdata.csv", index=True)


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
