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
    elif function_name == 'CONSTANT':
        constant = np.random.randint(lower, upper)
        print(constant)
        data = constant_value(constant)
    elif function_name == 'PEAKS':
        data = generating_peaks(lower, upper)

    return data


def step_increase_function(lower, upper):
    data = []
    step_num = 20
    length = Config.NUMBER_OF_ITERATIONS
    value = lower
    step = np.round((upper - lower) / np.round(length/step_num))
    for i in range(length):
        if i % step_num == 0:
            value = value + step
            if value >= upper:
                value = upper-1
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
            if value < lower:
                value = lower
        data.append(value)
    data_plot.general_plot(data)
    return data


def up_and_down_function(lower, upper):
    data = []
    length = Config.NUMBER_OF_ITERATIONS
    step_num = round(length/5)

    value = np.random.randint(lower, upper/2)
    for i in range(length):
        if i % step_num == 0 and i is not 0:
            value = np.random.randint(lower, upper)
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


def constant_value(constant):
    data = []
    length = Config.NUMBER_OF_ITERATIONS
    value = constant
    for i in range(length):
        data.append(value)
    data_plot.general_plot(data)
    return data


def generating_peaks(lower, upper):
    data = []
    step_num = 30
    check_iter = 0
    length = Config.NUMBER_OF_ITERATIONS
    value = np.random.randint(lower, upper/3)
    for i in range(length):
        if i == 0:
            value_old = value
        elif i % step_num == 0:
            value = np.random.randint(upper/2, upper)
            check_iter = i
        elif i == (int(check_iter)+2):
            value = value_old
        data.append(value)
    data_plot.general_plot(data)
    return data
