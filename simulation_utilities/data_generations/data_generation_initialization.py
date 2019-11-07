# import Config_simulation as Config
import numpy as np
import Config_simulation_para_and_feature as Config
from simulation_utilities.data_generations.feature_generator import feature_generator
import logging
from simulation_utilities import ploting
from simulation_utilities.Training_point_generator import get_training_points
from simulation_utilities.simulation_function_generator import function_generation
from general_utilities import global_data
from simulation_utilities.initial_data_assign import initial_runs
import sys
from simulation_utilities.data_generations.min_data_generator import min_data_generator

parameter_names = Config.PARAMETERS
parameter_bounds = Config.PARAMETER_BOUNDS
feature_names = Config.FEATURE
feature_bounds = Config.FEATURE_BOUNDS
feature_function = Config.FEATURE_FUNCTION

relation_function = Config.FUNCTION
number_of_initial_points = Config.NUMBER_OF_TRAINING_POINTS


def data_generation_ini():

    parameter_count, feature_count = config_errors()

    if feature_count == 0:
        parameter_plot_data = data_generator(parameter_bounds)
        function_generation(parameter_plot_data)
        parameter_data, optimizer_data = get_training_points(number_of_initial_points, parameter_bounds)
        return parameter_data, optimizer_data, parameter_plot_data
    else:
        feature_changing_data = feature_data_generation()
        parameter_plot_data = data_generator(parameter_bounds)
        feature_plot_data = data_generator(feature_bounds)
        #function_generation(parameter_plot_data, feature_plot_data)
        parameter_data, optimizer_data, feature_data = get_training_points(number_of_initial_points, parameter_bounds, feature_bounds)
        return parameter_data, optimizer_data, feature_data, parameter_plot_data, feature_plot_data, feature_changing_data
"""
    if parameter_count == 1 and feature_count == 0:
        print("one")
        parameter_plot_data = data_generator(parameter_bounds)
        optimizer_plot_data = function_generation(parameter_plot_data)
        ploting.initial_plot(parameter_plot_data, optimizer_plot_data)
        global_data.parameter_plot_data = parameter_plot_data
        global_data.optimizer_plot_data = optimizer_plot_data

        # parameter_data, optimizer_data, parameter_history = get_training_points_parameter_only(
        # number_of_initial_points, parameter_bounds[0][0], parameter_bounds[0][1])

    elif (parameter_count == 1 and feature_count == 1) or (parameter_count == 2):
        print("one_each")
        feature_data = feature_data_generation()
        parameter_plot_data = data_generator(parameter_bounds)
        feature_plot_data = data_generator(feature_bounds)
        parameter_plot_data, feature_plot_data = np.meshgrid(parameter_plot_data, feature_plot_data)
        print(len(feature_plot_data))
        print(len(parameter_plot_data))
        optimizer_plot_data = function_generation(parameter_plot_data, feature_plot_data)
        print(len(optimizer_plot_data))
        # ploting.initial_2d_plot(parameter_bounds[0][0], parameter_bounds[0][1],
        #                         feature_bounds[0][0], feature_bounds[0][1])
        ploting.initial_2d_plot(parameter_bounds[0][0], parameter_bounds[0][1],
                                parameter_bounds[1][0], parameter_bounds[1][1])
    else:
        if feature_count == 0:
            parameter_plot_data = data_generator(parameter_bounds)
            optimizer_plot_data = function_generation(parameter_plot_data)
        else:
            feature_data = feature_data_generation()
            parameter_plot_data = data_generator(parameter_bounds)
            feature_plot_data = data_generator(feature_bounds)
            optimizer_plot_data = function_generation(parameter_plot_data, feature_plot_data)
            
    """

#min_data_generator(relation_function, parameter_bounds, feature_bounds)


def config_errors():
    if len(parameter_names) != len(parameter_bounds):
        logging.error("Parameter names or bounds are not defined properly")
    elif len(parameter_names) == 0:
        logging.error("Parameter names are not defined")
    elif len(parameter_bounds) == 0:
        logging.error("Parameter bounds are not defined")
    elif len(feature_names) != len(feature_bounds) or len(feature_names) != len(feature_function):
        logging.error("Feature names or bounds or functions are not defined properly")
    else:
        return len(parameter_names), len(feature_names)


def feature_data_generation():
    feature_changing_data = []
    for i in range(len(feature_names)):
        feature_changing_data.append(feature_generator(feature_function[i], feature_bounds[i]))
    return feature_changing_data


def data_generator(data_bounds):
    data = []
    for i in range(len(data_bounds)):
        bounds = np.array([[data_bounds[i][0], data_bounds[i][1]]])
        data.append(np.arange(bounds[:, 0], bounds[:, 1], 1).reshape(-1, 1))
    return data



