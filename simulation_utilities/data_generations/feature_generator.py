from simulation_utilities import ploting
import numpy as np
import Config_simulation as Config

step_num = 10


def feature_generator(function_name, bounds):
    lower = bounds[0]
    upper = bounds[1]

    if function_name == 'STEP_INCREASE_FUNCTION':
        data = step_increase_function(lower, upper)
    elif function_name == 'STEP_DECREASE_FUNCTION':
        data = step_decrease_function(lower, upper)

    return data


def step_increase_function(lower, upper):
    data = []
    length = Config.NUMBER_OF_ITERATIONS
    value = lower
    step = np.round((upper - lower) / np.round(length/step_num))
    for i in range(length):
        if i % step_num == 0:
            value = value + step
        data.append(value)
    ploting.general_plot(data)
    return data


def step_decrease_function(lower, upper):
    data = []
    length = Config.NUMBER_OF_ITERATIONS
    value = upper
    step = (upper - lower) / np.round(length/step_num)
    for i in range(length):
        if i % step_num == 0:
            value = int(value - step)
        data.append(value)
    ploting.general_plot(data)
    return data
