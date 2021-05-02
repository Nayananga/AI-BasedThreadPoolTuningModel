import logging

import pandas as pd

import Config

parameter_names = Config.PARAMETERS
parameter_bounds = Config.PARAMETER_BOUNDS
parameter_count = Config.NUMBER_OF_PARAMETERS

feature_names = Config.FEATURE
feature_bounds = Config.FEATURE_BOUNDS
feature_count = Config.NUMBER_OF_FEATURES


def data_generation_ini():
    config_errors()
    optimize_data, object_data = get_training_points()
    return optimize_data, object_data


def config_errors():
    feature_function = Config.FEATURE_FUNCTION

    if len(parameter_names) != len(parameter_bounds):
        logging.error("Parameter names or bounds are not defined properly")
    elif len(parameter_names) == 0:
        logging.error("Parameter names are not defined")
    elif len(parameter_bounds) == 0:
        logging.error("Parameter bounds are not defined")
    elif len(feature_names) != len(feature_bounds) or len(feature_names) != len(feature_function):
        logging.error("Feature names or bounds or functions are not defined properly")
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
