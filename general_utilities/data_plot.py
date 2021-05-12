import os

import matplotlib.pyplot as plt

import Config


def plot_data(threadpool_data, throughput_data, latency_data, pause_time=Config.PAUSE_TIME, save=False):
    folder_name = Config.RESULT_DATA_PATH

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
