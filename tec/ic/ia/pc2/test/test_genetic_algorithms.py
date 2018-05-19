
import numpy as np

from random import seed
from time import time

from model.genetic_algorithms import *


def test_initialization():

    matrix = np.matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    generation, matrix_shape = initialization(matrix, 3, 'arriba', False)

    assert len(generation) == 3
    assert generation[0].get_array()[1] == 2

    # Se cambia el valor de otro objeto para asegurar que son instancias aparte
    generation[1].get_array()[1] = 3

    # Pero el valor de la arreglo 0 sigue siendo 2, y el del arreglo 1 es 3
    assert generation[0].get_array()[1] == 2
    assert generation[1].get_array()[1] == 3


def test_crossing():
    """
    Prueba de la función de cruce para 2 genes, con ambos tipos de cruce
    definidos
    :return: None
    """
    parent1 = Gen(np.array(['A', 'B', 'C', 'D', 'E', 'F', '7', '8', '9']))
    parent2 = Gen(np.array(['1', '2', '3', '4', '5', '6', 'G', 'H', 'I']))

    seed(7)

    child1, child2 = cross(parent1, parent2, 1)

    assert child1.get_array().tolist() == ['1', '2', '3',
                                           '4', '5', '6',
                                           '7', '8', '9']
    assert child2.get_array().tolist() == ['A', 'B', 'C',
                                           'D', 'E', 'F',
                                           'G', 'H', 'I']

    seed(1)

    child1, child2 = cross(child1, child2, 2)

    assert child1.get_array().tolist() == ['1', '2', 'C',
                                           '4', '5', '6',
                                           '7', '8', '9']
    assert child2.get_array().tolist() == ['A', 'B', '3',
                                           'D', 'E', 'F',
                                           'G', 'H', 'I']

    seed(time())


def test_mutation():

    gen = Gen(np.array([' ', ' ', 'C', ' ', ' ', ' ', 'Z', 'Z', ' '],
                       dtype=object))

    seed(1)
    mutation1, _ = mutate(gen, 20)  # Inserción de una flecha
    assert mutation1.get_array().tolist() == [' ', 'A', 'C', ' ', ' ',
                                              ' ', 'Z', 'Z', ' ']

    seed(2)
    mutation2, _ = mutate(gen, 20)  # Inserción de una flecha
    assert mutation2.get_array().tolist() == [' ', '<', 'C', ' ', ' ',
                                              ' ', 'Z', 'Z', ' ']

    seed(2)
    mutation3, _ = mutate(mutation2, 20)  # Cambio de dirección de la flecha
    assert mutation3.get_array().tolist() == [' ', '>', 'C', ' ', ' ',
                                              ' ', 'Z', 'Z', ' ']

    seed(time())


def test_fitness():
    """
    Prueba de la función de aptitud con cuatro soluciones diferentes
    :return: None
    """
    test_not_optimal = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '<'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['>', ' ', ' ', ' ', ' ', ' ', 'V', ' ', ' ', ' ', '>', ' ', 'Z', 'A'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '>', ' ', ' ', ' ', 'A', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['A', ' ', '<', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

    test_not_optimal = Gen((np.matrix(test_not_optimal, dtype=object)).getA1())
    eval_fitness(test_not_optimal, 'arriba', (15, 14))

    test_optimal = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['V', 'Z', '<', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['>', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Z', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

    test_optimal = Gen((np.matrix(test_optimal, dtype=object)).getA1())
    eval_fitness(test_optimal, 'arriba', (15, 14))

    assert test_not_optimal.get_score() < test_optimal.get_score()


def test_creating_generation():

    seed(2018)

    test_matrix = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Z', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

    test_matrix = np.matrix(test_matrix, dtype=object)
    first_generation, shape = initialization(initial_board=test_matrix,
                                             individuals=5,
                                             direction='arriba')
    new_generation = generate(first_generation, 1, 'arriba', shape,
                              mutation_chance=100, cross_type=1)

    assert len(new_generation) == 13

    seed(time())


def test_generation_replacement():

    seed(2018)

    test_matrix = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Z', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    individuals = 5

    test_matrix = np.matrix(test_matrix, dtype=object)
    first_generation, shape = initialization(initial_board=test_matrix,
                                             individuals= individuals,
                                             direction='arriba')

    assert len(first_generation) == individuals

    untrimmed_generation = generate(first_generation, 1, 'arriba', shape,
                                    mutation_chance=100, cross_type=1)

    assert len(untrimmed_generation) == 13

    second_generation = replacement(untrimmed_generation, individuals)

    assert len(second_generation) == individuals

    seed(time())
