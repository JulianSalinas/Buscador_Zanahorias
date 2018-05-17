
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

    seed(0)

    child1, child2 = cross(parent1, parent2, 1)

    assert child1.tolist() == ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    assert child2.tolist() == ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    seed(1)

    child1, child2 = cross(child1, child2, 2)

    assert child1.tolist() == ['1', 'B', '3', '4', '5', '6', '7', '8', '9']
    assert child2.tolist() == ['A', '2', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    seed(time())


def test_mutation():

    seed(1)

    gen = np.array(['', '', 'C', '', '', '', 'Z', 'Z', ''])

    mutation1 = mutate(gen, 20)  # rgn = 17
    print(mutation1)

    mutation2 = mutate(gen, 20)  # rgn = 32
    print(mutation2)

    mutation3 = mutate(gen, 20)  # rgn = 15
    print(mutation3)