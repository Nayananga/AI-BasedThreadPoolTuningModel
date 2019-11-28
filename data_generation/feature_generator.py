from general_utilities import data_plot
import numpy as np
import Config as Config


def feature_generator(function_name, bounds):
    lower = bounds[0]
    upper = bounds[1]

    if function_name == 'STEP_INCREASE_FUNCTION':
        data = step_increase_function(lower, upper)
    elif function_name == 'STEP_DECREASE_FUNCTION':
        data = step_decrease_function(lower, upper)
    elif function_name == 'UP_AND_DOWN_FUNCTION':
        data = up_and_down_function(lower, upper)
    elif function_name == 'RANDOM':
        data = random_data(lower, upper)

    return data


def step_increase_function(lower, upper):
    data = []
    step_num = 10
    length = Config.NUMBER_OF_ITERATIONS
    value = lower
    step = np.round((upper - lower) / np.round(length/step_num))
    for i in range(length):
        if i % step_num == 0:
            value = value + step
        data.append(value)
    data_plot.general_plot(data)
    return data


def step_decrease_function(lower, upper):
    data = []
    step_num = 10
    length = Config.NUMBER_OF_ITERATIONS
    value = upper
    step = (upper - lower) / np.round(length/step_num)
    for i in range(length):
        if i % step_num == 0:
            value = int(value - step)
        data.append(value)
    data_plot.general_plot(data)
    return data


def up_and_down_function(lower, upper):
    data = []
    length = Config.NUMBER_OF_ITERATIONS
    step_num = round(length/5)
    lower_value = round((upper-lower)/4)
    upper_value = lower_value*3
    value = lower_value
    for i in range(length):
        if i % step_num == 0:
            if value== upper_value:
                value = lower_value
            else:
                value = upper_value
        data.append(value)
    data_plot.general_plot(data)
    return data


def random_data(lower, upper):
    data = []
    length = Config.NUMBER_OF_ITERATIONS
    for i in range(length):
        if i % 2 == 0:
            value = np.random.randint(lower, upper)
        else:
            value = value
        data.append(value)
    data_plot.general_plot(data)
    return data
