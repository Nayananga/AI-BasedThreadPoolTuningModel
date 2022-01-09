from general_utilities.bayesian_opt import next_x_point_selection
from general_utilities.Bayesian_point_selection import generate_min_point
from general_utilities.gaussian_process import GPR


def find_next_threadpool_size(
        trade_off_level,
        model,
        feature_value,
        object_value):
    (
        max_expected_improvement,
        min_threadpool_size,
        max_threadpool_sizes,
    ) = generate_min_point(feature_value, object_value, model)

    next_threadpool_size, trade_off_level = next_x_point_selection(
        max_expected_improvement,
        min_threadpool_size,
        trade_off_level,
        max_threadpool_sizes,
    )
    # select a random threadpool_size from max_threadpool_sizes

    return next_threadpool_size, trade_off_level


def update_model(threadpool_and_throughput_data, latency_data):

    # fit new data to gaussian process
    model = GPR(threadpool_and_throughput_data, latency_data)

    return model
