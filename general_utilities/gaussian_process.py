import numpy as np
from sklearn import gaussian_process
from sklearn.preprocessing import StandardScaler

from general_utilities.FIFO import sample_by_fifo

'''
Gaussian Model calculation with new threadpool_data
'''


def gpr(sample_data, target_data, feature_data):
    # Define the Kernel for gaussian process
    kernel = gaussian_process.kernels.Matern()

    # level of noise for gaussian
    noise_level = 1e-6

    model = gaussian_process.GaussianProcessRegressor(kernel=kernel, alpha=noise_level,
                                                      n_restarts_optimizer=10,
                                                      normalize_y=True)
    _x = np.column_stack((sample_data, feature_data))
    x = StandardScaler().fit_transform(_x)

    model.fit(x, target_data)

    return model


def update_model(next_threadpool_size, threadpool_data, target_data, feature_data, trade_off_level):
    threadpool_data, target_data, feature_data, trade_off_level = sample_by_fifo(next_threadpool_size,
                                                                                 threadpool_data,
                                                                                 target_data, feature_data,
                                                                                 trade_off_level)

    # fit new threadpool_data to gaussian process
    model = gpr(threadpool_data, target_data, feature_data)

    return threadpool_data, target_data, feature_data, trade_off_level, model
