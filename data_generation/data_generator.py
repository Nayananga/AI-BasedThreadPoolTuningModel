import global_data as gd
from data_generation.data_generation_initialization import data_generation_ini
from general_utilities.commom_functions import *
from general_utilities.commom_functions import data_point_finder


def generate_data():
    """initial data Configuration"""
    initial_configurations()

    optimize_data, object_data, feature_changing_data = data_generation_ini()
    gd.min_x_data, gd.min_y_data = ini_min_point_find_with_feature(optimize_data, object_data)

    gd.threadpool_and_concurrency = optimize_data
    gd.percentile = object_data
    gd.concurrency = feature_changing_data

    return optimize_data, object_data, feature_changing_data


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
        gd.random_eval_check = True
    else:
        eval_pool = data_point_finder(thread_pool_bound)
        gd.eval_pool = eval_pool
        gd.random_eval_check = False
