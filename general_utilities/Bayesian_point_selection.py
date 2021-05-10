import numpy as np
from skopt.acquisition import gaussian_ei

import Config
import global_data
from general_utilities.data_generator import generate_random_eval_points


def update_min_data(threadpool_data, feature_data, feature_value=None):
    min_threadpool_data = global_data.min_threadpool_data
    min_feature_data = global_data.min_feature_data

    min_location = get_index(feature_value, min_feature_data)

    if min_location:
        minimum_threadpool_size = min(
            [threadpool_data[i] for i, feature_data_value in enumerate(feature_data) if
             feature_data_value == feature_value])
        if minimum_threadpool_size is None:
            global_data.min_threadpool_data.remove(global_data.min_threadpool_data[min_location])
            global_data.min_feature_data.remove(global_data.min_feature_data[min_location])
        elif minimum_threadpool_size < min_threadpool_data[min_location]:
            global_data.min_threadpool_data[min_location] = minimum_threadpool_size
    else:
        min_threadpool_data.append(threadpool_data[-1])
        min_feature_data.append(feature_data[-1])


def estimate_minimum_point(feature_value, model, explore_factor=None):
    minimum_threadpool_size = None

    if Config.SELECTION_METHOD == "Random":
        minimum_threadpool_size = generate_random_eval_points(1, Config.PARAMETER_BOUNDS).pop()

    elif Config.SELECTION_METHOD == "From_model":
        minimum_threadpool_size = generate_min_point_based_on_model(feature_value, model, explore_factor)

    elif Config.SELECTION_METHOD == "Nearest_point":
        minimum_threadpool_size, _minimum_feature_value = generate_min_point_based_on_distance(feature_value)

    return minimum_threadpool_size


def generate_min_point_based_on_model(feature_value, model, explore_factor=0.01):
    max_expected_improvement = 0
    max_threadpool_sizes = []

    if not global_data.random_eval_check:
        evaluation_pool = global_data.eval_pool
    else:
        evaluation_pool = generate_random_eval_points(Config.EVAL_POINT_SIZE, Config.PARAMETER_BOUNDS)

    for evaluation_point in evaluation_pool:
        max_expected_improvement, max_threadpool_sizes = calculate_maximum_bayesian_expected_improvement(
            evaluation_point, max_expected_improvement, max_threadpool_sizes, feature_value, explore_factor,
            model)

    return max_threadpool_sizes, max_expected_improvement


def calculate_maximum_bayesian_expected_improvement(evaluation_point, max_expected_improvement, max_threadpool_sizes,
                                                    minimum_feature_value, trade_off_level, model):
    expected_improvement = gaussian_ei(
        np.atleast_2d(evaluation_point),
        model,
        minimum_feature_value,
        trade_off_level)

    if expected_improvement > max_expected_improvement:
        max_expected_improvement = expected_improvement
        max_threadpool_sizes = [evaluation_point]
    elif expected_improvement == max_expected_improvement:
        max_threadpool_sizes.append(evaluation_point)

    return max_expected_improvement, max_threadpool_sizes


def generate_min_point_based_on_distance(feature_value):
    min_threadpool_data = global_data.min_threadpool_data
    min_feature_data = global_data.min_feature_data

    distances = [calculate_distance(min_feature_data_value, feature_value) for min_feature_data_value in
                 min_feature_data]
    min_distance = min(distances)

    min_distance_location = distances.index(min_distance)

    minimum_threadpool_value = min_threadpool_data[min_distance_location]
    minimum_feature_value = min_feature_data[min_distance_location]

    return minimum_threadpool_value, minimum_feature_value


def get_index(value, in_list):
    try:
        return in_list.index(value)
    except ValueError:
        return -1


def calculate_distance(v, u):
    s = 0
    for v_i, u_i in zip(v, u):
        s += (v_i - u_i) ** 2
    return s ** 0.5
