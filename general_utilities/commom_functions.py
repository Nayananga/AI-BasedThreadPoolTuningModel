import csv
import itertools
import os
import random

import numpy as np

import Config

parameter_count = Config.NUMBER_OF_PARAMETERS
feature_count = Config.NUMBER_OF_FEATURES


def data_point_finder(parameter_bounds, feature_bounds=None):
    points_combined = [
        np.arange(parameter_bounds[i][0], parameter_bounds[i][1]).tolist() for i in range(parameter_count)]

    if parameter_count == 1 and feature_count == 0:
        points_combined = points_combined[0]
    else:
        if feature_bounds is not None:
            for k in range(feature_count):
                points_combined.append(np.arange(feature_bounds[k][0], feature_bounds[k][1]).tolist())

        points_combined = list(itertools.product(*points_combined))

    return points_combined


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
        random_choice = []
        for parameter_bound in parameter_bounds:
            random_choice.append(np.random.randint(parameter_bound[0], parameter_bound[1]))
        if feature_bounds is not None:
            for feature_bound in feature_bounds:
                random_choice.append(np.random.randint(feature_bound[0], feature_bound[1]))
        point.append(random.choice(random_choice))
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
        print("requested directory already exists")


def file_write(threadpool_and_throughput_data, latency_data, exploration_factor, noise_data=None,
               folder_name=Config.PATH):
    if os.path.exists(folder_name + "99th_percentile_data.csv"):
        os.remove(folder_name + "99th_percentile_data.csv")

    with open(folder_name + "99th_percentile_data.csv", 'w') as f:
        writer = csv.writer(f)
        for val in latency_data:
            writer.writerow([val])

    if noise_data is not None:

        if os.path.exists(folder_name + "noise_data.csv"):
            os.remove(folder_name + "noise_data.csv")

        with open(folder_name + "noise_data.csv", 'w') as f:
            writer = csv.writer(f)
            for val in noise_data:
                writer.writerow([val])

    if os.path.exists(folder_name + "thread_and_con_data.csv"):
        os.remove(folder_name + "thread_and_con_data.csv")

    with open(folder_name + "thread_and_con_data.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(threadpool_and_throughput_data)

    if os.path.exists(folder_name + "Exploration_factor.csv"):
        os.remove(folder_name + "Exploration_factor.csv")

    with open(folder_name + "Exploration_factor.csv", 'w') as f:
        writer = csv.writer(f)
        for val in exploration_factor:
            writer.writerow([val])
