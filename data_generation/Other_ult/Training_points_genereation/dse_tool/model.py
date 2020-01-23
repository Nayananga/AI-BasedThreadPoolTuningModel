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

import numpy as np

import pyro
import pyro.contrib.gp as gp
import torch

assert pyro.__version__.startswith('1.1.0')
# pyro.enable_validation(True)  # can help with debugging

seed = 42
np.random.seed(seed)
pyro.set_rng_seed(seed)


class GPR:

    def __init__(self, dim, lengthscale=0.5, variance=1):
        self.dim = dim
        self.kernel = gp.kernels.RBF(input_dim=dim, variance=torch.tensor(variance),
                                     lengthscale=torch.tensor(lengthscale))

        self.gpr = self.optimizer = self.loss_fn = None

    def fit(self, X, y, n_iter=100, learning_rate=0.005):

        if X.shape[1] != self.dim:
            raise Exception("number of features should be %d, provided %d" % (self.dim, X.shape[1]))

        if not torch.is_tensor(X):
            X = np.copy(X)
            X = torch.tensor(X)

        if not torch.is_tensor(y):
            y = np.copy(y)
            y = torch.tensor(y)

        if self.gpr is None:
            self.gpr = gp.models.GPRegression(X, y, self.kernel, noise=torch.tensor(0.1))

            # initiate the optimizer
            self.optimizer = torch.optim.Adam(self.gpr.parameters(), lr=learning_rate)
            self.loss_fn = pyro.infer.Trace_ELBO().differentiable_loss

        else:
            self.gpr.set_data(X, y)

        # learning hyper-parameters from the model
        losses = []
        for i in range(n_iter):
            self.optimizer.zero_grad()
            loss = self.loss_fn(self.gpr.model, self.gpr.guide)
            loss.backward()
            self.optimizer.step()
            losses.append(loss.item())

        return losses

    def predict(self, X, return_unc=True):

        if X.shape[1] != self.dim:
            raise Exception("number of features should be %d, provided %d" % (self.dim, X.shape[1]))

        if self.gpr is None:
            raise Exception("train the model once first")

        X = np.copy(X)

        if not torch.is_tensor(X):
            X = torch.tensor(X)

        with torch.no_grad():
            mean, cov = self.gpr(X, full_cov=True, noiseless=False)
        mean, cov = mean.numpy(), cov.numpy()

        if return_unc:
            return mean, np.sqrt(np.diag(cov))
        return mean
