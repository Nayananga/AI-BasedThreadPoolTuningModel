import time
import numpy as np
import sys

import Config_simulation_para_and_feature as Config
from simulation_utilities.data_generations.data_generation_initialization import data_generation_ini
from general_utilities.gaussian_process import gaussian_model
from general_utilities import global_data as gd

"""
from general_utilities.Bayesian_point_selection import each_point_analysis
from general_utilities.FIFO import fifo_sampling
from simulation_utilities import ploting"""
from simulation_utilities import reference_minimum_point_finder
# from simulation_utilities.initial_data_assign import initial_data_assign


np.random.seed(42)

# start a timer
start_time = time.time()


def main():
    pause_time = Config.PAUSE_TIME
    max_iterations = Config.NUMBER_OF_ITERATIONS
    number_of_features = Config.NUMBER_OF_FEATURES

    if number_of_features == 0:
        parameter_data, optimizer_data, parameter_plot_data = data_generation_ini()
        # fit initial data to gaussian model
    else:
        parameter_data, optimizer_data, feature_data, parameter_plot_data, feature_plot_data, feature_changing_data = \
            data_generation_ini()
    sys.exit()

    model = gaussian_model(x_data, y_data)
    # exploration and exploitation trade off value
    trade_off_level = Cg.default_trade_off_level

    # use bayesian optimization
    for iteration in range(max_iterations):
        next_x, next_y, max_expected_improvement, minimum, min_x, trade_off_level = each_point_analysis(
            one_parameter, x_data, y_data, trade_off_level, model, workload[iteration])

        # Data appending
        parameter_history.append(next_x)
        y_data.append(next_y)
        x_data.append(next_x)
        x_data, y_data, trade_off_level = fifo_sampling(next_x, x_data, y_data, trade_off_level)

        print("inter -", iteration)
        print("workers -", workload[iteration])
        print("trade_off_level -", trade_off_level)
        print("EI -", max_expected_improvement)
        print("Next x- ", next_x)
        print("Next y- ", next_y)
        print("minimum_obtained - y", minimum)
        print("minimum_obtained - x", min_x)

        # fit new data to gaussian process
        model = gaussian_model(x_data, y_data)

        if one_parameter:
            ploting.data_plot(next_x, iteration, model, x_plot_data, y_plot_data, x_data, y_data)
        else:
            print("minimum - point", minimum_ref_array[reference_array.index(workload[iteration])])

        print("-------------------------------------")

        time.sleep(pause_time)

    print("minimum found : %f", min(y_data))


if __name__ == "__main__":
    main()
