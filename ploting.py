import numpy as np
import matplotlib.pyplot as plt
from simulation_utilities.bayesian_optimization_util import plot_approximation
from simulation_function_generator import function_generation


# plotting of initial function
def initial_plot():
    # Boundary for the simulation data
    bounds = np.array([[1, 181]])

    # global X_plot_data
    x_plot_data = np.arange(bounds[:, 0], bounds[:, 1], 1).reshape(-1, 1)
    # global Y_plot_data
    y_plot_data = function_generation(x_plot_data)

    plt.plot(x_plot_data, y_plot_data, lw=2, label='Noise-free objective')
    plt.legend()
    plt.show()

    return x_plot_data, y_plot_data


# plot the gaussian model with new data points
def data_plot(next_x, i, model, x_plot_data, y_plot_data, parameter_history, y_data):
    plot_approximation(model, x_plot_data, y_plot_data, parameter_history, y_data, next_x, show_legend=i == 0)
    plt.title(f'Iteration {i + 1}')
    plt.show(block=False)
    plt.pause(0.5)
    plt.close()