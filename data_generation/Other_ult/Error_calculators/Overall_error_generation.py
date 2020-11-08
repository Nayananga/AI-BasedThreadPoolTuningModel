import Config
from data_generation.Referance_data_plot import compare_data

COMMON_PATH = Config.ROOT_PATH + Config.FUNCTION_NAME + '/'


def write_overall_all_error(data, data_names, identifiers):
    f = open(COMMON_PATH + "Overall_error.csv", "w+")
    for name in data_names:
        f.write(name)
        f.write(",")

    f.write("\n")

    for i in range(len(data)):
        for identity in identifiers[i]:
            f.write(str(identity))
            f.write(",")
        for error in data[i]:
            f.write(str(error))
            f.write(",")
        f.write("\n")
    f.close()


def generate_overall_error():
    error_data = []
    noise_change = Config.NOISE_CHANGE
    overall_error_name = []
    for noise in noise_change:
        for concurrency in range(len(Config.FEATURE_FUNCTION_ARRAY)):
            error_name = []
            Config.FOLDER = COMMON_PATH + noise + '/' + Config.FILE_NAME[concurrency]
            Config.PATH = Config.FOLDER + '/'
            Config.FEATURE_FUNCTION = Config.FEATURE_FUNCTION_ARRAY[concurrency]

            print(Config.FEATURE_FUNCTION)

            error_name.append(noise)
            error_name.append(Config.FILE_NAME[concurrency])
            overall_error_name.append(error_name)

            error_data.append(compare_data(return_check=True))

    data_write_names = "Noise", "Concurrency change", "Threadpool size RMS", "Threadpool size RMS %", "Latency RMS", "Latency RMS %", "Sliced_Threadpool size RMS", "Sliced_Threadpool size RMS %", "Sliced_Latency RMS", "Sliced_Latency RMS %"
    write_overall_all_error(error_data, data_write_names, overall_error_name)

# generate_overall_error()
