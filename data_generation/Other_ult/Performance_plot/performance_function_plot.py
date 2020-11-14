"""
This is used to visualize the performance curve for a given concurrency level through the parameter bounds
"""

import matplotlib.pyplot as plt
import sympy as sy

import Config as Config

threadpool_bounds = Config.PARAMETER_BOUNDS
concurrency_bounds = Config.FEATURE_BOUNDS

equation = Config.FUNCTION

concurrency = []
thread_size = []

min_points = []
min_point_location = []

min_point_collection = []

concurrency_level = 300


def sample_system(formula, **kwargs):
    expr = sy.sympify(formula)
    return float(expr.evalf(subs=kwargs))


def point_plot(data, title="observation", x_label='threadpool size', y_label='latency'):
    plt.plot(data, label='thread pool size')

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    # Show the plot

    plt.show()


if __name__ == '__main__':
    for i in range(len(threadpool_bounds)):
        for j in range(threadpool_bounds[i][1] - threadpool_bounds[i][0]):
            thread_size.append(j + threadpool_bounds[i][0])

    data_points = []

    for thread in thread_size:
        data_points.append(sample_system(p1=thread, f1=concurrency_level, formula=equation))

    point_plot(data_points)
