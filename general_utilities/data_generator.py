import Config
import global_data
from general_utilities.commom_functions import data_point_finder, ini_min_point_find_with_feature
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
        eval_pool = data_point_finder(thread_pool_bound)
        global_data.eval_pool = eval_pool
        global_data.random_eval_check = False
