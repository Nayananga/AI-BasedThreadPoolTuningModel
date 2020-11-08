import sklearn.gaussian_process as gp
from sklearn.preprocessing import StandardScaler

'''
Gaussian Model calculation with new data
'''


class GPR:

    def __init__(self, X, y):
        # Define the Kernel for gaussian process
        kernel = gp.kernels.Matern()

        # level of noise for gaussian
        noise_level = 1e-6

        self.scaler = StandardScaler()
        X = self.scaler.fit_transform(X)
        self.model = gp.GaussianProcessRegressor(kernel=kernel, alpha=noise_level, n_restarts_optimizer=10,
                                                 normalize_y=True)
        self.model.fit(X, y)
        print(self.model.log_marginal_likelihood_value_)

    def predict(self, X, return_std=False):
        X = self.scaler.transform(X)
        return self.model.predict(X, return_std)

    def thread_pool_tuning_model(xx, yy):
        # Define the Kernel for gaussian process
        kernel = gp.kernels.Matern()

        # level of noise for gaussian
        noise_level = 1e-6

        model = gp.GaussianProcessRegressor(kernel=kernel, alpha=noise_level, n_restarts_optimizer=10, normalize_y=True)
        model.fit(xx, yy)
        print(model.log_marginal_likelihood_value_)
        return model
