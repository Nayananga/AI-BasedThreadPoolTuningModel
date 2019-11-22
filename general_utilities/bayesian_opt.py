import numpy as np
import random
from general_utilities.acquisition import gaussian_ei
from simulation_utilities.data_generations.simulation_get_performance import simulation_get_performance


"""
bayesian_expected_improvement : Bayesian expected improvement calculation
next_x_point_selection : Next x point selection algorithm according to the expected improvement
"""


# Bayesian expected improvement calculation
def bayesian_expected_improvement(x_val, max_expected_improvement, max_improve_points, min_y, trade_off_level,
                                  model):
    x_val = np.array(x_val).reshape(1, -1)
    expected_improvement = gaussian_ei(x_val, model, min_y, trade_off_level)

    if expected_improvement > max_expected_improvement:
        max_expected_improvement = expected_improvement
        max_improve_points = [x_val[0]]

    elif expected_improvement == max_expected_improvement:
        max_improve_points.append(x_val[0])

    return max_expected_improvement, max_improve_points


def next_x_point_selection(max_expected_improvement, min_x, trade_off_level, max_points):
    if max_expected_improvement == 0:
        print("WARN: Maximum expected improvement was 0")
        next_x = min_x
        trade_off_level = trade_off_level - trade_off_level / 10
        if trade_off_level < 0.00001:
            trade_off_level = 0
    else:
        # select the point with maximum expected improvement
        # if there're multiple points with same ei, chose randomly
        idx = random.randint(0, len(max_points) - 1)
        next_x = max_points[idx]

        """if not one_parameter:
            x_point = next_x[0][0]
            feature_point = next_x[0][1]
            next_x = [x_point, feature_point]"""

        trade_off_level = trade_off_level + trade_off_level / 8
        if trade_off_level > 0.01:
            trade_off_level = 0.01
        elif trade_off_level == 0:
            trade_off_level = 0.00002

    """if len(next_x) == 1:
        next_y = get_performance(next_x)
    else:
        next_y = get_performance(next_x[0], next_x[1])"""

    next_x = list(next_x)

    next_y = simulation_get_performance(next_x)

    return next_x, next_y, trade_off_level
