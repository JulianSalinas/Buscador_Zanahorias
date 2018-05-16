
import numpy as np
from random import randint

test_matrix = [
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', 'Z', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', 'Z', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', 'C', '', '', '', '', '', '', '', '', '', '', '', '']
]
test_matrix = np.matrix(test_matrix)


def initialization(initial_board, individuals):
    """
    Convierte a vector y genera la población inicial
    :param initial_board: matriz de numpy del estado inicial
    :param individuals: cantidad de individuos por generacion
    :return: lista con los genes de la generación inicial, shape de initial
    board
    """
    return [initial_board.getA1()]*individuals, initial_board.shape


def cross(parent1, parent2, cross_type):
    """
    Realiza el tipo de cruce entre dos genes padres
    :param parent1: array unidimensional
    :param parent2: array unidimensional
    :param cross_type: 1 -> cruce en 1 punto, 2 -> cruce en dos puntos
    :return: los dos np array genes hijos resultantes
    """
    gen1 = np.array(parent1.tolist())
    gen2 = np.array(parent2.tolist())

    idx1 = randint(0, len(gen1) - 1)
    print(idx1)
    if cross_type == 1:
        gen1[:idx1], gen2[:idx1] = gen2[:idx1].tolist(), gen1[:idx1].tolist()
    else:
        idx2 = randint(0, len(gen1) - 1)
        idx1, idx2 = min(idx1, idx2), max(idx1, idx2)
        gen1[idx1:idx2], gen2[idx1:idx2] = \
            gen2[idx1:idx2].tolist(), gen1[idx1:idx2].tolist()

    return gen1, gen2


def run_carrot_finder(initial_direction, individuals, generations,
                      initial_board):
    pass


generation1, shapeOfMatrix = initialization(test_matrix, 3)
child1, child2 = cross(generation1[0], generation1[1], 1)

print(child1.reshape(shapeOfMatrix))
print(child2.reshape(shapeOfMatrix))
