# Genetic Algortihm for TSP
This project is an application of a [genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm) for the [Travelling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem). I've written it to experiment with this peculiar nature-inspired approach to optimization problems. You can use it to solve TSP problem for any n-dimensional set of points. Furthermore, solutions for 2 and 3-dimensional datasets can be visualized. The package can be utilized both as a command line tool and as a library imported into some other Python code.


## Installation
Clone the repository and install the package using a prepared setup script.
```
git clone https://github.com/sgol13/genetic-tsp.git
cd genetic-tsp
python3 setup.py install --user
```

## Usage
#### Command line
As mentioned previously, you can use the package as a command line tool. The program will read a set of points from a given file, perform the calculations and visualize the obtained solution.
```
genetictsp -v --config custom_cfg.json in.txt out.txt
```


The full manual is presented below. It can be accessed also by `genetictsp --help`.
```
usage: genetictsp [-h] [-r2 N] [-r3 N] [-v] [--config FILE]
                  [--population_size N] [--generations_num N]
                  [--initial_selection N] [--children_selection N]
                  [--parents_selection N] [--mutation_probability N]
                  [IN] [OUT]

Multi-dimensional Traveling Salesman Problem using genetic algorithm.

positional arguments:
  IN                    Path to a file containing a set of points.
  OUT                   Path to a file to which the result should be written.
                        If not specified, the result is printed to stdout.

optional arguments:
  -h, --help            show this help message and exit
  -r2 N, --random2 N    Generates a random set of N 2D points and uses it as
                        input data.
  -r3 N, --random3 N    Generates a random set of N 3D points and uses it as
                        input data.
  -v, --visual          Displays a solution visualization. Works only if the
                        given points are 2 or 3-dimensional.
  --config FILE         Reads custom algorithm configuration from a given json
                        FILE.
  --population_size N   Number of individuals in a single generation. Note
                        that it directly affects only the first generation.
  --generations_num N   Number of generations processed by the algorithm.
  --initial_selection N
                        Number of selected best solutions during the first
                        phase of the algorithm.
  --children_selection N
                        Number of selected best children during the second
                        phase of the algorithm.
  --parents_selection N
                        Number of selected best parents during the second
                        phase of the algorithm.
  --mutation_probability N
                        Probability of mutation for a single children.
```
#### Import
If you want to use the package as a 

## License
This project is under MIT [license](LICENSE).


