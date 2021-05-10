import logging

import pandas as pd

import Config

parameter_bounds = Config.PARAMETER_BOUNDS


def initialize_data_generation():
    check_config_errors()
    thread_data, latency_data, throughput_data = get_training_points()
    return thread_data, latency_data, throughput_data


def check_config_errors():
    if len(parameter_bounds) == 0:
        logging.error("Parameter bounds are not defined")
    else:
        logging.info("Everything is defined properly")


def get_training_points():
    folder_name = Config.TRAINING_DATA_PATH + '/' + Config.TEST_NAME
    train_data = pd.read_csv(folder_name + '/train_data.csv')

    threadpool_data = train_data["Thread pool size"].tolist()
    latency_data = train_data["99th percentile Latency"].tolist()
    throughput_data = train_data["Current 10 Second Throughput"].tolist()

    return threadpool_data, latency_data, throughput_data
