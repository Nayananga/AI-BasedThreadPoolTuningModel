import numpy as np
from skopt.acquisition import gaussian_ei

import config
import global_data


def generate_random_eval_points(number_of_points, parameter_bounds):
    size = 0
    random_points = []

    while size < number_of_points:
        point = np.random.randint(parameter_bounds[0], parameter_bounds[1])

        if point not in random_points:
            size += 1
            random_points.append(point)

    return random_points


def find_min_point_based_on_model(min_target_value, feature_value, model, explore_factor):
    max_expected_improvement = 0.0
    threadpool_sizes = []

    if not global_data.random_eval_check:
        evaluation_pool = global_data.eval_pool
    else:
        evaluation_pool = generate_random_eval_points(config.EVAL_POINT_SIZE, config.PARAMETER_BOUNDS)

    for evaluation_point in evaluation_pool:
        query_point = np.column_stack((evaluation_point, feature_value))
        max_expected_improvement, threadpool_sizes = calculate_maximum_bayesian_expected_improvement(
            query_point, max_expected_improvement, threadpool_sizes, min_target_value, explore_factor,
            model)

    return threadpool_sizes, max_expected_improvement


def calculate_maximum_bayesian_expected_improvement(query_point, max_expected_improvement, threadpool_sizes,
                                                    minimum_feature_value, trade_off_level, model):
    expected_improvement = gaussian_ei(
        query_point,
        model,
        minimum_feature_value,
        trade_off_level)
    expected_improvement = float(expected_improvement[0])
    threadpool_point = int(query_point[0][0])
    if expected_improvement > max_expected_improvement:
        max_expected_improvement = expected_improvement
        threadpool_sizes = [threadpool_point]
    elif expected_improvement == max_expected_improvement:
        threadpool_sizes.append(threadpool_point)

    return max_expected_improvement, threadpool_sizes


def find_min_threadpool_size_based_on_distance(feature_value):
    min_threadpool_data = global_data.min_threadpool_data

    min_distance_location = find_min_feature_location_based_on_distance(feature_value)
    minimum_threadpool_value = min_threadpool_data[min_distance_location]

    return minimum_threadpool_value


def find_min_target_value_based_on_distance(feature_value):
    min_target_data = global_data.min_target_data

    min_distance_location = find_min_feature_location_based_on_distance(feature_value)
    minimum_target_value = min_target_data[min_distance_location]

    return minimum_target_value


def find_min_feature_location_based_on_distance(feature_value):
    min_feature_data = global_data.min_feature_data
    distances = [calculate_distance([min_feature_data_value], [feature_value]) for min_feature_data_value in
                 min_feature_data]
    min_distance = min(distances)
    min_distance_location = distances.index(min_distance)
    return min_distance_location


def calculate_distance(v, u):
    s = 0
    for v_i, u_i in zip(v, u):
        s += (v_i - u_i) ** 2
    return s ** 0.5
