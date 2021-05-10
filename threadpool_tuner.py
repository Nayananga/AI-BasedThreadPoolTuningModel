import random

import Config
from general_utilities.Bayesian_point_selection \
    import generate_min_point_based_on_distance, generate_min_point_based_on_model
from general_utilities.FIFO import sample_by_fifo
from general_utilities.data_generator import generate_random_eval_points
from general_utilities.gaussian_process import gpr


def find_next_threadpool_size(target_value, feature_value, trade_off_level, model):
    next_threadpool_size = None

    if Config.SELECTION_METHOD == "Random":
        next_threadpool_size = generate_random_eval_points(1, Config.PARAMETER_BOUNDS).pop()

    elif Config.SELECTION_METHOD == "From_model":
        min_threadpool_sizes, max_expected_improvement = generate_min_point_based_on_model(
            target_value, feature_value, model, trade_off_level)

        next_threadpool_size, trade_off_level = select_next_threadpool(
            max_expected_improvement, target_value, trade_off_level, min_threadpool_sizes)

    elif Config.SELECTION_METHOD == "Nearest_point":
        next_threadpool_size = generate_min_point_based_on_distance(target_value)

    return next_threadpool_size, trade_off_level


def select_next_threadpool(max_expected_improvement, target_value, trade_off_level, max_threadpool_sizes):
    if not max_expected_improvement:
        print("WARN: Maximum expected improvement was 0")
        next_threadpool_size = generate_min_point_based_on_distance(target_value)
        trade_off_level = trade_off_level - (trade_off_level / 10)
        if trade_off_level < 0.00001:
            trade_off_level = 0
    else:
        next_threadpool_size = random.choice(max_threadpool_sizes)
        trade_off_level = trade_off_level + (trade_off_level / 8)

        if trade_off_level > 0.01:
            trade_off_level = 0.01
        elif trade_off_level == 0:
            trade_off_level = 0.00002

    return next_threadpool_size[0][0], trade_off_level


def update_model(next_threadpool_size, threadpool_data, target_data, feature_data, trade_off_level):
    threadpool_data, target_data, feature_data, trade_off_level = sample_by_fifo(next_threadpool_size,
                                                                                 threadpool_data,
                                                                                 target_data, feature_data,
                                                                                 trade_off_level)

    # fit new threadpool_data to gaussian process
    model = gpr(threadpool_data, target_data, feature_data)

    return threadpool_data, target_data, feature_data, trade_off_level, model
