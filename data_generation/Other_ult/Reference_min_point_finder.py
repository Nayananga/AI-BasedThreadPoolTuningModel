import csv

import Config
from general_utilities.commom_functions import create_folders
from general_utilities.data_plot import min_point_plot
from general_utilities.sample_system import sample_system

threadpool_bounds = Config.PARAMETER_BOUNDS
concurrency_bounds = Config.FEATURE_BOUNDS

equation = Config.FUNCTION

concurrency = []
thread_size = []

min_points = []
min_point_location = []

min_point_collection = []


def file_write(data, path):
    with open(path + "Reference_min_data.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)


def find_reference_min_points():
    min_location = None
    create_folders(Config.REFERENCE_PATH)

    for i in range(len(concurrency_bounds)):
        for j in range(concurrency_bounds[i][1] - concurrency_bounds[i][0]):
            concurrency.append(j + concurrency_bounds[i][0])

    for i in range(len(threadpool_bounds)):
        for j in range(threadpool_bounds[i][1] - threadpool_bounds[i][0]):
            thread_size.append(j + threadpool_bounds[i][0])

    for con in concurrency:
        _min = None
        min_point_detail = []
        for thread in thread_size:
            data_point = sample_system(p1=thread, f1=con, formula=equation)
            if _min is None or data_point < _min:
                _min = data_point
                min_location = thread

        min_point_detail.append(con)
        min_point_detail.append(min_location)
        min_point_detail.append(_min)

        min_point_collection.append(min_point_detail)

        min_point_location.append(min_location)
        min_points.append(_min)
        print(min_point_detail)

    min_point_plot(min_point_location)
    file_write(min_point_collection, Config.REFERENCE_PATH)


if __name__ == '__main__':
    find_reference_min_points()
