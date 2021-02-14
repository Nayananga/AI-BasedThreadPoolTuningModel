from flask import Flask, request, session

import Config
import global_data as gd
import threadpool_tuner as tp
from data_generation import data_generator
from general_utilities.Bayesian_point_selection import update_min_point
from general_utilities.commom_functions import create_folders
from general_utilities.data_plot import plot_data, save_plots
from general_utilities.gaussian_process import GPR

app = Flask(__name__)

app.secret_key = "My secret key"

model = None


@app.before_first_request
def build_model():
    global model
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

    train_threadpool, train_latency = data_generator.generate_data()
    model = GPR(train_threadpool, train_latency)  # fit initial data to gaussian model
    session['ITERATION'] = int(1)
    session['TRADE_OFF_LEVEL'] = float(Config.DEFAULT_TRADE_OFF_LEVEL)
    session['EXPLORATION_FACTOR'] = list([])
    session['PLOT_DATA'] = list([[], [], []])
    session['LATENCY_DATA'] = list(train_latency)
    session['THREADPOOL_DATA'] = list(train_threadpool)


@app.route('/', methods=['POST'])
def threadpool_tuner():
    global model
    trade_off_level = float(session['TRADE_OFF_LEVEL'])
    latency_data = list(session['LATENCY_DATA'])
    threadpool_and_concurrency_data = list(session['THREADPOOL_DATA'])
    request_data = request.get_json()
    print(request_data)
    next_threadpool_size, trade_off_level = tp.find_next_threadpool_size(threadpool_and_concurrency_data,
                                                                         latency_data, trade_off_level, model,
                                                                         [request_data['currentTenSecondRate']])

    latency_data.append(float(request_data['currentMeanLatency']))
    threadpool_and_concurrency_data.append(next_threadpool_size)

    session['CONCURRENCY'] = [request_data['currentTenSecondRate']]
    session['NEXT_THREADPOOL_SIZE'] = next_threadpool_size
    session['TRADE_OFF_LEVEL'] = trade_off_level
    session['LATENCY_DATA'] = latency_data
    session['THREADPOOL_DATA'] = threadpool_and_concurrency_data
    return str(next_threadpool_size[0])


@app.after_request
def after_request_func(response):
    global model
    iteration = int(session['ITERATION'])
    next_threadpool_size = list(session['NEXT_THREADPOOL_SIZE'])
    trade_off_level = float(session['TRADE_OFF_LEVEL'])
    exploration_factor = list(session['EXPLORATION_FACTOR'])
    concurrency = list(session['CONCURRENCY'])
    latency_data = list(session['LATENCY_DATA'])
    threadpool_and_concurrency_data = list(session['THREADPOOL_DATA'])
    plot_data_1 = list(session['PLOT_DATA'])
    next_latency_value = latency_data[-1]

    threadpool_and_concurrency_data, latency_data, trade_off_level, model = tp.update_model(
        next_threadpool_size, threadpool_and_concurrency_data, latency_data, trade_off_level)

    print("inter -", iteration)
    print("workers -", concurrency)
    print("trade_off_level -", trade_off_level)
    print("Next x- ", next_threadpool_size)
    print("Next y- ", next_latency_value)
    print("min_x_data", gd.min_x_data)
    print("min_y_data", gd.min_y_data)
    print("-------------------------------------")

    plot_data_1[0].append(next_latency_value)
    plot_data_1[1].append(next_threadpool_size)
    plot_data_1[2].append(trade_off_level)

    update_min_point(threadpool_and_concurrency_data, latency_data, concurrency, model)
    exploration_factor.append(trade_off_level)

    if iteration % 20 == 0:
        plot_data(plot_data_1[1], plot_data_1[0], Config.PAUSE_TIME, save=True)
        save_plots(plot_data_1[1])
        tp.file_write(plot_data_1[1], plot_data_1[0], exploration_factor, folder_name=Config.PATH + 'plot_')
        tp.file_write(threadpool_and_concurrency_data, latency_data, exploration_factor, folder_name=Config.PATH)
        # compare_data()
        # generate_overall_error()

    else:
        plot_data(plot_data_1[1], plot_data_1[0], Config.PAUSE_TIME)

    session['ITERATION'] = iteration + 1
    session['TRADE_OFF_LEVEL'] = trade_off_level
    session['EXPLORATION_FACTOR'] = exploration_factor
    session['LATENCY_DATA'] = latency_data
    session['THREADPOOL_DATA'] = threadpool_and_concurrency_data
    session['PLOT_DATA'] = plot_data_1

    return response


if __name__ == '__main__':
    app.run()
