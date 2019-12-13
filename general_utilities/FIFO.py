import numpy as np
import Config

'''
FIFO calculation in y direction of the gaussian process
According to the variance in distribution in Y direction data was removed
'''

maximum_in_sampler = 5
variance_threshold = 50


def fifo_sampling(next_x, x_data, y_data, trade_off_level):

    point_locations = index_get(next_x, x_data)
    number_of_points = len(point_locations)

    if number_of_points > 1:
        variance = variance_calculation(number_of_points, point_locations, y_data)
        if variance >= variance_threshold:
            x_data, y_data = remove_data(number_of_points, point_locations, x_data, y_data)
            trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL
        elif number_of_points >= maximum_in_sampler:
            x_data.remove(x_data[point_locations[0]])
            y_data.remove(y_data[point_locations[0]])

    return x_data, y_data, trade_off_level


def remove_data(number_of_points, point_locations, x_data, y_data):
    for i in range(number_of_points - 1, -1, -1):
        x_data.remove(x_data[point_locations[i]])
        y_data.remove(y_data[point_locations[i]])

    return x_data, y_data


def index_get(value, data):

    index_p_val = []
    if type(value) == list or type(value) == tuple:
        p_val = value
    else:
        p_val = list(value)

    for i in range(len(data)):
        darsdf = data[i]
        if data[i] == p_val:
            index_p_val.append(i)

    return index_p_val

"""
Variance is calculated according of the given distribution
"""


def variance_calculation(number_of_points, point_locations, y_data):
    variance_matrix = []

    for i in range(number_of_points):
        variance_matrix.append(y_data[point_locations[i]])

    variance = np.var(variance_matrix)
    return variance
