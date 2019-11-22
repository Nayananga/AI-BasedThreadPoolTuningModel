import Config_simulation as Config
import global_data as gd
from general_utilities.commom_functions import *

eval_point_size = Config.EVAL_POINT_SIZE
parameter_bounds = Config.PARAMETER_BOUNDS
parameter_count = Config.NUMBER_OF_PARAMETERS

feature_bounds = Config.FEATURE_BOUNDS
feature_count = Config.NUMBER_OF_PARAMETERS


def initial_configurations():
    number_of_total_points = evaluation_point_number()
    if number_of_total_points > eval_point_size:
        gd.random_eval_check = True
    else:
        gd.random_eval_check = False
        gd.eval_pool = data_point_finder(parameter_bounds)


def evaluation_point_number():
    number_of_points = 1
    for i in range(parameter_count):
        number_of_points = number_of_points*(parameter_bounds[i][1] - parameter_bounds[i][0])
    """if feature_count > 0:
        feature_bound = feature_bounds
        for j in range(feature_count):
            number_of_points = number_of_points*(feature_bound[j][1] - feature_bound[j][0])"""

    return number_of_points

"""
if __name__ == "__main__":
    initial_configurations()"""
