import random

from general_utilities.predict_functions import find_min_point_based_on_model


def find_next_threadpool_size(current_threadpool_size, target_value, feature_value, trade_off_level, model):
    threadpool_sizes, max_expected_improvement = find_min_point_based_on_model(
        target_value, feature_value, model, trade_off_level)

    next_threadpool_size, trade_off_level = select_next_threadpool_size(
        max_expected_improvement, trade_off_level, threadpool_sizes, current_threadpool_size)

    return next_threadpool_size, trade_off_level


def select_next_threadpool_size(max_expected_improvement, trade_off_level, threadpool_sizes, current_threadpool_size):
    if max_expected_improvement:
        print("check", len(threadpool_sizes))
        next_threadpool_size = random.choice(threadpool_sizes)
        trade_off_level = trade_off_level + (trade_off_level / 8)

        if trade_off_level > 0.01:
            trade_off_level = 0.01
        elif trade_off_level == 0:
            trade_off_level = 0.00002
    else:
        print("WARN: Maximum expected improvement was 0")
        next_threadpool_size = current_threadpool_size
        trade_off_level = trade_off_level - (trade_off_level / 10)
        if trade_off_level < 0.00001:
            trade_off_level = 0

    return next_threadpool_size, trade_off_level
