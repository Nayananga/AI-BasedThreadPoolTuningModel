import sklearn.gaussian_process as gp

'''
Gaussian Model calculation with new data
'''


def thread_pool_tuning_model(xx, yy):
    # Define the Kernel for gaussian process
    kernel = gp.kernels.Matern()

    # level of noise for gaussian
    noise_level = 1e-6

    model = gp.GaussianProcessRegressor(kernel=kernel, alpha=noise_level, n_restarts_optimizer=10, normalize_y=True)
    model.fit(xx, yy)
    return model
