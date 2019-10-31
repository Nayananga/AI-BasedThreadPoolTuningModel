import Config as Cg
from general_utilities.performance_collection import get_performance

# bounds for the gaussian
thread_pool_max = Cg.thread_pool_max
thread_pool_min = Cg.thread_pool_min

x_data = []
y_data = []
parameter_history = []


# get the initial points
def get_initial_points(number_of_initial_points, feature=None):
    for initial_point in range(0, (number_of_initial_points+1)):

        thread_pool_value = thread_pool_min+initial_point*(thread_pool_max - thread_pool_min)/number_of_initial_points
        thread_pool_value = int(thread_pool_value)

        if feature is None:
            y_data.append(get_performance(thread_pool_value))
            x_data.append([thread_pool_value])
            parameter_history.append([thread_pool_value])
        else:
            x_temp = []
            y_temp = get_performance(thread_pool_value, feature[initial_point])
            y_data.append(y_temp)
            x_temp.append(thread_pool_value)
            x_temp.append(feature[initial_point])
            x_data.append(x_temp)
            parameter_history.append(x_temp)

    return x_data, y_data, parameter_history
