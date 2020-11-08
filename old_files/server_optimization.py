import csv
import logging
import random
import sys
import time

import numpy as np
import requests

from general_utilities import gaussian_process as gp
from general_utilities.acquisition import gaussian_ei

logging.basicConfig(level=logging.INFO)

####################
bounds = np.array([[1, 201]])

np.random.seed(42)

kernel = gp.kernels.Matern()


def get_performance(x_pass, lower_bound, loc, online_check):
    global data

    requests.put("http://192.168.32.2:8080/setThreadPoolNetty?size=" + str(x_pass[0]))

    time.sleep((loc + 1) * tuning_interval + start_time - time.time())

    res = requests.get("http://192.168.32.2:8080/performance-netty").json()

    data.append(res)
    logging.info("99th Percentile :" + str(res[3]))
    return float(res[3])


def get_initial_points():
    for i in range(0, (number_of_initial_points + 1)):
        x = thread_pool_min + i * (thread_pool_max - thread_pool_min) / number_of_initial_points
        x = int(x)
        logging.info('X = %i', x)
        x_data.append([x])
        y_data.append(get_performance([x], thread_pool_min, i, online))
        param_history.append([x])


def gausian_model(kern, xx, yy):
    model = gp.GaussianProcessRegressor(kernel=kern, alpha=noise_level,
                                        n_restarts_optimizer=10, normalize_y=True)

    model.fit(xx, yy)

    return model


check_srt = sys.argv[7]
# check_srt = False
online = True if check_srt == 'True' else False

if online:
    folder_name = sys.argv[1] if sys.argv[1][-1] == "/" else sys.argv[1] + "/"
    case_name = sys.argv[2]

    ru = int(sys.argv[3])
    mi = int(sys.argv[4])
    rd = int(sys.argv[5])
    tuning_interval = int(sys.argv[6])

else:
    ru = 0
    mi = 1000
    rd = 0
    tuning_interval = 10

data = []
X_plot_data = []
Y_plot_data = []
param_history = []
test_duration = ru + mi + rd
iterations = test_duration // tuning_interval

noise_level = 1e-6
number_of_initial_points = 8

x_data = []
y_data = []

start_time = time.time()

thread_pool_max = 200
thread_pool_min = 4

get_initial_points()

model = gausian_model(kernel, x_data, y_data)

xi = 0.1

# use bayesian optimization
for i in range((number_of_initial_points + 1), iterations):
    minimum = min(y_data)
    x_location = y_data.index(min(y_data))
    max_expected_improvement = 0
    max_points = []
    max_points_unnormalized = []

    logging.info("xi - %f", xi)
    logging.info("iter - %i", i)

    for pool_size in range(thread_pool_min, thread_pool_max + 1):
        x = [pool_size]
        x_val = [x[0]]

        # may be add a condition to stop explorering the already expored locations
        ei = gaussian_ei(np.array(x_val).reshape(1, -1), model, minimum, xi)

        if ei > max_expected_improvement:
            max_expected_improvement = ei
            max_points = [x_val]

        elif ei == max_expected_improvement:
            max_points.append(x_val)

    if max_expected_improvement == 0:
        logging.info("WARN: Maximum expected improvement was 0. Most likely to pick a random point next")
        next_x = x_data[x_location]
        logging.info(next_x)
        xi = xi - xi / 10
        if xi < 0.00001:
            xi = 0
    else:
        # select the point with maximum expected improvement
        # if there're multiple points with same ei, chose randomly
        idx = random.randint(0, len(max_points) - 1)
        next_x = max_points[idx]
        xi = xi + xi / 8
        if xi > 0.01:
            xi = 0.01
        elif xi == 0:
            xi = 0.00002

    logging.info(next_x)

    param_history.append(next_x)
    next_y = get_performance(next_x, thread_pool_min, i, online)
    y_data.append(next_y)
    x_data.append(next_x)

    x_data_arr = np.array(x_data)
    y_data_arr = np.array(y_data)

    model = gausian_model(kernel, x_data, y_data_arr)

logging.info("minimum found : %f", min(y_data))

if online:
    with open(folder_name + case_name + "/results.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["IRR", "Request Count", "Mean Latency (for window)", "99th Latency"])
        for line in data:
            writer.writerow(line)

    with open(folder_name + case_name + "/param_history.csv", "w") as f:
        writer = csv.writer(f)
        for line in param_history:
            writer.writerow(line)
