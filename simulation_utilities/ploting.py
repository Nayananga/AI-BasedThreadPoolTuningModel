import numpy as np
import matplotlib.pyplot as plt
from simulation_utilities.bayesian_optimization_util import plot_approximation
from simulation_utilities.simulation_function_generator import function_generation
import Config as Cg
from mpl_toolkits.mplot3d import axes3d
a = axes3d


# plotting of initial function
def initial_plot():
    # Boundary for the simulation data
    lover_bound = Cg.thread_pool_min - 1
    upper_bound = Cg.thread_pool_max + 1
    bounds = np.array([[lover_bound, upper_bound]])

    # global X_plot_data
    x_plot_data = np.arange(bounds[:, 0], bounds[:, 1], 1).reshape(-1, 1)
    # global Y_plot_data
    y_plot_data = function_generation(x_plot_data)

    plt.plot(x_plot_data, y_plot_data, lw=2, label='Noise-free objective')
    plt.legend()
    plt.show()

    return x_plot_data, y_plot_data


def initial_2d_plot():

    # Boundary for the simulation data
    lover_bound = Cg.thread_pool_min - 1
    upper_bound = Cg.thread_pool_max + 1
    x_bounds = np.array([[lover_bound, upper_bound]])

    workload = Cg.workload_array
    workload_min = min(workload) - 1
    workload_max = max(workload) + 1
    y_bounds = np.array([[workload_min, workload_max]])

    # global X_plot_data
    x_plot_data = np.arange(x_bounds[:, 0], x_bounds[:, 1], 1).reshape(-1, 1)

    # global Y_plot_data
    y_plot_data = np.arange(y_bounds[:, 0], y_bounds[:, 1], 1).reshape(-1, 1)

    x_plot_data, y_plot_data = np.meshgrid(x_plot_data, y_plot_data)

    # global Z_plot_data
    z_plot_data = function_generation(x_plot_data, y_plot_data)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Plot a 3D surface
    ax.plot_surface(x_plot_data, y_plot_data, z_plot_data)

    plt.show()

    return x_plot_data, y_plot_data, z_plot_data


# plot the gaussian model with new data points
def data_plot(next_x, i, model, x_plot_data, y_plot_data, parameter_history, y_data):
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
