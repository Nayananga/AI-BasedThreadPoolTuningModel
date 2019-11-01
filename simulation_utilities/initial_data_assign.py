import Config as Cg
from simulation_utilities import ploting
from simulation_utilities.Training_point_generator import get_training_points
from simulation_utilities.workload_generator import workload_config

workload_ini = Cg.workload_array

# number of initial points for the gaussian
number_of_training_points = Cg.number_of_training_points

max_iterations = Cg.number_of_iterations


def initial_data_assign():

    one_parameter = False

    workload = workload_config(workload_ini, max_iterations)

    if len(workload_ini) == 1:
        one_parameter = True
        x_plot_data, y_plot_data = ploting.initial_plot()
        x_data, y_data, parameter_history = get_training_points(number_of_training_points)
        z_plot_data = []

    else:
        x_plot_data, y_plot_data, z_plot_data = ploting.initial_2d_plot()
        x_data, y_data, parameter_history = get_training_points(number_of_training_points, workload)

    return one_parameter, x_plot_data, y_plot_data, z_plot_data, x_data, y_data, parameter_history, workload
