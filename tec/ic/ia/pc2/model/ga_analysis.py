
from model.genetic_algorithms import *

"""
    Este archivo no es utilizado durante la ejecución normal de cualquiera 
    de los algoritmos del proyecto.
"""


def mutation_chance_effect_on_scores(custom_seed=0):
    """
    La intención de esta función es ejecutar el algoritmo genético
    definiendo una semilla para controlar la aleatoriedad, para así realizar
    el análisis entre la probabilidad de mutación y los puntajes de aptitud
    máximos que se obtiene con diferentes poblaciones.
    :return: Sin retorno
    """
    starting_board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'Z', ' ', ' ', ' ', 'Z', 'Z', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    starting_board = np.matrix(starting_board, object)

    mutation40 = list()
    mutation80 = list()

    seed(custom_seed)
    for gen_number in range(100, 1100, 100):
        best_gen = run_carrot_finder(initial_direction='derecha',
                                     individuals=15,
                                     max_generations=gen_number,
                                     mutation_chance=40,
                                     initial_board=starting_board,
                                     cross_type=1)[0]
        mutation40.append(best_gen.get_score())

        best_gen = run_carrot_finder(initial_direction='derecha',
                                     individuals=15,
                                     max_generations=gen_number,
                                     mutation_chance=80,
                                     initial_board=starting_board,
                                     cross_type=1)[0]
        mutation80.append(best_gen.get_score())

        print(str(gen_number) + ' generaciones terminadas.')

    print(mutation40)
    print(mutation80)


def mutation_chance_effect_on_speed(custom_seed=0):
    """
    La intención de esta función es ejecutar el algoritmo genético
    definiendo una semilla para controlar la aleatoriedad, para así realizar
    el análisis entre la probabilidad de mutación y la velocidad con que se
    llega a la solución de mejor aptitud según el algoritmo.
    :return: Sin retorno
    """
    starting_board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'Z', ' ', ' ', ' ', 'Z', 'Z', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    starting_board = np.matrix(starting_board, object)

    mutation40 = list()
    mutation80 = list()

    seed(custom_seed)
    for gen_number in range(0, 10):
        best_gen, optimal_generation = run_carrot_finder(
            initial_direction='derecha',
            individuals=15,
            max_generations=550,
            mutation_chance=40,
            initial_board=starting_board,
            cross_type=1, return_generation_number=True)

        mutation40.append((best_gen[0].get_score(), optimal_generation))

        best_gen, optimal_generation = run_carrot_finder(
            initial_direction='derecha',
            individuals=15,
            max_generations=550,
            mutation_chance=80,
            initial_board=starting_board,
            cross_type=1, return_generation_number=True)

        mutation80.append((best_gen[0].get_score(), optimal_generation))

        print(str(gen_number) + ' terminadas.')

    print(mutation40)
    print(mutation80)


# SOLUTION SPEED

# seed 2018
# mutation 40: [(3980, 254), (4507, 428), (4423, 226), (4318, 390),
# (3989, 227), (4427, 77), (4423, 167), (4489, 482), (4522, 79), (4427, 40)]
# mutation 80: [(4507, 85), (3996, 335), (3982, 305), (4427, 393),
# (4370, 295), (4522, 236), (4522, 52), (3993, 179), (3991, 70), (3980, 160)]


# SCORES

# seed 2018 -> diferencia: 607 osea m40 > m80
# mutation 40: [3041, 3995, 3906, 4423, 4508, 4423, 4423, 4394, 4425, 4425]
# mutation 80: [2958, 4418, 4506, 3807, 4427, 3908, 4487, 4425, 4425, 3995]

# seed 2011 -> diferencia: -3674 osea m80 > m40
# mutation 40: [1529, 3993, 4427, 3896, 3984, 4316, 4510, 4427, 3991, 4405]
# mutation 80: [3965, 4494, 4427, 4520, 4427, 4513, 4402, 4423, 3988, 3993]

# seed 1996 -> diferencia: 243 osea m40 > m80
# mutation 40: [4415, 4019, 4472, 3982, 4524, 3991, 4425, 4512, 4427, 4515]
# mutation 80: [3063, 4425, 4423, 4491, 4427, 4427, 4421, 4508, 4427, 4427]

# seed 5 -> diferencia: -3393 osea m80 > m40
# mutation 40: [1037, 4518, 4425, 4423, 4427, 4414, 3993, 3986, 3994, 4320]
# mutation 80: [4006, 4379, 4423, 4423, 4006, 4427, 4425, 4423, 3991, 4427]


def cross_policy_effect_on_scores(custom_seed=0):
    """
    La intención de esta función es ejecutar el algoritmo genético
    definiendo una semilla para controlar la aleatoriedad, para así realizar
    el análisis entre la política de cruce y los puntajes de aptitud
    máximos que se obtiene con diferentes poblaciones.
    :return: Sin retorno
    """
    starting_board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'Z', ' ', ' ', ' ', 'Z', 'Z', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    starting_board = np.matrix(starting_board, object)

    cross1point = list()
    cross2points = list()

    seed(custom_seed)
    for gen_number in range(100, 900, 100):
        best_gen = run_carrot_finder(initial_direction='derecha',
                                     individuals=15,
                                     max_generations=gen_number,
                                     mutation_chance=50,
                                     initial_board=starting_board,
                                     cross_type=1)[0]
        cross1point.append(best_gen.get_score())

        best_gen = run_carrot_finder(initial_direction='derecha',
                                     individuals=15,
                                     max_generations=gen_number,
                                     mutation_chance=50,
                                     initial_board=starting_board,
                                     cross_type=2)[0]
        cross2points.append(best_gen.get_score())

        print(str(gen_number) + ' generaciones terminadas.')

    print(cross1point)
    print(cross2points)


def cross_policy_effect_on_speed(custom_seed=0):
    """
    La intención de esta función es ejecutar el algoritmo genético
    definiendo una semilla para controlar la aleatoriedad, para así realizar
    el análisis entre la probabilidad de mutación y la velocidad con que se
    llega a la solución de mejor aptitud según el algoritmo.
    :return: Sin retorno
    """
    starting_board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'Z', ' ', ' ', ' ', 'Z', 'Z', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    starting_board = np.matrix(starting_board, object)

    cross1 = list()
    cross2 = list()

    seed(custom_seed)
    for gen_number in range(0, 10):
        best_gen, optimal_generation = run_carrot_finder(
            initial_direction='derecha',
            individuals=15,
            max_generations=550,
            mutation_chance=50,
            initial_board=starting_board,
            cross_type=1, return_generation_number=True)

        cross1.append((best_gen[0].get_score(), optimal_generation))

        best_gen, optimal_generation = run_carrot_finder(
            initial_direction='derecha',
            individuals=15,
            max_generations=550,
            mutation_chance=50,
            initial_board=starting_board,
            cross_type=1, return_generation_number=True)

        cross2.append((best_gen[0].get_score(), optimal_generation))

        print(str(gen_number) + ' terminadas.')

    print(cross1)
    print(cross2)


# SOLUTION SPEED

# seed 2018
# cross type 1: [(4425, 39), (3910, 237), (4391, 227), (3984, 248),
# (4427, 203), (4425, 27), (4425, 39), (3976, 161), (4425, 140), (4425, 186)]
# cross type 1: [(3908, 154), (4019, 161), (4427, 295), (4522, 192),
# (4520, 228), (4427, 133), (4427, 76), (4427, 135), (4423, 163), (4425, 329)]


# SCORES

# seed 2018 -> diferencia: - 839 osea c2 > c1
# cross type 1: [4425, 4425, 3991, 3083, 3904, 4425, 3991, 4423]
# cross type 2: [4390, 4415, 3982, 3983, 3995, 3891, 4427, 4423]

# seed 2011 -> diferencia: - 1201 osea c2 > c1
# cross type 1: [3039, 4423, 4516, 4318, 4481, 3995, 4423, 4502]
# cross type 2: [4417, 3888, 4427, 4427, 4409, 4423, 4484, 4423]

# seed 1996 -> diferencia: 525 osea c1 > c2
# cross type 1: [4415, 4405, 3800, 4517, 3987, 3906, 4425, 4427]
# cross type 2: [3993, 3995, 4524, 3995, 3993, 4524, 4423, 3910]

# seed 5 -> diferencia: - 1612 osea c2 > c1
# cross type 1: [2953, 4522, 4508, 4423, 3982, 4524, 3995, 3987]
# cross type 2: [4401, 4423, 4423, 4418, 3908, 3985, 4521, 4427]
