import numpy as np


# Function to minimize
def function_generation(x_value):
    return -1.0*np.sin(x_value/10.0)*x_value