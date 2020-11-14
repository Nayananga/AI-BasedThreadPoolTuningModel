import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import Config


def compare_data(return_check=False):
    data_write_names = ("Threadpool size RMS",
                        "Threadpool size RMS %",
                        "Latency RMS",
                        "Latency RMS %",
                        "Sliced_Threadpool size RMS",
                        "Sliced_Threadpool size RMS %",
                        "Sliced_Latency RMS",
                        "Sliced_Latency RMS %")

    actual_data = pd.read_csv(Config.PATH + 'plot_thread_and_con_data.csv')
    actual_latency_data = pd.read_csv(Config.PATH + 'plot_99th_percentile_data.csv')
    reference_data = pd.read_csv(Config.REFERENCE_PATH + 'Reference_min_data.csv')
    noise_data = pd.read_csv(Config.PATH + 'plot_noise_data.csv')

    actual_threadpool = actual_data.iloc[:, 0]
    actual_concurrency = actual_data.iloc[:, 1]
    actual_latency = actual_latency_data.iloc[:, 0]
    noise_data = noise_data.iloc[:, 0]

    reference_threadpool = reference_data.iloc[:, 1]
    reference_concurrency = reference_data.iloc[:, 0]
    reference_latency = reference_data.iloc[:, 2]

    plot_reference_threadpool = []
    plot_reference_latency = []

    for j, concurrency in enumerate(actual_concurrency):
        for i in range(len(reference_concurrency)):
            if reference_concurrency[i] == concurrency:
                plot_reference_threadpool.append(reference_threadpool[i])
                plot_reference_latency.append(reference_latency[i] + noise_data[j])

    all_data = error_calculations(plot_reference_threadpool, actual_threadpool, plot_reference_latency, actual_latency)
    file_write(all_data, data_write_names)

    plot_comparison(plot_reference_threadpool, 'reference', actual_threadpool, 'actual', actual_concurrency,
                    'concurrency')

    if return_check:
        return all_data


def error_calculations(plot_reference_threadpool, actual_threadpool, plot_reference_latency, actual_latency):
    all_data = []
    sliced_number = 10
    rms_threadpool, rmsper_threadpool = rms_threadpool_calculation(plot_reference_threadpool, actual_threadpool)
    rms_latency, rmsper_latency = rms_latency_calculation(plot_reference_latency, actual_latency)

    sliced_plot_reference_threadpool = list(plot_reference_threadpool[sliced_number:])
    sliced_actual_threadpool = list(actual_threadpool[sliced_number:])
    sliced_plot_reference_latency = list(plot_reference_latency[sliced_number:])
    sliced_actual_latency = list(actual_latency[sliced_number:])

    sliced_rms_threadpool, sliced_rmsper_threadpool = rms_threadpool_calculation(sliced_plot_reference_threadpool,
                                                                                 sliced_actual_threadpool,
                                                                                 title="Sliced_Thread_pool")
    sliced_rms_latency, sliced_rmsper_latency = rms_latency_calculation(sliced_plot_reference_latency,
                                                                        sliced_actual_latency, title="Sliced_Latency")

    all_data.append(rms_threadpool)
    all_data.append(rmsper_threadpool)
    all_data.append(rms_latency)
    all_data.append(rmsper_latency)

    all_data.append(sliced_rms_threadpool)
    all_data.append(sliced_rmsper_threadpool)
    all_data.append(sliced_rms_latency)
    all_data.append(sliced_rmsper_latency)

    return all_data


def file_write(data, data_names):
    f = open(Config.PATH + "RMS.csv", "w+")
    for name in data_names:
        f.write(name)
        f.write(",")
    f.write("\n")

    for i in range(len(data)):
        f.write(str(data[i]))
        f.write(",")
    f.close()


def plot_comparison(p1=None, p1_label=None, p2=None, p2_label=None, p3=None, p3_label=None):
    plt.figure(figsize=(17, 10))

    plt.plot(p1, label=p1_label)
    plt.plot(p2, label=p2_label)
    plt.plot(p3, label=p3_label)

    plt.title('Thread pool comparison')
    plt.xlabel('time')
    plt.ylabel('threadpool_size')

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    plt.savefig(Config.PATH + "Comparison.png", bbox_inches="tight")

    # Show the plot
    # plt.show(block=False)
    #
    # plt.pause(5)
    plt.close()


def plot_error(p1=None, p1_label=None, title=None, name=None):
    plt.figure(figsize=(17, 10))

    plt.plot(p1, label=p1_label)

    plt.title(title)
    plt.xlabel('time')
    plt.ylabel('error')

    plt.grid(color='k', linestyle='-', linewidth=.1)

    # Add a legend
    plt.legend()

    plt.savefig(Config.PATH + name + ".png", bbox_inches="tight")

    # Show the plot
    # plt.show(block=False)
    #
    # plt.pause(1)
    plt.close()


def rms_threadpool_calculation(targets, predictions, title="Thread_pool"):
    error_values = []
    percentage_error_values = []
    for i in range(len(targets)):
        error = predictions[i] - targets[i]
        error_values.append(error)
        percentage_error = (error / targets[i]) * 100
        percentage_error_values.append(percentage_error)
    rms = (np.sqrt(np.mean(np.square(error_values))))
    rmsp = (np.sqrt(np.mean(np.square(percentage_error_values))))
    plot_error(error_values, title + '_error', title + '_error', title + '_error')
    plot_error(percentage_error_values, title + 'percentage_error', title + 'percentage_error',
               title + 'percentage_error')
    return rms, rmsp


def rms_latency_calculation(targets, predictions, title="Latency"):
    error_values = []
    percentage_error_values = []
    for i in range(len(targets)):
        error = targets[i] - predictions[i]
        if error < 0:
            error_values.append(error)
        else:
            error_values.append(0)
        percentage_error = (error / targets[i]) * 100
        percentage_error_values.append(percentage_error)
    rms = (np.sqrt(np.mean(np.square(error_values))))
    rmsp = (np.sqrt(np.mean(np.square(percentage_error_values))))
    plot_error(error_values, title + '_error', title + '_error', title + '_error')
    plot_error(percentage_error_values, title + 'percentage_error', title + 'percentage_error',
               title + 'percentage_error')
    return rms, rmsp
