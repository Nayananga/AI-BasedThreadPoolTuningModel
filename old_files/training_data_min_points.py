import Config
import global_data as gd


def min_point_assign(x_data, y_data):
    if Config.NUMBER_OF_FEATURES == 0:
        min_point_find_no_feature(x_data, y_data)
    else:
        min_point_find_with_feature(x_data, y_data)


def min_point_find_no_feature(x_data, y_data):
    min_y = min(y_data)
    x_location = y_data.index(min(y_data))
    min_x = x_data[x_location]

    gd.min_x = min_x
    gd.min_y = min_y


def min_point_find_with_feature(x_data, y_data):
    for i in range(len(x_data)):
        found_feature_val = False
        check_feature_val = x_data[i][Config.NUMBER_OF_PARAMETERS:]
        for j in range(len(gd.min_x_data)):
            if gd.min_x_data[j][Config.NUMBER_OF_PARAMETERS:] == check_feature_val:
                found_feature_val = True
                if y_data[i] < gd.min_y_data[j]:
                    gd.min_y_data[j] = y_data[i]
                    gd.min_x_data[j] = x_data[i]
            break

        if not found_feature_val:
            gd.min_y_data.append(y_data[i])
            gd.min_x_data.append(x_data[i])
