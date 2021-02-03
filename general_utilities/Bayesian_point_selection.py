import global_data as gd
from general_utilities.bayesian_opt import bayesian_expected_improvement
from general_utilities.commom_functions import *


def update_min_point(x_data, y_data, feature_val, model=None):
    min_x, min_y, min_location = None, None, None
    min_x_data = gd.min_x_data
    min_y_data = gd.min_y_data
    found_feature_val = False

    for j in range(len(min_x_data)):
        if min_x_data[j][Config.NUMBER_OF_PARAMETERS:] == feature_val:
            found_feature_val = True
            min_y = min_y_data[j]
            min_x = min_x_data[j]
            min_location = j  # saved first occurrence
            break
            # TODO: what if feature_val found more than one time?

    if found_feature_val:
        if min_x in x_data and min_y in y_data:
            # min_x1 is in min_x_data which made up from x_data later it may change min_x1 can be removed from x_data
            if y_data[-1] < min_y and x_data[-1][Config.NUMBER_OF_PARAMETERS:] == feature_val:
                # estimated value may be the best one for the same feature_val
                min_y = y_data[-1]
                min_x = x_data[-1]

                gd.min_y_data[min_location] = min_y
                gd.min_x_data[min_location] = min_x
        else:
            min_x, min_y = replace_min_point(x_data, y_data, feature_val, min_location, model)
    else:
        min_x = estimate_minimum_point(x_data, y_data, feature_val, model)
        # we dont know the latency for the estimated parameters so min_y is none

    return min_x, min_y


def estimate_minimum_point(x_data, y_data, feature_val, model):
    min_x = None
    if x_data[-1][Config.NUMBER_OF_PARAMETERS:] == feature_val:
        # if we couldn't find feature_val in min_x_data then we check in x_data for a clue
        # TODO: what if feature_val found more than one time?
        min_y = y_data[-1]
        min_x = x_data[-1]
        gd.min_y_data.append(min_y)
        gd.min_x_data.append(min_x)
    else:
        if Config.SELECTION_METHOD == "Random":
            min_x = selecting_random_point(number_of_points=1, parameter_bounds=Config.PARAMETER_BOUNDS,
                                           feature_value=feature_val)
            min_x = min_x[0]
            print('Random_selection')
        elif Config.SELECTION_METHOD == "From_model":
            min_x = generate_min_point(feature_val, model)
            # we got the best threadpool size for the feature_val nothing minimum may be minimum latency value can
            # obtain while keeping the same feature_val
            print('From_model')
        elif Config.SELECTION_METHOD == "Nearest_point":
            _min_y, min_x = generate_min_point_based_on_distance(feature_val)

        return min_x


def replace_min_point(x_data, y_data, feature_val, min_location, model):
    min_x, min_y = None, None
    for i in range(len(x_data)):
        if x_data[i][Config.NUMBER_OF_PARAMETERS:] == feature_val:
            if min_y is None:
                min_y = y_data[i]  # TODO: we can initialize these before the loop but training data should not None
                min_x = x_data[i]
            elif y_data[i] < min_y:
                # TODO: y_data.index(min(y_data)) by this we can find the minimum for the matching feature_val
                min_y = y_data[i]
                min_x = x_data[i]

    if min_x is None:
        print(min_x)
        print(min_y)
        gd.min_y_data.remove(gd.min_y_data[min_location])
        gd.min_x_data.remove(gd.min_x_data[min_location])
        min_x = estimate_minimum_point(x_data, y_data, feature_val, model)
        # this is a fucking redundant but have make sure this to happen if not exact match found for the feature_val
        # from training data we dont know the latency for the estimated parameters so min_y is none
    else:
        gd.min_y_data[min_location] = min_y  # ok
        gd.min_x_data[min_location] = min_x

    return min_x, min_y


def from_model(model):
    print("check")
    model.predict([[100], [100]])
    return [100, 100]


def generate_min_point(feature_value, model):
    # finding the minimum point based on the model

    max_expected_improvement = 0
    max_threadpool_sizes = []
    if not gd.random_eval_check:
        eval_pool = gd.eval_pool
    else:
        eval_pool = selecting_random_point(Config.EVAL_POINT_SIZE, Config.PARAMETER_BOUNDS,
                                           feature_value=feature_value)

    min_percentile, min_eval_value = generate_min_point_based_on_distance(feature_value)
    explore_factor = 0.01
    for eval_point in range(len(eval_pool)):
        check_point = list(eval_pool[eval_point])
        for f_val in feature_value:
            check_point.append(f_val)

        max_expected_improvement, max_threadpool_sizes = bayesian_expected_improvement(
            check_point, max_expected_improvement, max_threadpool_sizes, min_percentile, explore_factor, model)

    if max_expected_improvement == 0:
        next_x = min_eval_value
    else:
        idx = np.random.randint(0, len(max_threadpool_sizes))  # TODO:obviously first element?
        next_x = max_threadpool_sizes[idx]

    min_x = list(next_x)

    return min_x


def generate_min_point_based_on_distance(feature_value):
    # Finding the minimum points according to the closest point
    num_parameters = Config.NUMBER_OF_PARAMETERS
    min_x_data = gd.min_x_data
    min_y_data = gd.min_y_data
    min_distance = None
    min_distance_location = None
    min_y = []
    for i in range(len(min_x_data)):
        distance = distance_calculation(feature_value, min_x_data[i][num_parameters:])
        if min_distance is None:
            min_distance = distance
            min_distance_location = i
            min_y = min_y_data[i]
        elif min_distance > distance:
            min_distance = distance
            min_distance_location = i
            min_y = min_y_data[i]
    # get the most similar concurrency to the feature value from min_x_data and get the respective latency from
    # min_y_data using the location value
    min_x = min_x_data[min_distance_location][:num_parameters]
    # get the threadpool size to the respective similar concurrency we found
    for feature in feature_value:
        min_x.append(feature)  # threadpool_size, concurrency

    return min_y, min_x  # respective latency, respective threadpool_size, similar concurrency to the feature_val


def distance_calculation(v, u):
    s = 0
    # dist = [(v_i - v_i)**2 for a, b in zip(v, U)]
    # dist = math.sqrt(sum(dist))
    for v_i, u_i in zip(v, u):
        s += (v_i - u_i) ** 2
    return s ** 0.5
