import json
import os

import config
from general_utilities.data_sampler import sample_by_fifo
from general_utilities.gaussian_process import GPR
from general_utilities.initialization_functions import generate_data
from general_utilities.utility_functions import create_folder


def build_model():
    create_folder(config.RESULT_DATA_PATH)

    train_threadpool_data, train_target_data, train_feature_data = generate_data()

    # fit initial threadpool_data to gaussian model
    gpr_model = GPR(train_threadpool_data, train_target_data, train_feature_data)

    initial_global_data = {
        "train_target_data": train_target_data,
        "train_threadpool_data": train_threadpool_data,
        "train_feature_data": train_feature_data
    }

    if os.path.exists(config.ROOT_PATH + 'initial_global_data.json'):
        os.remove(config.ROOT_PATH + 'initial_global_data.json')

    with open(config.ROOT_PATH + 'initial_global_data.json', 'w') as fp:
        json.dump(initial_global_data, fp)

    return gpr_model


def update_model(threadpool_data, target_data, feature_data, trade_off_level):
    threadpool_data, target_data, feature_data, trade_off_level = sample_by_fifo(threadpool_data,
                                                                                 target_data, feature_data,
                                                                                 trade_off_level)

    # fit new threadpool_data to gaussian process
    model = GPR(threadpool_data, target_data, feature_data)

    return threadpool_data, target_data, feature_data, trade_off_level, model
