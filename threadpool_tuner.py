import Config
import global_data
from general_utilities.Bayesian_point_selection import update_min_point
from general_utilities.FIFO import fifo_sampling
from general_utilities.bayesian_opt import bayesian_expected_improvement, next_x_point_selection
from general_utilities.data_generator import selecting_random_point
from general_utilities.gaussian_process import gpr


def find_next_threadpool_size(threadpool_and_throughput_data, latency_data, trade_off_level, model, throughput):
    min_threadpool_size, min_latency = update_min_point(threadpool_and_throughput_data, latency_data,
                                                        throughput, model)

    if min_latency is None:
        next_threadpool_size = min_threadpool_size
        trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL

    else:
        max_expected_improvement = 0
        max_threadpool_sizes = []

        if not global_data.random_eval_check:
            eval_pool = global_data.eval_pool
        else:
            eval_pool = selecting_random_point(Config.EVAL_POINT_SIZE, Config.PARAMETER_BOUNDS)

        for eval_point in eval_pool:
            check_point = list(eval_point)
            for throughput_val in throughput:
                check_point.append(throughput_val)

            max_expected_improvement, max_threadpool_sizes = bayesian_expected_improvement(
                check_point, max_expected_improvement, max_threadpool_sizes, min_latency, trade_off_level, model)

        next_threadpool_size, trade_off_level = next_x_point_selection(
            max_expected_improvement, min_threadpool_size, trade_off_level, max_threadpool_sizes)

    return next_threadpool_size, trade_off_level


def update_model(next_threadpool_size, threadpool_and_throughput_data, latency_data, trade_off_level):
    threadpool_and_throughput_data, latency_data, trade_off_level = fifo_sampling(next_threadpool_size,
                                                                                  threadpool_and_throughput_data,
                                                                                  latency_data, trade_off_level)

    # fit new data to gaussian process
    model = gpr(threadpool_and_throughput_data, latency_data)

    return threadpool_and_throughput_data, latency_data, trade_off_level, model
