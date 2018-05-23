
from model.genetic_algorithms import *


def mutation_chance_effect_on_scores():
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

    seed(2011)
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


def mutation_chance_effect_on_speed():
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

    seed(2018)
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

# seed 2018
# mutation 40: [3041, 3995, 3906, 4423, 4508, 4423, 4423, 4394, 4425, 4425]
# mutation 80: [2958, 4418, 4506, 3807, 4427, 3908, 4487, 4425, 4425, 3995]

# seed 2011
# mutation 40: [1529, 3993, 4427, 3896, 3984, 4316, 4510, 4427, 3991, 4405]
# mutation 80: [3965, 4494, 4427, 4520, 4427, 4513, 4402, 4423, 3988, 3993]

# seed 1996
# mutation 40: [4415, 4019, 4472, 3982, 4524, 3991, 4425, 4512, 4427, 4515]
# mutation 80: [3063, 4425, 4423, 4491, 4427, 4427, 4421, 4508, 4427, 4427]


mutation_chance_effect_on_speed()
