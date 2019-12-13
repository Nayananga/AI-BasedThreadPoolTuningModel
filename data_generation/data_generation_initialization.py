import logging

from data_generation.feature_generator import feature_generator
from general_utilities import data_plot
from old_files.sample_system import sample_system
from general_utilities.commom_functions import *
import Config as Config
import global_data as gd

parameter_names = Config.PARAMETERS
parameter_bounds = Config.PARAMETER_BOUNDS
parameter_count = Config.NUMBER_OF_PARAMETERS

feature_names = Config.FEATURE
feature_bounds = Config.FEATURE_BOUNDS
feature_count = Config.NUMBER_OF_FEATURES
feature_function = Config.FEATURE_FUNCTION

relation_function = Config.FUNCTION
number_of_initial_points = Config.NUMBER_OF_TRAINING_POINTS


def data_generation_ini():
    config_errors()

    if feature_count == 0:
        optimizer_plot_data = data_point_finder(parameter_bounds)
        # ref_min_optimizer, ref_min_object = ref_min_data_finder(optimizer_plot_data)
        parameter_data, optimizer_data = get_training_points(number_of_initial_points, parameter_bounds)
        if parameter_count == 1:
            object_plot_data = []
            for i in range(len(optimizer_plot_data)):
                object_plot_data.append(sample_system(optimizer_plot_data[i]))
            gd.optimizer_plot_data = optimizer_plot_data
            gd.object_plot_data = object_plot_data
            data_plot.initial_plot(optimizer_plot_data, object_plot_data)
        # return parameter_data, optimizer_data, ref_min_optimizer, ref_min_object
        return parameter_data, optimizer_data
    else:
        feature_changing_data = feature_data_generation()
        optimizer_plot_data = data_point_finder(parameter_bounds, feature_bounds)
        # ref_min_optimizer, ref_min_object = ref_min_data_finder(optimizer_plot_data)
        optimize_data, object_data = get_training_points(number_of_initial_points, parameter_bounds, feature_bounds)
        # return optimize_data, object_data, feature_changing_data, ref_min_optimizer, ref_min_object
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


def feature_data_generation():
    feature_function = Config.FEATURE_FUNCTION

    feature_changing_data = []
    for i in range(len(feature_names)):
        feature_changing_data.append(feature_generator(feature_function[i], feature_bounds[i]))
    feature_changing_data = list(map(list, zip(*feature_changing_data)))
    return feature_changing_data


def data_generator(data_bounds):
    data = []
    for i in range(len(data_bounds)):
        temp_collect = []
        bounds = np.array([[data_bounds[i][0], data_bounds[i][1]]])
        temp = (np.arange(bounds[:, 0], bounds[:, 1], 1).reshape(-1, 1))
        for j in range(len(temp)):
            temp_collect.append(temp[j][0])
        data.append(temp_collect)
    return data


def ref_min_data_finder(optimize_data):
    object_data = []
    for i in range(len(optimize_data)):
        object_data.append(sample_system(optimize_data[i]))

    if feature_count == 0:
        minimum_x_data, minimum_y_data = min_point_find_no_feature(optimize_data, object_data)
    else:
        minimum_x_data, minimum_y_data = ini_min_point_find_with_feature(optimize_data, object_data)

    return minimum_x_data, minimum_y_data


def get_training_points(number_of_training_points, para_bounds, feat_bounds=None):
    object_data = []
    if feat_bounds is None:
        optimize_data = selecting_random_point(number_of_training_points, para_bounds)
    else:
        optimize_data = selecting_random_point(number_of_training_points, para_bounds, feat_bounds)

    for i in range(len(optimize_data)):
        object_data.append(sample_system(optimize_data[i]))

    return optimize_data, object_data


