NUMBER_OF_ITERATIONS = 1000
NUMBER_OF_TRAINING_POINTS = 10
DEFAULT_TRADE_OFF_LEVEL = 0.1
PAUSE_TIME = 1

NUMBER_OF_PARAMETERS = 2
NUMBER_OF_FEATURES = 2

PARAMETERS = ['thread_pool_size', 'parameter_2']
# PARAMETERS = ['thread_pool_size']

FEATURE = ['workload', 'feature_2']
# FEATURE = ['workload']
# FEATURE = []

# PARAMETER BOUNDS
PARAMETER_BOUNDS = [[4, 10], [20, 30]]
# PARAMETER_BOUNDS = [[4, 100]]

# PARAMETER BOUNDS
FEATURE_BOUNDS = [[10, 20], [100, 110]]
# FEATURE_BOUNDS = [[10, 1000]]
# FEATURE_BOUNDS = []


# To define a new function go to simulation_utilities/data_generations/feature_generator.py
FEATURE_FUNCTION = ['STEP_INCREASE_FUNCTION', 'STEP_DECREASE_FUNCTION']
# FEATURE_FUNCTION = ['STEP_INCREASE_FUNCTION']
# FEATURE_FUNCTION = []

# FUNCTION = "(p1^2+p2^3)/(f1+f2)"
FUNCTION = "(p1^2)/(f1)"
# FUNCTION = "(pow(p1, 3) + pow(f1, 3))/(pow(p1, 2) + pow(f1, 2))"

