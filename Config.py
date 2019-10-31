from simulation_utilities.workload_generator import workload_generator

# number of training points for the gaussian
number_of_training_points = 10
default_trade_off_level = 0.1

# number_of_parameters = 2
# number_of_features = 3

'''
For simulation
'''
# bounds for the gaussian
thread_pool_max = 100
thread_pool_min = 4

pause_time = 1

# Define the number of iterations to run the bayesian optimization process
number_of_iterations = 500

# workload to simulate
# if need to check the bayesian process only for one parameter, keep the workload array as a 1x1 matrix
# For manual generation give workload manually or generate by changing the function in workload generator
# workload_array = [10]
workload_array = workload_generator(number_of_iterations)

feature_max = 1000
feature_min = 10

'''
Server optimizing
# Server optimizing
test_duration = 1000
tuning_interval = 30
'''