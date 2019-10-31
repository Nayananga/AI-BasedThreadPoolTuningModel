import numpy as np
from simulation_utilities.simulation_function_generator import function_generation
import time
import requests


# get the values when the x values are set by bayesian
def get_performance(x_pass, feature=None):
    # noise distribution for the generated function
    noise_distribution = np.random.normal(0, 2, 10)

    noise_loc = np.random.randint(0, 9)
    if type(x_pass) == list:
        x_pass = x_pass[0]

    if feature:
        if type(feature) == list:
            y_val = feature[0]
        else:
            y_val = feature
        y_pass = function_generation(x_pass, y_val)
    else:
        y_pass = function_generation(x_pass)

    return_val = y_pass + noise_distribution[noise_loc]
    return return_val


'''def get_server_performance(x_pass, lower_bound, loc, online_check):

    requests.put("http://192.168.32.2:8080/setThreadPoolNetty?size=" + str(x_pass[0]))

    time.sleep((loc + 1) * tuning_interval + start_time - time.time())

    res = requests.get("http://192.168.32.2:8080/performance-netty").json()

    data.append(res)
    logging.info("99th Percentile :" + str(res[3]))
    return float(res[3])
'''
