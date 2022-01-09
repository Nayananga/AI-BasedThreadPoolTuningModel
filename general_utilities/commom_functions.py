import numpy as np


def data_point_finder(parameter_bounds):
    return np.arange(parameter_bounds[0][0], parameter_bounds[0][1]).tolist()
