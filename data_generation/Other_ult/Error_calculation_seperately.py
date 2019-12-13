import Config
from data_generation.Referance_data_plot import compare_data


def main():
    for i in range(len(Config.FEATURE_FUNCTION_ARRAY)):
        Config.FOLDER = Config.COMMON_PATH + Config.FILE_NAME[i]
        Config.PATH = Config.FOLDER + '/'
        Config.FEATURE_FUNCTION = Config.FEATURE_FUNCTION_ARRAY[i]

        print(Config.FEATURE_FUNCTION)

        compare_data()


if __name__ == "__main__":
    main()