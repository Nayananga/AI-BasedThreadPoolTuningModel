import time

from general_utilities.gaussian_process import thread_pool_tuning_model
from general_utilities.Bayesian_point_selection import min_point_check_with_feature
from general_utilities.bayesian_opt import bayesian_expected_improvement, next_x_point_selection
from sample_system import sample_system
import global_data as gd
from general_utilities.commom_functions import *
from general_utilities.FIFO import fifo_sampling
import Config as Config
from general_utilities.data_plot import data_plotting

from data_generation import data_generator

# from simulation_utilities.initial_data_assign import initial_data_assign

np.random.seed(42)

# start a timer
start_time = time.time()

"""# Data from the Config file
pause_time = Config.PAUSE_TIME
max_iterations = Config.NUMBER_OF_ITERATIONS
number_of_features = Config.NUMBER_OF_FEATURES
number_of_parameters = Config.NUMBER_OF_PARAMETERS

# exploration and exploitation trade off value
trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL

threadpool_and_concurrency_data = gd.threadpool_and_concurrency
percentile_data = gd.percentile
concurrency_workload = gd.concurrency"""


def find_next_threadpool_size(threadpool_and_concurrency_data, percentile_data, trade_off_level, model, concurrency):
    min_threadpool_size, min_percentile = min_point_check_with_feature(threadpool_and_concurrency_data, percentile_data, concurrency)

    if min_percentile is None:
        next_threadpool_size = min_threadpool_size
        trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL
    else:
        max_expected_improvement = 0
        max_threadpool_sizes = []
        if not gd.random_eval_check:
            eval_pool = gd.eval_pool
        else:
            eval_pool = selecting_random_point(Config.EVAL_POINT_SIZE, Config.PARAMETER_BOUNDS, feature_value=concurrency)

        for eval_point in range(len(eval_pool)):
            check_point = list(eval_pool[eval_point])
            for concurrency_val in concurrency:
                check_point.append(concurrency_val)

            max_expected_improvement, max_threadpool_sizes = bayesian_expected_improvement(
                check_point, max_expected_improvement, max_threadpool_sizes, min_percentile, trade_off_level, model)

        next_threadpool_size, trade_off_level = next_x_point_selection(
            max_expected_improvement, min_threadpool_size, trade_off_level, max_threadpool_sizes)

    return next_threadpool_size, trade_off_level


def tune_threadpool_size(model, threadpool_and_concurrency_data, percentile_data):
    iteration = 0
    x_plot = []
    y_plot = []
    pause_time = Config.PAUSE_TIME
    trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL

    concurrency_workload = gd.concurrency

    """tracing_data = []
    for concurrency in concurrency_workload:
        next_threadpool_size = find_next_threadpool_size(model, concurrency)
        next_latency_values = system_sample_fn(concurrency, next_threadpool_size)
        model = update_thredpool_tunning_model(model, concurrency, next_latency_values)
        for latency in next_latency_values:
            tracing_data.append([concurrency, next_threadpool_size, latency])"""

    # use bayesian optimization
    for concurrency in concurrency_workload:
        next_threadpool_size, trade_off_level = \
            find_next_threadpool_size(threadpool_and_concurrency_data, percentile_data, trade_off_level, model, concurrency)

        next_percentile_values = sample_system(next_threadpool_size)

        # Data appending
        percentile_data.append(next_percentile_values)
        threadpool_and_concurrency_data.append(next_threadpool_size)

        threadpool_and_concurrency_data, percentile_data, trade_off_level = \
            fifo_sampling(next_threadpool_size, threadpool_and_concurrency_data, percentile_data, trade_off_level)

        # fit new data to gaussian process
        model = thread_pool_tuning_model(threadpool_and_concurrency_data, percentile_data)

        print("inter -", iteration)
        print("workers -", concurrency)
        print("trade_off_level -", trade_off_level)
        print("Next x- ", next_threadpool_size)
        print("Next y- ", next_percentile_values)
        print("min_data", gd.min_x_data)
        print("min_data", gd.min_y_data)
        print("-------------------------------------")

        #time.sleep(pause_time)
        y_plot.append(next_percentile_values)
        x_plot.append(next_threadpool_size)
        iteration += 1
        if iteration == len(concurrency_workload):
            data_plotting(x_plot, y_plot, pause_time, save=True)
        else:
            data_plotting(x_plot, y_plot, pause_time)
    return threadpool_and_concurrency_data, percentile_data


def main():

    data_generator.data_generator()

    threadpool_and_concurrency_data = gd.threadpool_and_concurrency
    percentile_data = gd.percentile

    # fit initial data to gaussian model
    model = thread_pool_tuning_model(threadpool_and_concurrency_data, percentile_data)

    threadpool_and_concurrency_data, percentile_data = tune_threadpool_size(model, threadpool_and_concurrency_data, percentile_data)

if __name__ == "__main__":
    main()
