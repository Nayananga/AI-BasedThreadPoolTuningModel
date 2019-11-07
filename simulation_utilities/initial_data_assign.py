from simulation_utilities import ploting
from simulation_utilities.Training_point_generator import get_training_points


def initial_runs(check_number, number_of_training_points):
    if check_number == 1:
        parameter_plot_data, optimizer_plot_data = ploting.initial_plot()
        #parameter_data, optimizer_data, parameter_history = get_training_points(number_of_training_points)
        #return parameter_plot_data, optimizer_plot_data, parameter_data, optimizer_data, parameter_history

    else:
        print("asdasd")
        # x_plot_data, y_plot_data, z_plot_data = ploting.initial_2d_plot()
        # x_data, y_data, parameter_history = get_training_points(number_of_training_points, workload)


