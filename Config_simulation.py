NUMBER_OF_ITERATIONS = 100
NUMBER_OF_TRAINING_POINTS = 10
EVAL_POINT_SIZE = 1000
DEFAULT_TRADE_OFF_LEVEL = 0.1
PAUSE_TIME = 1

"""NUMBER_OF_PARAMETERS = 1
NUMBER_OF_FEATURES = 0

PARAMETERS = ['para_1']

FEATURE = []

# PARAMETER BOUNDS
PARAMETER_BOUNDS = [[10, 40]]

# PARAMETER BOUNDS
FEATURE_BOUNDS = []


# To define a new function go to simulation_utilities/data_generations/feature_generator.py
FEATURE_FUNCTION = []

#FUNCTION = "-1.0 * sin(p1 / 10.0) * p1"
FUNCTION = "p1"""

# #################################################

"""NUMBER_OF_PARAMETERS = 2
NUMBER_OF_FEATURES = 0

PARAMETERS = ['para_1', 'para_2']

FEATURE = []

# PARAMETER BOUNDS
PARAMETER_BOUNDS = [[10, 20], [10, 20]]

# PARAMETER BOUNDS
FEATURE_BOUNDS = []


# To define a new function go to simulation_utilities/data_generations/feature_generator.py
FEATURE_FUNCTION = []

FUNCTION = "p1+p2"""

# #################################################

NUMBER_OF_PARAMETERS = 1
NUMBER_OF_FEATURES = 1

PARAMETERS = ['para_1']

FEATURE = ['feature_1']

# PARAMETER BOUNDS
PARAMETER_BOUNDS = [[10, 20]]

# PARAMETER BOUNDS
FEATURE_BOUNDS = [[1, 10]]


# To define a new function go to simulation_utilities/data_generations/feature_generator.py
FEATURE_FUNCTION = ['STEP_INCREASE_FUNCTION']

FUNCTION = "p1+f1"

# #################################################


"""NUMBER_OF_PARAMETERS = 2
NUMBER_OF_FEATURES = 2

PARAMETERS = ['para_1', 'para_2']

FEATURE = ['feature_1', 'feature_2']

# PARAMETER BOUNDS
# PARAMETER_BOUNDS = [[10, 20], [20, 30]]
PARAMETER_BOUNDS = [[10, 25], [20, 25]]

# PARAMETER BOUNDS
FEATURE_BOUNDS = [[0, 5], [15, 20]]
# FEATURE_BOUNDS = [[0, 10], [15, 25]]


# To define a new function go to simulation_utilities/data_generations/feature_generator.py
FEATURE_FUNCTION = ['STEP_INCREASE_FUNCTION', 'STEP_DECREASE_FUNCTION']

FUNCTION = "p1+p2+f1+f2"""
