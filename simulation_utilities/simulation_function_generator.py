import numpy as np


# Function to minimize
def function_generation(parameter_value, feature_value=None):
    #return -1.0 * np.sin(parameter_value / 10.0) * parameter_value
    #return (pow(parameter_value, 3) + pow(feature_value, 3))/(pow(parameter_value, 2) + pow(feature_value, 2))
    p1 = parameter_value[0]
    p2 = parameter_value[1]
    f1 = parameter_value[0]
    f2 = parameter_value[1]
    return p1+p2


