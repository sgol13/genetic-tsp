# Genetic TSP
# Szymon Golebiowski

import matplotlib.pyplot as plt


def draw_path(solution, points):

    path = [points[i] for i in solution]

    points_num = len(solution)
    dimension = len(path[0])

    lines = [[path[i], path[i+1]] for i in range(points_num-1)]
    lines.append([path[-1], path[0]])

    if dimension == 2:

        plt.scatter(*zip(*path))

        for p1, p2 in lines:
            xs = p1[0], p2[0]
            ys = p1[1], p2[1]
            line = plt.plot(xs, ys)
            plt.setp(line, color='b', linewidth=1.5)

    elif dimension == 3:

        ax = plt.axes(projection='3d')
        ax.scatter3D(*zip(*path))

        for p1, p2 in lines:
            xs = p1[0], p2[0]
            ys = p1[1], p2[1]
            zs = p1[2], p2[2]
            line = ax.plot(xs, ys, zs)
            plt.setp(line, color='b', linewidth=1.5)

    plt.show()
