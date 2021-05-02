from sklearn import gaussian_process
from sklearn.preprocessing import StandardScaler

'''
Gaussian Model calculation with new data
'''


def gpr(x, y):
    # Define the Kernel for gaussian process
    kernel = gaussian_process.kernels.Matern()

    # level of noise for gaussian
    noise_level = 1e-6

    model = gaussian_process.GaussianProcessRegressor(kernel=kernel, alpha=noise_level,
                                                      n_restarts_optimizer=10,
                                                      normalize_y=True)
    x = StandardScaler().fit_transform(x)
    model.fit(x, y)

    return model
