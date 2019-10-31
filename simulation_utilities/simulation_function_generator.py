import numpy as np


# Function to minimize
def function_generation(x_value, y_value=None):
    if y_value is None:
        return -1.0 * np.sin(x_value / 10.0) * x_value
    else:
        # return pow(x_value, 3) - 3 * x_value * pow(y_value, 2)
        return (pow(x_value, 3) + pow(y_value, 3))/(pow(x_value, 2) + pow(y_value, 2))
