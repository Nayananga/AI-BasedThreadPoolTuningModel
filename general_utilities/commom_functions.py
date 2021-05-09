import csv
import os

import Config


def create_folders(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print("requested directory already exists")


def write_into_file(threadpool_and_throughput_data, latency_data, exploration_factor, noise_data=None,
                    folder_name=Config.RESULT_DATA_PATH):
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
