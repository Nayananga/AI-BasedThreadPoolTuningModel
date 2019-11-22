import Config_simulation as Config
from simulation_utilities.data_generations.simulation_get_performance import simulation_get_performance
import itertools

def min_data_generator(parameters, features=None):
    minimum_y = 0
    minimum_x = 0
    if features is None:
        optimizing_data = data_combine(parameters)
    else:
        optimizing_data = data_combine(parameters, features)

    for i in range(len(optimizing_data)):
        y_data = simulation_get_performance(optimizing_data[i])
        if i == 0:
            minimum_y = y_data
            minimum_x = optimizing_data[i]
        else:
            if minimum_y > y_data:
                minimum_y = y_data
                minimum_x = optimizing_data[i]

        return minimum_x, minimum_y


def data_combine(parameters, features=None):
    data = parameters
    if features is not None:
        for i in range(len(features)):
            data.append(features[i])
        combined_data = list(itertools.product(*data))
    else:
        if Config.NUMBER_OF_PARAMETERS == 1:
            combined_data = data
        else:
            combined_data = list(itertools.product(*data))

    return combined_data

