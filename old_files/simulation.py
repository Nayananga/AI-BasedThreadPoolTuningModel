import time

from data_generation.initial_configurations import initial_configurations

import global_data as gd
from data_generation.data_generation_initialization import data_generation_ini
from general_utilities import data_plot
from general_utilities.Bayesian_point_selection import each_point_analysis
from general_utilities.FIFO import fifo_sampling
from general_utilities.commom_functions import *
from general_utilities.gaussian_process import thread_pool_tuning_model

# from simulation_utilities.initial_data_assign import initial_data_assign

np.random.seed(42)

# start a timer
start_time = time.time()


def main():
    # Data from the Config file
    pause_time = Config.PAUSE_TIME
    max_iterations = Config.NUMBER_OF_ITERATIONS
    number_of_features = Config.NUMBER_OF_FEATURES
    number_of_parameters = Config.NUMBER_OF_PARAMETERS

    print("parameters - ", number_of_parameters, "Features - ", number_of_features)

    # exploration and exploitation trade off value
    trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL

    initial_configurations()

    # generating the initial data
    """if number_of_features == 0:
        if number_of_parameters == 1:
            optimize_data, object_data, optimize_plot_data, object_plot_data, ref_min_optimizer, ref_min_object = data_generation_ini()
        else:
            optimize_data, object_data, ref_min_optimizer, ref_min_object = data_generation_ini()
    else:
        optimize_data, object_data, feature_changing_data, ref_min_optimizer, ref_min_object = data_generation_ini()"""

    if number_of_features == 0:
        optimize_data, object_data, ref_min_optimizer, ref_min_object = data_generation_ini()
        gd.min_x_data, gd.min_y_data = min_point_find_no_feature(optimize_data, object_data)
    else:
        optimize_data, object_data, feature_changing_data, ref_min_optimizer, ref_min_object = data_generation_ini()
        gd.min_x_data, gd.min_y_data = ini_min_point_find_with_feature(optimize_data, object_data)

    # fit initial data to gaussian model
    model = thread_pool_tuning_model(optimize_data, object_data)

    min_optimizer = gd.min_x_data
    min_object = gd.min_y_data

    # use bayesian optimization
    for iteration in range(max_iterations):
        if number_of_features == 0:
            # next_location, next_value, max_expected_improvement, min_object, min_optimizer, trade_off_level = each_point_analysis(optimize_data, object_data, trade_off_level, model)
            next_optimize, next_object, max_expected_improvement, min_optimizer, min_object, trade_off_level = each_point_analysis(
                optimize_data, object_data, trade_off_level, model)
        else:
            feature_level = feature_changing_data[iteration]
            next_optimize, next_object, max_expected_improvement, min_optimizer, min_object, trade_off_level = each_point_analysis(
                optimize_data, object_data, trade_off_level, model, feature_level)

        """if number_of_features == 0:
            next_location, next_value, max_expected_improvement, min_object, min_optimizer, trade_off_level = each_point_analysis(
                optimize_data, object_data, trade_off_level, model)
        else:
            if iteration == 0:
                prev_feature = feature_changing_data[iteration]
                current_feature = feature_changing_data[iteration]
            else:
                prev_feature = current_feature
                current_feature = feature_changing_data[iteration]
            next_location, next_value, max_expected_improvement, min_object, min_optimizer, trade_off_level = each_point_analysis(
                optimize_data, object_data, trade_off_level, model, current_feature, prev_feature)"""

        # Data appending
        object_data.append(next_object)
        optimize_data.append(next_optimize)
        x_data, y_data, trade_off_level = fifo_sampling(next_optimize, optimize_data, object_data, trade_off_level)

        print("inter -", iteration)
        if number_of_features > 0:
            print("workers -", feature_changing_data[iteration])
        print("trade_off_level -", trade_off_level)
        print("EI -", max_expected_improvement)
        print("Next x- ", next_optimize)
        print("Next y- ", next_object)
        print("minimum_point_obtained", min_object, min_optimizer)
        print("Minimum data", ref_min_object, ref_min_optimizer)

        # fit new data to gaussian process
        model = thread_pool_tuning_model(optimize_data, object_data)

        if number_of_features == 0 and number_of_parameters == 1:
            optimize_plot_data = gd.optimizer_plot_data
            object_plot_data = gd.object_plot_data
            data_plot.surrogate_data_plot(next_optimize, iteration, model, optimize_plot_data, object_plot_data,
                                          optimize_data, object_data)
        print("-------------------------------------")

        time.sleep(pause_time)

    print("minimum found : %f", min_object)


if __name__ == "__main__":
    main()
