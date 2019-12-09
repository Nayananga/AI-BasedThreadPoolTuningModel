NUMBER_OF_ITERATIONS = 200
NUMBER_OF_TRAINING_POINTS = 10
EVAL_POINT_SIZE = 1000
DEFAULT_TRADE_OFF_LEVEL = 0.1
PAUSE_TIME = 0.1


NUMBER_OF_PARAMETERS = 1
NUMBER_OF_FEATURES = 1

PARAMETERS = ['para_1']

FEATURE = ['feature_1']

# PARAMETER BOUNDS
PARAMETER_BOUNDS = [[1, 1000]]

# PARAMETER BOUNDS
FEATURE_BOUNDS = [[1, 500]]


# To define a new function go to simulation_utilities/data_generations/feature_generator.py

"""FEATURE_FUNCTION = ['CONSTANT']
# FEATURE_FUNCTION = ['PEAKS']
# FEATURE_FUNCTION = ['RANDOM']
# FEATURE_FUNCTION = ['STEP_INCREASE_FUNCTION']
# FEATURE_FUNCTION = ['UP_AND_DOWN_FUNCTION']

# PATH = 'Data/Function_1/With_Noise_std_5/Constant/'
PATH = 'Data/Function_3/Without_Noise/Constant/'
# PATH = 'Data/Function_1/Without_Noise/Peaks/'
# PATH = 'Data/Function_1/With_Noise_std_5/Random/'
# PATH = 'Data/Function_1/With_Noise_std_5/Step_increase/'
# PATH = 'Data/Function_1/With_Noise_std_5/Up_and_down/'"""


FEATURE_FUNCTION_ARRAY = [['CONSTANT'], ['PEAKS'], ['RANDOM'], ['STEP_INCREASE_FUNCTION'], ['UP_AND_DOWN_FUNCTION']]
FILE_NAME = ['Constant', 'Peaks', 'Random', 'Step_increase', 'Up_and_down']

# FUNCTION = "((p1-f1)^2)/20+(f1^2/1000)"
FUNCTION = "0.000002*(p1 - f1)^4 - 0.00091*(p1 - f1) ^ 3 + 0.123*(p1 - f1) ^ 2 - 4.8411*(p1 - f1)+200+ (f1 ^ 2)/1000"


REFERENCE_PATH = 'Data/Function_0/Reference_min_point/'
COMMON_PATH = '/Users/isuru/PycharmProjects/Auto-Tuning-with-Bayesian/Data/Function_0/With_Noise_std_5/'

FOLDER = None
PATH = None
FEATURE_FUNCTION = None
# #################################################

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

FUNCTION = "p1+p2+f1+f2"""""
