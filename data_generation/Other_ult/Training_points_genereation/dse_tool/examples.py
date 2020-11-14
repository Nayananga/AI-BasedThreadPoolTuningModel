"""
 Copyright (c) 2019, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.

  WSO2 Inc. licenses this file to you under the Apache License,
  Version 2.0 (the "License"); you may not use this file except
  in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing,
  software distributed under the License is distributed on an
  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  KIND, either express or implied.  See the License for the
  specific language governing permissions and limitations
  under the License.
"""

import logging
import time
import warnings

import numpy as np
import xgboost
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from sklearn.base import clone
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.metrics import mean_squared_error

from data_generation.Other_ult.Training_points_genereation.dse_tool.explorer import Explorer
# from ..explorer import Explorer
from data_generation.Other_ult.Training_points_genereation.dse_tool.util import RandomFloat

warnings.filterwarnings("ignore")

plt3d = mplot3d
seed = 42
np.random.seed(seed)

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def mean_absolute_percentage_error(y_true, y_pred):
    """
    compute mean absolute percentage error
    :param y_true:
    :param y_pred:
    :return:
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)

    for i, y in enumerate(y_true):
        if y == 0:
            y_true[i] = 1
            y_pred[i] = 1

    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def plot1D(X, y, plot_observed_data=False, plot_predictions=False, model=None, n_test=500, ):
    plt.figure(figsize=(20, 10))

    if plot_observed_data:
        plt.plot(X, y, 'kx')

    if plot_predictions:
        Xtest = np.linspace(-0.05, 1.05, n_test).reshape(-1, 1)  # test inputs
        # compute predictive mean and variance
        mean, sd = model.predict(Xtest)
        plt.plot(Xtest, mean, 'r', lw=2)  # plot the mean
        plt.fill_between(Xtest.flatten(),  # plot the two-sigma uncertainty about the mean
                         (mean - 2.0 * sd),
                         (mean + 2.0 * sd),
                         color='C0', alpha=0.3)

    plt.xlabel("feature values")
    plt.ylabel("target values")
    plt.xlim(-0.05, 1.05)


def plot2D(X, y, model, estimator, eval_func, input_domain):
    fig = plt.figure(figsize=plt.figaspect(0.5))

    n = 30
    min_X, max_X = input_domain

    x1 = np.outer(np.linspace(min_X, max_X, n), np.ones(n))
    x2 = np.outer(np.linspace(min_X, max_X, n), np.ones(n)).T
    z = eval_func({"x1": x1.flatten(), "x2": x2.flatten()}).reshape(n, n)

    cmap = 'Spectral'
    ax = fig.add_subplot(1, 5, 1, projection='3d')
    ax.plot_surface(x1, x2, z, cmap=cmap, edgecolor='none')
    ax.set_title("true plot")
    z = model.predict(np.array([x1, x2]).T.reshape(-1, 2))[0].reshape(n, n).T

    ax = fig.add_subplot(1, 5, 2, projection='3d')
    # ax.scatter(X.T[0], X.T[1], y, marker="x")
    ax.plot_surface(x1, x2, z, cmap=cmap, edgecolor='none')
    ax.set_title("Bayesian + GP")

    xgb_adv = clone(estimator)
    xgb_adv.fit(X, y)
    z = xgb_adv.predict(np.array([x1, x2]).T.reshape(-1, 2)).reshape(n, n).T

    ax = fig.add_subplot(1, 5, 3, projection='3d')
    # ax.scatter(X.T[0], X.T[1], y, marker="x")
    ax.plot_surface(x1, x2, z, cmap=cmap, edgecolor='none')
    ax.set_title("Bayesian + XGB")

    rand_X = np.random.uniform(min_X, max_X, X.shape)
    rand_y = eval_func({"x%d" % i: _x for i, _x in enumerate(rand_X.T)})

    gpr_rand = GaussianProcessRegressor(RBF(2), alpha=0.01)
    gpr_rand.fit(rand_X, rand_y)
    z = gpr_rand.predict(np.array([x1, x2]).T.reshape(-1, 2)).reshape(n, n).T

    ax = fig.add_subplot(1, 5, 4, projection='3d')
    # ax.scatter(rand_X.T[0], rand_X.T[1], rand_y, marker="x")
    ax.plot_surface(x1, x2, z, cmap=cmap, edgecolor='none')
    ax.set_title("uniform random + GP")

    xgb_rand = clone(estimator)
    xgb_rand.fit(rand_X, rand_y)
    z = xgb_rand.predict(np.array([x1, x2]).T.reshape(-1, 2)).reshape(n, n).T

    ax = fig.add_subplot(1, 5, 5, projection='3d')
    # ax.scatter(rand_X.T[0], rand_X.T[1], rand_y, marker="x")
    ax.plot_surface(x1, x2, z, cmap=cmap, edgecolor='none')
    ax.set_title("uniform random + XGB")


def eval_accuracy(X, y, model, estimator, eval_func, input_domain):
    n = 30
    min_X, max_X, = input_domain

    test_x1 = np.outer(np.linspace(min_X, max_X, n), np.ones(n)).flatten()
    test_x2 = np.outer(np.linspace(min_X, max_X, n), np.ones(n)).T.flatten()
    test_X = np.array([test_x1, test_x2]).T.reshape(-1, 2)
    test_y = eval_func({"x1": test_x1, "x2": test_x2})

    pred_gpr = model.predict(np.array([test_x1, test_x2]).T.reshape(-1, 2))[0]
    print("Error using %d explored data with GPR MSE : %.4f ,MAPE : %.4f" % (
        X.shape[0], mean_squared_error(test_y, pred_gpr),
        mean_absolute_percentage_error(test_y, pred_gpr)))

    model_best = clone(estimator)
    model_best.fit(X, y)
    pred_best = model_best.predict(test_X)

    print("Error using %d explored data with XGB MSE : %.4f ,MAPE : %.4f" % (
        X.shape[0], mean_squared_error(test_y, pred_best),
        mean_absolute_percentage_error(test_y, pred_best)))

    rand_X = np.random.uniform(min_X, max_X, X.shape)
    rand_y = eval_func({"x%d" % i: _x for i, _x in enumerate(rand_X.T)})

    model_rand = GaussianProcessRegressor(RBF(2), alpha=0.01)
    model_rand.fit(rand_X, rand_y)
    pred_rand = model_rand.predict(test_X)

    print("Error using %d uniform sampled data with GPR MSE : %.4f ,MAPE : %.4f" % (
        rand_X.shape[0], mean_squared_error(test_y, pred_rand),
        mean_absolute_percentage_error(test_y, pred_rand)))

    model_rand = xgboost.XGBRegressor()
    model_rand.fit(rand_X, rand_y)
    pred_rand = model_rand.predict(test_X)

    print("Error using %d uniform sampled data with XGB MSE : %.4f ,MAPE : %.4f" % (
        rand_X.shape[0], mean_squared_error(test_y, pred_rand),
        mean_absolute_percentage_error(test_y, pred_rand)))


def test_eval(param_dict):
    """
    input_domain = [-2, 2]
    :param param_dict:
    :return:
    """
    X = np.array([param_dict[params] for params in param_dict])
    return np.cos(X[0].T ** 2 + X[1].T ** 2)


def rastrigin_function(param_dict):
    """
    input_domain = [-5.12, 5.12]
    :param param_dict:
    :return:
    """
    X = np.array([param_dict[params] for params in param_dict]).T.reshape(-1, 2)
    return 10 * len(param_dict) + np.sum(np.square(X) - 10 * np.cos(2 * np.pi * X), axis=1).flatten()


def rosenbrock_function(param_dict):
    """
    input_domain = [-2, 2]
    :param param_dict:
    :return:
    """
    a, b = 1, 100
    X = np.array([param_dict[params] for params in param_dict]).reshape(2, -1)
    return (a - X[0].flatten()) ** 2 + b * (X[1] - X[0] ** 2) ** 2 + np.random.normal(0, 0.2, len(X[0]))


def himmelblau_function(param_dict):
    """
    input_domain = [-5, 5]
    :param param_dict:
    :return:
    """
    X = np.array([param_dict[params] for params in param_dict]).reshape(2, -1)
    return (X[0] ** 2 + X[1] + 11) ** 2 + (X[0] + X[1] ** 2 - 7) ** 2 + np.random.normal(0, 0.2, len(X[0]))


def styblinski_tang_function(param_dict):
    """
    input_domain = [-4, 4]
    :param param_dict:
    :return:
    """
    X = np.array([param_dict[params] for params in param_dict]).reshape(2, -1).T
    return 0.5 * np.sum(X ** 4 - 16 * X ** 2 + 5 * X, axis=1) + np.random.normal(0, 0.2, X.shape[0])


def eggholder_function(param_dict):
    """
    input_domain = [-212, 212]
    :param param_dict:
    :return:
    """
    X = np.array([param_dict[params] for params in param_dict]).reshape(2, -1)
    return -(X[1] + 47) * np.sin(np.sqrt(np.abs(X[0] / 2.0 + (X[1] + 47)))) - X[0] * np.sin(
        np.sqrt(np.abs(X[0] - (X[1] + 47)))) + np.random.normal(0, 0.2, len(X[0]))


if __name__ == '__main__':
    file_id = time.time()
    step = 30
    n = 200

    eval_func = eggholder_function
    input_domain = [-212, 212]

    xgb = xgboost.XGBRegressor(verbosity=0)
    init_df = None

    explorer = Explorer(
        {
            'param1': RandomFloat(input_domain[0], input_domain[1]),
            'param2': RandomFloat(input_domain[0], input_domain[1]),
        },
        path="data/out_%d.csv" % file_id
    )

    for i in range(0, n, step):
        init_df = explorer.explore(step, eval_func, init_n=5)

        X, y = init_df.iloc[:, :-1].values, init_df.iloc[:, -1].values

        print("Number of data points : %d" % X.shape[0])
        eval_accuracy(X, y, explorer.gpr, xgb, eval_func, input_domain)

        plot2D(X, y, explorer.gpr, xgb, eval_func, input_domain)
        plt.show()
