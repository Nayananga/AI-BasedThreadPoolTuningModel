import time
import csv
import sys
import sympy as sy

from general_utilities.gaussian_process import GPR
from general_utilities.bayesian_opt import bayesian_expected_improvement, next_x_point_selection
import global_data as gd
from general_utilities.commom_functions import *
from general_utilities.FIFO import fifo_sampling
import Config
from general_utilities.data_plot import plot_data, save_plots, general_plot
from data_generation import data_generator
from general_utilities.Bayesian_point_selection import update_min_point
from data_generation.Referance_data_plot import compare_data
from data_generation.Other_ult.Error_calculators.Overall_error_generation import generate_overall_error
from general_utilities.sample_system import sample_system


# start a timer
start_time = time.time()


def find_next_threadpool_size(threadpool_and_concurrency_data, percentile_data, trade_off_level, model, concurrency):

    min_threadpool_size, min_percentile = update_min_point(threadpool_and_concurrency_data, percentile_data,
                                                                       concurrency, model)

    if min_percentile is None:
        next_threadpool_size = min_threadpool_size
        trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL
    else:
        max_expected_improvement = 0
        max_threadpool_sizes = []
        if not gd.random_eval_check:
            eval_pool = gd.eval_pool
        else:
            eval_pool = selecting_random_point(Config.EVAL_POINT_SIZE, Config.PARAMETER_BOUNDS,
                                               feature_value=concurrency)

        for eval_point in range(len(eval_pool)):
            check_point = list(eval_pool[eval_point])
            for concurrency_val in concurrency:
                check_point.append(concurrency_val)

            max_expected_improvement, max_threadpool_sizes = bayesian_expected_improvement(
                check_point, max_expected_improvement, max_threadpool_sizes, min_percentile, trade_off_level, model)

        next_threadpool_size, trade_off_level = next_x_point_selection(
            max_expected_improvement, min_threadpool_size, trade_off_level, max_threadpool_sizes)

    return next_threadpool_size, trade_off_level


def file_write(threadpool_and_concurrency_data, percentile_data, exploration_factor, noise_data=None, folder_name=Config.PATH):

    with open(folder_name + "99th_percentile_data.csv", 'w') as f:
        writer = csv.writer(f)
        for val in percentile_data:
            writer.writerow([val])

    if noise_data is not None:
        with open(folder_name + "noise_data.csv", 'w') as f:
            writer = csv.writer(f)
            for val in noise_data:
                writer.writerow([val])

    with open(folder_name + "thread_and_con_data.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(threadpool_and_concurrency_data)

    with open(folder_name + "Exploration_factor.csv", 'w') as f:
        writer = csv.writer(f)
        for val in exploration_factor:
            writer.writerow([val])


def update_model(next_threadpool_size, threadpool_and_concurrency_data, percentile_data, trade_off_level):
    threadpool_and_concurrency_data, percentile_data, trade_off_level = fifo_sampling(next_threadpool_size,
                                                                                      threadpool_and_concurrency_data,
                                                                                      percentile_data, trade_off_level)

    # fit new data to gaussian process
    model = GPR(threadpool_and_concurrency_data, percentile_data)

    return threadpool_and_concurrency_data, percentile_data, trade_off_level, model


def tune_threadpool_size(model, threadpool_and_concurrency_data, percentile_data, concurrency_workload, latency_func,
                         noise_std):
    iteration = 0
    thread_pool_plot_data = []
    percentile_plot_data = []
    exploration_factor = []
    noise_data = []
    trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL

    # use bayesian optimization
    for concurrency in concurrency_workload:
        next_threadpool_size, trade_off_level = find_next_threadpool_size(threadpool_and_concurrency_data,
                                                                          percentile_data, trade_off_level, model,
                                                                          concurrency)

        p1 = next_threadpool_size[0]
        f1 = next_threadpool_size[1]
        next_percentile_values, noise = sample_system(p1=p1, f1=f1, formula=latency_func, noise_level=noise_std)

        # Data appending
        noise_data.append(noise)
        percentile_data.append(next_percentile_values)
        threadpool_and_concurrency_data.append(next_threadpool_size)

        # Update the model
        threadpool_and_concurrency_data, percentile_data, trade_off_level, model = update_model(next_threadpool_size,
                                                                                                threadpool_and_concurrency_data,
                                                                                                percentile_data,
                                                                                                trade_off_level)

        print("inter -", iteration)
        print("workers -", concurrency)
        print("trade_off_level -", trade_off_level)
        print("Next x- ", next_threadpool_size)
        print("Next y- ", next_percentile_values)
        print("min_data", gd.min_x_data)
        print("min_data", gd.min_y_data)
        print("-------------------------------------")

        # data plotting
        percentile_plot_data.append(next_percentile_values)
        thread_pool_plot_data.append(next_threadpool_size)
        exploration_factor.append(trade_off_level)
        iteration += 1

        if iteration == len(concurrency_workload):
            plot_data(thread_pool_plot_data, percentile_plot_data, Config.PAUSE_TIME, save=True)
        else:
            plot_data(thread_pool_plot_data, percentile_plot_data, Config.PAUSE_TIME)

        # updating the minimum value
        update_min_point(threadpool_and_concurrency_data, percentile_data, concurrency, model)

    save_plots(thread_pool_plot_data)
    general_plot(noise_data, title="noise", x_label='time', y_label='noise_level', label='noise_level',
                 plot_name="Noise_plot", pause_time=5)
    file_write(thread_pool_plot_data, percentile_plot_data, exploration_factor, noise_data,
               folder_name=Config.PATH + 'plot_')
    compare_data()
    return threadpool_and_concurrency_data, percentile_data, exploration_factor


def main():
    latency_func = Config.FUNCTION
    common_path = Config.COMMON_PATH
    noise_name = Config.NOISE_CHANGE

    for j, noise in enumerate(Config.NOISE_LEVEL):

        Config.COMMON_PATH = common_path + '/' + noise_name[j] + '/'

        for i in range(len(Config.FEATURE_FUNCTION_ARRAY)):
            Config.FOLDER = Config.COMMON_PATH + Config.FILE_NAME[i]
            Config.PATH = Config.FOLDER + '/'
            Config.FEATURE_FUNCTION = Config.FEATURE_FUNCTION_ARRAY[i]

            print(Config.FEATURE_FUNCTION)

            create_folders(Config.FOLDER)

            train_threadpool, train_percentile, concurrency_workload = data_generator.generate_data()

            # fit initial data to gaussian model
            model = GPR(train_threadpool, train_percentile)

            threadpool_and_concurrency_data, percentile_data, exploration_factor = tune_threadpool_size(model,
                                                                                                        train_threadpool,
                                                                                                        train_percentile,
                                                                                                        concurrency_workload,
                                                                                                        latency_func,
                                                                                                        noise_std=noise)

            file_write(threadpool_and_concurrency_data, percentile_data, exploration_factor, folder_name=Config.PATH)

    generate_overall_error()


if __name__ == "__main__":
    main()
