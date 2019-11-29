import global_data as gd
from general_utilities.commom_functions import *


def update_min_point(x_data, y_data, feature_val):
    min_x_data = gd.min_x_data
    min_y_data = gd.min_y_data
    min_y = None
    found_feature_val = False

    for j in range(len(min_x_data)):
        if min_x_data[j][Config.NUMBER_OF_PARAMETERS:] == feature_val:
            found_feature_val = True
            min_y = min_y_data[j]
            min_x = min_x_data[j]
            min_location = j
            break

    if found_feature_val:
        if min_x in x_data and min_y in y_data:
            if y_data[-1] < min_y and x_data[-1][Config.NUMBER_OF_PARAMETERS:] == feature_val:
                min_y = y_data[-1]
                min_x = x_data[-1]

                gd.min_y_data[min_location] = min_y
                gd.min_x_data[min_location] = min_x
        else:
            min_x, min_y = min_point_update(x_data, y_data, feature_val, min_location)
    else:
        if x_data[-1][Config.NUMBER_OF_PARAMETERS:] == feature_val:
            min_y = y_data[-1]
            min_x = x_data[-1]
            gd.min_y_data.append(min_y)
            gd.min_x_data.append(min_x)
        else:
            min_x = selecting_random_point(number_of_points=1, parameter_bounds=Config.PARAMETER_BOUNDS, feature_value=feature_val)
            min_x = min_x[0]

    return min_x, min_y


def min_point_update(x_data, y_data, check_feature_val, min_location):
    min_y = None
    for i in range(len(x_data)):
        if x_data[i][Config.NUMBER_OF_PARAMETERS:] == check_feature_val:
            if min_y is None:
                min_y = y_data[i]
                min_x = x_data[i]
            elif y_data[i] < min_y:
                min_y = y_data[i]
                min_x = x_data[i]

    gd.min_y_data[min_location] = min_y
    gd.min_x_data[min_location] = min_x

    return min_x, min_y
