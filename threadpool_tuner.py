import random

from general_utilities.Bayesian_point_selection import estimate_minimum_point, generate_min_point_based_on_distance
from general_utilities.FIFO import sample_by_fifo
from general_utilities.gaussian_process import gpr


def find_next_threadpool_size(trade_off_level, model, feature_value):
    max_threadpool_sizes, max_expected_improvement = estimate_minimum_point(
        feature_value, model, explore_factor=trade_off_level)

    next_threadpool_size, trade_off_level = select_next_threadpool(
        max_expected_improvement, feature_value, trade_off_level, max_threadpool_sizes)

    return next_threadpool_size, trade_off_level


def select_next_threadpool(max_expected_improvement, feature_value, trade_off_level, max_threadpool_sizes):
    if not max_expected_improvement:
        print("WARN: Maximum expected improvement was 0")
        next_threadpool_size, _minimum_feature_value = generate_min_point_based_on_distance(feature_value)
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

    return next_threadpool_size, trade_off_level


def update_model(next_threadpool_size, threadpool_data, feature_data, trade_off_level):
    threadpool_data, feature_data, trade_off_level = sample_by_fifo(next_threadpool_size,
                                                                    threadpool_data,
                                                                    feature_data, trade_off_level)

    # fit new threadpool_data to gaussian process
    model = gpr(threadpool_data, feature_data)

    return threadpool_data, feature_data, trade_off_level, model
