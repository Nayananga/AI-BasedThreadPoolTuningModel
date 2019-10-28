import numpy as np
import random
# from skopt.acquisition import gaussian_ei
from general_utilities.acquisition import gaussian_ei

# Bayesian expected improvement calculation
def bayesian_expected_improvement(x_val, max_expected_improvement, max_improve_points_points, minimum, trade_off_level,
                                  model):
    x_val = [x_val]
    x_val = np.array(x_val).reshape(1, -1)
    expected_improvement = gaussian_ei(x_val, model, minimum, trade_off_level)

    if expected_improvement > max_expected_improvement:
        max_expected_improvement = expected_improvement
        max_improve_points_points = [x_val]

    elif expected_improvement == max_expected_improvement:
        max_improve_points_points.append(x_val)

    return max_expected_improvement, max_improve_points_points


def next_x_point_selection(max_expected_improvement, min_x, trade_off_level, max_points):
    if max_expected_improvement == 0:
        print("WARN: Maximum expected improvement was 0. Most likely to pick a random point next")
        next_x = min_x
        print(next_x)
        trade_off_level = trade_off_level - trade_off_level / 10
        if trade_off_level < 0.00001:
            trade_off_level = 0
    else:
        # select the point with maximum expected improvement
        # if there're multiple points with same ei, chose randomly
        idx = random.randint(0, len(max_points) - 1)
        next_x = max_points[idx]
        trade_off_level = trade_off_level + trade_off_level / 8
        if trade_off_level > 0.01:
            trade_off_level = 0.01
        elif trade_off_level == 0:
            trade_off_level = 0.00002

    return next_x, trade_off_level