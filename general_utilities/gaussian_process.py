import sklearn.gaussian_process as gp
from sklearn.preprocessing import StandardScaler

'''
Gaussian Model calculation with new data
'''


class GPR:

    def __init__(self, x, y):
        # Define the Kernel for gaussian process
        kernel = gp.kernels.Matern()  # TODO: Check

        # level of noise for gaussian
        noise_level = 1e-6

        self.scaler = StandardScaler()  # TODO: Check
        x = self.scaler.fit_transform(x)  # TODO: Check
        self.model = gp.GaussianProcessRegressor(kernel=kernel, alpha=noise_level, n_restarts_optimizer=10,
                                                 normalize_y=True)  # TODO: Check
        self.model.fit(x, y)

    def predict(self, x, return_std=False):
        x = self.scaler.transform(x)
        return self.model.predict(x, return_std)

    def thread_pool_tuning_model(self, yy):
        # Define the Kernel for gaussian process
        kernel = gp.kernels.Matern()

        # level of noise for gaussian
        noise_level = 1e-6

        model = gp.GaussianProcessRegressor(kernel=kernel, alpha=noise_level, n_restarts_optimizer=10, normalize_y=True)
        model.fit(self, yy)
        return model
