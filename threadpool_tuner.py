import csv

import global_data as gd
from general_utilities.Bayesian_point_selection import update_min_point
from general_utilities.FIFO import fifo_sampling
from general_utilities.bayesian_opt import bayesian_expected_improvement, next_x_point_selection
from general_utilities.commom_functions import *
from general_utilities.gaussian_process import GPR


def find_next_threadpool_size(threadpool_and_throughput_data, latency_data, trade_off_level, model, throughput):
    min_threadpool_size, min_latency = update_min_point(threadpool_and_throughput_data, latency_data,
                                                        throughput, model)

    if min_latency is None:
        next_threadpool_size = min_threadpool_size
        trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL
    else:
        # else means we found exact match for the throughput from the training data
        max_expected_improvement = 0
        max_threadpool_sizes = []
        if not gd.random_eval_check:
            eval_pool = gd.eval_pool
        else:
            eval_pool = selecting_random_point(Config.EVAL_POINT_SIZE, Config.PARAMETER_BOUNDS,
                                               feature_value=throughput)
            # get a list of length is 1000 of lists including random numbers including throughput value

        for eval_point in eval_pool:
            check_point = list(eval_point)
            for throughput_val in throughput:
                check_point.append(throughput_val)

            max_expected_improvement, max_threadpool_sizes = bayesian_expected_improvement(
                check_point, max_expected_improvement, max_threadpool_sizes, min_latency, trade_off_level, model)

        next_threadpool_size, trade_off_level = next_x_point_selection(
            max_expected_improvement, min_threadpool_size, trade_off_level, max_threadpool_sizes)
        # select a random threadpool_size from max_threadpool_sizes

    return next_threadpool_size, trade_off_level


def update_model(next_threadpool_size, threadpool_and_throughput_data, latency_data, trade_off_level):
    threadpool_and_throughput_data, latency_data, trade_off_level = fifo_sampling(next_threadpool_size,
                                                                                  threadpool_and_throughput_data,
                                                                                  latency_data, trade_off_level)

    # fit new data to gaussian process
    model = GPR(threadpool_and_throughput_data, latency_data)

    return threadpool_and_throughput_data, latency_data, trade_off_level, model


def file_write(threadpool_and_throughput_data, latency_data, exploration_factor, noise_data=None,
               folder_name=Config.PATH):
    if os.path.exists(folder_name + "99th_percentile_data.csv"):
        os.remove(folder_name + "99th_percentile_data.csv")  # this deletes the file

    with open(folder_name + "99th_percentile_data.csv", 'w') as f:
        writer = csv.writer(f)
        for val in latency_data:
            writer.writerow([val])

    if noise_data is not None:

        if os.path.exists(folder_name + "noise_data.csv"):
            os.remove(folder_name + "noise_data.csv")  # this deletes the file

        with open(folder_name + "noise_data.csv", 'w') as f:
            writer = csv.writer(f)
            for val in noise_data:
                writer.writerow([val])

    if os.path.exists(folder_name + "thread_and_con_data.csv"):
        os.remove(folder_name + "thread_and_con_data.csv")  # this deletes the file

    with open(folder_name + "thread_and_con_data.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(threadpool_and_throughput_data)

    if os.path.exists(folder_name + "Exploration_factor.csv"):
        os.remove(folder_name + "Exploration_factor.csv")  # this deletes the file

    with open(folder_name + "Exploration_factor.csv", 'w') as f:
        writer = csv.writer(f)
        for val in exploration_factor:
            writer.writerow([val])
