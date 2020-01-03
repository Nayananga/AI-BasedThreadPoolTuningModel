import sys
import numpy as np

import global_data as gd
from general_utilities.commom_functions import *
from general_utilities.bayesian_opt import bayesian_expected_improvement, next_x_point_selection


def update_min_point(x_data, y_data, feature_val, model=None):
    min_x_data = gd.min_x_data
    min_y_data = gd.min_y_data
    min_y = None
    found_feature_val = False

    for j in range(len(min_x_data)):
        if min_x_data[j][Config.NUMBER_OF_PARAMETERS:] == feature_val:
            found_feature_val = True
            min_y = min_y_data[j]
            min_x = min_x_data[j]
            min_location = j
            break

    if found_feature_val:
        if min_x in x_data and min_y in y_data:
            if y_data[-1] < min_y and x_data[-1][Config.NUMBER_OF_PARAMETERS:] == feature_val:
                min_y = y_data[-1]
                min_x = x_data[-1]

                gd.min_y_data[min_location] = min_y
                gd.min_x_data[min_location] = min_x
        else:
            min_x, min_y = min_point_update(x_data, y_data, feature_val, min_location)
    else:
        if x_data[-1][Config.NUMBER_OF_PARAMETERS:] == feature_val:
            min_y = y_data[-1]
            min_x = x_data[-1]
            gd.min_y_data.append(min_y)
            gd.min_x_data.append(min_x)
        else:
            if Config.RANDOM_SELECTION:
                min_x = selecting_random_point(number_of_points=1, parameter_bounds=Config.PARAMETER_BOUNDS, feature_value=feature_val)
                min_x = min_x[0]
            else:
                min_x = generate_min_point(feature_val, model)

    return min_x, min_y


def min_point_update(x_data, y_data, check_feature_val, min_location):
    min_y = None
    min_x = None
    for i in range(len(x_data)):
        if x_data[i][Config.NUMBER_OF_PARAMETERS:] == check_feature_val:
            if min_y is None:
                min_y = y_data[i]
                min_x = x_data[i]
            elif y_data[i] < min_y:
                min_y = y_data[i]
                min_x = x_data[i]

    if min_x == None:
        print(min_x)
        print(min_y)

    gd.min_y_data[min_location] = min_y
    gd.min_x_data[min_location] = min_x

    return min_x, min_y


def generate_min_point(feature_value, model):

    # finding the minimum point based on the model

    max_expected_improvement = 0
    max_threadpool_sizes = []
    if not gd.random_eval_check:
        eval_pool = gd.eval_pool
    else:
        eval_pool = selecting_random_point(Config.EVAL_POINT_SIZE, Config.PARAMETER_BOUNDS,
                                           feature_value=feature_value)

    min_percentile, min_eval_value = generate_min_point_based_on_distance(feature_value)
    explore_factor = 0.01
    for eval_point in range(len(eval_pool)):
        check_point = list(eval_pool[eval_point])
        for f_val in feature_value:
            check_point.append(f_val)

        max_expected_improvement, max_threadpool_sizes = bayesian_expected_improvement(
            check_point, max_expected_improvement, max_threadpool_sizes, min_percentile, explore_factor, model)

    if max_expected_improvement == 0:
        next_x = min_eval_value
    else:
        idx = np.random.randint(0, len(max_threadpool_sizes))
        next_x = max_threadpool_sizes[idx]

    min_x = list(next_x)

    return min_x

def generate_min_point_based_on_distance(feature_value):
    # Finding the minimum points according to the closest point
    num_parameters = Config.NUMBER_OF_PARAMETERS
    min_x_data = gd.min_x_data
    min_y_data = gd.min_y_data
    min_distance = None
    min_distance_location = None
    min_x = []
    min_y = []
    for i in range(len(min_x_data)):
        distance = distance_calculation(feature_value, min_x_data[i][num_parameters:])
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
        min_x.append(feature)

    return min_y, min_x


def distance_calculation(v, u):
    s = 0
    for v_i, u_i in zip(v, u):
        s += (v_i - u_i) ** 2
    return s ** 0.5


