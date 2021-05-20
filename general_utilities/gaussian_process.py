import numpy as np
from sklearn import gaussian_process
from sklearn.preprocessing import StandardScaler

'''
Gaussian Model calculation with new threadpool_data
'''


class GPR:

    def __init__(self, sample_data, target_data, feature_data):
        # Define the Kernel for gaussian process
        kernel = gaussian_process.kernels.Matern()

        # level of noise for gaussian
        noise_level = 1e-6

        self.model = gaussian_process.GaussianProcessRegressor(kernel=kernel, alpha=noise_level,
                                                               n_restarts_optimizer=10,
                                                               normalize_y=True)

        self.scaler = StandardScaler()
        _x = np.column_stack((sample_data, feature_data))
        x = self.scaler.fit_transform(_x)

        self.model.fit(x, target_data)

    def predict(self, query_point, return_std=False):
        x = self.scaler.transform(query_point)
        return self.model.predict(x, return_std)
