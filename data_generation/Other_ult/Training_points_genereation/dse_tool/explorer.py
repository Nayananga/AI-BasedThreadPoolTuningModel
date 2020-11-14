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
import os
from itertools import product

import numpy as np
import pandas as pd
from mpl_toolkits import mplot3d
from sklearn.utils import shuffle

from data_generation.Other_ult.Training_points_genereation.dse_tool.model import GPR

seed = 42
np.random.seed(seed)

plt3d = mplot3d
logger = logging.getLogger()


def eval_target(exp_func, eval_points):
    if isinstance(eval_points, dict):
        return exp_func(eval_points)
    elif isinstance(eval_points, pd.DataFrame):
        target_values = []
        for i, eval_point in eval_points.iterrows():
            target_values.append(exp_func(eval_point.to_dict()))
        return np.array(target_values).flatten()


class Explorer:

    def __init__(self, param_dist, path=None):
        """
        Register the parameters and their bounds require exploring
        Only the variables registered as a param will be explored
        :param param_dist: dictionary random distributions: {'param1':RandomInt(0, 1), 'param2':RandomFloat(0.1,0.5)}
        :param path: stores the discovered experiment results
        """
        self.param_dist = param_dist
        self.gpr = GPR(len(param_dist))

        self.path = path

    def initialize(self, n: int):
        """
        initialize the exploration by randomly sampling some design points to create the initial models
        :param n:
        :return:
        """

        to_explore = {}

        params = self.param_dist.keys()

        # finds the corners of the search space
        # reduce the extrapolation effort
        edges = []
        for prod in product(range(0, 2), repeat=len(self.param_dist)):
            edges.append(
                [self.param_dist[param].high if i else self.param_dist[param].low for i, param in zip(prod, params)])
        edges = np.array(edges).T

        # rest of the points are randomly sampled
        if n > len(edges):
            for i, param in enumerate(params):
                dist = self.param_dist[param]
                to_explore[param] = np.append(edges[i], dist.sample(n - edges.shape[1]))
        else:
            for i, param in enumerate(params):
                to_explore[param] = edges[i]

        return pd.DataFrame(data=to_explore)

    def explore(self, n: int, exp_func, target_col='target', samples=500, init_n=20):
        """
        performs Bayesian exploration
        :param n: number of iterations (number of experiments to run)
        :param exp_func: function that execute the experiment.
                        the output of the function should be the desired observation (e.g. latency or throughput)
        :param target_col: column name of the observations
        :param samples: number of samples used to profile the Gaussian models during an iteration
        :param init_n: number of randomly selected experiments to construct initial model
        :return:
        """

        if not os.path.exists(self.path):
            _dir = os.path.dirname(self.path)
            if not os.path.exists(_dir):
                os.makedirs(_dir)
            init_df = self.initialize(init_n)
            init_df[target_col] = eval_target(exp_func, init_df)
            init_df.to_csv(self.path, index=False)
        else:
            init_df = pd.read_csv(self.path)

        params = [param for param in init_df.columns if param != target_col]
        init_df = pd.read_csv(self.path)
        x = init_df[params].values
        y = init_df[target_col].values

        for i in range(n):

            losses = self.gpr.fit(x.astype(np.float), y, n_iter=100 if i > 0 else 2000, learning_rate=0.1)

            eval_data = np.empty((samples, 0))
            for param in init_df.columns:
                if param != target_col:
                    eval_data = np.append(eval_data, self.param_dist[param].sample(samples), axis=1)

            pred, unc = self.gpr.predict(eval_data)

            max_idx = np.argmax(shuffle(unc, random_state=seed))
            next_point = np.array([eval_data[max_idx]]).flatten()

            eval_y = np.array(eval_target(exp_func, {param: next_point[i]
                                                     for i, param in enumerate(init_df.columns) if
                                                     param != target_col})).flatten()
            x = np.append(x, [next_point], axis=0)
            y = np.append(y, eval_y)

            logger.info("explored params : %a eval results : %.4f" % (next_point.tolist(), eval_y))
            logger.info("iter %d with loss %.4f" % (i, losses[-1]))
            new_row = pd.DataFrame(data=np.append(next_point, eval_y).reshape(1, -1), columns=init_df.columns)
            new_row.to_csv(self.path, mode='a', header=False, index=False)

        new_df = pd.DataFrame(data=np.append(x, y.reshape(-1, 1), axis=1), columns=init_df.columns)

        return new_df
