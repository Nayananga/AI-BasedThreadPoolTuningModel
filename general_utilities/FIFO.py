import numpy as np

import Config

'''
FIFO calculation in y direction of the gaussian process
According to the variance in distribution in Y direction data was removed
'''

maximum_in_sampler = 5
variance_threshold = 50


def sample_by_fifo(next_x, x_data, y_data, trade_off_level):
    point_locations = get_index(next_x, x_data)
    points = [[x_data[i], y_data[i]] for i in point_locations]
    number_of_points = len(point_locations)

    if number_of_points > 1:
        variance = calculate_variance(points)
        if variance >= variance_threshold:
            x_data, y_data = remove_data(number_of_points, points, x_data, y_data)
            trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL
        elif number_of_points >= maximum_in_sampler:
            x_data.remove(points[0][0])
            y_data.remove(points[0][1])

    return x_data, y_data, trade_off_level


def get_index(value, data):
    return [i for i, data_item in enumerate(data) if data_item == value]


def calculate_variance(points):
    """
    Variance is calculated according of the given distribution
    """

    variance_matrix = [i[1] for i in points]
    variance = np.var(variance_matrix)

    return variance


def remove_data(number_of_points, points, x_data, y_data):
    for i in range(number_of_points - 1, -1, -1):
        x_data.remove(points[i][0])
        y_data.remove(points[i][1])

    return x_data, y_data
