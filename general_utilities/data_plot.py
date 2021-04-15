import os

import matplotlib.pyplot as plt
import numpy as np

import Config
from old_files.bayesian_optimization_util import plot_approximation


# plotting of initial function
def initial_plot(parameter_plot_data, object_plot_data):
    # object_plot_data = ini_object_plot_data_generator(parameter_plot_data[0])
    plt.plot(parameter_plot_data, object_plot_data, lw=2, label='Noise-free objective')
    plt.legend()
    plt.show()


# plot the gaussian model with new data points
def surrogate_data_plot(next_x, i, model, x_plot_data, y_plot_data, parameter_history, y_data):
    x_plot_data = np.array(x_plot_data).reshape(-1, 1)
    plot_approximation(model, x_plot_data, y_plot_data, parameter_history, y_data, next_x, show_legend=i == 0)
    plt.title(f'Iteration {i + 1}')
    plt.show(block=False)
    plt.pause(0.5)
    plt.close()


def feature_function_plot(data, title="workload", x_label='time', y_label='workers', plot_name='Concurrency',
                          pause_time=5):
    folder_name = Config.ROOT_PATH + 'Workload_data/'

    create_folders(folder_name)

    plt.plot(data, label='workload')

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    # Show the plot

    plt.savefig(folder_name + plot_name + ".png", bbox_inches="tight")

    plt.show(block=False)

    plt.pause(pause_time)
    plt.close()


def general_plot(data, title="workload", x_label='time', y_label='workers', label='workload', plot_name="General_plot",
                 pause_time=5):
    folder_name = Config.PATH

    plt.plot(data, label=label)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    # Show the plot

    plt.savefig(folder_name + plot_name + ".png", bbox_inches="tight")

    plt.show(block=False)

    plt.pause(pause_time)
    plt.close()


def plot_data(threadpool_and_concurrency_data, percentile_data, pause_time, save=False):
    folder_name = Config.PATH

    threadpool_size, concurrency = map(list, zip(*threadpool_and_concurrency_data))
    plt.plot(threadpool_size, label='thread pool size')
    plt.plot(concurrency, label='throughput')
    plt.plot(percentile_data, label='latency (ns)')

    plt.title("Data plot")
    plt.xlabel("Time (Minutes)")

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    if save:
        plt.savefig(folder_name + "data.png", bbox_inches="tight")

    # Show the plot
    plt.show(block=False)
    plt.pause(pause_time)
    plt.close()


def save_plots(threadpool_and_concurrency_data):
    folder_name = Config.PATH

    threadpool_size, concurrency = map(list, zip(*threadpool_and_concurrency_data))

    plt.plot(threadpool_size, label='thread pool size')
    plt.plot(concurrency, label='throughput')

    plt.title("Throughput and Threadpool size")
    plt.xlabel("Time (Minutes)")

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    if os.path.exists(folder_name + "Concurrency and Threadpool size.png"):
        os.remove(folder_name + "Concurrency and Threadpool size.png")

    plt.savefig(folder_name + "Concurrency and Threadpool size.png", bbox_inches="tight")

    # Show the plot
    plt.show(block=False)

    plt.pause(5)
    plt.close()


def min_point_plot(thread_pool, title="Minimum_points", x_label='throughput', y_label='Threadpool size',
                   pause_time=0.1):
    path = Config.REFERENCE_PATH
    plt.plot(thread_pool, label='thread pool size')

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    # Show the plot

    plt.savefig(path + "Reference_min.png", bbox_inches="tight")

    plt.show(block=False)

    plt.pause(pause_time)
    plt.close()


def create_folders(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print("directory already exists")
