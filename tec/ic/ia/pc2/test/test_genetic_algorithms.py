
import numpy as np

from random import seed
from time import time

from model.genetic_algorithms import *


def test_crossing():
    """
    Prueba de la función de cruce para 2 genes, con ambos tipos de cruce
    definidos
    :return: None
    """
    parent1 = np.array(['A', 'B', 'C', 'D', 'E', 'F', '7', '8', '9'])
    parent2 = np.array(['1', '2', '3', '4', '5', '6', 'G', 'H', 'I'])

    seed(7)

    child1, child2 = cross(parent1, parent2, 1)

    assert child1.tolist() == ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    assert child2.tolist() == ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    seed(1)

    child1, child2 = cross(child1, child2, 2)

    child1.tolist() == ['1', '2', 'C', '4', '5', '6', '7', '8', '9']
    child2.tolist() == ['A', 'B', '3', 'D', 'E', 'F', 'G', 'H', 'I']

    seed(time())


def test_mutation():

    gen = np.array(['', '', 'C', '', '', '', 'Z', 'Z', ''], dtype=object)

    seed(1)
    mutation1 = mutate(gen, 20)  # Inserción de una flecha
    assert mutation1.tolist() == ['', 'A', 'C', '', '', '', 'Z', 'Z', '']

    seed(2)
    mutation2 = mutate(gen, 20)  # Inserción de una flecha
    assert mutation2.tolist() == ['', '<', 'C', '', '', '', 'Z', 'Z', '']

    seed(2)
    mutation3 = mutate(mutation2, 20)  # Cambio de dirección de la flecha
    assert mutation3.tolist() == ['', '>', 'C', '', '', '', 'Z', 'Z', '']

    seed(time())
