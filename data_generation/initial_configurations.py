import Config

import global_data as gd
from general_utilities.commom_functions import *

evaluation_size = Config.EVAL_POINT_SIZE
thread_pool_bound = Config.PARAMETER_BOUNDS

workload_bound = Config.FEATURE_BOUNDS


def initial_configurations():
    number_of_total_points = evaluation_point_number()
    if number_of_total_points > evaluation_size:
        gd.random_eval_check = True
    else:
        eval_pool = data_point_finder(thread_pool_bound)
        gd.eval_pool = eval_pool
        gd.random_eval_check = False


def evaluation_point_number():
    number_of_points = 1
    for i in range(parameter_count):
        number_of_points = number_of_points*(thread_pool_bound[i][1] - thread_pool_bound[i][0])

    return number_of_points
