
import numpy as np
from simulation_function_generator import function_generation
import matplotlib.pyplot as plt
import time
import ploting
import bayesian_opt
from gaussian_process import gaussian_model


np.random.seed(42)

#############################

parameter_history = []

x_data = []
y_data = []

# start a timer
start_time = time.time()

# bounds for the gaussian
thread_pool_max = 180
thread_pool_min = 4


# get the values when the x values are set by bayesian
def get_performance(x_pass):
    # noise distribution for the generated function
    noise_distribution = np.random.normal(0, 5, 20)

    noise_loc = np.random.randint(0, 19)
    if type(x_pass) == list:
        x_pass = x_pass[0]
    y_pass = function_generation(x_pass)
    return_val = y_pass + noise_distribution[noise_loc]
    return return_val


# get the initial points
def get_initial_points(number_of_initial_points):
    for initial_point in range(0, (number_of_initial_points+1)):
        thread_pool_value = thread_pool_min+initial_point*(thread_pool_max - thread_pool_min)/number_of_initial_points
        thread_pool_value = int(thread_pool_value)
        print('X =', thread_pool_value)
        x_data.append([thread_pool_value])
        y_data.append(get_performance([thread_pool_value]))
        parameter_history.append([thread_pool_value])


def main():
    # test Duration selection
    # test_duration = 1000
    # tuning_interval = 10
    # iterations = test_duration // tuning_interval
    max_iterations = 100

    # number of initial points for the gaussian
    number_of_initial_points = 8

    # call initial functions
    # variables
    x_plot_data, y_plot_data = ploting.initial_plot()
    get_initial_points(number_of_initial_points)

    # fit initial data to gaussian model
    model = gaussian_model(x_data, y_data)

    # exploration and exploitation trade off value
    trade_off_level = 0.1

    # use bayesian optimization
    for iteration in range((number_of_initial_points+1), max_iterations):
        minimum = min(y_data)
        x_location = y_data.index(min(y_data))
        min_x = x_data[x_location]

        max_expected_improvement = 0
        max_points = []

        print("trade_off_level -", trade_off_level)
        print("inter -", iteration)

        for evaluating_pool_size in range(thread_pool_min, thread_pool_max + 1):

            max_expected_improvement, max_points = bayesian_opt.bayesian_expected_improvement(
                evaluating_pool_size, max_expected_improvement, max_points, minimum, trade_off_level, model)

        next_x, trade_off_level = bayesian_opt.next_x_point_selection(max_expected_improvement,
                                                         min_x, trade_off_level, max_points)

        print(next_x)
        # Data appending
        parameter_history.append(next_x)
        next_y = get_performance(next_x)
        y_data.append(next_y)
        x_data.append(next_x)

        y_data_arr = np.array(y_data)

        # fit new data to gaussian process
        model = gaussian_model(x_data, y_data_arr)

        ploting.data_plot(next_x, iteration, model, x_plot_data, y_plot_data, parameter_history, y_data)

    print("minimum found : %f", min(y_data))


if __name__ == "__main__":
    main()
