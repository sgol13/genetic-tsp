from random import randint, shuffle, seed, random
import matplotlib.pyplot as plt

# seed(10)

# parametry losowania miast
N_CITIES = 12
MAX_X = 100
MAX_Y = 100

# parametry algorytmu genetycznego
POPULATION_SIZE = 16
N_GENERATIONS = 15
INITIAL_SELECTION = 10
CHILDREN_SELECTION = 8
PARENTS_SELECTION = 8
MUTATION_PROBABILITY = 0.5


# losuje miasta o zadanych wspolrzednych
def generate_random_cities():
    return [(randint(0, MAX_X), randint(0, MAX_Y)) for _ in range(N_CITIES)]


# na podstawie listy wspolrzednych miast oblicza macierz odleglosci miedzy miastami
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


# oblicza dlugosc trasy ustalonej przez kolejnosc wierzcholkow
def calculate_path_length(path, distances):
    length = distances[path[-1]][path[0]]
    for i in range(0, N_CITIES-1):
        length += distances[path[i]][path[i+1]]
    return length


# wyswietla trase w formie graficznej, korzystajac z biblioteki matplotlib
def draw_path(cities, path):
    plt.scatter(*zip(*cities))
    for i in range(N_CITIES):
        plt.annotate(i, cities[path[i]])

    # rysuje linie pomiedzy punktami p1 i p2
    def draw_line(p1, p2):
        xs = [cities[p1][0], cities[p2][0]]
        ys = [cities[p1][1], cities[p2][1]]
        lines = plt.plot(xs, ys)
        plt.setp(lines, color='b', linewidth=1.5)

    for i in range(N_CITIES-1):
        draw_line(path[i], path[i+1])
    draw_line(path[-1], path[0])

    plt.show()


# generuje losowo poczatkowa populacje do algorytmu genetycznego
def generate_initial_population():
    population = [[i for i in range(N_CITIES)] for _ in range(POPULATION_SIZE)]
    for path in population:
        shuffle(path)

    return population


# sposrod podanych rozwiazan wybiera choose_num najlepszych
def choose_best_solutions(distances, solutions, choose_num):
    solutions = [(calculate_path_length(path, distances), path)
                 for path in solutions]
    solutions.sort()
    _, solutions = zip(*solutions[:choose_num])
    return list(solutions)


# wykonuje krzyzowanie losowych par
def crossover(population):

    # wykonuje krzyzowanie pary osobnikow w populacji
    def crossover_pair(path1, path2):

        # losuje liczbe miast, ktore biore od pierwszego osobnika
        divide = randint(1, N_CITIES-1)

        # przepisuje poczatkowe miasta od pierwszego osobnika
        child = path1[:divide]

        # przechodze przez wszystkie miasta drugiego osobnika i w odpowiedniej
        # kolejnosci dodaje te, ktore jeszcze nie wystapily
        for city in path2:
            if city not in child:
                child.append(city)
        return child

    # losowy dobor par zapewniam w ten sposob, ze mieszam cala populacje i krzyzuje
    # te osobniki, ktore znalazly sie obok siebie (oraz pierwszy z ostatnim)
    shuffle(population)
    children = []
    for i in range(0, len(population)-1, 1):
        # krzyzuje sasiednie osobniki
        children.append(crossover_pair(population[i], population[i+1]))

    # krzyzuje pierwszego z ostatnim
    children.append(crossover_pair(population[0], population[-1]))

    return children


# dokonuje losowej mutacji osobnikow
def mutation(population):

    # tablica z indeksami - pomocna do losowania dwoch indeksow do zamiany
    indices = [i for i in range(N_CITIES)]

    # dokonuje mutacji pojedynczego osobnika
    def mutation_single(path):

        nonlocal indices
        shuffle(indices)  # mieszam tablice z indeksami

        # wybieram dwa indeksy z poczatku tablicy
        i1, i2 = indices[0], indices[1]

        # zamieniam miasta o podanych indeksach
        path[i1], path[i2] = path[i2], path[i1]

    # dla kazdego osobnika z populacji losuje czy nalezy dokonac mutacji,
    # jesli tak to uruchamiam odpowiednio funkcje, ktora mutuje osobnika
    for path in population:
        if random() < MUTATION_PROBABILITY:
            mutation_single(path)


def genetic_algorithm(cities, distances):
    population = generate_initial_population()

    for generation_num in range(N_GENERATIONS):

        # wybieram najlepsze osobniki z populacji
        population = choose_best_solutions(
            distances, population, INITIAL_SELECTION)

        # krzyzuje losowo osobniki, tworzac populacje dzieci
        children = crossover(population)

        # dokonuje losowej mutacji niektorych dzieci
        mutation(children)

        # wybieram najlepsze wyniki sposrod dzieci
        children = choose_best_solutions(
            distances, children, CHILDREN_SELECTION)

        # wybieram najlepsze wyniki sposrod rodzicow
        population = choose_best_solutions(
            distances, population, PARENTS_SELECTION)

        # lacze dzieci i rodzicow, tworzac nowa populacje
        population = population + children

    # zwracam najlepszego osobnika z koncowej populacji jako wynink
    return choose_best_solutions(distances, population, 1)[0]


cities = generate_random_cities()
distances = calculate_distance_matrix(cities)
solution = genetic_algorithm(cities, distances)

draw_path(cities, solution)
