import Config as Cg
from general_utilities import bayesian_opt
from general_utilities.minimum_point_finder import min_point_find

thread_pool_min = Cg.thread_pool_min
thread_pool_max = Cg.thread_pool_max


def each_point_analysis(one_parameter, x_data, y_data, trade_off_level, model, feature_val=None):

    if one_parameter:
        minimum = min(y_data)
        x_location = y_data.index(min(y_data))
        min_x = x_data[x_location]
    else:
        minimum, min_x, trade_off_level = min_point_find(x_value=x_data, y_value=y_data,
                                                         feature_val=feature_val,
                                                         trade_off_level=trade_off_level)

    max_expected_improvement = 0
    max_points = []

    for evaluating_pool_size in range(thread_pool_min, thread_pool_max + 1):
        if one_parameter:
            pool_size = evaluating_pool_size
        else:
            pool_size = [evaluating_pool_size, feature_val]

        max_expected_improvement, max_points = bayesian_opt.bayesian_expected_improvement(
            pool_size, max_expected_improvement, max_points, minimum, trade_off_level, model)

    next_x, next_y, trade_off_level = bayesian_opt.next_x_point_selection(
        max_expected_improvement, min_x, trade_off_level, max_points, one_parameter)

    return next_x, next_y, max_expected_improvement, minimum, min_x, trade_off_level
