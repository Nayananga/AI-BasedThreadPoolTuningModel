import itertools
import numpy as np
import os

import Config

parameter_count = Config.NUMBER_OF_PARAMETERS
feature_count = Config.NUMBER_OF_FEATURES


def data_point_finder(parameter_bounds, feature_bounds=None):
    print(feature_bounds)
    points_combined = []
    for i in range(parameter_count):
        points = []
        for j in range(parameter_bounds[i][0], parameter_bounds[i][1]):
            points.append(j)
        points_combined.append(points)

    if feature_bounds is not None:
        for k in range(feature_count):
            points = []
            for m in range(feature_bounds[k][0], feature_bounds[k][1]):
                points.append(m)
            points_combined.append(points)

    if parameter_count == 1 and feature_count == 0:
        points_combined = points_combined[0]
    else:
        points_combined = list(itertools.product(*points_combined))

    return points_combined


def min_point_find_no_feature(x_data, y_data, min_x=None, min_y=None):
    if min_x in x_data and min_y in y_data:
        if y_data[-1] < min_y:
            min_y = y_data[-1]
            min_x = x_data[-1]
    else:
        min_y = min(y_data)
        x_location = y_data.index(min(y_data))
        min_x = x_data[x_location]
    return min_x, min_y


def ini_min_point_find_with_feature(x_data, y_data):
    min_x_data = []
    min_y_data = []
    for i in range(len(x_data)):
        found_feature_val = False
        check_feature_val = x_data[i][Config.NUMBER_OF_PARAMETERS:]
        for j in range(len(min_x_data)):
            if min_x_data[j][Config.NUMBER_OF_PARAMETERS:] == check_feature_val:
                found_feature_val = True
                if y_data[i] < min_y_data[j]:
                    min_y_data[j] = y_data[i]
                    min_x_data[j] = x_data[i]
                break

        if not found_feature_val:
            min_y_data.append(y_data[i])
            min_x_data.append(x_data[i])

    return min_x_data, min_y_data


def selecting_random_point(number_of_points, parameter_bounds, feature_bounds=None, feature_value=None):
    size = 0
    random_points = []

    while size < number_of_points:
        point = []
        for j in range(len(parameter_bounds)):
            point.append(np.random.randint(parameter_bounds[j][0], parameter_bounds[j][1]))
        if feature_bounds is not None:
            for k in range(len(feature_bounds)):
                point.append(np.random.randint(feature_bounds[k][0], feature_bounds[k][1]))
        if feature_value is not None:
            for f_loc in range(Config.NUMBER_OF_FEATURES):
                point.append(feature_value[f_loc])
        if point not in random_points:
            size += 1
            random_points.append(point)

    return random_points


def create_folders(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print("directory already exists")
        # if input("are you sure want to go ahead (Y/n)?") == "n":
        #     exit()