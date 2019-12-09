from data_generation.initial_configurations import initial_configurations
import global_data as gd
from data_generation.data_generation_initialization import data_generation_ini
from general_utilities.commom_functions import *
import csv


def generate_data():
    initial_configurations()

    optimize_data, object_data, feature_changing_data = data_generation_ini()
    gd.min_x_data, gd.min_y_data = ini_min_point_find_with_feature(optimize_data, object_data)

    gd.threadpool_and_concurrency = optimize_data
    gd.percentile = object_data
    gd.concurrency = feature_changing_data

    return optimize_data, object_data, feature_changing_data
