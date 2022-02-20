# Genetic TSP
# Szymon Golebiowski

import argparse
import random
from genetictsp.algorithm import GeneticTSP
from genetictsp.visualizer import draw_path


def create_arguments_parser():

    parser = argparse.ArgumentParser(
        description='Multi-dimensional Traveling Salesman Problem using genetic algorithm.'
    )

    parser.add_argument(
        '-r2', '--random2',
        type=int, action='store', default=0, metavar='N',
        help='Generates a random set of N 2D points and uses it as input data.'
    )

    parser.add_argument(
        '-r3', '--random3',
        type=int, action='store', default=0, metavar='N',
        help='Generates a random set of N 3D points and uses it as input data.'
    )

    parser.add_argument(
        '-v', '--visual',
        action='store_true',
        help='Displays a solution visualization. Works only if the given points are 2 or 3-dimensional.'
    )

    parser.add_argument(
        '--config',
        action='store', default='config.json', metavar='FILE',
        help='Reads custom algorithm configuration from a given json FILE.'
    )

    parser.add_argument(
        'input_filename',
        action='store', metavar='IN', nargs='?', default=None,
        help='Path to a file containing a set of points.'
    )

    parser.add_argument(
        'output_filename',
        action='store', metavar='OUT', nargs='?', default=None,
        help='Path to a file to which the result should be written. '
        'If not specified, the result is printed to stdout.'
    )

    parser.add_argument(
        '--population_size',
        type=int, action='store', metavar='N', default=None,
        help='Number of individuals in a single generation. Note that it directly affects only the first generation. '
    )

    parser.add_argument(
        '--generations_num',
        type=int, action='store', metavar='N', default=None,
        help='Number of generations processed by the algorithm.'
    )

    parser.add_argument(
        '--initial_selection',
        type=int, action='store', metavar='N', default=None,
        help='Number of selected best solutions during the first phase of the algorithm.'
    )

    parser.add_argument(
        '--children_selection',
        type=int, action='store', metavar='N', default=None,
        help='Number of selected best children during the second phase of the algorithm.'
    )

    parser.add_argument(
        '--parents_selection',
        type=int, action='store', metavar='N', default=None,
        help='Number of selected best parents during the second phase of the algorithm.'
    )

    parser.add_argument(
        '--mutation_probability',
        type=float, action='store', metavar='N', default=None,
        help='Probability of mutation for a single children.'
    )

    return parser


def check_arguments(args):

    if args.random2 or args.random3:
        args.output_filename = args.input_filename
        args.input_filename = None

    elif not args.input_filename:
        raise Exception('No input data provided.')


def generate_random_2d_points(points_num):
    return [[random.randint(0, 100), random.randint(0, 100)] for _ in range(points_num)]


def generate_random_3d_points(points_num):
    return [[random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
            for _ in range(points_num)]


def read_points_from_file(filename):

    with open(filename, "r") as file:
        lines = file.readlines()
        points = [[float(x) for x in line.split()] for line in lines]

        dimension = len(points[0])
        for point in points:
            if len(point) != dimension:
                raise Exception('Incorrect points\' dimensions.')

        return points


def set_custom_solver_parameters(solver, args):

    if args.population_size:
        solver.set_parameters(population_size=args.population_size)

    if args.generations_num:
        solver.set_parameters(generations_num=args.generations_num)

    if args.initial_selection:
        solver.set_parameters(initial_selection=args.initial_selection)

    if args.children_selection:
        solver.set_parameters(children_selection=args.children_selection)

    if args.parents_selection:
        solver.set_parameters(parents_selection=args.parents_selection)

    if args.mutation_probability:
        solver.set_parameters(mutation_probability=args.mutation_probability)


def solution_to_string(path, distance):
    string = "{:.3f}".format(round(distance, 3)) + '\n'
    string += '\n'.join([' '.join([str(x) for x in point]) for point in path])
    return string


def main():

    # parse command line arguments
    parser = create_arguments_parser()
    args = parser.parse_args()
    check_arguments(args)

    # prepare a set of points
    if args.random2:
        points = generate_random_2d_points(args.random2)
    elif args.random3:
        points = generate_random_3d_points(args.random3)
    else:
        points = read_points_from_file(args.input_filename)

    # run the genetic algorithm
    solver = GeneticTSP(path=args.config)
    set_custom_solver_parameters(solver, args)
    solution, distance = solver.solve(points)

    path = [points[i] for i in solution]
    string_solution = solution_to_string(path, distance)

    # save or print the result
    if args.output_filename:
        with open(args.output_filename, 'w') as file:
            file.write(string_solution)
    else:
        print(string_solution)

    # display visualization
    if args.visual:

        dimension = len(points[0])
        if dimension not in [2, 3]:
            raise Exception(
                'You can visualize only 2/3-dimensional sets of points.')

        draw_path(solution, path)


if __name__ == '__main__':
    main()
