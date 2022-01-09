import pandas as pd

import Config


def get_training_points():
    folder_name = Config.TRAINING_DATA_PATH + "/" + Config.TEST_NAME
    data = pd.read_csv(
        folder_name + "/train_data.csv",
        usecols=[
            "99th percentile Latency",
            "Thread pool size",
            "Current 10 Second Throughput",
        ],
    )

    latency_data = data.iloc[:, 0]
    thread_pool_data = data.iloc[:, 1]
    throughput_data = data.iloc[:, 2]

    object_data = [float(latency_point) for latency_point in latency_data]

    optimize_data = [
        [int(thread_pool_data[i]), float(throughput_data[i])]
        for i in range(len(thread_pool_data))
    ]

    return optimize_data, object_data
