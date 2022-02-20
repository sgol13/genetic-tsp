from setuptools import setup, find_packages

setup(
    name='genetictsp',
    version='1.0',
    packages=['genetictsp'],
    url='https://github.com/sgol13/genetic-tsp',
    license='MIT',
    author='Szymon Gołębiowski',
    author_email='szymon13gol@gmail.com',
    description='Multi-dimensional Traveling Salesman Problem using genetic algorithm',
    install_requires=['matplotlib>=3.3.4'],
    entry_points={'console_scripts': [
        'genetictsp = genetictsp.main:main', ], }
)
