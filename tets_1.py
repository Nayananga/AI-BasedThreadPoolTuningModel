# Create your dictionary class
import numpy as np

class my_dictionary(dict):

    # __init__ function 
    def __init__(self):
        self = dict()

        # Function to add key:value 

    def add(self, key, value):
        self[key] = value

dict_obj = my_dictionary()

bounds = np.array([[1, 181]])

dict_obj.add('p%s' % 1, np.arange(bounds[:, 0], bounds[:, 1], 1).reshape(-1, 1))
dict_obj.add(2, 'forGeeks')

print(dict_obj)
