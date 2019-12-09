import Config as Config
import sympy as sy
import csv
from general_utilities.data_plot import min_point_plot
import os

threadpool_bounds = Config.PARAMETER_BOUNDS
concurrency_bounds = Config.FEATURE_BOUNDS

equation = Config.FUNCTION

concurrency = []
thread_size = []

min_points = []
min_point_location = []

min_point_collection = []


def sample_system(formula, **kwargs):
    expr = sy.sympify(formula)
    return float(expr.evalf(subs=kwargs))


def file_write(data):
    common_path = Config.COMMON_PATH
    folder_name = Config.REFERENCE_PATH

    with open(common_path + folder_name + "Reference_min_data.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)


for i in range(len(concurrency_bounds)):
    for j in range(concurrency_bounds[i][1] - concurrency_bounds[i][0]):
        concurrency.append(j+concurrency_bounds[i][0])

for i in range(len(threadpool_bounds)):
    for j in range(threadpool_bounds[i][1] - threadpool_bounds[i][0]):
        thread_size.append(j+threadpool_bounds[i][0])

for con in concurrency:
    min = None
    min_point_detail = []
    for thread in thread_size:
        data_point = sample_system(p1=thread, f1=con, formula=equation)
        if min is None or data_point<min:
            min = data_point
            min_location = thread

    min_point_detail.append(con)
    min_point_detail.append(min_location)
    min_point_detail.append(min)

    min_point_collection.append(min_point_detail)

    min_point_location.append(min_location)
    min_points.append(min)
    print(min_point_detail)

min_point_plot(concurrency, min_point_location)
file_write(min_point_collection)
