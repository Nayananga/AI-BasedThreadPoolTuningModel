import matplotlib.pyplot as plt
import numpy as np


def plot_approximation(gpr, x, y, x_sample, y_sample, x_next=None, show_legend=False):
    mu, std = gpr.predict(x)
    plt.fill_between(x.ravel(),
                     mu.ravel() + 1.96 * std,
                     mu.ravel() - 1.96 * std,
                     alpha=0.1)
    plt.plot(x, y, 'y--', lw=1, label='Noise-free objective')
    plt.plot(x, mu, 'b-', lw=1, label='Surrogate function')
    plt.plot(x_sample, y_sample, 'kx', mew=3, label='Noisy samples')
    if x_next:
        plt.axvline(x=x_next, ls='--', c='k', lw=1)
    if show_legend:
        plt.legend()


def plot_acquisition(x, y, x_next, show_legend=False):
    plt.plot(x, y, 'r-', lw=1, label='Acquisition function')
    plt.axvline(x=x_next, ls='--', c='k', lw=1, label='Next sampling location')
    if show_legend:
        plt.legend()


def plot_convergence(x_sample, y_sample, n_init=2):
    plt.figure(figsize=(12, 3))

    x = x_sample[n_init:].ravel()
    y = y_sample[n_init:].ravel()
    r = range(1, len(x) + 1)

    x_neighbor_dist = [np.abs(a - b) for a, b in zip(x, x[1:])]
    y_max_watermark = np.maximum.accumulate(y)

    plt.subplot(1, 2, 1)
    plt.plot(r[1:], x_neighbor_dist, 'bo-')
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title('Distance between consecutive x\'s')

    plt.subplot(1, 2, 2)
    plt.plot(r, y_max_watermark, 'ro-')
    plt.xlabel('Iteration')
    plt.ylabel('Best Y')
    plt.title('Value of best selected sample')
