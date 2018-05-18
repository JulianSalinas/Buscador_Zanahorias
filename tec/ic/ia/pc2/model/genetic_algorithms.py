
import numpy as np
from random import randint, shuffle


class Gen:
    """
    'Escructura' para manejar cada gen
    :var gen_array: numpy array con los contenidos del tablero
    :var score: puntaje fitness del gen
    """
    def __init__(self, array, score=None):
        self.gen_array = array
        self.score = score

    def set_score(self, score): self.score = score

    def get_score(self): return self.score

    def get_array(self): return self.gen_array


def _weights_():
    # [0] = picked carrots weight
    # [1] = steps weight
    # [2] = arrows found weight
    # [3] = arrows not used weight
    return [100, -1, -5, -10]


def initialization(initial_board, individuals):
    """
    Convierte a Gen y genera la población inicial
    :param initial_board: matriz de numpy del estado inicial
    :param individuals: cantidad de individuos por generacion
    :return: lista con los genes de la generación inicial, shape de initial
    board
    """
    first_generation = list()
    content = initial_board.getA1().tolist()

    for _ in range(0, individuals):
        first_generation.append(Gen(np.array(content)))

    return first_generation, initial_board.shape


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

    return gen, mutates


def eval_fitness(gen, direction, mat_shape):

    temp = (gen.copy()).reshape(mat_shape)

    carrot_count = np.count_nonzero(temp == 'Z')
    arrow_count = np.count_nonzero(temp != ' ') - carrot_count - 1

    picked_carrots = 0
    steps = 0
    arrows_found = 0

    init_position = np.where(temp == 'C')
    row = init_position[0][0]
    col = init_position[1][0]

    def move_up():
        nonlocal row
        row -= 1
        return False if row < 0 else True

    def move_down():
        nonlocal row
        row += 1
        return False if row == mat_shape[0] else True

    def move_left():
        nonlocal col
        col -= 1
        return False if col < 0 else True

    def move_right():
        nonlocal col
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
                arrows_found += 1
                direction = 'abajo'
                temp[row][col] = ' '
            elif cell_content is 'A':
                arrows_found += 1
                direction = 'arriba'
                temp[row][col] = ' '
            elif cell_content is '<':
                arrows_found += 1
                direction = 'izquierda'
                temp[row][col] = ' '
            elif cell_content is '>':
                arrows_found += 1
                direction = 'derecha'
                temp[row][col] = ' '
        else:
            break

    cw = picked_carrots * _weights_()[0]                 # zanahorias cogidas
    sw = steps * _weights_()[1]                          # pasos dados
    aw = arrows_found * _weights_()[2]                   # flechas usadas
    auw = (arrow_count - arrows_found) * _weights_()[3]  # flechas sin usar

    return cw + sw + aw + auw


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


def generate(parents, selection_type, mutation_chance=20, cross_type=1):
    """
    Realiza el cruce de los genes según dos tipos de selección diferente
    1 -> random
    2 -> parejas en orden de entrada
    :param parents: lista de genes para cruzar
    :param selection_type: 1 o 2 según el tipo de selección
    :param: mutation_chance: probabilidad de 0 a 100 de mutación
    :param: cross_type: 1 -> corte en un punto, 2 -> corte en dos puntos
    :return: una lista con todos los genes (hijos, mutos, padres) resultantes
    """
    resulting_generation = list()

    if selection_type == 1:
        index_list = list(range(0, len(parents)))
        shuffle[index_list]

        for gen1_idx, gen2_idx in zip(*[iter(index_list)] * 2):
            child1, child2 = cross(parents[gen1_idx],
                                   parents[gen2_idx],
                                   cross_type)
            mutation1, mutated = mutate(child1, mutation_chance)


def run_carrot_finder(initial_direction, individuals, generations,
                      initial_board):
    pass
