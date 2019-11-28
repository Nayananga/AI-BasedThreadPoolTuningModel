from data_generation.initial_configurations import initial_configurations
import global_data as gd
from data_generation.data_generation_initialization import data_generation_ini
from general_utilities.commom_functions import *
import csv


def data_generator():

    folder_name  = 'Data/'
    initial_configurations()

    optimize_data, object_data, feature_changing_data = data_generation_ini()
    gd.min_x_data, gd.min_y_data = ini_min_point_find_with_feature(optimize_data, object_data)

    gd.threadpool_and_concurrency = optimize_data
    gd.percentile = object_data
    gd.concurrency = feature_changing_data

    print(optimize_data)

    with open(folder_name+"99th_percentile.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(object_data)

    with open(folder_name+"training_data.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(optimize_data)

    with open(folder_name+"workload.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(feature_changing_data)


if __name__ == "__data_generator__":
    data_generator()