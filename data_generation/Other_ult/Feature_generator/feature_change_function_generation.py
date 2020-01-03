import csv

import Config
from data_generation.Other_ult.Feature_generator.feature_functions import feature_generator


def feature_data_generation():
    feature_function = Config.FEATURE_FUNCTION
    feature_changing_data = []
    for i in range(len(feature_names)):
        feature_changing_data.append(feature_generator(feature_function[i], feature_bounds[i]))
    feature_changing_data = list(map(list, zip(*feature_changing_data)))
    write_feature_data(feature_changing_data, feature_function[0])


def write_feature_data(data, feature_data_name):
    folder_name = Config.ROOT_PATH + 'Workload_data/'
    # with open(folder_name + feature_data_name + ".csv", 'w') as f:
    #     writer = csv.writer(f)
    #     for val in data:
    #         writer.writerow([val])
    with open(folder_name + feature_data_name + ".csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)

if __name__ == "__main__":
    feature_bounds = Config.FEATURE_BOUNDS
    feature_names = Config.FEATURE

    for feature_function in Config.FEATURE_FUNCTION_ARRAY:
        Config.FEATURE_FUNCTION = feature_function

        feature_data_generation()


