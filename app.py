import json
import sys

import redis as redis
from flask import Flask, request, session
from flask_session import Session

import Config
import global_data
from general_utilities.commom_functions import data_point_finder
from general_utilities.data_generation_initialization import \
    get_training_points
from general_utilities.gaussian_process import GPR
from threadpool_tuner import find_next_threadpool_size, update_model

app = Flask(__name__)

app.secret_key = "My secret key"

# Configure Redis for storing the session data on the server-side
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.from_url("redis://192.168.1.2:6379")

# Create and initialize the Flask-Session object AFTER `app` has been
# configured
Session(app)

model = None


@app.before_request
def before_request_func():
    if "INITIALIZED" not in session:
        print("New User : ", session.sid)

        with open("Data/initial_global_data.json") as f:
            initial_global_data = json.load(f)

        session["INITIALIZED"] = True
        session["ITERATION"] = int(1)
        session["TRADE_OFF_LEVEL"] = float(Config.DEFAULT_TRADE_OFF_LEVEL)
        session["EXPLORATION_FACTOR"] = [float(Config.DEFAULT_TRADE_OFF_LEVEL)]
        session["USER_PLOT_DATA"] = list([[], [], []])
        session["USER_LATENCY_DATA"] = list(
            initial_global_data["train_latency_data"])
        session["USER_THREADPOOL_AND_THROUGHPUT_DATA"] = list(
            initial_global_data["train_threadpool_and_throughput_data"]
        )
        session["EVAL_POOL"] = initial_global_data["eval_pool"]


@app.route("/", methods=["POST"])
def threadpool_tuner():
    global model
    trade_off_level = float(session["TRADE_OFF_LEVEL"])
    latency_data = list(session["USER_LATENCY_DATA"])
    threadpool_and_throughput_data = list(
        session["USER_THREADPOOL_AND_THROUGHPUT_DATA"]
    )

    update_global_data()

    request_data = request.get_json()
    print(request_data)

    next_threadpool_size_with_throughput, trade_off_level = find_next_threadpool_size(
        trade_off_level, model, float(
            request_data["currentTenSecondRate"]), float(
            request_data["current99PLatency"]), )

    # T = ThroughputOptimized, M = Mean latency Optimized, 99P = 99th
    # Percentile of latency optimized
    if request_data["optimization"] == "T":
        latency_data.append(float(request_data["currentTenSecondRate"]))
    elif request_data["optimization"] == "M":
        latency_data.append(float(request_data["currentMeanLatency"]))
    elif request_data["optimization"] == "99P":
        latency_data.append(float(request_data["current99PLatency"]))
    else:
        Exception(
            "Invalid optimization, use T = ThroughputOptimized, M = Mean latency Optimized, 99P = 99th "
            "Percentile of latency optimized")

    threadpool_and_throughput_data.append(
        [request_data["currentThreadPoolSize"], request_data["currentTenSecondRate"]]
    )

    session["TRADE_OFF_LEVEL"] = trade_off_level
    session["USER_LATENCY_DATA"] = latency_data
    session["USER_THREADPOOL_AND_THROUGHPUT_DATA"] = threadpool_and_throughput_data

    return str(next_threadpool_size_with_throughput[0])


@app.after_request
def after_request_func(response):
    global model
    iteration = int(session["ITERATION"])
    trade_off_level = float(session["TRADE_OFF_LEVEL"])
    exploration_factor = list(session["EXPLORATION_FACTOR"])
    plot_data_1 = list(session["USER_PLOT_DATA"])
    latency_data = list(session["USER_LATENCY_DATA"])
    threadpool_and_throughput_data = list(
        session["USER_THREADPOOL_AND_THROUGHPUT_DATA"]
    )

    update_global_data()

    model = update_model(threadpool_and_throughput_data, latency_data)

    plot_data_1[0].append(latency_data[-1])
    plot_data_1[1].append(threadpool_and_throughput_data[-1])
    plot_data_1[2].append(exploration_factor[-1])  # if we want to plot this
    exploration_factor.append(trade_off_level)

    print("inter -", iteration)
    print("trade_off_level -", exploration_factor[-1])
    print("Next x- ", threadpool_and_throughput_data[-1])
    print("Next y- ", latency_data[-1])
    print("min_x_data", global_data.min_x_data)
    print("min_y_data", global_data.min_y_data)
    print("-------------------------------------")

    session["ITERATION"] = iteration + 1
    session["TRADE_OFF_LEVEL"] = trade_off_level
    session["EXPLORATION_FACTOR"] = exploration_factor
    session["USER_LATENCY_DATA"] = latency_data
    session["USER_THREADPOOL_AND_THROUGHPUT_DATA"] = threadpool_and_throughput_data
    session["USER_PLOT_DATA"] = plot_data_1

    return response


def update_global_data():
    global_data.min_x_data = session["USER_THREADPOOL_AND_THROUGHPUT_DATA"]
    global_data.min_y_data = session["USER_LATENCY_DATA"]
    global_data.eval_pool = session["EVAL_POOL"]


def build_model():

    train_threadpool_and_throughput_data, train_latency_data = get_training_points()

    gpr_model = GPR(
        train_threadpool_and_throughput_data, train_latency_data
    )  # fit initial data to gaussian model

    initial_global_data = {
        "train_latency_data": train_latency_data,
        "train_threadpool_and_throughput_data": train_threadpool_and_throughput_data,
        "eval_pool": data_point_finder(
            Config.PARAMETER_BOUNDS),
    }

    with open("Data/initial_global_data.json", "w") as fp:
        json.dump(initial_global_data, fp)

    return gpr_model


if __name__ == "__main__":
    Config.TEST_NAME = sys.argv[1]
    model = build_model()
    app.run(host="0.0.0.0")
