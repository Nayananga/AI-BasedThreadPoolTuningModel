import pandas as pd
import matplotlib.pyplot as plt
import Config
import numpy as np
import csv
import sys


def compare_data():
    actual_data = pd.read_csv(Config.PATH + 'plot_thread_and_con_data.csv')
    actual_latency_data = pd.read_csv(Config.PATH + 'plot_99th_percentile_data.csv')
    reference_data = pd.read_csv(Config.REFERENCE_PATH + 'Reference_min_data.csv')

    actual_threadpool = actual_data.iloc[:, 0]
    actual_concurrency = actual_data.iloc[:, 1]
    actual_latency = actual_latency_data.iloc[:,0]

    reference_threadpool = reference_data.iloc[:, 1]
    reference_concurrency = reference_data.iloc[:, 0]
    reference_latency = reference_data.iloc[:, 2]

    plot_reference_threadpool = []
    plot_reference_latency = []

    for concurrency in actual_concurrency:
        for i in range(len(reference_concurrency)):
            if reference_concurrency[i] == concurrency:
                plot_reference_threadpool.append(reference_threadpool[i])
                plot_reference_latency.append(reference_latency[i])

    rms_error_threadpool = rms_theadpool_calculation(plot_reference_threadpool, actual_threadpool)
    rms_error_latency = rms_latency_calculation(plot_reference_latency, actual_latency)
    file_write(rms_error_threadpool, rms_error_latency)
    plot_comparison(plot_reference_threadpool, 'reference', actual_threadpool, 'actual', actual_concurrency,
                    'concurrency')


def file_write(rms_thread, rms_latency):
    f = open(Config.PATH + "RMS.csv", "w+")
    f.write('rms_error_threadpool - ' + str(rms_thread)+'\n')
    f.write('rms_error_latency - ' + str(rms_latency))
    f.close()


def plot_comparison(p1=None, p1_lable=None, p2=None, p2_lable=None, p3=None, p3_lable=None):
    plt.figure(figsize=(17, 10))

    plt.plot(p1, label=p1_lable)
    plt.plot(p2, label=p2_lable)
    plt.plot(p3, label=p3_lable)

    plt.title('Thread pool comparison')
    plt.xlabel('time')
    plt.ylabel('threadpool_size')

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    plt.savefig(Config.PATH+"Comparison.png", bbox_inches="tight")

    # Show the plot
    plt.show(block=False)

    plt.pause(5)
    plt.close()


def rms_theadpool_calculation(targets, predictions):
    error_values = []
    for i in range(len(targets)):
        error = predictions[i] - targets[i]
        error_values.append(error)
    rms = (np.sqrt(np.mean(np.square(error_values))))
    return rms


def rms_latency_calculation(targets, predictions):
    error_values = []
    for i in range(len(targets)):
        error = targets[i] - predictions[i]
        if error < 0:
            error_values.append(error)
        else:
            error_values.append(0)
    rms = (np.sqrt(np.mean(np.square(error_values))))

    return rms
