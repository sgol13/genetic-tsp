# Genetic TSP
# Szymon Golebiowski

import random
import json


class GeneticTSP:
    def __init__(self, **parameters):

        self.__config = {
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
            if par_name in self.__config:
                self.__config[par_name] = par_val
            else:
                raise ValueError('illegal argument ' + par_name)

    def read_configuration(self, path):

        with open(path, 'r') as file:
            new_config = json.load(file)
            self.set_parameters(**new_config)

    def solve(self, points):

        distances = self.__calculate_distance_matrix(points)
        result = self.__genetic_algorithm(points, distances)

        return result

    def __genetic_algorithm(self, points, distances):

        GENERATIONS_NUM = self.__config['generations_num']
        INITIAL_SELECTION = self.__config['initial_selection']
        CHILDREN_SELECTION = self.__config['children_selection']
        PARENTS_SELECTION = self.__config['parents_selection']

        population = self.__generate_initial_population(len(points))

        for generation_num in range(GENERATIONS_NUM):

            population = self.__choose_best_solutions(
                distances, population, INITIAL_SELECTION)

            children = self.__crossover(population)
            self.__mutation(children, len(points))

            children = self.__choose_best_solutions(
                distances, children, CHILDREN_SELECTION)

            population = self.__choose_best_solutions(
                distances, population, PARENTS_SELECTION)

            population = population + children

        solution = self.__choose_best_solutions(distances, population, 1)[0]
        dis = self.__calculate_path_length(solution, distances)

        return solution, dis

    def __calculate_distance_matrix(self, points):

        points_num = len(points)
        distances = [[0]*points_num for _ in range(points_num)]

        for i in range(points_num):
            for j in range(points_num):

                squares_sum = 0
                for d in range(len(points[i])):
                    squares_sum += (points[i][d] - points[j][d]) ** 2

                dis = squares_sum ** 0.5
                distances[i][j] = dis
                distances[j][i] = dis

        return distances

    def __calculate_path_length(self, path, distances):

        length = distances[path[-1]][path[0]]
        for i in range(0, len(path)-1):
            length += distances[path[i]][path[i+1]]

        return length

    def __generate_initial_population(self, points_num):

        CHILDREN_SELECTION = self.__config['children_selection']
        PARENTS_SELECTION = self.__config['parents_selection']

        population = [[i for i in range(points_num)]
                      for _ in range(CHILDREN_SELECTION + PARENTS_SELECTION)]

        for path in population:
            random.shuffle(path)

        return population

    def __choose_best_solutions(self, distances, solutions, choose_num):

        solutions = [(self.__calculate_path_length(path, distances), path)
                     for path in solutions]
        solutions.sort()
        _, solutions = zip(*solutions[:choose_num])
        return list(solutions)

    def __crossover(self, population):

        def crossover_pair(path1, path2):

            divide = random.randint(1, len(path1)-1)

            child1 = path1[:divide]
            child2 = path2[:divide]

            for point in path2:
                if point not in child1:
                    child1.append(point)

            for point in path1:
                if point not in child2:
                    child2.append(point)

            return child1, child2

        random.shuffle(population)
        children = []
        for i in range(0, len(population)-1, 1):
            child1, child2 = crossover_pair(population[i], population[i+1])
            children.append(child1)
            children.append(child2)

        children.append(crossover_pair(population[0], population[-1]))

        return children

    def __mutation(self, population, points_num):

        MUTATION_PROBABILITY = self.__config['mutation_probability']
        indices = [i for i in range(points_num)]

        def mutation_single(path):

            nonlocal indices
            random.shuffle(indices)

            i1, i2 = indices[0], indices[1]

            path[i1], path[i2] = path[i2], path[i1]

        for path in population:
            if random.random() < MUTATION_PROBABILITY:
                mutation_single(path)
