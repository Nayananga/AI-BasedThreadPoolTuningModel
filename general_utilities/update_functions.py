import global_data


def update_session_data(session):
    session['MIN_THREADPOOL_DATA'] = global_data.min_threadpool_data
    session['MIN_TARGET_DATA'] = global_data.min_target_data
    session['MIN_FEATURE_DATA'] = global_data.min_feature_data


def update_global_data(session):
    global_data.min_threadpool_data = session['MIN_THREADPOOL_DATA']
    global_data.min_target_data = session['MIN_TARGET_DATA']
    global_data.min_feature_data = session['MIN_FEATURE_DATA']


def update_min_data(threadpool_data, target_data, feature_data, target_value=None):
    min_threadpool_data = global_data.min_threadpool_data
    min_target_data = global_data.min_target_data
    min_feature_data = global_data.min_feature_data

    min_location = get_index(target_value, min_target_data)

    if min_location > -1:
        minimum_threadpool_size = min(
            [threadpool_data[i] for i, target_data_value in enumerate(target_data) if
             target_data_value == target_value])
        if minimum_threadpool_size is None:
            global_data.min_threadpool_data.remove(global_data.min_threadpool_data[min_location])
            global_data.min_target_data.remove(global_data.min_target_data[min_location])
            global_data.min_feature_data.remove(global_data.min_feature_data[min_location])
        elif minimum_threadpool_size < min_threadpool_data[min_location]:
            global_data.min_threadpool_data[min_location] = minimum_threadpool_size
            global_data.min_feature_data[min_location] = feature_data[threadpool_data.index(minimum_threadpool_size)]
    else:
        min_threadpool_data.append(threadpool_data[-1])
        min_target_data.append(target_data[-1])
        min_feature_data.append(feature_data[-1])

    global_data.min_threadpool_data = min_threadpool_data
    global_data.min_target_data = min_target_data
    global_data.min_feature_data = min_feature_data


def get_index(value, in_list):
    try:
        return in_list.index(value)
    except ValueError:
        return -1
