import numpy as np

"""
Variance is calculated according of the given distribution
"""


def variance_calculation(number_of_points, point_locations, y_data):
    variance_matrix = []

    for i in range(number_of_points):
        variance_matrix.append(y_data[point_locations[i]])

    variance = np.var(variance_matrix)
    return variance
