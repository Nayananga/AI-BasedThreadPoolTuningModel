import numpy as np

import Config as Cg
from general_utilities.performance_collection import get_performance

"""
If the system haven explored in the corresponding feature level, a random point is selected as the minimum point
"""

thread_pool_min = Cg.thread_pool_min
thread_pool_max = Cg.thread_pool_max


def min_point_find(x_value, y_value, feature_val, trade_off_level):

    min_y = []
    x_loc = []
    for i in range(len(y_value)):
        if x_value[i][1] == feature_val:
            min_y.append(y_value[i])
            x_loc.append(i)

    if not min_y:
        minimum_x = []
        x_val = np.random.randint(thread_pool_min, thread_pool_max)
        minimum_x.append(x_val)
        minimum_x.append(feature_val)
        minimum_y = get_performance(minimum_x[0], minimum_x[1])
        trade_off_level = Cg.default_trade_off_level

    else:
        minimum_y = min(min_y)
        x_location = min_y.index(min(min_y))
        minimum_x_loc = x_loc[x_location]
        minimum_x = x_value[minimum_x_loc]

    return minimum_y, minimum_x, trade_off_level