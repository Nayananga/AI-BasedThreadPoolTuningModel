import numpy as np

import Config
import global_data
from general_utilities.bayesian_opt import bayesian_expected_improvement
from general_utilities.commom_functions import data_point_finder


def generate_min_point(feature_value, object_value, model):
    # finding the minimum point based on the model

    max_expected_improvement = 0
    max_threadpool_sizes = []
    eval_pool = data_point_finder(Config.PARAMETER_BOUNDS)
    min_eval_value = generate_min_point_based_on_distance(object_value)
    explore_factor = 0.01
    for eval_point in eval_pool:
        check_point = [eval_point, feature_value]
        max_expected_improvement, max_threadpool_sizes = bayesian_expected_improvement(
            check_point,
            max_expected_improvement,
            max_threadpool_sizes,
            object_value,
            explore_factor,
            model,
        )

    if max_expected_improvement == 0:
        next_x = min_eval_value
    else:
        idx = np.random.randint(0, len(max_threadpool_sizes))
        next_x = max_threadpool_sizes[idx]

    min_x = list(next_x)

    return max_expected_improvement, min_x, max_threadpool_sizes


def generate_min_point_based_on_distance(object_value):
    # Finding the minimum points according to the closest point
    min_x_data = global_data.min_x_data
    min_y_data = global_data.min_y_data
    min_distance = distance_calculation(object_value, min_y_data[0])
    min_distance_location = 0
    for i in range(1, len(min_y_data)):
        distance = distance_calculation(object_value, min_y_data[i])
        if min_distance > distance:
            min_distance = distance
            min_distance_location = i
    return min_x_data[min_distance_location]


def distance_calculation(v, u):
    s = (v - u) ** 2
    return s ** 0.5
