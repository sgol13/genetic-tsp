# Genetic TSP
# Szymon Golebiowski

import matplotlib.pyplot as plt


def draw_path(cities, path):
    N_CITIES = len(cities)
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
