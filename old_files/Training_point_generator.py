import numpy as np
from simulation_utilities.data_generations.simulation_get_performance import simulation_get_performance

'''
Training points selection for the simulation
Number of training points were decided based on the number in config file
'''


# get the initial points
def get_training_points(number_of_training_points, parameter_bounds, feature_bounds=None):
    optimize_data = []
    object_data = []

    if feature_bounds is None:
        for training_points in range(0, number_of_training_points):
            optimize_value = []
            for i in range(len(parameter_bounds)):
                optimize_value.append(np.random.randint(parameter_bounds[i][0], parameter_bounds[i][1]))

            object_data.append(simulation_get_performance(optimize_value))
            optimize_data.append(optimize_value)

        print("Initial Parameter length", len(optimize_data))
        print("Initial object length", len(object_data))

        print("Initial Parameter", optimize_data)
        print("Initial object", object_data)

        return optimize_data, object_data

    else:
        for training_points in range(0, number_of_training_points):
            optimize_value = []
            for i in range(len(parameter_bounds)):
                # optimize_value.append(round(np.random.uniform(parameter_bounds[i][0], parameter_bounds[i][1]), 2))
                optimize_value.append(np.random.randint(parameter_bounds[i][0], parameter_bounds[i][1]))

            for j in range(len(feature_bounds)):
                # optimize_value.append(round(np.random.uniform(feature_bounds[j][0], feature_bounds[j][1]), 2))
                optimize_value.append(np.random.randint(feature_bounds[j][0], feature_bounds[j][1]))

            object_data.append(simulation_get_performance(optimize_value))
            optimize_data.append(optimize_value)

        print("Initial Parameter length", len(optimize_data))
        print("Initial object length", len(object_data))

        print("Initial Parameter", optimize_data)
        print("Initial object", object_data)

        return optimize_data, object_data
