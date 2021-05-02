import itertools

import numpy as np

import Config
import global_data
from general_utilities.commom_functions import parameter_count, feature_count
from general_utilities.data_generation_initialization import data_generation_ini


def generate_data():
    """initial data Configuration"""
    initial_configurations()

    optimize_data, object_data = data_generation_ini()
    global_data.min_x_data, global_data.min_y_data = ini_min_point_find_with_feature(optimize_data, object_data)

    return optimize_data, object_data


def initial_configurations():
    """
    Find out whether the number of parameter points to check in one bayesian optimization is greater than
    the number of evaluation points configured.
    """

    thread_pool_bound = Config.PARAMETER_BOUNDS
    number_of_points = 0

    for i in range(Config.NUMBER_OF_PARAMETERS):
        number_of_points = number_of_points + (thread_pool_bound[i][1] - thread_pool_bound[i][0])

    if number_of_points > Config.EVAL_POINT_SIZE:
        global_data.random_eval_check = True
    else:
        eval_pool = eval_points_generator(thread_pool_bound)
        global_data.eval_pool = eval_pool
        global_data.random_eval_check = False


def eval_points_generator(parameter_bounds, feature_bounds=None):
    points_combined = [
        np.arange(parameter_bounds[i][0], parameter_bounds[i][1]).tolist() for i in range(parameter_count)]

    if parameter_count == 1 and feature_count == 0:
        points_combined = points_combined[0]
    else:
        if feature_bounds is not None:
            for k in range(feature_count):
                points_combined.append(np.arange(feature_bounds[k][0], feature_bounds[k][1]).tolist())

        points_combined = list(itertools.product(*points_combined))

    return points_combined


def ini_min_point_find_with_feature(x_data, y_data):
    min_x_data = []
    min_y_data = []
    for i in range(len(x_data)):
        found_feature_val = False
        check_feature_val = x_data[i][Config.NUMBER_OF_PARAMETERS:]
        for j in range(len(min_x_data)):
            if min_x_data[j][Config.NUMBER_OF_PARAMETERS:] == check_feature_val:

                found_feature_val = True
                if y_data[i] < min_y_data[j]:
                    min_y_data[j] = y_data[i]
                    min_x_data[j] = x_data[i]
                break

        if not found_feature_val:
            min_y_data.append(y_data[i])
            min_x_data.append(x_data[i])

    return min_x_data, min_y_data


def selecting_random_point(number_of_points, parameter_bounds, feature_value=None):
    size = 0
    random_points = []

    while size < number_of_points:
        point = []

        for parameter_bound in parameter_bounds:
            point.append(np.random.randint(parameter_bound[0], parameter_bound[1]))

        if feature_value is not None:
            for f_loc in range(Config.NUMBER_OF_FEATURES):
                point.append(feature_value[f_loc])

        if point not in random_points:
            size += 1
            random_points.append(point)

    return random_points
