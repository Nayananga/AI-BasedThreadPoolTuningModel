import numpy as np

import Config
import global_data
from general_utilities.data_generation_initialization import initialize_data_generation


def generate_data():
    """initial threadpool_data Configuration"""
    initialize_configurations()
    threadpool_data, latency_data = initialize_data_generation()
    global_data.min_threadpool_data, global_data.min_feature_data = find_initial_min_point_with_feature(threadpool_data,
                                                                                                        latency_data)

    return threadpool_data, latency_data


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


def find_initial_min_point_with_feature(threadpool_data, feature_data):
    min_threadpool_data = []
    min_feature_data = []
    for i, feature_value in enumerate(feature_data):
        if feature_value not in min_feature_data:
            minimum_threadpool_size = min(
                [threadpool_data[i] for i, feature_data_value in enumerate(feature_data) if
                 feature_data_value == feature_value])

            min_threadpool_data.append(minimum_threadpool_size)
            min_feature_data.append(feature_value)

        else:
            pass

    return min_threadpool_data, min_feature_data


def generate_random_eval_points(number_of_points, parameter_bounds):
    size = 0
    random_points = []

    while size < number_of_points:
        point = np.random.randint(parameter_bounds[0], parameter_bounds[1])

        if point not in random_points:
            size += 1
            random_points.append(point)

    return random_points
