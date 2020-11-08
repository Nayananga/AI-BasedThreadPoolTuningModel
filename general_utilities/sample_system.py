import numpy as np
import sympy as sy


def generate_noise(std):
    noise_dist = np.random.normal(0, std, 1)
    return noise_dist[0]


def sample_system(formula, noise_level=0, **kwargs):
    expr = sy.sympify(formula)
    if noise_level == 0:
        latency = float(expr.evalf(subs=kwargs))
        noise = 0
    else:
        noise = generate_noise(noise_level)
        latency = float(expr.evalf(subs=kwargs)) + noise
        print(latency)
    return latency, noise
