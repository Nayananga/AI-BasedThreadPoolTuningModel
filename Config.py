NUMBER_OF_ITERATIONS = 200
NUMBER_OF_TRAINING_POINTS = 30
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
# FEATURE_FUNCTION_ARRAY = [['INCREASE_AND_DECREASE_FUNCTION'], ['ONE_STEP_FUNCTION'], ['CONSTANT'], ['PEAKS'],
#                           ['RANDOM'], ['STEP_INCREASE_FUNCTION'], ['UP_AND_DOWN_FUNCTION']]

FEATURE_FUNCTION_ARRAY = [['ACTUAL']]

# FILE_NAME = ['Increase_and_decrease', 'One_step', 'Constant', 'Peaks', 'Random', 'Step_increase', 'Up_and_down']
FILE_NAME = ['ACTUAL']

# FUNCTION = "((p1-f1)^2)/20+(f1^2/1000)"
FUNCTION = "0.000002*(p1 - f1)^4 - 0.00091*(p1 - f1) ^ 3 + 0.123*(p1 - f1) ^ 2 - 4.8411*(p1 - f1)+200+ (f1 ^ 2)/1000"

ROOT_PATH = '/home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/Data/'

FUNCTION_NAME = 'Function_2'

REFERENCE_PATH = ROOT_PATH + FUNCTION_NAME + '/Reference_min_point/'

# NOISE_CHANGE = ['Without_Noise', 'With_Noise_std_1', 'With_Noise_std_5']
NOISE_CHANGE = ['Without_Noise']

# NOISE_LEVEL = [0, 1, 5]
NOISE_LEVEL = [0]

COMMON_PATH = ROOT_PATH + FUNCTION_NAME

FOLDER = None
PATH = None
FEATURE_FUNCTION = None

"""Random, From_model, Nearest_point"""
SELECTION_METHOD = "From_model"
