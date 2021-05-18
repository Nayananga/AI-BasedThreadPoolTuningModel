import logging

import pandas as pd

import config
import global_data


def generate_data():
    """initial threadpool_data Configuration"""
    initialize_configurations()
    threadpool_data, latency_data, throughput_data = get_training_points()
    find_initial_min_data(threadpool_data, latency_data, throughput_data)

    return threadpool_data, latency_data, throughput_data


def initialize_configurations():
    """
    Find out whether the number of parameter points to check in one bayesian optimization is greater than
    the number of evaluation points configured.
    """

    thread_pool_bound = config.PARAMETER_BOUNDS

    if len(thread_pool_bound) == 0:
        logging.error("Parameter bounds are not defined")
    else:
        logging.info("Everything is defined properly")

    number_of_points = thread_pool_bound[1] - thread_pool_bound[0]

    if number_of_points > config.EVAL_POINT_SIZE:
        global_data.random_eval_check = True
    else:
        global_data.eval_pool = list(range(thread_pool_bound[0], thread_pool_bound[1]))
        global_data.random_eval_check = False


def get_training_points():
    folder_name = config.TRAINING_DATA_PATH + '/' + config.TEST_NAME
    train_data = pd.read_csv(folder_name + '/train_data.csv')

    threadpool_data = train_data["Thread pool size"].tolist()
    latency_data = train_data["99th percentile Latency"].tolist()
    throughput_data = train_data["Current 10 Second Throughput"].tolist()

    return threadpool_data, latency_data, throughput_data


def find_initial_min_data(threadpool_data, target_data, feature_data):
    min_threadpool_data = []
    min_target_data = []
    min_feature_data = []
    for i, feature_value in enumerate(feature_data):
        if feature_value not in min_feature_data:
            min_target_value = min(
                [target_data[i] for i, f_value in enumerate(feature_data) if
                 f_value == feature_value])

            min_threadpool_data.append(threadpool_data[target_data.index(min_target_value)])
            min_target_data.append(min_target_value)
            min_feature_data.append(feature_value)

        else:
            pass

    global_data.min_threadpool_data = min_threadpool_data
    global_data.min_target_data = min_target_data
    global_data.min_feature_data = min_feature_data
