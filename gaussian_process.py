import sklearn.gaussian_process as gp


# gaussian model calculation with new data
def gaussian_model(xx, yy):
    # Define the Kernel for gaussian process
    kernel = gp.kernels.Matern()

    # level of noise for gaussian
    noise_level = 1e-6

    gaussian = gp.GaussianProcessRegressor(kernel=kernel, alpha=noise_level, n_restarts_optimizer=10, normalize_y=True)
    gaussian.fit(xx, yy)
    return gaussian