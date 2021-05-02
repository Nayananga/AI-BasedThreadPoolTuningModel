from sklearn import gaussian_process
from sklearn.preprocessing import StandardScaler

'''
Gaussian Model calculation with new data
'''


class GPR:

    def __init__(self, x, y):
        # Define the Kernel for gaussian process
        kernel = gaussian_process.kernels.Matern()

        # level of noise for gaussian
        noise_level = 1e-6

        self.scaler = StandardScaler()
        x = self.scaler.fit_transform(x)
        self.model = gaussian_process.GaussianProcessRegressor(kernel=kernel, alpha=noise_level,
                                                               n_restarts_optimizer=10,
                                                               normalize_y=True)
        self.model.fit(x, y)

    def predict(self, x, return_std=False):
        x = self.scaler.transform(x)
        return self.model.predict(x, return_std)
