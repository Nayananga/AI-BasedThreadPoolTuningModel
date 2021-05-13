import numpy as np
from sklearn import gaussian_process
from sklearn.preprocessing import StandardScaler

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
    _x = np.column_stack((target_data, feature_data))
    x = StandardScaler().fit_transform(_x)

    model.fit(x, sample_data)

    return model
