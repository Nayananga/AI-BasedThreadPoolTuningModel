import os

import matplotlib.pyplot as plt

import Config


def plot_data(threadpool_and_throughput_data, latency_data, pause_time, save=False):
    folder_name = Config.RESULT_DATA_PATH

    threadpool_size, throughput = map(list, zip(*threadpool_and_throughput_data))

    plt.plot(threadpool_size, label='thread pool size')
    plt.plot(throughput, label='target_value')
    plt.plot(latency_data, label='latency (ms)')

    plt.title("Data plot")
    plt.xlabel("Time (Minutes)")

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    if save:
        plt.savefig(folder_name + "threadpool_data.png", bbox_inches="tight")

    # Show the plot
    plt.show(block=False)
    plt.pause(pause_time)
    plt.close()


def save_plots(threadpool_and_throughput_data):
    folder_name = Config.RESULT_DATA_PATH

    threadpool_size, throughput = map(list, zip(*threadpool_and_throughput_data))

    plt.plot(threadpool_size, label='thread pool size')
    plt.plot(throughput, label='target_value')

    plt.title("Throughput and Threadpool size")
    plt.xlabel("Time (Minutes)")

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    if os.path.exists(folder_name + "Throughput and Threadpool size.png"):
        os.remove(folder_name + "Throughput and Threadpool size.png")

    plt.savefig(folder_name + "Throughput and Threadpool size.png", bbox_inches="tight")

    # Show the plot
    plt.show(block=False)

    plt.pause(5)
    plt.close()
