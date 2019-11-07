import numpy as np
import matplotlib.pyplot as plt
from simulation_utilities.bayesian_optimization_util import plot_approximation
from simulation_utilities.simulation_function_generator import function_generation
from mpl_toolkits.mplot3d import axes3d
from general_utilities import global_data as gd
a = axes3d


# plotting of initial function
def initial_plot(parameter_plot_data, optimizer_plot_data):

    plt.plot(parameter_plot_data, optimizer_plot_data, lw=2, label='Noise-free objective')
    plt.legend()
    plt.show()

    optimizer_min_location = np.where(optimizer_plot_data == min(optimizer_plot_data))
    optimizer_min = min(optimizer_plot_data)
    return parameter_plot_data[optimizer_min_location], optimizer_min


def initial_2d_plot(parameter_min, parameter_max, feature_min, feature_max):

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

    return x_plot_data, y_plot_data, z_plot_data


# plot the gaussian model with new data points
def surrogate_data_plot(next_x, i, model, x_plot_data, y_plot_data, parameter_history, y_data):
    plot_approximation(model, x_plot_data, y_plot_data, parameter_history, y_data, next_x, show_legend=i == 0)
    plt.title(f'Iteration {i + 1}')
    plt.show(block=False)
    plt.pause(0.5)
    plt.close()


def general_plot(data):

    plt.plot(data, label='workload')

    plt.title('Workload')
    plt.xlabel('time')
    plt.ylabel('workers')

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    # Show the plot
    plt.show()
