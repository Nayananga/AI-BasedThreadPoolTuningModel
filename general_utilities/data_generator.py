import numpy as np

import Config
import global_data
from general_utilities.data_generation_initialization import initialize_data_generation


def generate_data():
    """initial threadpool_data Configuration"""
    initialize_configurations()
    threadpool_data, latency_data, throughput_data = initialize_data_generation()
    global_data.min_threadpool_data, global_data.min_target_data, global_data.min_feature_data = \
        find_initial_min_point_with_feature(threadpool_data, latency_data, throughput_data)

    return threadpool_data, latency_data, throughput_data


def initialize_configurations():
    """
    Find out whether the number of parameter points to check in one bayesian optimization is greater than
    the number of evaluation points configured.
    """

    thread_pool_bound = Config.PARAMETER_BOUNDS
    number_of_points = thread_pool_bound[1] - thread_pool_bound[0]

    if number_of_points > Config.EVAL_POINT_SIZE:
        global_data.random_eval_check = True
    else:
        global_data.eval_pool = list(range(thread_pool_bound[0], thread_pool_bound[1]))
        global_data.random_eval_check = False


def find_initial_min_point_with_feature(threadpool_data, target_data, feature_data):
    min_threadpool_data = []
    min_target_data = []
    min_feature_data = []
    for i, target_value in enumerate(target_data):
        if target_value not in min_target_data:
            minimum_threadpool_size = min(
                [threadpool_data[i] for i, feature_data_value in enumerate(target_data) if
                 feature_data_value == target_value])

            min_threadpool_data.append(minimum_threadpool_size)
            min_target_data.append(target_value)
            min_feature_data.append(feature_data[threadpool_data.index(minimum_threadpool_size)])

        else:
            pass

    return min_threadpool_data, min_target_data, min_feature_data


def generate_random_eval_points(number_of_points, parameter_bounds):
    size = 0
    random_points = []

    while size < number_of_points:
        point = np.random.randint(parameter_bounds[0], parameter_bounds[1])

        if point not in random_points:
            size += 1
            random_points.append(point)

    return random_points


def update_min_data(threadpool_data, target_data, feature_data, target_value=None):
    min_threadpool_data = global_data.min_threadpool_data
    min_target_data = global_data.min_target_data
    min_feature_data = global_data.min_feature_data

    min_location = get_index(target_value, min_target_data)

    if min_location > -1:
        minimum_threadpool_size = min(
            [threadpool_data[i] for i, target_data_value in enumerate(target_data) if
             target_data_value == target_value])
        if minimum_threadpool_size is None:
            global_data.min_threadpool_data.remove(global_data.min_threadpool_data[min_location])
            global_data.min_target_data.remove(global_data.min_target_data[min_location])
            global_data.min_feature_data.remove(global_data.min_feature_data[min_location])
        elif minimum_threadpool_size < min_threadpool_data[min_location]:
            global_data.min_threadpool_data[min_location] = minimum_threadpool_size
            global_data.min_feature_data[min_location] = feature_data[threadpool_data.index(minimum_threadpool_size)]
    else:
        min_threadpool_data.append(threadpool_data[-1])
        min_target_data.append(target_data[-1])
        min_feature_data.append(feature_data[-1])


def get_index(value, in_list):
    try:
        return in_list.index(value)
    except ValueError:
        return -1
