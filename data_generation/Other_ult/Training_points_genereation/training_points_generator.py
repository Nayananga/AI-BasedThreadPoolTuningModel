import csv

import numpy as np
import sympy as sy

import Config
from data_generation.Other_ult.Training_points_genereation.dse_tool.explorer import Explorer
from data_generation.Other_ult.Training_points_genereation.dse_tool.util import RandomInt
from general_utilities.commom_functions import selecting_random_point
from old_files.sample_system import sample_system


def generate_training_points(number_of_training_points, para_bounds, feat_bounds=None, select_random=False):
    if select_random:
        """
        This method is for random selection of the training points.
        """

        object_data = []
        if feat_bounds is None:
            optimize_data = selecting_random_point(number_of_training_points, para_bounds)
        else:
            optimize_data = selecting_random_point(number_of_training_points, para_bounds, feat_bounds)
        for i in range(len(optimize_data)):
            object_data.append(sample_system(optimize_data[i]))

        return optimize_data, object_data

    else:

        """
        This method is for DSE for selecting training points.
        Initializing number of random points should be defined. 
        """

        data = dse(number_of_random_points=20)
        optimize_data = []
        object_data = []

        for i in range(len(data)):
            parameters = [data[i][0], data[i][1]]
            values = data[i][2]

            optimize_data.append(parameters)
            object_data.append(values)

        return optimize_data, object_data


def corner_point_selection(para_bounds, feat_bounds):
    para_corners = []
    feature_corners = []
    corner_points = []

    for para in para_bounds:
        para_corners.append(para[0])
        para_corners.append(para[1])

    for feature in feat_bounds:
        feature_corners.append(feature[0])
        feature_corners.append(feature[1])

    for para in para_corners:
        for feature in feature_corners:
            temp_point = [para, feature]
            corner_points.append(temp_point)

    return corner_points


def write_training_data(data, name):
    folder_name = Config.ROOT_PATH + "Training_data/"
    with open(folder_name + name + "_training_data.csv", "w") as f:
        if isinstance(data[0], list):
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)
        else:
            writer = csv.writer(f)
            for val in data:
                writer.writerow([val])


def dse(number_of_random_points=10):
    explorer = Explorer(
        {
            'p1': RandomInt(Config.PARAMETER_BOUNDS[0][0], Config.PARAMETER_BOUNDS[0][1]),
            'f1': RandomInt(Config.FEATURE_BOUNDS[0][0], Config.FEATURE_BOUNDS[0][1]),
        },
        path=Config.ROOT_PATH + "Training_data/temp.csv"
    )

    expr = sy.sympify(Config.FUNCTION)
    eval_func = lambda x: np.float64(expr.evalf(subs=x))
    init_df = explorer.explore(Config.NUMBER_OF_TRAINING_POINTS - number_of_random_points, eval_func,
                               init_n=number_of_random_points)
    print(init_df.values)

    return init_df.values


if __name__ == '__main__':
    threadpool_and_concurrency, latency = generate_training_points(Config.NUMBER_OF_TRAINING_POINTS,
                                                                   Config.PARAMETER_BOUNDS, Config.FEATURE_BOUNDS)

    print(np.shape(threadpool_and_concurrency))
    print(np.shape(latency))

    write_training_data(threadpool_and_concurrency, "threadpool_and_concurrency")
    write_training_data(latency, "latency")
