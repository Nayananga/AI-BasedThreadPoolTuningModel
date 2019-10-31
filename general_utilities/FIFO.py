from general_utilities.indexing import index_get
from general_utilities.variance_calcutation import variance_calculation
import Config as Cg

maximum_in_sampler = 5
variance_threshold = 50


def fifo_sampling(next_x, x_data, y_data, trade_off_level):

    point_locations = index_get(next_x, x_data)
    number_of_points = len(point_locations)

    if number_of_points == 1:
        pass
    elif number_of_points > 1:
        variance = variance_calculation(number_of_points, point_locations, y_data)
        if variance >= variance_threshold:
            x_data, y_data = remove_data(number_of_points, point_locations, x_data, y_data)
            trade_off_level = Cg.default_trade_off_level
        elif number_of_points < maximum_in_sampler:
            pass
        else:
            x_data.remove(x_data[point_locations[0]])
            y_data.remove(y_data[point_locations[0]])

    return x_data, y_data, trade_off_level


def remove_data(number_of_points, point_locations, x_data, y_data):
    for i in range(number_of_points - 1):
        x_data.remove(x_data[point_locations[i]])
        y_data.remove(y_data[point_locations[0]])

    return x_data, y_data
