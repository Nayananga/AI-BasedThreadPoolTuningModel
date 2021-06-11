import json
import sys

import numpy as np
import redis as redis
from flask import Flask, request, session
from flask_session import Session

import config
from general_utilities.model_functions import build_model, update_model
from general_utilities.threadpool_tuner import find_next_threadpool_size
from general_utilities.utility_functions import shutdown_server, create_folder, write_into_file, plot_data

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

        session['USER_PLOT_DATA'] = {
            "latency_data": [],
            "threadpool_data": [],
            "throughput_data": [],
            "model_predict_data": [],
            "exploration_factor_data": []
        }

        session['USER_TARGET_DATA'] = list(initial_global_data['train_target_data'])

        session['USER_THREADPOOL_DATA'] = list(
            initial_global_data['train_threadpool_data'])

        session['USER_FEATURE_DATA'] = list(
            initial_global_data['train_feature_data'])


@app.route('/', methods=['POST'])
def threadpool_tuner():
    global model
    target_value = None
    exploration_factor = session['EXPLORATION_FACTOR']
    target_data = session['USER_TARGET_DATA']
    threadpool_data = session['USER_THREADPOOL_DATA']
    feature_data = session['USER_FEATURE_DATA']
    plot_data_1 = session['USER_PLOT_DATA']

    request_data = dict(request.get_json())
    print(request_data)

    if float(request_data['currentTenSecondRate']) <= 0.0:
        create_folder(config.RESULT_DATA_PATH + '/' + config.TEST_NAME)
        write_into_file(plot_data_1, config.RESULT_DATA_PATH + config.TEST_NAME + '/')
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

    next_threadpool_size, next_trade_off_level = find_next_threadpool_size(int(request_data['currentThreadPoolSize']),
                                                                           target_value,
                                                                           float(request_data['currentTenSecondRate']),
                                                                           exploration_factor[-1],
                                                                           model)

    target_data.append(target_value)

    threadpool_data.append(int(request_data['currentThreadPoolSize']))

    feature_data.append(float(request_data['currentTenSecondRate']))

    session['NEXT_TRADE_OFF_LEVEL'] = next_trade_off_level
    session['USER_TARGET_DATA'] = target_data
    session['USER_THREADPOOL_DATA'] = threadpool_data
    session['USER_FEATURE_DATA'] = feature_data

    return str(next_threadpool_size)


@app.after_request
def after_request_func(response):
    global model
    iteration = session['ITERATION']
    next_trade_off_level = session['NEXT_TRADE_OFF_LEVEL']
    target_data = session['USER_TARGET_DATA']
    threadpool_data = session['USER_THREADPOOL_DATA']
    feature_data = session['USER_FEATURE_DATA']
    exploration_factor = session['EXPLORATION_FACTOR']
    plot_data_1 = session['USER_PLOT_DATA']

    predicted_target = model.predict(np.column_stack((threadpool_data[-1], feature_data[-1])))

    threadpool_data, target_data, feature_data, new_trade_off_level, model = update_model(
        threadpool_data, target_data, feature_data, next_trade_off_level)

    plot_data_1["latency_data"].append(target_data[-1])
    plot_data_1["threadpool_data"].append(threadpool_data[-1])
    plot_data_1["throughput_data"].append(feature_data[-1])
    plot_data_1["model_predict_data"].append(predicted_target[-1])
    plot_data_1["exploration_factor_data"].append(exploration_factor[-1])  # if we want to plot this

    exploration_factor.append(new_trade_off_level)

    print("inter -", iteration)
    print("Current latency_data - ", target_data[-1])
    print("Predicted latency_data - ", predicted_target[-1])
    print("Current threadpool_data - ", threadpool_data[-1])
    print("Current throughput - ", feature_data[-1])
    print("-------------------------------------")

    # plot_data(plot_data_1)

    session['ITERATION'] = iteration + 1
    session['EXPLORATION_FACTOR'] = exploration_factor
    session['USER_TARGET_DATA'] = target_data
    session['USER_THREADPOOL_DATA'] = threadpool_data
    session['USER_FEATURE_DATA'] = feature_data
    session['USER_PLOT_DATA'] = plot_data_1

    return response


if __name__ == '__main__':
    config.TEST_NAME = sys.argv[1]
    model = build_model()
    app.run()
