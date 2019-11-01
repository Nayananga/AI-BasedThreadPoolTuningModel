import time

import numpy as np

import Config as Cg
from general_utilities.Bayesian_point_selection import each_point_analysis
from general_utilities.FIFO import fifo_sampling
from general_utilities.gaussian_process import gaussian_model
from simulation_utilities import ploting
from simulation_utilities import reference_minimum_point_finder
from simulation_utilities.initial_data_assign import initial_data_assign

np.random.seed(42)

# start a timer
start_time = time.time()


def main():
    pause_time = Cg.pause_time
    max_iterations = Cg.number_of_iterations

    # call initial functions
    one_parameter, x_plot_data, y_plot_data, z_plot_data, x_data, y_data, parameter_history, workload = initial_data_assign()

    if one_parameter:
        pass
    else:
        reference_array, minimum_ref_array = reference_minimum_point_finder.min_array(x_plot_data,
                                                                                      y_plot_data, z_plot_data)

    # fit initial data to gaussian model
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
