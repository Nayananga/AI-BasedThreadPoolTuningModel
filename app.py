import json
import sys

import redis as redis
from flask import Flask, request, session
from flask_session import Session

import Config
import global_data
from general_utilities import data_generator
from general_utilities.Bayesian_point_selection import update_min_point
from general_utilities.commom_functions import create_folders
from general_utilities.gaussian_process import gpr
from threadpool_tuner import find_next_threadpool_size, update_model

app = Flask(__name__)

app.secret_key = "My secret key"

# Configure Redis for storing the session data on the server-side
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

        session['TRADE_OFF_LEVEL'] = float(Config.DEFAULT_TRADE_OFF_LEVEL)

        session['EXPLORATION_FACTOR'] = [float(Config.DEFAULT_TRADE_OFF_LEVEL)]

        session['USER_PLOT_DATA'] = [[], [], []]

        session['USER_LATENCY_DATA'] = list(initial_global_data['train_latency_data'])

        session['USER_THREADPOOL_AND_THROUGHPUT_DATA'] = list(
            initial_global_data['train_threadpool_and_throughput_data'])

        session['MIN_X_DATA'] = list(initial_global_data['min_x_data'])
        session['MIN_Y_DATA'] = list(initial_global_data['min_y_data'])

        session['RANDOM_EVAL_CHECK'] = bool(initial_global_data['random_eval_check'])
        session['EVAL_POOL'] = list(initial_global_data['eval_pool'])


@app.route('/', methods=['POST'])
def threadpool_tuner():
    global model
    trade_off_level = float(session['TRADE_OFF_LEVEL'])
    latency_data = list(session['USER_LATENCY_DATA'])
    threadpool_and_throughput_data = list(session['USER_THREADPOOL_AND_THROUGHPUT_DATA'])

    update_global_data()

    request_data = dict(request.get_json())
    print(request_data)

    if float(request_data['currentTenSecondRate']) <= 0.0:
        shutdown_server()

    next_threadpool_size_with_throughput, trade_off_level = find_next_threadpool_size(
        threadpool_and_throughput_data,
        latency_data, trade_off_level, model,
        [float(request_data['currentTenSecondRate'])])

    # T = ThroughputOptimized, M = Mean latency Optimized, 99P = 99th Percentile of latency optimized
    if str(request_data['optimization']) == 'T':
        latency_data.append(float(request_data['currentTenSecondRate']))
    elif str(request_data['optimization']) == 'M':
        latency_data.append(float(request_data['currentMeanLatency']))
    elif str(request_data['optimization']) == '99P':
        latency_data.append(float(request_data['current99PLatency']))
    else:
        Exception("Invalid optimization, use T = ThroughputOptimized, M = Mean latency Optimized, 99P = 99th "
                  "Percentile of latency optimized")

    threadpool_and_throughput_data.append(
        [float(request_data['currentThreadPoolSize']), float(request_data['currentTenSecondRate'])])

    session['TRADE_OFF_LEVEL'] = trade_off_level
    session['NEXT_THROUGHPUT'] = [float(request_data['currentTenSecondRate'])]
    session['NEXT_THREADPOOL_SIZE_WITH_THROUGHPUT'] = next_threadpool_size_with_throughput
    session['USER_LATENCY_DATA'] = latency_data
    session['USER_THREADPOOL_AND_THROUGHPUT_DATA'] = threadpool_and_throughput_data

    update_session_data()

    return str(next_threadpool_size_with_throughput[0])


@app.after_request
def after_request_func(response):
    global model
    iteration = int(session['ITERATION'])
    trade_off_level = float(session['TRADE_OFF_LEVEL'])
    next_throughput = list(session['NEXT_THROUGHPUT'])
    next_threadpool_size_with_throughput = list(session['NEXT_THREADPOOL_SIZE_WITH_THROUGHPUT'])
    exploration_factor = list(session['EXPLORATION_FACTOR'])
    plot_data_1 = list(session['USER_PLOT_DATA'])
    latency_data = list(session['USER_LATENCY_DATA'])
    threadpool_and_throughput_data = list(session['USER_THREADPOOL_AND_THROUGHPUT_DATA'])

    update_global_data()

    threadpool_and_throughput_data, latency_data, trade_off_level, model = update_model(
        next_threadpool_size_with_throughput, threadpool_and_throughput_data, latency_data, trade_off_level)

    plot_data_1[0].append(latency_data[-1])
    plot_data_1[1].append(threadpool_and_throughput_data[-1])
    plot_data_1[2].append(exploration_factor[-1])  # if we want to plot this

    update_min_point(threadpool_and_throughput_data, latency_data, next_throughput, model)
    exploration_factor.append(trade_off_level)

    print("inter -", iteration)
    print("workers -", next_throughput)
    print("trade_off_level -", exploration_factor[-1])
    print("Next x- ", threadpool_and_throughput_data[-1])
    print("Next y- ", latency_data[-1])
    print("min_x_data", global_data.min_x_data)
    print("min_y_data", global_data.min_y_data)
    print("-------------------------------------")

    # if iteration % 20 == 0:
    #     plot_data(plot_data_1[1], plot_data_1[0], Config.PAUSE_TIME, save=True)
    #     save_plots(plot_data_1[1])
    #     file_write(plot_data_1[1], plot_data_1[0], exploration_factor, folder_name=Config.RESULT_DATA_PATH + 'plot_')
    #     file_write(threadpool_and_throughput_data, latency_data, exploration_factor, folder_name=Config.RESULT_DATA_PATH)
    #
    # else:
    #     plot_data(plot_data_1[1], plot_data_1[0], Config.PAUSE_TIME)

    session['ITERATION'] = iteration + 1
    session['TRADE_OFF_LEVEL'] = trade_off_level
    session['EXPLORATION_FACTOR'] = exploration_factor
    session['USER_LATENCY_DATA'] = latency_data
    session['USER_THREADPOOL_AND_THROUGHPUT_DATA'] = threadpool_and_throughput_data
    session['USER_PLOT_DATA'] = plot_data_1

    update_session_data()

    return response


def update_global_data():
    global_data.min_x_data = session['MIN_X_DATA']
    global_data.min_y_data = session['MIN_Y_DATA']

    global_data.random_eval_check = session['RANDOM_EVAL_CHECK']
    global_data.eval_pool = session['EVAL_POOL']


def update_session_data():
    session['MIN_X_DATA'] = global_data.min_x_data
    session['MIN_Y_DATA'] = global_data.min_y_data

    session['RANDOM_EVAL_CHECK'] = global_data.random_eval_check
    session['EVAL_POOL'] = global_data.eval_pool


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def build_model():

    create_folders(Config.RESULT_DATA_PATH)

    train_threadpool_and_throughput_data, train_latency_data = data_generator.generate_data()

    # fit initial data to gaussian model
    gpr_model = gpr(train_threadpool_and_throughput_data, train_latency_data)

    initial_global_data = {
        "train_latency_data": train_latency_data,
        "train_threadpool_and_throughput_data": train_threadpool_and_throughput_data,

        "min_x_data": global_data.min_x_data,
        "min_y_data": global_data.min_y_data,

        "random_eval_check": global_data.random_eval_check,
        "eval_pool": global_data.eval_pool,
    }

    with open('Data/Training_data/initial_global_data.json', 'w') as fp:
        json.dump(initial_global_data, fp)

    return gpr_model


if __name__ == '__main__':
    Config.TEST_NAME = sys.argv[1]
    model = build_model()
    app.run()
