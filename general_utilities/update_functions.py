import global_data


def update_session_data(session):
    session['MIN_THREADPOOL_DATA'] = global_data.min_threadpool_data
    session['MIN_TARGET_DATA'] = global_data.min_target_data
    session['MIN_FEATURE_DATA'] = global_data.min_feature_data


def update_global_data(session):
    global_data.min_threadpool_data = session['MIN_THREADPOOL_DATA']
    global_data.min_target_data = session['MIN_TARGET_DATA']
    global_data.min_feature_data = session['MIN_FEATURE_DATA']


def update_min_data(threadpool_data, target_data, feature_data):
    feature_value = feature_data[-1]
    min_threadpool_data = global_data.min_threadpool_data
    min_target_data = global_data.min_target_data
    min_feature_data = global_data.min_feature_data

    min_location = get_index(feature_value, min_feature_data)

    if min_location > -1:
        min_target_value = min(
            [target_data[i] for i, f_value in enumerate(feature_data) if
             f_value == feature_value])
        if min_target_value is None:
            global_data.min_threadpool_data.remove(global_data.min_threadpool_data[min_location])
            global_data.min_target_data.remove(global_data.min_target_data[min_location])
            global_data.min_feature_data.remove(feature_value)
        elif min_target_value < min_target_data[min_location]:
            global_data.min_target_data[min_location] = min_target_value
            global_data.min_threadpool_data[min_location] = threadpool_data[target_data.index(min_target_value)]
    else:
        min_threadpool_data.append(threadpool_data[-1])
        min_target_data.append(target_data[-1])
        min_feature_data.append(feature_value)

    global_data.min_threadpool_data = min_threadpool_data
    global_data.min_target_data = min_target_data
    global_data.min_feature_data = min_feature_data


def get_index(value, in_list):
    try:
        return in_list.index(value)
    except ValueError:
        return -1
