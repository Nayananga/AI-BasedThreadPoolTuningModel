import logging

import pandas as pd

import Config

parameter_bounds = Config.PARAMETER_BOUNDS


def data_generation_ini():
    config_errors()
    optimize_data, object_data = get_training_points()
    return optimize_data, object_data


def config_errors():
    if len(parameter_bounds) == 0:
        logging.error("Parameter bounds are not defined")
    else:
        logging.info("Everything is defined properly")


def get_training_points():
    folder_name = Config.TRAINING_DATA_PATH + '/' + Config.TEST_NAME
    latency = pd.read_csv(folder_name + '/train_data.csv', usecols=['99th percentile Latency'])
    thread = pd.read_csv(folder_name + '/train_data.csv', usecols=['Thread pool size', 'Current 10 Second Throughput'])

    object_data = []
    optimize_data = []

    latency_data = latency.iloc[:, 0]
    thread_data = thread.iloc[:, 0]
    feature_data = thread.iloc[:, 1]

    for latency_point in latency_data:
        object_data.append(float(latency_point))

    for i, thread_point in enumerate(thread_data):
        point = [int(thread_point), float(feature_data[i])]
        optimize_data.append(point)

    return optimize_data, object_data
