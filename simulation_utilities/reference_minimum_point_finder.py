import numpy as np

"""
Rough minimum point calculation just for the reference
"""


def min_array(x_value, y_value, z_value):

    minimum_array = []
    feature_array = []
    z_value_list = list(z_value)
    for i in range(len(z_value_list)):
        min_raw = []
        min_y = y_value[i][0]
        z_value_list = z_value[i]
        min_z = min(z_value_list)
        min_location = np.where(z_value_list == min(z_value_list))
        min_x = x_value[i][min_location]

        feature_array.append(min_y)
        min_raw.append(min_x[0])
        min_raw.append(min_z)
        minimum_array.append(min_raw)

    return feature_array, minimum_array
