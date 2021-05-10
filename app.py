import json
import sys

import redis as redis
from flask import Flask, request, session
from flask_session import Session

import Config
import global_data
from general_utilities.Bayesian_point_selection import update_min_data
from general_utilities.commom_functions import create_folders
from general_utilities.data_generator import generate_data
from general_utilities.gaussian_process import gpr
from threadpool_tuner import find_next_threadpool_size, update_model

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

        with open('Data/Training_data/initial_global_data.json') as f:
            initial_global_data = json.load(f)

        session['INITIALIZED'] = bool(True)

        session['ITERATION'] = int(1)

        session['EXPLORATION_FACTOR'] = [float(Config.DEFAULT_TRADE_OFF_LEVEL)]

        session['USER_PLOT_DATA'] = [[], [], [], []]

        session['USER_LATENCY_DATA'] = list(initial_global_data['train_latency_data'])

        session['USER_THREADPOOL_DATA'] = list(
            initial_global_data['train_threadpool_data'])

        session['MIN_X_DATA'] = list(initial_global_data['min_threadpool_data'])
        session['MIN_Y_DATA'] = list(initial_global_data['min_feature_data'])


@app.route('/', methods=['POST'])
def threadpool_tuner():
    global model
    feature_value = None
    exploration_factor = session['EXPLORATION_FACTOR']
    latency_data = session['USER_LATENCY_DATA']
    threadpool_data = session['USER_THREADPOOL_DATA']

    update_global_data()

    request_data = dict(request.get_json())
    print(request_data)

    if float(request_data['currentTenSecondRate']) <= 0.0:
        shutdown_server()

    # T = ThroughputOptimized, M = Mean latency Optimized, 99P = 99th Percentile of latency optimized
    if str(request_data['optimization']) == 'T':
        feature_value = float(request_data['currentTenSecondRate'])
    elif str(request_data['optimization']) == 'M':
        feature_value = float(request_data['currentMeanLatency'])
    elif str(request_data['optimization']) == '99P':
        feature_value = float(request_data['current99PLatency'])
    else:
        Exception("Invalid optimization, use T = ThroughputOptimized, M = Mean latency Optimized, 99P = 99th "
                  "Percentile of latency optimized")

    next_threadpool_size, next_trade_off_level = find_next_threadpool_size(exploration_factor[-1], model, feature_value)

    latency_data.append(feature_value)

    threadpool_data.append(float(request_data['currentThreadPoolSize']))

    session['NEXT_THROUGHPUT'] = float(request_data['currentTenSecondRate'])
    session['NEXT_TRADE_OFF_LEVEL'] = next_trade_off_level
    session['NEXT_THREADPOOL_SIZE'] = next_threadpool_size
    session['USER_LATENCY_DATA'] = latency_data
    session['USER_THREADPOOL_DATA'] = threadpool_data

    update_session_data()

    return str(next_threadpool_size)


@app.after_request
def after_request_func(response):
    global model
    iteration = session['ITERATION']
    exploration_factor = session['EXPLORATION_FACTOR']
    plot_data_1 = session['USER_PLOT_DATA']
    feature_data = session['USER_LATENCY_DATA']
    threadpool_data = session['USER_THREADPOOL_DATA']
    next_threadpool_size = session['NEXT_THREADPOOL_SIZE']
    next_throughput = session['NEXT_THROUGHPUT']
    next_trade_off_level = session['NEXT_TRADE_OFF_LEVEL']

    update_global_data()

    threadpool_data, feature_data, new_trade_off_level, model = update_model(
        next_threadpool_size, threadpool_data, feature_data, next_trade_off_level)

    plot_data_1[0].append(feature_data[-1])
    plot_data_1[1].append(threadpool_data[-1])
    plot_data_1[2].append(exploration_factor[-1])
    plot_data_1[3].append(next_throughput)  # if we want to plot this

    update_min_data(threadpool_data, feature_data)
    exploration_factor.append(new_trade_off_level)

    print("inter -", iteration)
    print("workers -", next_throughput)
    print("trade_off_level -", new_trade_off_level)
    print("Next x- ", threadpool_data[-1])
    print("Next y- ", feature_data[-1])
    print("min_threadpool_data", global_data.min_threadpool_data)
    print("min_feature_data", global_data.min_feature_data)
    print("-------------------------------------")

    # if iteration % 20 == 0:
    #     plot_data(plot_data_1[1], plot_data_1[0], Config.PAUSE_TIME, save=True)
    #     save_plots(plot_data_1[1])
    #     write_into_file(plot_data_1[1], plot_data_1[0], exploration_factor,
    #                     folder_name=Config.RESULT_DATA_PATH + 'plot_')
    #     write_into_file(threadpool_data, feature_data, exploration_factor,
    #                     folder_name=Config.RESULT_DATA_PATH)
    #
    # else:
    #     plot_data(plot_data_1[1], plot_data_1[0], Config.PAUSE_TIME)

    session['ITERATION'] = iteration + 1
    session['EXPLORATION_FACTOR'] = exploration_factor
    session['USER_LATENCY_DATA'] = feature_data
    session['USER_THREADPOOL_DATA'] = threadpool_data
    session['USER_PLOT_DATA'] = plot_data_1

    update_session_data()

    return response


def update_global_data():
    global_data.min_threadpool_data = session['MIN_X_DATA']
    global_data.min_feature_data = session['MIN_Y_DATA']


def update_session_data():
    session['MIN_X_DATA'] = global_data.min_threadpool_data
    session['MIN_Y_DATA'] = global_data.min_feature_data


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def build_model():
    create_folders(Config.RESULT_DATA_PATH)

    train_threadpool_data, train_latency_data = generate_data()

    # fit initial threadpool_data to gaussian model
    gpr_model = gpr(train_threadpool_data, train_latency_data)

    initial_global_data = {
        "train_latency_data": train_latency_data,
        "train_threadpool_data": train_threadpool_data,

        "min_threadpool_data": global_data.min_threadpool_data,
        "min_feature_data": global_data.min_feature_data
    }

    with open('Data/Training_data/initial_global_data.json', 'w') as fp:
        json.dump(initial_global_data, fp)

    return gpr_model


if __name__ == '__main__':
    Config.TEST_NAME = sys.argv[1]
    model = build_model()
    app.run()
