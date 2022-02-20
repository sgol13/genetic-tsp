# Genetic TSP
# Szymon Golebiowski

from random import randint, shuffle, seed, random
import json


class GeneticTSP:
    def __init__(self, **parameters):

        self.config = {
            'population_size': 16,
            'generations_num': 30,
            'initial_selection': 10,
            'children_selection': 8,
            'parents_selection': 8,
            'mutation_probability': 0.5
        }

        if 'path' in parameters.keys():
            self.read_configuration(parameters['path'])
        else:
            self.set_parameters(**parameters)

    def set_parameters(self, **parameters):

        for par_name, par_val in parameters.items():
            if par_name in self.config:
                self.config[par_name] = par_val
                print(par_name, par_val)
            else:
                raise ValueError('illegal argument ' + par_name)

    def read_configuration(self, path):

        with open(path, 'r') as file:
            new_config = json.load(file)
            self.set_parameters(**new_config)

    def solve(self, points):
        pass


solver = GeneticTSP(path='config.json')

# solver.set_parameters()
