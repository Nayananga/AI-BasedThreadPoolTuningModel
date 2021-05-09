import numpy as np

import Config
import global_data
from general_utilities.bayesian_opt import calculate_maximum_bayesian_expected_improvement
from general_utilities.data_generator import generate_random_eval_points


def update_min_point(x_data, y_data, feature_val, model=None):
    min_x, min_y, min_location = None, None, None
    min_x_data = global_data.min_x_data
    min_y_data = global_data.min_y_data
    found_feature_val = False

    for j in range(len(min_x_data)):
        if min_x_data[j][Config.NUMBER_OF_PARAMETERS:] == feature_val:
            found_feature_val = True
            min_y = min_y_data[j]
            min_x = min_x_data[j]
            min_location = j  # saved first occurrence
            break

    if found_feature_val:
        if min_x in x_data and min_y in y_data:
            if y_data[-1] < min_y and x_data[-1][Config.NUMBER_OF_PARAMETERS:] == feature_val:
                min_y = y_data[-1]
                min_x = x_data[-1]
                global_data.min_y_data[min_location] = min_y
                global_data.min_x_data[min_location] = min_x
        else:
            min_x, min_y = replace_min_point(x_data, y_data, feature_val, min_location, model)
    else:
        min_x = estimate_minimum_point(x_data, y_data, feature_val, model)

    return min_x, min_y


def estimate_minimum_point(x_data, y_data, feature_val, model):
    min_x = None

    if x_data[-1][Config.NUMBER_OF_PARAMETERS:] == feature_val:
        min_y = y_data[-1]
        min_x = x_data[-1]
        global_data.min_y_data.append(min_y)
        global_data.min_x_data.append(min_x)
    else:
        if Config.SELECTION_METHOD == "Random":
            min_x = generate_random_eval_points(1, Config.PARAMETER_BOUNDS, feature_value=feature_val).pop()
        elif Config.SELECTION_METHOD == "From_model":
            min_x = generate_min_point_based_on_model(feature_val, model)
        elif Config.SELECTION_METHOD == "Nearest_point":
            _min_y, min_x = generate_min_point_based_on_distance(feature_val)

    return min_x


def replace_min_point(x_data, y_data, feature_val, min_location, model):
    min_x, min_y = None, None

    for i in range(len(x_data)):
        if x_data[i][Config.NUMBER_OF_PARAMETERS:] == feature_val:
            if min_y is None:
                min_y = y_data[i]
                min_x = x_data[i]
            elif y_data[i] < min_y:
                min_y = y_data[i]
                min_x = x_data[i]

    if min_x is None:
        global_data.min_y_data.remove(global_data.min_y_data[min_location])
        global_data.min_x_data.remove(global_data.min_x_data[min_location])
        min_x = estimate_minimum_point(x_data, y_data, feature_val, model)
    else:
        global_data.min_y_data[min_location] = min_y
        global_data.min_x_data[min_location] = min_x

    return min_x, min_y


def generate_min_point_based_on_model(feature_value, model):
    max_expected_improvement = 0
    max_threadpool_sizes = []

    if not global_data.random_eval_check:
        eval_pool = global_data.eval_pool
    else:
        eval_pool = generate_random_eval_points(Config.EVAL_POINT_SIZE, Config.PARAMETER_BOUNDS)

    min_latency, min_eval_value = generate_min_point_based_on_distance(feature_value)
    explore_factor = 0.01

    for eval_point in eval_pool:
        check_point = list(eval_point)
        for f_val in feature_value:
            check_point.append(f_val)

        max_expected_improvement, max_threadpool_sizes = calculate_maximum_bayesian_expected_improvement(
            check_point, max_expected_improvement, max_threadpool_sizes, min_latency, explore_factor, model)

    if max_expected_improvement == 0:
        next_x = min_eval_value
    else:
        idx = np.random.randint(0, len(max_threadpool_sizes))
        next_x = max_threadpool_sizes[idx]

    min_x = list(next_x)

    return min_x


def generate_min_point_based_on_distance(feature_value):
    num_parameters = Config.NUMBER_OF_PARAMETERS
    min_x_data = global_data.min_x_data
    min_y_data = global_data.min_y_data
    min_distance = None
    min_distance_location = None
    min_y = []

    for i in range(len(min_x_data)):
        distance = calculate_distance(feature_value, min_x_data[i][num_parameters:])
        if min_distance is None:
            min_distance = distance
            min_distance_location = i
            min_y = min_y_data[i]
        elif min_distance > distance:
            min_distance = distance
            min_distance_location = i
            min_y = min_y_data[i]

    min_x = min_x_data[min_distance_location][:num_parameters]

    for feature in feature_value:
        min_x.append(feature)  # threadpool_size, throughput

    return min_y, min_x  # respective latency, respective threadpool_size, similar throughput to the feature_val


def calculate_distance(v, u):
    s = 0
    for v_i, u_i in zip(v, u):
        s += (v_i - u_i) ** 2
    return s ** 0.5
