import sys

import numpy as np

import Config
from general_utilities import data_plot


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
        data = constant_value(constant)
    elif function_name == 'PEAKS':
        data = generating_peaks(lower, upper)
    elif function_name == 'ONE_STEP_FUNCTION':
        data = one_step_function(lower, upper)
    elif function_name == 'INCREASE_AND_DECREASE_FUNCTION':
        data = increase_and_decrease(lower, upper)
    else:
        print("Function are not define properly")
        sys.exit()

    data_plot.feature_function_plot(data, plot_name=function_name)
    return data


def increase_and_decrease(lower, upper):
    data = []
    length = Config.NUMBER_OF_ITERATIONS
    changing_point = round(length / 2)
    lower_concurrency = np.random.randint(lower, upper / 2)
    upper_concurrency = np.random.randint(upper / 2, upper)

    value = lower_concurrency
    step = (upper_concurrency - lower_concurrency) / changing_point
    for i in range(length):
        value = round(value + step)
        if i % changing_point == 0 and i is not 0:
            step = (-step)
        data.append(value)
    return data


def one_step_function(lower, upper):
    data = []
    length = Config.NUMBER_OF_ITERATIONS
    step_num = round(length / 2)

    value = np.random.randint(lower, upper / 2)
    for i in range(length):
        if i % step_num == 0 and i is not 0:
            value = np.random.randint(lower, upper)
        data.append(value)
    return data


def step_increase_function(lower, upper):
    data = []
    step_num = 20
    length = Config.NUMBER_OF_ITERATIONS
    value = lower
    step = np.round((upper - lower) / np.round(length / step_num))
    for i in range(length):
        if i % step_num == 0:
            value = value + step
            if value >= upper:
                value = upper - 1
        data.append(value)
    return data


def step_decrease_function(lower, upper):
    data = []
    step_num = 10
    length = Config.NUMBER_OF_ITERATIONS
    value = upper
    step = (upper - lower) / np.round(length / step_num)
    for i in range(length):
        if i % step_num == 0:
            value = int(value - step)
            if value < lower:
                value = lower
        data.append(value)
    return data


def up_and_down_function(lower, upper):
    data = []
    length = Config.NUMBER_OF_ITERATIONS
    step_num = round(length / 5)

    value = np.random.randint(lower, upper / 2)
    for i in range(length):
        if i % step_num == 0 and i is not 0:
            value = np.random.randint(lower, upper)
        data.append(value)
    return data


def random_data(lower, upper):
    value = None
    data = []
    length = Config.NUMBER_OF_ITERATIONS
    for i in range(length):
        if i % 2 == 0:
            value = np.random.randint(lower, upper)
        else:
            value = value
        data.append(value)
    return data


def constant_value(constant):
    data = []
    length = Config.NUMBER_OF_ITERATIONS
    value = constant
    for i in range(length):
        data.append(value)
    return data


def generating_peaks(lower, upper):
    value_old = None
    data = []
    step_num = 30
    check_iter = 0
    length = Config.NUMBER_OF_ITERATIONS
    value = np.random.randint(lower, upper / 3)
    for i in range(length):
        if i == 0:
            value_old = value
        elif i % step_num == 0:
            value = np.random.randint(upper / 2, upper)
            check_iter = i
        elif i == (int(check_iter) + 2):
            value = value_old
        data.append(value)
    return data
