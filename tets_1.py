import Config_simulation as Config
import numpy as np
import itertools

eval_point_size = Config.EVAL_POINT_SIZE
parameter_bounds = Config.PARAMETER_BOUNDS
parameter_count = Config.NUMBER_OF_PARAMETERS

feature_bounds = Config.FEATURE_BOUNDS
feature_count = Config.NUMBER_OF_FEATURES

print(parameter_count)
print(feature_count)

x_plot_data = [1,2,3,4]
print(x_plot_data)
x_plot_data = list(np.array(x_plot_data).reshape(-1, 1))
print(x_plot_data)
