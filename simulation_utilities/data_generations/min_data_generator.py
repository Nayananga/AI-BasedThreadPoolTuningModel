import numpy as np
from other_utilities.dictionary_creator import MyDictionary
from simulation_utilities.data_generations.relationship_generator import multiple_data

data_dictionary = MyDictionary()


def min_data_generator(formula, parameter_bounds, feature_bounds):

    for para_count in range(len(parameter_bounds)):
        bounds = np.array([[parameter_bounds[para_count][0], parameter_bounds[para_count][1] + 1]])
        data_dictionary.add('p%s' % (para_count + 1), np.arange(bounds[:, 0], bounds[:, 1], 1).reshape(-1, 1))

    for feat_count in range(len(feature_bounds)):
        bounds = np.array([[feature_bounds[feat_count][0], feature_bounds[feat_count][1] + 1]])
        data_dictionary.add('f%s' % (feat_count + 1), np.arange(bounds[:, 0], bounds[:, 1], 1).reshape(-1, 1))

    print(multiple_data(**data_dictionary, formula=formula))
