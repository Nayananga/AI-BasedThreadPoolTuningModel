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


def generate_min_point_based_on_model(target_value, feature_value, model, explore_factor=0.01):
    max_expected_improvement = 0
    max_threadpool_sizes = []

    if not global_data.random_eval_check:
        evaluation_pool = global_data.eval_pool
    else:
        evaluation_pool = generate_random_eval_points(config.EVAL_POINT_SIZE, config.PARAMETER_BOUNDS)

    query_point = np.column_stack(([target_value], [feature_value]))

    for evaluation_point in evaluation_pool:
        max_expected_improvement, max_threadpool_sizes = calculate_maximum_bayesian_expected_improvement(
            query_point, max_expected_improvement, max_threadpool_sizes, evaluation_point, explore_factor,
            model)

    return max_threadpool_sizes, max_expected_improvement


def calculate_maximum_bayesian_expected_improvement(evaluation_point, max_expected_improvement, max_threadpool_sizes,
                                                    minimum_feature_value, trade_off_level, model):
    expected_improvement = gaussian_ei(
        evaluation_point,
        model,
        minimum_feature_value,
        trade_off_level)

    if expected_improvement > max_expected_improvement:
        max_expected_improvement = expected_improvement
        max_threadpool_sizes = [evaluation_point]
    elif expected_improvement == max_expected_improvement:
        max_threadpool_sizes.append(evaluation_point)

    return max_expected_improvement, max_threadpool_sizes


def generate_min_point_based_on_distance(target_value):
    min_threadpool_data = global_data.min_threadpool_data
    min_target_data = global_data.min_target_data

    distances = [calculate_distance([min_target_data_value], [target_value]) for min_target_data_value in
                 min_target_data]
    min_distance = min(distances)

    min_distance_location = distances.index(min_distance)

    minimum_threadpool_value = min_threadpool_data[min_distance_location]

    return minimum_threadpool_value


def calculate_distance(v, u):
    s = 0
    for v_i, u_i in zip(v, u):
        s += (v_i - u_i) ** 2
    return s ** 0.5