import sklearn.gaussian_process as gp
from sklearn.preprocessing import StandardScaler

'''
Gaussian Model calculation with new data
'''


class GPR:

    def __init__(self, x, y):
        # Define the Kernel for gaussian process
        kernel = gp.kernels.Matern()

        # level of noise for gaussian
        noise_level = 1e-6

        self.scaler = StandardScaler()
        x = self.scaler.fit_transform(x)
        self.model = gp.GaussianProcessRegressor(kernel=kernel, alpha=noise_level, n_restarts_optimizer=10,
                                                 normalize_y=True)
        self.model.fit(x, y)
        print(self.model.log_marginal_likelihood_value_)

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
        print(model.log_marginal_likelihood_value_)
        return model
