import time
import logging
import numpy as np

import Config as Cg
from general_utilities import bayesian_opt
from general_utilities.gaussian_process import gaussian_model
from simulation_utilities import ploting
from simulation_utilities.workload_generator import workload_config
from simulation_utilities import min_value_finder
from old_files.Training_point_generator import get_training_points

logging.basicConfig(level=logging.INFO)

np.random.seed(42)

# start a timer
start_time = time.time()


def main():
    one_parameter = False

    workload_ini = Cg.workload_array

    # bounds for the gaussian
    thread_pool_max = Cg.thread_pool_max
    thread_pool_min = Cg.thread_pool_min

    max_iterations = Cg.number_of_iterations

    # number of initial points for the gaussian
    number_of_training_points = Cg.number_of_training_points

    # call initial functions
    if len(workload_ini) == 1:
        one_parameter = True
        x_plot_data, y_plot_data = ploting.initial_plot()
        x_data, y_data, parameter_history = get_training_points(number_of_training_points)
    else:
        workload = workload_config(workload_ini, max_iterations)
        x_plot_data, y_plot_data, z_plot_data = ploting.initial_2d_plot()
        x_data, y_data, parameter_history = get_training_points(number_of_training_points, workload)
        reference_array, minimum_ref_array = min_value_finder.min_array(x_plot_data, y_plot_data, z_plot_data)

    # fit initial data to gaussian model
    model = gaussian_model(x_data, y_data)

    # exploration and exploitation trade off value
    trade_off_level = 0.1

    # use bayesian optimization
    for iteration in range(max_iterations):
        if one_parameter:
            minimum = min(y_data)
            x_location = y_data.index(min(y_data))
            min_x = x_data[x_location]
        else:
            print("workers -", workload[iteration])
            minimum, min_x = min_value_finder.min_point_find(x_value=x_data, y_value=y_data, feature_val=workload[iteration])
            print(minimum)
            print(min_x)

        max_expected_improvement = 0
        max_points = []

        print("trade_off_level -", trade_off_level)
        print("inter -", iteration)

        for evaluating_pool_size in range(thread_pool_min, thread_pool_max + 1):
            if one_parameter:
                pool_size = evaluating_pool_size
            else:
                pool_size = [evaluating_pool_size, workload[iteration]]

            max_expected_improvement, max_points = bayesian_opt.bayesian_expected_improvement(
                pool_size, max_expected_improvement, max_points, minimum, trade_off_level, model)

        next_x, next_y, trade_off_level = bayesian_opt.next_x_point_selection(
            max_expected_improvement, min_x, trade_off_level, max_points, one_parameter)

        print("EI -", max_expected_improvement)
        print("Next x- ", next_x)
        # Data appending
        parameter_history.append(next_x)
        y_data.append(next_y)
        x_data.append(next_x)
        print("Next y- ", next_y)

        # fit new data to gaussian process
        model = gaussian_model(x_data, y_data)

        if one_parameter:
            ploting.data_plot(next_x, iteration, model, x_plot_data, y_plot_data, parameter_history, y_data)

        print("-------------------------------------")

        #time.sleep(5)

    print("minimum found : %f", min(y_data))


if __name__ == "__main__":
    main()
