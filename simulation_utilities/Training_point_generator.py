import numpy as np

import Config as Cg
from general_utilities.performance_collection import get_performance

'''
Training points selection for the simulation
Number of taining points were decided based on the number in config file
'''

# bounds for the gaussian
thread_pool_max = Cg.thread_pool_max
thread_pool_min = Cg.thread_pool_min

feature_max = Cg.feature_max
feature_min = Cg.feature_min

x_data = []
y_data = []
parameter_history = []


# get the initial points
def get_training_points(number_of_training_points, feature=None):
    for training_points in range(0, (number_of_training_points+1)):

        if feature is None:
            thread_pool_value = thread_pool_min + training_points * (
                        thread_pool_max - thread_pool_min) / number_of_training_points
            thread_pool_value = int(thread_pool_value)
            y_data.append(get_performance(thread_pool_value))
            x_data.append([thread_pool_value])
            parameter_history.append([thread_pool_value])
        else:
            thread_pool_value = np.random.randint(thread_pool_min, thread_pool_max)
            feature_value = np.random.randint(feature_min, feature_max)
            x_temp = []
            y_temp = get_performance(thread_pool_value, feature_value)
            y_data.append(y_temp)
            x_temp.append(thread_pool_value)
            x_temp.append(feature_value)
            x_data.append(x_temp)
            parameter_history.append(x_temp)

    return x_data, y_data, parameter_history
