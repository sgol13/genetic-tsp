# Genetic TSP
# Szymon Golebiowski

from random import randint, shuffle, seed, random
import matplotlib.pyplot as plt

# class GeneticTSP:


N_CITIES = 12
MAX_X = 100
MAX_Y = 100

POPULATION_SIZE = 30
N_GENERATIONS = 30
INITIAL_SELECTION = 10
CHILDREN_SELECTION = 8
PARENTS_SELECTION = 8
MUTATION_PROBABILITY = 0.5


def generate_random_cities():
    return [(randint(0, MAX_X), randint(0, MAX_Y)) for _ in range(N_CITIES)]


def calculate_distance_matrix(cities):
    distances = [[0]*N_CITIES for _ in range(N_CITIES)]
    for i in range(N_CITIES):
        for j in range(N_CITIES):
            dx = cities[i][0] - cities[j][0]
            dy = cities[i][1] - cities[j][1]
            dis = (dx**2 + dy**2) ** (0.5)
            distances[i][j] = dis
            distances[j][i] = dis
    return distances


def calculate_path_length(path, distances):
    length = distances[path[-1]][path[0]]
    for i in range(0, N_CITIES-1):
        length += distances[path[i]][path[i+1]]
    return length


def draw_path(cities, path):
    plt.scatter(*zip(*cities))
    for i in range(N_CITIES):
        plt.annotate(i, cities[path[i]])

    def draw_line(p1, p2):
        xs = [cities[p1][0], cities[p2][0]]
        ys = [cities[p1][1], cities[p2][1]]
        lines = plt.plot(xs, ys)
        plt.setp(lines, color='b', linewidth=1.5)

    for i in range(N_CITIES-1):
        draw_line(path[i], path[i+1])
    draw_line(path[-1], path[0])

    plt.show()


def generate_initial_population():
    population = [[i for i in range(N_CITIES)] for _ in range(POPULATION_SIZE)]
    for path in population:
        shuffle(path)

    return population


def choose_best_solutions(distances, solutions, choose_num):
    solutions = [(calculate_path_length(path, distances), path)
                 for path in solutions]
    solutions.sort()
    _, solutions = zip(*solutions[:choose_num])
    return list(solutions)


def crossover(population):

    def crossover_pair(path1, path2):

        divide = randint(1, N_CITIES-1)

        child = path1[:divide]

        for city in path2:
            if city not in child:
                child.append(city)
        return child

    shuffle(population)
    children = []
    for i in range(0, len(population)-1, 1):
        children.append(crossover_pair(population[i], population[i+1]))

    children.append(crossover_pair(population[0], population[-1]))

    return children


def mutation(population):

    indices = [i for i in range(N_CITIES)]

    def mutation_single(path):

        nonlocal indices
        shuffle(indices)

        i1, i2 = indices[0], indices[1]

        path[i1], path[i2] = path[i2], path[i1]

    for path in population:
        if random() < MUTATION_PROBABILITY:
            mutation_single(path)


def genetic_algorithm(cities, distances):
    population = generate_initial_population()

    for generation_num in range(N_GENERATIONS):

        population = choose_best_solutions(
            distances, population, INITIAL_SELECTION)

        children = crossover(population)
        mutation(children)

        children = choose_best_solutions(
            distances, children, CHILDREN_SELECTION)

        population = choose_best_solutions(
            distances, population, PARENTS_SELECTION)

        population = population + children

    return choose_best_solutions(distances, population, 1)[0]


cities = generate_random_cities()
distances = calculate_distance_matrix(cities)
solution = genetic_algorithm(cities, distances)

draw_path(cities, solution)
