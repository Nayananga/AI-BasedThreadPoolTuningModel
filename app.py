import redis as redis
from flask import Flask, request, session
from flask_session import Session

import Config
import global_data
from data_generation import data_generator
from general_utilities.Bayesian_point_selection import update_min_point
from general_utilities.commom_functions import create_folders
from general_utilities.data_plot import plot_data, save_plots
from general_utilities.gaussian_process import GPR
from threadpool_tuner import find_next_threadpool_size, update_model, file_write

app = Flask(__name__)

app.secret_key = "My secret key"

# Configure Redis for storing the session data on the server-side
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# Create and initialize the Flask-Session object AFTER `app` has been configured
Session(app)


class InitialData:
    min_x_data = []
    min_y_data = []

    random_eval_check = False
    eval_pool = []

    optimizer_plot_data = []
    object_plot_data = []

    threadpool_and_throughput = []
    latency = []

    train_threadpool_and_throughput_data = []
    train_latency_data = []


model = None
initial_data = None


@app.before_request
def before_request_func():
    global model, initial_data

    if "INITIALIZED" not in session:
        print("New User : ", session.sid)

        session['INITIALIZED'] = True

        session['ITERATION'] = int(1)

        session['TRADE_OFF_LEVEL'] = float(Config.DEFAULT_TRADE_OFF_LEVEL)

        session['EXPLORATION_FACTOR'] = [float(Config.DEFAULT_TRADE_OFF_LEVEL)]

        session['PLOT_DATA'] = list([[], [], []])

        session['USER_LATENCY_DATA'] = list(initial_data.train_latency_data)

        session['USER_THREADPOOL_AND_THROUGHPUT_DATA'] = list(initial_data.train_threadpool_and_throughput_data)

        print(initial_data.min_x_data)
        session['MIN_X_DATA'] = initial_data.min_x_data
        session['MIN_Y_DATA'] = initial_data.min_y_data

        session['RANDOM_EVAL_CHECK'] = initial_data.random_eval_check
        session['EVAL_POOL'] = initial_data.eval_pool

        session['OPTIMIZER_PLOT_DATA'] = initial_data.optimizer_plot_data
        session['OBJECT_PLOT_DATA'] = initial_data.object_plot_data

        session['LATENCY'] = initial_data.latency
        session['THREADPOOL_AND_THROUGHPUT'] = initial_data.threadpool_and_throughput


@app.route('/', methods=['POST'])
def threadpool_tuner():
    global model
    trade_off_level = float(session['TRADE_OFF_LEVEL'])
    latency_data = list(session['USER_LATENCY_DATA'])
    threadpool_and_throughput_data = list(session['USER_THREADPOOL_AND_THROUGHPUT_DATA'])

    update_global_data()

    request_data = request.get_json()
    print(request_data)

    next_threadpool_size_with_throughput, trade_off_level = find_next_threadpool_size(
        threadpool_and_throughput_data,
        latency_data, trade_off_level, model,
        [request_data['currentTenSecondRate']])

    latency_data.append(float(request_data['currentMeanLatency']))
    threadpool_and_throughput_data.append(
        [request_data['currentThreadPoolSize'], request_data['currentTenSecondRate']])

    session['NEXT_THROUGHPUT'] = [request_data['currentTenSecondRate']]
    session['NEXT_THREADPOOL_SIZE_WITH_THROUGHPUT'] = next_threadpool_size_with_throughput
    session['TRADE_OFF_LEVEL'] = trade_off_level
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
    latency_data = list(session['USER_LATENCY_DATA'])
    threadpool_and_throughput_data = list(session['USER_THREADPOOL_AND_THROUGHPUT_DATA'])
    plot_data_1 = list(session['PLOT_DATA'])

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

    if iteration % 20 == 0:
        plot_data(plot_data_1[1], plot_data_1[0], Config.PAUSE_TIME, save=True)
        save_plots(plot_data_1[1])
        file_write(plot_data_1[1], plot_data_1[0], exploration_factor, folder_name=Config.PATH + 'plot_')
        file_write(threadpool_and_throughput_data, latency_data, exploration_factor, folder_name=Config.PATH)
        # compare_data()
        # generate_overall_error()

    else:
        plot_data(plot_data_1[1], plot_data_1[0], Config.PAUSE_TIME)

    session['ITERATION'] = iteration + 1
    session['TRADE_OFF_LEVEL'] = trade_off_level
    session['EXPLORATION_FACTOR'] = exploration_factor
    session['USER_LATENCY_DATA'] = latency_data
    session['USER_THREADPOOL_AND_THROUGHPUT_DATA'] = threadpool_and_throughput_data
    session['PLOT_DATA'] = plot_data_1

    update_session_data()

    return response


def update_global_data():
    global_data.min_x_data = session['MIN_X_DATA']
    global_data.min_y_data = session['MIN_Y_DATA']

    global_data.random_eval_check = session['RANDOM_EVAL_CHECK']
    global_data.eval_pool = session['EVAL_POOL']

    global_data.optimizer_plot_data = session['OPTIMIZER_PLOT_DATA']
    global_data.object_plot_data = session['OBJECT_PLOT_DATA']

    global_data.threadpool_and_throughput = session['THREADPOOL_AND_THROUGHPUT']
    global_data.latency = session['LATENCY']


def update_session_data():
    session['MIN_X_DATA'] = global_data.min_x_data
    session['MIN_Y_DATA'] = global_data.min_y_data

    session['RANDOM_EVAL_CHECK'] = global_data.random_eval_check
    session['EVAL_POOL'] = global_data.eval_pool

    session['OPTIMIZER_PLOT_DATA'] = global_data.optimizer_plot_data
    session['OBJECT_PLOT_DATA'] = global_data.object_plot_data

    session['THREADPOOL_AND_THROUGHPUT'] = global_data.threadpool_and_throughput
    session['LATENCY'] = global_data.latency


def build_model():
    common_path = Config.COMMON_PATH
    noise_name = Config.NOISE_CHANGE
    initial_global_data = InitialData()

    for j, noise in enumerate(Config.NOISE_LEVEL):
        Config.COMMON_PATH = common_path + '/' + noise_name[j] + '/'
        for i in range(len(Config.FEATURE_FUNCTION_ARRAY)):
            Config.FOLDER = Config.COMMON_PATH + Config.FILE_NAME[i]
            Config.PATH = Config.FOLDER + '/'
            Config.FEATURE_FUNCTION = Config.FEATURE_FUNCTION_ARRAY[i]

            create_folders(Config.FOLDER)

    train_threadpool_and_throughput_data, train_latency_data = data_generator.generate_data()

    gpr_model = GPR(train_threadpool_and_throughput_data, train_latency_data)  # fit initial data to gaussian model

    initial_global_data.min_x_data = global_data.min_x_data
    initial_global_data.min_y_data = global_data.min_y_data

    initial_global_data.random_eval_check = global_data.random_eval_check
    initial_global_data.eval_pool = global_data.eval_pool

    initial_global_data.optimizer_plot_data = global_data.optimizer_plot_data
    initial_global_data.object_plot_data = global_data.object_plot_data

    initial_global_data.threadpool_and_throughput = global_data.threadpool_and_throughput
    initial_global_data.latency = global_data.latency

    initial_global_data.train_latency_data = train_latency_data
    initial_global_data.train_threadpool_and_throughput_data = train_threadpool_and_throughput_data

    return gpr_model, initial_global_data


if __name__ == '__main__':
    model, initial_data = build_model()
    app.run()
