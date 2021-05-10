import numpy as np

import Config

'''
FIFO calculation in y direction of the gaussian process
According to the variance in distribution in Y direction threadpool_data was removed
'''

maximum_in_sampler = 5
variance_threshold = 50


def sample_by_fifo(next_threadpool_size, threadpool_data, feature_data, trade_off_level):
    point_locations = get_index(next_threadpool_size, threadpool_data)
    points = [[threadpool_data[i], feature_data[i]] for i in point_locations]
    number_of_points = len(point_locations)

    if number_of_points > 1:
        variance = calculate_variance(points)
        if variance >= variance_threshold:
            threadpool_data, feature_data = remove_data(number_of_points, points, threadpool_data, feature_data)
            trade_off_level = Config.DEFAULT_TRADE_OFF_LEVEL
        elif number_of_points >= maximum_in_sampler:
            threadpool_data.remove(points[0][0])
            feature_data.remove(points[0][1])

    return threadpool_data, feature_data, trade_off_level


def get_index(next_threadpool_size, threadpool_data):
    return [i for i, data_item in enumerate(threadpool_data) if data_item == next_threadpool_size]


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
