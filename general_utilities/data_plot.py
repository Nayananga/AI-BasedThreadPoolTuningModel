import numpy as np
import matplotlib.pyplot as plt
import time

from old_files.bayesian_optimization_util import plot_approximation
import Config

from mpl_toolkits.mplot3d import axes3d

a = axes3d


# plotting of initial function
def initial_plot(parameter_plot_data, object_plot_data):
    # object_plot_data = ini_object_plot_data_generator(parameter_plot_data[0])
    plt.plot(parameter_plot_data, object_plot_data, lw=2, label='Noise-free objective')
    plt.legend()
    plt.show()



"""def initial_2d_plot(parameter_min, parameter_max, feature_min, feature_max):

    # Boundary for the simulation data
    lover_bound = parameter_min - 1
    upper_bound = parameter_max + 1
    x_bounds = np.array([[lover_bound, upper_bound]])

    workload_min = feature_min - 1
    workload_max = feature_max + 1
    y_bounds = np.array([[workload_min, workload_max]])

    x_plot_data = np.arange(x_bounds[:, 0], x_bounds[:, 1], 1).reshape(-1, 1)
    y_plot_data = np.arange(y_bounds[:, 0], y_bounds[:, 1], 1).reshape(-1, 1)

    x_plot_data, y_plot_data = np.meshgrid(x_plot_data, y_plot_data)
    z_plot_data = function_generation(x_plot_data, y_plot_data)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Plot a 3D surface
    ax.plot_surface(x_plot_data, y_plot_data, z_plot_data)

    plt.show()

    return x_plot_data, y_plot_data, z_plot_data"""


# plot the gaussian model with new data points
def surrogate_data_plot(next_x, i, model, x_plot_data, y_plot_data, parameter_history, y_data):
    x_plot_data = np.array(x_plot_data).reshape(-1, 1)
    plot_approximation(model, x_plot_data, y_plot_data, parameter_history, y_data, next_x, show_legend=i == 0)
    plt.title(f'Iteration {i + 1}')
    plt.show(block=False)
    plt.pause(0.5)
    plt.close()


def general_plot(data, title="workload", x_label='time', y_label='workers', pause_time = 5):
    folder_name = Config.PATH

    plt.plot(data, label='workload')

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    # Show the plot

    plt.savefig(folder_name+"Concurrency.png", bbox_inches="tight")

    plt.show(block=False)

    plt.pause(pause_time)
    plt.close()


def plot_data(threadpool_and_concurrency_data, percentile_data, pause_time, save=False):
    folder_name = Config.PATH

    threapool_size, concurrency = map(list, zip(*threadpool_and_concurrency_data))
    plt.plot(threapool_size, label='thread pool size')
    plt.plot(concurrency, label='concurrency')
    plt.plot(percentile_data, label='latency')

    plt.title("Data plot")
    plt.xlabel("Time")
    # plt.ylabel("y_label")

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    if save:
        time_stamp = time.asctime(time.localtime(time.time()))
        plt.savefig(folder_name+"data.png", bbox_inches="tight")

    # Show the plot
    plt.show(block=False)
    plt.pause(pause_time)
    plt.close()


def save_plots(threadpool_and_concurrency_data):
    folder_name = Config.PATH

    threapool_size, concurrency = map(list, zip(*threadpool_and_concurrency_data))
    time_stamp = time.asctime(time.localtime(time.time()))

    plt.plot(threapool_size, label='thread pool size')
    plt.plot(concurrency, label='concurrency')

    plt.title("Concurency and Threadpool size")
    plt.xlabel("Time")
    # plt.ylabel("y_label")

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    plt.savefig(folder_name + "Concurency and Threadpool size.png", bbox_inches="tight")

    # Show the plot
    plt.show(block=False)

    plt.pause(5)
    plt.close()

def min_point_plot(concurrency, thread_pool, title="Minimum_points", x_label='concurrency', y_label='Threadpool size', pause_time = 0):
    common_path = Config.COMMON_PATH
    folder_name = Config.REFERENCE_PATH
    plt.plot(thread_pool, label='thread pool size')

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    # Show the plot

    plt.savefig(common_path+folder_name + "Reference_min.png", bbox_inches="tight")

    plt.show(block=False)

    plt.pause(pause_time)
    plt.close()
