
import numpy as np
from random import randint

test_matrix = [
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '<', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', ' ', '>', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Z', 'A', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
 [' ', ' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

test_gen = (np.matrix(test_matrix, dtype=object)).getA1()


def initialization(initial_board, individuals):
    """
    Convierte a vector y genera la población inicial
    :param initial_board: matriz de numpy del estado inicial
    :param individuals: cantidad de individuos por generacion
    :return: lista con los genes de la generación inicial, shape de initial
    board
    """
    return [initial_board.getA1()]*individuals, initial_board.shape


def mutate(gen, mutation_chance):
    """
    Dada una probabilidad de mutación, muta o no al gen recibido,
    la mutación puede ser la adición de una flecha, eliminación de flecha,
    o el cambio de dirección de una flecha
    :param gen: flatten array de numpy
    :param mutation_chance: probabilidad de mutación de 0 a 100
    :return: el gen luego de la mutación o sin mutar
    """
    gen = gen.copy()

    arrow_symbols = ['<', '>', 'A', 'V']

    mutates = True if randint(0, 99) < mutation_chance else False

    if mutates:

        cell_idx = randint(0, len(gen) - 1)
        cell_content = gen[cell_idx]

        if cell_content is ' ':
            gen[cell_idx] = arrow_symbols[randint(0, 3)]
        elif cell_content in arrow_symbols:
            arrow_symbols += [' ']
            arrow_symbols.remove(cell_content)
            gen[cell_idx] = arrow_symbols[randint(0, 3)]

    return gen


def eval_fitness(gen, direction, mat_shape):

    temp = (gen.copy()).reshape(mat_shape)

    picked_carrots = 0
    carrot_count = len(np.where(gen == 'Z')[0])
    steps = 0
    arrow_count = 0

    init_position = np.where(temp == 'C')
    row = init_position[0][0]
    col = init_position[1][0]

    def move_up():
        row -= 1
        return False if row < 0 else True

    def move_down():
        row += 1
        return False if row == mat_shape[0] else True

    def move_left():
        col -= 1
        return False if col < 0 else True

    def move_right():
        col += 1
        return False if col == mat_shape[1] else True

    def move():
        if direction == 'arriba':
            return move_up()
        elif direction == 'abajo':
            return move_down()
        elif direction == 'derecha':
            return move_right()
        else:
            return move_left()

    while True:
        if picked_carrots == carrot_count:
            break

        if move():
            steps += 1
            cell_content = temp[row][col]
            if cell_content is 'Z':
                picked_carrots += 1
                temp[row][col] = ' '
            elif cell_content is 'V':
                arrow_count += 1
                direction = 'abajo'
                temp[row][col] = ' '
            elif cell_content is 'A':
                arrow_count += 1
                direction = 'arriba'
                temp[row][col] = ' '
            elif cell_content is '<':
                arrow_count += 1
                direction = 'izquierda'
                temp[row][col] = ' '
            elif cell_content is '>':
                arrow_count += 1
                direction = 'derecha'
                temp[row][col] = ' '
        else:
            break

    print('carrots: ' + str(picked_carrots))
    print('arrows found: ' + str(arrow_count))
    print('steps: ' + str(steps))


eval_fitness(test_gen, 'arriba', (15,15))


def cross(parent1, parent2, cross_type):
    """
    Realiza el tipo de cruce entre dos genes padres
    :param parent1: array unidimensional
    :param parent2: array unidimensional
    :param cross_type: 1 -> cruce en 1 punto, 2 -> cruce en dos puntos
    :return: los dos np array genes hijos resultantes
    """
    child1 = np.array(parent1.tolist())
    child2 = np.array(parent2.tolist())

    idx1 = randint(1, len(child1) - 1)
    if cross_type == 1:
        child1[:idx1], child2[:idx1] = child2[:idx1].tolist(), child1[
                                                               :idx1].tolist()
    else:
        idx2 = randint(1, len(child1) - 1)
        idx1, idx2 = min(idx1, idx2), max(idx1, idx2)
        child1[idx1:idx2], child2[idx1:idx2] = \
            child2[idx1:idx2].tolist(), child1[idx1:idx2].tolist()

    return child1, child2


def run_carrot_finder(initial_direction, individuals, generations,
                      initial_board):
    pass
