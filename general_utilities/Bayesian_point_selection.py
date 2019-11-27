import Config_simulation as Config
import global_data as gd
from general_utilities import bayesian_opt
import numpy as np
from simulation_utilities.data_generations.simulation_get_performance import simulation_get_performance
from general_utilities.commom_functions import *


def each_point_analysis(x_data, y_data, trade_off_level, model, feature_val=None):
    if feature_val is None:
        min_x = gd.min_x
        min_y = gd.min_y
        min_x, min_y = min_point_find_no_feature(x_data, y_data, min_x, min_y)
    else:
        min_x, min_y = min_point_check_with_feature(x_data, y_data, feature_val)

    max_expected_improvement = 0
    max_optimize_point = []

    if min_y is None:
        next_optimize_point = min_x
        next_object_point = simulation_get_performance(next_optimize_point)
        min_y = next_object_point
        trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL
        gd.min_x_data.append(min_x)
        gd.min_y_data.append(min_y)

    else:
        if not gd.random_eval_check:
            eval_pool = gd.eval_pool
            """if feature_count > 0:
                temp_eval = []
                eval_combined = []
                for i in range(len(eval_pool)):
                    temp_eval = list(eval_pool[i])
                    temp_eval.append(feature_val)
                    eval_combined.append(temp_eval)
                eval_pool = eval_combined"""
        else:
            eval_pool = selecting_random_point(Config.EVAL_POINT_SIZE, Config.PARAMETER_BOUNDS, feature_value=feature_val)

        for eval_point in range(len(eval_pool)):
            max_expected_improvement, max_optimize_point = bayesian_opt.bayesian_expected_improvement(
                eval_pool[eval_point], max_expected_improvement, max_optimize_point, min_y, trade_off_level, model)

        next_optimize_point, next_object_point, trade_off_level = bayesian_opt.next_x_point_selection(
            max_expected_improvement, min_x, trade_off_level, max_optimize_point)

    """for evaluating_pool_size in range(thread_pool_min, thread_pool_max + 1):
            if one_parameter:
                pool_size = evaluating_pool_size
            else:
                pool_size = [evaluating_pool_size, feature_val]

            max_expected_improvement, max_points = bayesian_opt.bayesian_expected_improvement(
                pool_size, max_expected_improvement, max_points, min, trade_off_level, model)

        next_x, next_y, trade_off_level = bayesian_opt.next_x_point_selection(
            max_expected_improvement, min_x, trade_off_level, max_points, one_parameter)"""

    return next_optimize_point, next_object_point, max_expected_improvement, min_y, min_x, trade_off_level

"""def min_point_check_no_feature(x_data, y_data):
    min_x = gd.min_x
    min_y = gd.min_y
    if min_x in x_data and min_y in y_data:
        if y_data[-1] < min_y:
            min_y = y_data[-1]
            min_x = x_data[-1]

            gd.min_x = min_x
            gd.min_y = min_y
    else:
        min_point_find_no_feature(x_data, y_data)
    return min_y, min_x"""


def min_point_check_with_feature(x_data, y_data, feature_val):
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
            if y_data[-1] < min_y:
                min_y = y_data[-1]
                min_x = x_data[-1]

                gd.min_y_data[min_location] = min_y
                gd.min_x_data[min_location] = min_x
        else:
            min_x, min_y = min_point_update(x_data, y_data, feature_val, min_location)
    else:
        new_point = selecting_random_point(number_of_points=1, parameter_bounds=Config.PARAMETER_BOUNDS, feature_value=feature_val)
        min_x = new_point[0]

    return min_x, min_y


"""def selecting_random_point(number_of_points, parameter_bounds, feature_bounds=None, feature_value=None):
    size = 0
    training_points = []

    while size < number_of_points:
        point = []
        for j in range(len(parameter_bounds)):
            point.append(np.random.randint(parameter_bounds[j][0], feature_bounds[j][1]))
        if feature_bounds is not None:
            for k in range(len(feature_bounds)):
                point.append(np.random.randint(feature_bounds[k][0], feature_bounds[k][1]))
        if feature_value is not None:
            for f_loc in range(Config.NUMBER_OF_FEATURES):
                point.append(feature_value[f_loc])
        if point not in training_points:
            size += 1
            training_points.append(point)

    return training_points"""


def min_point_update(x_data, y_data, check_feature_val, min_location):
    min_y = None
    for i in range(len(x_data)):
        if x_data[i][Config.NUMBER_OF_PARAMETERS:] == check_feature_val:
            if min_y is None:
                min_y = y_data[i]
                min_x = x_data[i]
            elif y_data[i] < min_y:
                min_y = y_data[i]
                min_x = x_data[i]

    gd.min_y_data[min_location] = min_y
    gd.min_x_data[min_location] = min_x

    return min_x, min_y
