import json

import pandas as pd

import Config
from general_utilities.gaussian_process import GPR


def get_training_points():
    folder_name = Config.TRAINING_DATA_PATH + "/" + Config.TEST_NAME
    data = pd.read_csv(
        folder_name + "/train_data.csv",
        usecols=[
            "Thread pool size",
            "Concurrency",
            "99th percentile Latency",
        ],
    )

    thread_pool_data = data.iloc[:, 0]
    throughput_data = data.iloc[:, 1]
    latency_data = data.iloc[:, 2]

    object_data = [float(latency_point) for latency_point in latency_data]

    optimize_data = [
        [int(thread_pool_data[i]), float(throughput_data[i])]
        for i in range(len(thread_pool_data))
    ]

    return optimize_data, object_data


def build_model():

    train_threadpool_and_feature_data, train_object_data = get_training_points()

    gpr_model = GPR(
        train_threadpool_and_feature_data, train_object_data
    )  # fit initial data to gaussian model

    initial_global_data = {
        "train_object_data": train_object_data,
        "train_threadpool_and_feature_data": train_threadpool_and_feature_data,
    }

    with open("Data/initial_global_data.json", "w") as fp:
        json.dump(initial_global_data, fp)

    return gpr_model
