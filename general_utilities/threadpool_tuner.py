import random

import config
from general_utilities.predict_functions import generate_min_point_based_on_distance, \
    generate_min_point_based_on_model, generate_random_eval_points


def find_next_threadpool_size(target_value, feature_value, trade_off_level, model):
    next_threadpool_size = None

    if config.SELECTION_METHOD == "Random":
        next_threadpool_size = generate_random_eval_points(1, config.PARAMETER_BOUNDS).pop()

    elif config.SELECTION_METHOD == "From_model":
        min_threadpool_sizes, max_expected_improvement = generate_min_point_based_on_model(
            target_value, feature_value, model, trade_off_level)

        next_threadpool_size, trade_off_level = select_next_threadpool_size(
            max_expected_improvement, target_value, trade_off_level, min_threadpool_sizes)

    elif config.SELECTION_METHOD == "Nearest_point":
        next_threadpool_size = generate_min_point_based_on_distance(target_value)

    return next_threadpool_size, trade_off_level


def select_next_threadpool_size(max_expected_improvement, target_value, trade_off_level, max_threadpool_sizes):
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
