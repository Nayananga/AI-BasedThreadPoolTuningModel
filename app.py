import json
import sys

import redis as redis
from flask import Flask, request, session
from flask_session import Session

import config
import global_data
from general_utilities.model_functions import build_model, update_model
from general_utilities.threadpool_tuner import find_next_threadpool_size
from general_utilities.update_functions import update_min_data, update_session_data, update_global_data
from general_utilities.utility_functions import shutdown_server

app = Flask(__name__)

app.secret_key = "My secret key"

# Configure Redis for storing the session threadpool_data on the server-side
app.config['SESSION_TYPE'] = str('redis')
app.config['SESSION_PERMANENT'] = bool(False)
app.config['SESSION_USE_SIGNER'] = bool(True)
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# Create and initialize the Flask-Session object AFTER `app` has been configured
Session(app)

model = None


@app.before_request
def before_request_func():
    if "INITIALIZED" not in session:
        print("New User : ", session.sid)

        with open(config.ROOT_PATH + 'initial_global_data.json') as f:
            initial_global_data = json.load(f)

        session['INITIALIZED'] = bool(True)

        session['ITERATION'] = int(1)

        session['EXPLORATION_FACTOR'] = [float(config.DEFAULT_TRADE_OFF_LEVEL)]

        session['USER_PLOT_DATA'] = [[], [], [], []]

        session['USER_TARGET_DATA'] = list(initial_global_data['train_target_data'])

        session['USER_THREADPOOL_DATA'] = list(
            initial_global_data['train_threadpool_data'])

        session['USER_FEATURE_DATA'] = list(
            initial_global_data['train_feature_data'])

        session['MIN_TARGET_DATA'] = list(initial_global_data['min_target_data'])
        session['MIN_THREADPOOL_DATA'] = list(initial_global_data['min_threadpool_data'])
        session['MIN_FEATURE_DATA'] = list(initial_global_data['min_feature_data'])


@app.route('/', methods=['POST'])
def threadpool_tuner():
    global model
    target_value = None
    exploration_factor = session['EXPLORATION_FACTOR']
    target_data = session['USER_TARGET_DATA']
    threadpool_data = session['USER_THREADPOOL_DATA']
    feature_data = session['USER_FEATURE_DATA']

    update_global_data(session)

    request_data = dict(request.get_json())
    print(request_data)

    if float(request_data['currentTenSecondRate']) <= 0.0:
        shutdown_server()

    # T = ThroughputOptimized, M = Mean latency Optimized, 99P = 99th Percentile of latency optimized
    if str(request_data['optimization']) == 'T':
        target_value = float(request_data['currentTenSecondRate'])
    elif str(request_data['optimization']) == 'M':
        target_value = float(request_data['currentMeanLatency'])
    elif str(request_data['optimization']) == '99P':
        target_value = float(request_data['current99PLatency'])
    else:
        Exception("Invalid optimization, use T = ThroughputOptimized, M = Mean latency Optimized, 99P = 99th "
                  "Percentile of latency optimized")

    next_threadpool_size, next_trade_off_level = find_next_threadpool_size(target_value,
                                                                           feature_value=float(
                                                                               request_data['currentTenSecondRate']),
                                                                           trade_off_level=exploration_factor[-1],
                                                                           model=model)

    target_data.append(target_value)

    threadpool_data.append(float(request_data['currentThreadPoolSize']))

    feature_data.append(float(request_data['currentTenSecondRate']))

    session['NEXT_TRADE_OFF_LEVEL'] = next_trade_off_level
    session['NEXT_THREADPOOL_SIZE'] = next_threadpool_size
    session['USER_TARGET_DATA'] = target_data
    session['USER_THREADPOOL_DATA'] = threadpool_data
    session['USER_FEATURE_DATA'] = feature_data

    update_session_data(session)

    return str(next_threadpool_size)


@app.after_request
def after_request_func(response):
    global model
    iteration = session['ITERATION']
    next_trade_off_level = session['NEXT_TRADE_OFF_LEVEL']
    next_threadpool_size = session['NEXT_THREADPOOL_SIZE']
    target_data = session['USER_TARGET_DATA']
    threadpool_data = session['USER_THREADPOOL_DATA']
    feature_data = session['USER_FEATURE_DATA']
    exploration_factor = session['EXPLORATION_FACTOR']
    plot_data_1 = session['USER_PLOT_DATA']

    update_global_data(session)

    threadpool_data, target_data, feature_data, new_trade_off_level, model = update_model(
        next_threadpool_size, threadpool_data, target_data, feature_data, next_trade_off_level)

    plot_data_1[0].append(target_data[-1])  # latency_data
    plot_data_1[1].append(threadpool_data[-1])  # threadpool_data
    plot_data_1[2].append(feature_data[-1])  # throughput
    plot_data_1[3].append(exploration_factor[-1])  # if we want to plot this

    update_min_data(threadpool_data, target_data, feature_data)
    exploration_factor.append(new_trade_off_level)

    print("inter -", iteration)
    print("Current trade_off_level - ", new_trade_off_level)
    print("Current threadpool_data - ", threadpool_data[-1])
    print("Current latency_data - ", target_data[-1])
    print("Current throughput - ", feature_data[-1])
    print("min_threadpool_data - ", global_data.min_threadpool_data)
    print("min_target_data - ", global_data.min_target_data)
    print("min_feature_data - ", global_data.min_feature_data)
    print("-------------------------------------")

    # if iteration % 20 == 0:
    #
    #     plot_data(latency_data=plot_data_1[0], threadpool_data=plot_data_1[1],
    #               throughput_data=plot_data_1[2], save=True)
    #
    #     write_into_file(latency_data=plot_data_1[0], threadpool_data=plot_data_1[1],
    #                     throughput_data=plot_data_1[2], exploration_factor=plot_data_1[3],
    #                     folder_name=Config.RESULT_DATA_PATH + 'plot_')
    #
    #     write_into_file(latency_data=target_data, threadpool_data=threadpool_data,
    #                     throughput_data=feature_data, exploration_factor=exploration_factor,
    #                     folder_name=Config.RESULT_DATA_PATH)
    #
    # else:
    #     plot_data(latency_data=plot_data_1[0], threadpool_data=plot_data_1[1], throughput_data=plot_data_1[2])

    session['ITERATION'] = iteration + 1
    session['EXPLORATION_FACTOR'] = exploration_factor
    session['USER_TARGET_DATA'] = target_data
    session['USER_THREADPOOL_DATA'] = threadpool_data
    session['USER_FEATURE_DATA'] = feature_data
    session['USER_PLOT_DATA'] = plot_data_1

    update_session_data(session)

    return response


if __name__ == '__main__':
    config.TEST_NAME = sys.argv[1]
    model = build_model()
    app.run()
