import numpy as np
from general_utilities.performance_collection import get_performance
from simulation_utilities.simulation_function_generator import function_generation

'''
Training points selection for the simulation
Number of taining points were decided based on the number in config file
'''


# get the initial points
def get_training_points(number_of_training_points, parameter_bounds, feature_bounds=None):
    parameter_data = []
    feature_data = []
    optimizer_data = []

    if feature_bounds is None:
        for training_points in range(0, number_of_training_points):
            parameter_values = []
            for i in range(len(parameter_bounds)):
                parameter_values.append(np.random.randint(parameter_bounds[i][0], parameter_bounds[i][1]))

            optimizer_data.append(function_generation(parameter_values))
            parameter_data.append(parameter_values)

        print(len(parameter_data))
        print(len(optimizer_data))

        return parameter_data, optimizer_data

    else:
        for training_points in range(0, number_of_training_points):
            parameter_values = []
            feature_values = []
            for i in range(len(parameter_bounds)):
                parameter_values.append(np.random.randint(parameter_bounds[i][0], parameter_bounds[i][1]))

            for j in range(len(feature_bounds)):
                feature_values.append(np.random.randint(feature_bounds[j][0], feature_bounds[j][1]))

            parameter_data.append(parameter_values)
            feature_data.append(feature_values)
            optimizer_data.append(function_generation(parameter_values, feature_values))

        print(len(parameter_data))
        print(len(optimizer_data))
        print(len(feature_data))

        return parameter_data, optimizer_data, feature_data
