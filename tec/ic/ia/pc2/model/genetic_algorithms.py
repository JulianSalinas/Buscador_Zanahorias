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
    # ['pc'] = picked carrots weight      (zanahorias pisadas)
    # ['f'] = fall                        (salirse del tablero)
    # ['s'] = steps weight                (pisadas)
    # ['af'] = arrows found weight        (flechas pisadas)
    # ['anf'] = arrows not found weight   (flechas sin usar)
    # ['apc'] = arrows pointing carrots   (flechas que apuntan directo a Z)
    # ['180°t'] = 180 turn                 (giro en 180 grados)

    _weights = {
        'pc': 5000,
        'f': -2500,
        's': -1,
        'af': -5,
        'anf': -10,
        'apc': 15,
        '180°t': -1000
    }
    return _weights


def gen_in_list(gen, gen_list):
    return any((gen.get_array() == g.get_array()).all() for g in gen_list)


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


def arrows_pointing_to_carrots(board, carrot_positions):
    """
    Cuenta la cantidad de flechas apuntando a una zanahoria
    :param board: tablero escenario
    :param carrot_positions: tupla de arrays con filas y columnas de las
    zanahorias
    :return: cantidad de flechas apuntando a alguna zanahoria
    """
    arrow_count = 0  # acumulador de flechas

    def arrow_count_in_subpath(subpath, arrow):
        if len(subpath) == 0:
            return 0
        try:
            cut = subpath.index('Z')
            subpath = subpath[:cut]
        except ValueError as ve:
            pass

        temp = np.array(subpath, object)
        return 1 if np.count_nonzero(temp == arrow) > 0 else 0

    for row, col in zip(carrot_positions[0], carrot_positions[1]):
        arrow_count += arrow_count_in_subpath(
            board[:, col][:row].flatten().tolist()[0][::-1], 'V'
        )
        arrow_count += arrow_count_in_subpath(
            board[:, col][row + 1:].flatten().tolist(), 'A'
        )
        arrow_count += arrow_count_in_subpath(
            board[row, :col].flatten().tolist()[::-1], '>'
        )
        arrow_count += arrow_count_in_subpath(
            board[row, col + 1:].flatten().tolist(), '<'
        )

    return arrow_count


def walk_rabbit_path(board, direction, row, col, carrot_count, mat_shape):
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

    def valid_move():
        if direction == 'A':
            return move_up()
        elif direction == 'V':
            return move_down()
        elif direction == '>':
            return move_right()
        else:
            return move_left()

    picked_carrots = 0
    steps = 0
    arrows_found = 0
    _180_degree_turns = 0

    arrow_symbols = ['<', '>', 'A', 'V']
    opposite_direction = {'A': 'V', 'V': 'A', '>': '<', '<': '>'}

    # Recorrer el camino del conejo para determinar las zanahorias, pasos y
    # las flechas que encuentra
    while True:
        if picked_carrots == carrot_count:
            rabbit_fall = False
            break

        if valid_move():
            steps += 1
            cell_content = board[row][col]
            if cell_content is 'Z':
                picked_carrots += 1
                board[row][col] = ' '
            elif cell_content in arrow_symbols:
                # Revisar los giros en 180 grados
                if opposite_direction[direction] is cell_content:
                    _180_degree_turns += 1
                arrows_found += 1
                direction = cell_content
                board[row][col] = ' '

        else:
            rabbit_fall = True
            break

    return picked_carrots, steps, arrows_found, _180_degree_turns, rabbit_fall


def eval_fitness(gen, direction, mat_shape):
    """
    calcula la aptitud para un gen
    :param gen: objeto tipo Gen
    :param direction: dirección inicial del conejo
    :param mat_shape: dimensiones de la matriz
    :return: Gen con el atributo score alterado
    """
    temp = (gen.get_array().copy()).reshape(mat_shape)

    carrot_positions = np.nonzero(temp == 'Z')

    arrows_pointing = arrows_pointing_to_carrots(temp.copy(), carrot_positions)

    carrot_count = len(carrot_positions)
    arrow_count = np.count_nonzero(temp != ' ') - carrot_count - 1

    init_position = np.where(temp == 'C')
    row = init_position[0][0]
    col = init_position[1][0]

    results = walk_rabbit_path(board=temp, direction=direction,
                               row=row, col=col, mat_shape=mat_shape,
                               carrot_count=carrot_count)

    picked_carrots = results[0]
    steps = results[1]
    arrows_found = results[2]
    _180_degree_turns = results[3]
    rabbit_fall = results[4]

    pcw = picked_carrots * weights()['pc']
    fw = weights()['f'] if rabbit_fall else 0
    sw = steps * weights()['s']
    afw = arrows_found * weights()['af']
    anfw = (arrow_count - arrows_found) * weights()['anf']
    apcw = arrows_pointing * weights()['apc']
    _180dtw = _180_degree_turns * weights()['180°t']

    score = pcw + sw + afw + anfw + apcw + _180dtw + fw

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
            children = get_children(parents[gen1_idx],
                                    parents[gen2_idx],
                                    cross_type,
                                    direction,
                                    mat_shape,
                                    mutation_chance)
            for child in children:
                if not gen_in_list(child, resulting_generation):
                    resulting_generation.append(child)

    elif selection_type == 2:
        _range = range(0, int(len(resulting_generation) / 2))
        for i in _range:
            children += get_children(parents[i * 2],
                                     parents[i * 2 + 1],
                                     cross_type,
                                     direction,
                                     mat_shape,
                                     mutation_chance)
            for child in children:
                if not gen_in_list(child, resulting_generation):
                    resulting_generation.append(child)

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

    for generation_number in range(1, max_generations + 1):

        # Se obtiene la generación completa sin ordenar
        generation = generate(parents=generation,
                              direction=initial_direction,
                              mutation_chance=mutation_chance,
                              mat_shape=dimensions,
                              selection_type=selection_type,
                              cross_type=cross_type)

        # Se seleccionan los mejores
        generation = replacement(generation, individuals)

        global optimal_origin_generation
        global current_best_score
        if generation[0].get_score() > current_best_score:
            optimal_origin_generation = generation_number
            current_best_score = generation[0].get_score()

    return generation


optimal_origin_generation = 0
current_best_score = -250

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
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
starting_board = np.matrix(starting_board, object)

optimal = run_carrot_finder(initial_direction='derecha',
                            individuals=10,
                            max_generations=300,
                            mutation_chance=80,
                            initial_board=starting_board,
                            selection_type=1,
                            cross_type=1)[0]

print(optimal.get_score())
print(optimal.get_array().reshape(starting_board.shape))

print(optimal_origin_generation)
