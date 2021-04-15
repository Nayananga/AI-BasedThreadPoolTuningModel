import redis as redis
from flask import Flask, request, session
from flask_session import Session

import Config
import global_data
import threadpool_tuner as tp
from data_generation import data_generator
from general_utilities.Bayesian_point_selection import update_min_point
from general_utilities.commom_functions import create_folders
from general_utilities.data_plot import plot_data, save_plots
from general_utilities.gaussian_process import GPR

app = Flask(__name__)

app.secret_key = "My secret key"

# Configure Redis for storing the session data on the server-side
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# Create and initialize the Flask-Session object AFTER `app` has been configured
server_session = Session(app)

model = None
train_threadpool_and_throughput_data = []
train_latency_data = []

min_x = 0
min_y = 0

min_x_data = []
min_y_data = []

random_eval_check = False
eval_pool = []

optimizer_plot_data = []
object_plot_data = []

threadpool_and_throughput = []
latency = []
throughput = []


@app.before_first_request
def build_model():
    global model, train_threadpool_and_throughput_data, train_latency_data, min_x, \
        min_y, min_x_data, min_y_data, random_eval_check, eval_pool, optimizer_plot_data, \
        object_plot_data, threadpool_and_throughput, latency, throughput

    common_path = Config.COMMON_PATH
    noise_name = Config.NOISE_CHANGE

    for j, noise in enumerate(Config.NOISE_LEVEL):
        Config.COMMON_PATH = common_path + '/' + noise_name[j] + '/'
        for i in range(len(Config.FEATURE_FUNCTION_ARRAY)):
            Config.FOLDER = Config.COMMON_PATH + Config.FILE_NAME[i]
            Config.PATH = Config.FOLDER + '/'
            Config.FEATURE_FUNCTION = Config.FEATURE_FUNCTION_ARRAY[i]

            print(Config.FEATURE_FUNCTION)

            create_folders(Config.FOLDER)

    train_threadpool_and_throughput_data, train_latency_data = data_generator.generate_data()

    model = GPR(train_threadpool_and_throughput_data, train_latency_data)  # fit initial data to gaussian model

    min_x = global_data.min_x
    min_y = global_data.min_y

    min_x_data = global_data.min_x_data
    min_y_data = global_data.min_y_data

    random_eval_check = global_data.random_eval_check
    eval_pool = global_data.eval_pool

    optimizer_plot_data = global_data.optimizer_plot_data
    object_plot_data = global_data.object_plot_data

    threadpool_and_throughput = global_data.threadpool_and_throughput
    latency = global_data.latency
    throughput = global_data.throughput


@app.before_request
def before_request_func():
    global model, train_threadpool_and_throughput_data, train_latency_data, min_x, \
        min_y, min_x_data, min_y_data, random_eval_check, eval_pool, optimizer_plot_data, \
        object_plot_data, threadpool_and_throughput, latency, throughput

    if "initialized" not in session:
        print("New User : ", session.sid)

        session["initialized"] = True

        session['ITERATION'] = int(1)

        session['TRADE_OFF_LEVEL'] = float(Config.DEFAULT_TRADE_OFF_LEVEL)

        train_exploration_factor = list()
        train_exploration_factor.append(Config.DEFAULT_TRADE_OFF_LEVEL)
        session['EXPLORATION_FACTOR'] = train_exploration_factor

        session['PLOT_DATA'] = list([[], [], []])

        session['LATENCY_DATA'] = list(train_latency_data)

        session['THREADPOOL_AND_THROUGHPUT_DATA'] = list(train_threadpool_and_throughput_data)

        session["min_x"] = min_x
        session["min_y"] = min_y

        session["min_x_data"] = min_x_data
        session["min_y_data"] = min_y_data

        session["random_eval_check"] = random_eval_check
        session["eval_pool"] = eval_pool

        session["optimizer_plot_data"] = optimizer_plot_data
        session["object_plot_data"] = object_plot_data

        session["threadpool_and_throughput"] = threadpool_and_throughput
        session["latency"] = latency
        session["latency"] = throughput


@app.route('/', methods=['POST'])
def threadpool_tuner():
    global model
    trade_off_level = float(session['TRADE_OFF_LEVEL'])
    latency_data = list(session['LATENCY_DATA'])
    threadpool_and_throughput_data = list(session['THREADPOOL_AND_THROUGHPUT_DATA'])

    update_global_data()

    request_data = request.get_json()
    print(request_data)

    next_threadpool_size_with_throughput, trade_off_level = tp.find_next_threadpool_size(
        threadpool_and_throughput_data,
        latency_data, trade_off_level, model,
        [request_data['currentTenSecondRate']])

    latency_data.append(float(request_data['currentMeanLatency']))
    threadpool_and_throughput_data.append(
        [request_data['currentThreadPoolSize'], request_data['currentTenSecondRate']])

    session['NEXT_THROUGHPUT'] = [request_data['currentTenSecondRate']]
    session['NEXT_THREADPOOL_SIZE_WITH_THROUGHPUT'] = next_threadpool_size_with_throughput
    session['TRADE_OFF_LEVEL'] = trade_off_level
    session['LATENCY_DATA'] = latency_data
    session['THREADPOOL_AND_THROUGHPUT_DATA'] = threadpool_and_throughput_data

    update_session_data()

    return str(next_threadpool_size_with_throughput[0])


@app.after_request
def after_request_func(response):
    global model
    iteration = int(session['ITERATION'])
    next_threadpool_size_with_throughput = list(session['NEXT_THREADPOOL_SIZE_WITH_THROUGHPUT'])
    trade_off_level = float(session['TRADE_OFF_LEVEL'])
    exploration_factor = list(session['EXPLORATION_FACTOR'])
    next_throughput = list(session['NEXT_THROUGHPUT'])
    latency_data = list(session['LATENCY_DATA'])
    threadpool_and_throughput_data = list(session['THREADPOOL_AND_THROUGHPUT_DATA'])
    plot_data_1 = list(session['PLOT_DATA'])

    update_global_data()

    threadpool_and_throughput_data, latency_data, trade_off_level, model = tp.update_model(
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
        tp.file_write(plot_data_1[1], plot_data_1[0], exploration_factor, folder_name=Config.PATH + 'plot_')
        tp.file_write(threadpool_and_throughput_data, latency_data, exploration_factor, folder_name=Config.PATH)
        # compare_data()
        # generate_overall_error()

    else:
        plot_data(plot_data_1[1], plot_data_1[0], Config.PAUSE_TIME)

    session['ITERATION'] = iteration + 1
    session['TRADE_OFF_LEVEL'] = trade_off_level
    session['EXPLORATION_FACTOR'] = exploration_factor
    session['LATENCY_DATA'] = latency_data
    session['THREADPOOL_AND_THROUGHPUT_DATA'] = threadpool_and_throughput_data
    session['PLOT_DATA'] = plot_data_1

    update_session_data()

    return response


def update_global_data():
    global_data.min_x = session["min_x"]
    global_data.min_y = session["min_y"]

    global_data.min_x_data = session["min_x_data"]
    global_data.min_y_data = session["min_y_data"]

    global_data.random_eval_check = session["random_eval_check"]
    global_data.eval_pool = session["eval_pool"]

    global_data.optimizer_plot_data = session["optimizer_plot_data"]
    global_data.object_plot_data = session["object_plot_data"]

    global_data.threadpool_and_throughput = session["threadpool_and_throughput"]
    global_data.latency = session["latency"]
    global_data.throughput = session["latency"]


def update_session_data():
    session["min_x"] = global_data.min_x
    session["min_y"] = global_data.min_y

    session["min_x_data"] = global_data.min_x_data
    session["min_y_data"] = global_data.min_y_data

    session["random_eval_check"] = global_data.random_eval_check
    session["eval_pool"] = global_data.eval_pool

    session["optimizer_plot_data"] = global_data.optimizer_plot_data
    session["object_plot_data"] = global_data.object_plot_data

    session["threadpool_and_throughput"] = global_data.threadpool_and_throughput
    session["latency"] = global_data.latency
    session["latency"] = global_data.throughput


if __name__ == '__main__':
    app.run()
