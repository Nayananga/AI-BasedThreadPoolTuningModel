import config
from general_utilities.predict_functions import find_min_threadpool_size_based_on_distance, \
    find_min_point_based_on_model, generate_random_eval_points, find_min_target_value_based_on_distance


def find_next_threadpool_size(target_value, feature_value, trade_off_level, model):
    next_threadpool_size = None

    if config.SELECTION_METHOD == "Random":
        next_threadpool_size = generate_random_eval_points(1, config.PARAMETER_BOUNDS).pop()

    elif config.SELECTION_METHOD == "From_model":

        estimated_min_target = find_min_target_value_based_on_distance(feature_value)

        if estimated_min_target < target_value:
            threadpool_sizes, max_expected_improvement = find_min_point_based_on_model(
                estimated_min_target, feature_value, model, 0.01)
        else:
            threadpool_sizes, max_expected_improvement = find_min_point_based_on_model(
                target_value, feature_value, model, trade_off_level)

        next_threadpool_size, trade_off_level = select_next_threadpool_size(
            max_expected_improvement, feature_value, trade_off_level, threadpool_sizes)

    elif config.SELECTION_METHOD == "Nearest_point":
        next_threadpool_size = find_min_threadpool_size_based_on_distance(feature_value)

    return next_threadpool_size, trade_off_level


def select_next_threadpool_size(max_expected_improvement, feature_value, trade_off_level, threadpool_sizes):
    if not max_expected_improvement:
        print("WARN: Maximum expected improvement was 0")
        next_threadpool_size = find_min_threadpool_size_based_on_distance(feature_value)
        trade_off_level = trade_off_level - (trade_off_level / 10)
        if trade_off_level < 0.00001:
            trade_off_level = 0
    else:
        print("check", len(threadpool_sizes))
        next_threadpool_size = min(threadpool_sizes)
        trade_off_level = trade_off_level + (trade_off_level / 8)

        if trade_off_level > 0.01:
            trade_off_level = 0.01
        elif trade_off_level == 0:
            trade_off_level = 0.00002

    return next_threadpool_size, trade_off_level
