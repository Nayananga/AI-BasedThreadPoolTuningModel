import logging

import pandas as pd

import global_data as gd
from general_utilities import data_plot
from general_utilities.commom_functions import *
from old_files.sample_system import sample_system

parameter_names = Config.PARAMETERS
parameter_bounds = Config.PARAMETER_BOUNDS
parameter_count = Config.NUMBER_OF_PARAMETERS

feature_names = Config.FEATURE
feature_bounds = Config.FEATURE_BOUNDS
feature_count = Config.NUMBER_OF_FEATURES


def data_generation_ini():
    config_errors()

    if feature_count == 0:
        optimizer_plot_data = data_point_finder(parameter_bounds)
        parameter_data, optimizer_data = get_training_points()
        if parameter_count == 1:
            object_plot_data = []
            for i in range(len(optimizer_plot_data)):
                object_plot_data.append(sample_system(optimizer_plot_data[i]))
            gd.optimizer_plot_data = optimizer_plot_data
            gd.object_plot_data = object_plot_data
            data_plot.initial_plot(optimizer_plot_data, object_plot_data)
        return parameter_data, optimizer_data
    else:
        feature_changing_data = read_feature_data()
        optimize_data, object_data = get_training_points()
        return optimize_data, object_data, feature_changing_data


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


def read_feature_data():
    folder_name = Config.ROOT_PATH + 'Workload_data/'
    file_name = Config.FEATURE_FUNCTION[0]
    actual_data = pd.read_csv(folder_name + file_name + '.csv')

    out_feature_data = []

    feature_data = actual_data.iloc[:, 0]
    for feature_point in feature_data:
        point = [feature_point]
        out_feature_data.append(point)

    return out_feature_data


def get_training_points():
    folder_name = Config.ROOT_PATH + 'Training_data/'
    latency = pd.read_csv(folder_name + 'latency_training_data.csv')
    thread = pd.read_csv(folder_name + 'threadpool_and_concurrency_training_data.csv')

    object_data = []
    optimize_data = []

    latency_data = latency.iloc[:, 0]
    thread_data = thread.iloc[:, 0]
    feature_data = thread.iloc[:, 1]

    for latency_point in latency_data:
        point = latency_point
        object_data.append(point)

    for i, thread_point in enumerate(thread_data):
        point = [thread_point, feature_data[i]]
        optimize_data.append(point)

    return optimize_data, object_data
