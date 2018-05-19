
import numpy as np
from random import randint, shuffle
from operator import attrgetter

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
    return [100, -1, -5, 2]


def initialization(initial_board, individuals, direction, fitness=True):
    """
    Convierte a Gen y genera la población inicial
    :param initial_board: matriz de numpy del estado inicial
    :param individuals: cantidad de individuos por generacion
    :param direction: dirección inicial del conejo
    :param fitness: define si se calcula el fitness para la 1ra generación o no
    :return: lista con los Genes de la generación inicial, shape de initial
    board
    """
    first_generation = list()
    content = initial_board.getA1().tolist()
    if fitness:
        score = eval_fitness(Gen(np.array(content, object)), direction,
                             initial_board.shape)
    else: score = None

    for _ in range(0, individuals):
        first_generation.append(Gen(np.array(content, object), score))

    return first_generation, initial_board.shape


def mutate(gen, mutation_chance):
    """
    Dada una probabilidad de mutación, muta o no al gen recibido,
    la mutación puede ser la adición de una flecha, eliminación de flecha,
    o el cambio de dirección de una flecha
    :param gen: objeto Gen
    :param mutation_chance: probabilidad de mutación de 0 a 100
    :param direction: direccion inicial del conejo para evaluar fitness
    :param mat_shape: dimensiones de la matriz para evaluar fitness
    :return: el gen luego de la mutación o sin mutar
    """
    temp = gen.get_array().copy()
    arrow_symbols = ['<', '>', 'A', 'V']

    mutates = True if randint(0, 99) < mutation_chance else False

    if mutates:

        cell_idx = randint(0, len(temp) - 1)
        cell_content = temp[cell_idx]

        if cell_content is ' ':
            temp[cell_idx] = arrow_symbols[randint(0, 3)]
        elif cell_content in arrow_symbols:
            arrow_symbols += [' ']
            arrow_symbols.remove(cell_content)
            temp[cell_idx] = arrow_symbols[randint(0, 3)]

    return Gen(temp), mutates


def eval_fitness(gen, direction, mat_shape):
    """
    calcula la aptitud para un gen
    :param gen: objeto tipo Gen
    :param direction: dirección inicial del conejo
    :param mat_shape: dimensiones de la matriz
    :return: Gen con el atributo score alterado
    """
    temp = (gen.get_array().copy()).reshape(mat_shape)

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

    score = cw + sw + aw + auw

    gen.set_score(score)

    return score


def cross(parent1, parent2, cross_type):
    """
    Realiza el tipo de cruce entre dos genes padres
    :param parent1: objeto Gen
    :param parent2: objeto Gen
    :param cross_type: 1 -> cruce en 1 punto, 2 -> cruce en dos puntos
    :return: los dos np array genes hijos resultantes
    """
    child1 = parent1.get_array().copy()
    child2 = parent2.get_array().copy()

    idx1 = randint(1, len(child1) - 1)
    if cross_type == 1:
        child1[:idx1], child2[:idx1] = child2[:idx1].tolist(), child1[
                                                               :idx1].tolist()
    else:
        idx2 = randint(1, len(child1) - 1)
        idx1, idx2 = min(idx1, idx2), max(idx1, idx2)
        child1[idx1:idx2], child2[idx1:idx2] = \
            child2[idx1:idx2].tolist(), child1[idx1:idx2].tolist()

    child1 = Gen(child1)
    child2 = Gen(child2)

    return child1, child2


def generate(parents, selection_type, direction, mat_shape,
             mutation_chance, cross_type):
    """
    Realiza el cruce de los genes según dos tipos de selección diferente
    :param parents: lista de Genes para cruzar
    :param selection_type: 1 -> random, 2 -> parejas en orden
    :param direction: dirección inicial del conejo para evaluar fitness
    :param mat_shape: dimensiones de la matriz para evaluar fitness
    :param mutation_chance: probabilidad de 0 a 100 de mutación
    :param cross_type: 1 -> corte en un punto, 2 -> corte en dos puntos
    :return: una lista con todos los Genes (hijos, mutos, padres) resultantes
    """
    resulting_generation = list()
    resulting_generation += parents

    if selection_type == 1:
        index_list = list(range(0, len(parents)))
        shuffle(index_list)

        for gen1_idx, gen2_idx in zip(*[iter(index_list)] * 2):
            child1, child2 = cross(parents[gen1_idx],
                                   parents[gen2_idx],
                                   cross_type)

            eval_fitness(child1, direction, mat_shape)
            eval_fitness(child2, direction, mat_shape)

            mutation1, mutated = mutate(child1, mutation_chance)
            if mutated:
                eval_fitness(mutation1, direction, mat_shape)
                resulting_generation.append(mutation1)

            mutation2, mutated = mutate(child2, mutation_chance)
            if mutated:
                eval_fitness(mutation2, direction, mat_shape)
                resulting_generation.append(mutation2)

            resulting_generation.append(child1)
            resulting_generation.append(child2)

    elif selection_type == 2:
        pass

    return resulting_generation


def replacement(generation, individuals):

    generation.sort(key=lambda gen: gen.get_score(), reverse=True)
    return generation[:individuals]


def run_carrot_finder(initial_direction, individuals, generations,
                      initial_board):
    pass
