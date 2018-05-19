
import numpy as np
from random import randint, shuffle, seed


class Gen:
    """
    'Escructura' para manejar cada gen
    :var gen_array: numpy array con los contenidos del tablero
    :var score: puntaje fitness del gen
    """
    def __init__(self, array, score=0):
        self.gen_array = array
        self.score = score

    def set_score(self, score): self.score = score

    def get_score(self): return self.score

    def get_array(self): return self.gen_array


def weights():
    # ['pc'] = picked carrots weight
    # ['s'] = steps weight
    # ['af'] = arrows found weight
    # ['anf'] = arrows not found weight
    # ['apc'] = arrows pointing carrots

    _weights = {
        'pc': 5000,
        's': -1,
        'af': -5,
        'anf': -2,
        'apc': 50
    }
    return _weights


def direction_to_arrow(direction):
    if direction == 'arriba':
        return 'A'
    if direction == 'abajo':
        return 'V'
    if direction == 'derecha':
        return '>'

    return '<'


def a_idx_to_m_index(a_idx, mat_shape):
    """
    Convierte un índice de array al correspondiente índide de matriz según
    las dimensiones de la matriz
    :param a_idx: índice del arreglo
    :param mat_shape: dimensiones de la matriz (f, c)
    :return: par ordenado, file x columna para el índice de una matriz
    """
    return int(a_idx / mat_shape[1]), a_idx % mat_shape[1]


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
    else:
        score = None

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
    :return: el gen luego de la mutación o sin mutar, y la posición del
    array donde muto, o en su defecto -1 en caso de no haber mutado
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


def carrot_found_on_subpath(board, path_start, direction):
    pass


def eval_fitness(gen, direction, mat_shape):
    """
    calcula la aptitud para un gen
    :param gen: objeto tipo Gen
    :param direction: dirección inicial del conejo
    :param mat_shape: dimensiones de la matriz
    de no haber mutado
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
        if direction == 'A':
            return move_up()
        elif direction == 'V':
            return move_down()
        elif direction == '>':
            return move_right()
        else:
            return move_left()

    arrow_symbols = ['<', '>', 'A', 'V']

    # Recorrer el camino del conejo para determinar las zanahorias, pasos y
    # las flechas que encuentra
    while True:
        if picked_carrots == carrot_count:
            break

        if move():
            steps += 1
            cell_content = temp[row][col]
            if cell_content is 'Z':
                picked_carrots += 1
                temp[row][col] = ' '
            elif cell_content in arrow_symbols:
                arrows_found += 1
                direction = cell_content
                temp[row][col] = ' '

        else:
            break

    pcw = picked_carrots * weights()['pc']
    sw = steps * weights()['s']
    afw = arrows_found * weights()['af']
    anfw = (arrow_count - arrows_found) * weights()['anf']

    score = pcw + sw + afw + anfw

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


def get_children(parent1, parent2, cross_type, direction, mat_shape,
                 mutation_chance):
    """
    Dados un par de padres, se crean los hijos y sus mutaciones en caso de
    haberlas
    :param parent1: objeto tipo Gen
    :param parent2: objeto tipo Gen
    :param cross_type: tipo de cruce, 1 o 2
    :param direction: dirección inicial del conejo para el fitness
    :param mat_shape: dimensiones del tablero para el fitness
    :param mutation_chance: porcentaje de mutación entre 0 y 100
    :return:
    """
    children = list()

    child1, child2 = cross(parent1, parent2, cross_type)

    eval_fitness(child1, direction, mat_shape)
    eval_fitness(child2, direction, mat_shape)

    mutation1, mutated = mutate(child1, mutation_chance)
    if mutated:
        eval_fitness(mutation1, direction, mat_shape)
        children.append(mutation1)

    mutation2, mutated = mutate(child2, mutation_chance)
    if mutated:
        eval_fitness(mutation2, direction, mat_shape)
        children.append(mutation2)

    children.append(child1)
    children.append(child2)

    return children


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
            resulting_generation += get_children(parents[gen1_idx],
                                                 parents[gen2_idx],
                                                 cross_type,
                                                 direction,
                                                 mat_shape,
                                                 mutation_chance)

    elif selection_type == 2:
        pass

    return resulting_generation


def replacement(generation, individuals):
    """
    Escoge los genes más aptos para conformar la siguiente generación
    :param generation: lista con todos los padres, hijos y mutos
    :param individuals: cantidad de individuos por generación
    :return: lista con la generación ya recortada
    """
    # Se ordena de mayor a menor
    generation.sort(key=lambda gen: gen.get_score(), reverse=True)
    return generation[:individuals]


def run_carrot_finder(initial_direction, individuals, max_generations,
                      mutation_chance, initial_board, selection_type=1,
                      cross_type=1):

    initial_direction = direction_to_arrow(initial_direction)

    # Definición de la población inicial
    generation, dimensions = initialization(initial_board=initial_board,
                                            individuals=individuals,
                                            direction=initial_direction)

    for generation_number in range(1, max_generations+1):

        # Se obtiene la generación completa sin ordenar
        generation = generate(parents=generation,
                              direction=initial_direction,
                              mutation_chance=mutation_chance,
                              mat_shape=dimensions,
                              selection_type=selection_type,
                              cross_type=cross_type)

        # Se seleccionan los mejores
        generation = replacement(generation, individuals)

    return generation



starting_board = [
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
starting_board = np.matrix(starting_board, object)

optimals = run_carrot_finder(initial_direction='arriba',
                            individuals=10,
                            max_generations=100,
                            mutation_chance=30,
                            initial_board=starting_board)

for optimal in optimals:
    print(optimal.get_score())
    print(optimal.get_array().reshape(starting_board.shape))
    print('__________________________________________________________________')
