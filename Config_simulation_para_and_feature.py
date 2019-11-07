NUMBER_OF_ITERATIONS = 1000
NUMBER_OF_TRAINING_POINTS = 10
DEFAULT_TRADE_OFF_LEVEL = 0.1
PAUSE_TIME = 1

NUMBER_OF_PARAMETERS = 2
NUMBER_OF_FEATURES = 2

PARAMETERS = ['para_1', 'para_2']

FEATURE = ['feature_1', 'feature_2']

# PARAMETER BOUNDS
PARAMETER_BOUNDS = [[10, 20], [20, 40]]

# PARAMETER BOUNDS
FEATURE_BOUNDS = [[1, 10], [15, 25]]


# To define a new function go to simulation_utilities/data_generations/feature_generator.py
FEATURE_FUNCTION = ['STEP_INCREASE_FUNCTION', 'STEP_DECREASE_FUNCTION']

# FUNCTION = "(p1^2+p2^3)/(f1+f2)"
FUNCTION = "(p1^2)/(f1)"
# FUNCTION = "(pow(p1, 3) + pow(f1, 3))/(pow(p1, 2) + pow(f1, 2))"

