import numpy as np
from random import randint, shuffle, seed
from math import ceil


class Gen:
    """
    'Escructura' para manejar cada gen
    :var array: numpy array con los contenidos del tablero
    :var score: puntaje fitness del gen
    """

    def __init__(self, array, score=0):
        self.gen_array = array
        self.score = score

    def set_score(self, score): self.score = score

    def get_score(self): return self.score

    def get_array(self): return self.gen_array


__console_output__ = True
__print_frecuency__ = 100
__print_per_generation__ = 3
__weigths__ = {}


def set_weights(mat_shape):
    # ['pc'] = picked carrots weight      (zanahorias pisadas)
    # ['s'] = steps weight                (pisadas)
    # ['af'] = arrows found weight        (flechas pisadas)
    # ['anf'] = arrows not found weight   (flechas sin usar)
    # ['apc'] = arrows pointing carrots   (flechas que apuntan directo a Z)
    # ['180°t'] = 180 turn                (giro en 180 grados)
    # ['bfc'] = best first carrot         (una flecha inicial idónea)

    _scalar = mat_shape[0] * mat_shape[1]

    global __weigths__
    __weigths__ = {
        'pc': round_up(_scalar, 1000),
        's': -1,
        'af': -5,
        'anf': -15,
        'apc': 10,
        '180°t': -(round_up(_scalar, 100)),
        'bfc': round_up(_scalar, 500)
    }


def round_up(number, base=10):
    return int(base * ceil(float(number)/base))


def gen_in_list(gen, gen_list):
    """
    Revisa si el genotipo de un determinado gen es igual a alguno de los
    genes en una lista
    :param gen: objeto Gen a buscar
    :param gen_list: lista con objetos Gen
    :return: True si encuentra un genotipo igual, False de lo contrario
    """
    return any((gen.get_array() == g.get_array()).all() for g in gen_list)


def direction_to_arrow():
    """
    Define la flecha correspondiente para el parámetro inicial del programa
    :return: diccionario con las correspondencias
    """
    return {'arriba': 'A', 'abajo': 'V', 'derecha': '>', 'izquierda': '<'}


def a_idx_to_m_idx(a_idx, mat_shape):
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
    set_weights(initial_board.shape)
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


def analyze_carrots(board, carrot_positions, rabbit_row, rabbit_col):
    """
    Para cada zanahoria, cuenta la cantidad de direcciones desde las que la
    apunta una flecha, para aprovechar el ciclo de recorrido de zanahorias,
    se identifica también la zanahoria más cercana
    :param board: tablero escenario
    :param carrot_positions: tupla de arrays con filas y columnas de las
    zanahorias
    :param rabbit_col: columna inicial del conejo
    :param rabbit_row: fila inicial del conejo
    :return: cantidad de flechas apuntando zanahorias, y la posición de la
    zanahoria más cercana
    """
    arrow_count = 0  # acumulador de flechas
    nearest_so_far = carrot_positions[0][0], carrot_positions[1][0]

    def arrow_count_in_subpath(subpath, arrow):
        if len(subpath) == 0:
            return 0

        temp = np.array(subpath, object)
        return 1 if np.count_nonzero(temp == arrow) > 0 else 0

    for row, col in zip(carrot_positions[0], carrot_positions[1]):

        current_distance = abs(row - rabbit_row) + abs(col - rabbit_col)
        best_distance = abs(nearest_so_far[0] - rabbit_row) + abs(
            nearest_so_far[1] - rabbit_col)

        if current_distance < best_distance:
            nearest_so_far = row, col

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

    return arrow_count, nearest_so_far


def walk_rabbit_path(board, direction, row, col, carrot_count, mat_shape,
                     nearest_carrot):
    """
    Simula el recorrido del conejo en el tablero para obtener datos usados
    por el fitness
    :param board: numpy matrix con el tablero disponible
    :param direction: dirección inicial del conejo
    :param row: fila de la posición inicial del conejo
    :param col: columna de la posición inicial del conejo
    :param carrot_count: cantidad de zanahorias existentes
    :param mat_shape: tupla con dimensiones de la matriz (filas, columnas)
    :param nearest_carrot: tupla con la fila y columna de la zanahoria más
    cercana
    :return: contadores usados por el fitness
    """
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
    last_cell = 'C'

    is_first_carrot = True
    first_carrot_is_optimal = 0
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
                if is_first_carrot:
                    is_first_carrot = False
                    if (row, col) == nearest_carrot:
                        first_carrot_is_optimal = 1

            elif cell_content in arrow_symbols:
                # Revisar los giros en 180 grados
                if cell_content is opposite_direction[direction]:
                    if last_cell is not 'Z':
                        _180_degree_turns += 1
                arrows_found += 1
                direction = cell_content
                board[row][col] = ' '

        else:
            rabbit_fall = True
            break

    return picked_carrots, steps, arrows_found, _180_degree_turns, \
        rabbit_fall, first_carrot_is_optimal


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

    init_position = np.where(temp == 'C')
    row = init_position[0][0]
    col = init_position[1][0]

    arrows_pointing, nearest_carrot_pos = analyze_carrots(temp.copy(),
                                                          carrot_positions,
                                                          row, col)

    carrot_count = len(carrot_positions[0])
    arrow_count = np.count_nonzero(temp != ' ') - carrot_count - 1

    results = walk_rabbit_path(board=temp, direction=direction,
                               row=row, col=col, mat_shape=mat_shape,
                               carrot_count=carrot_count,
                               nearest_carrot=nearest_carrot_pos)

    picked_carrots = results[0]
    steps = results[1]
    arrows_found = results[2]
    _180_degree_turns = results[3]
    rabbit_fall = results[4]
    first_carrot_is_optimal = results[5]

    pcw = picked_carrots * __weigths__['pc']
    sw = steps * __weigths__['s']
    if rabbit_fall:
        sw = -sw
    afw = arrows_found * __weigths__['af']
    anfw = (arrow_count - arrows_found) * __weigths__['anf']
    apcw = arrows_pointing * __weigths__['apc']
    _180dtw = _180_degree_turns * __weigths__['180°t']
    bfcw = first_carrot_is_optimal * __weigths__['bfc']

    score = pcw + sw + afw + anfw + apcw + _180dtw + bfcw

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


def generate(parents, direction, mat_shape,
             mutation_chance, cross_type):
    """
    Realiza el cruce de los genes según dos tipos de selección diferente
    :param parents: lista de Genes para cruzar
    :param direction: dirección inicial del conejo para evaluar fitness
    :param mat_shape: dimensiones de la matriz para evaluar fitness
    :param mutation_chance: probabilidad de 0 a 100 de mutación
    :param cross_type: 1 -> corte en un punto, 2 -> corte en dos puntos
    :return: una lista con todos los Genes (hijos, mutos, padres) resultantes
    """
    resulting_generation = list()
    resulting_generation += parents

    index_list = list(range(0, len(parents)))
    shuffle(index_list)

    for gen1_idx, gen2_idx in zip(*[iter(index_list)] * 2):
        children = get_children(parents[gen1_idx], parents[gen2_idx],
                                cross_type, direction, mat_shape,
                                mutation_chance)

        resulting_generation += [child for child in children if not
                                 gen_in_list(child, resulting_generation)]

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
                      mutation_chance, initial_board, cross_type=1,
                      custom_seed=-1):
    """
    Función principal de ejecución del algoritmo genético
    :param initial_direction: dirección en la que comienza a moverse el conejo
    :param individuals: cantidad de invididuos por generación
    :param max_generations: número máximo de generaciones por corrida
    :param mutation_chance: número de 0 a 100 para la probabilidad de mutación
    :param initial_board: numpy matrix con el tablero inicial
    :param cross_type: 1 -> corte en un punto 2 -> corte en dos puntos
    :param custom_seed: semilla de random para reproducibilidad de resultados
    :return: lista con la última generación ordenada por fitness de Genes
    """
    if custom_seed < 0:
        seed(time())
    else:
        seed(custom_seed)

    initial_direction = direction_to_arrow()[initial_direction]

    optimal_origin_generation = -1
    current_best_score = 0

    # Definición de la población inicial
    generation, dimensions = initialization(initial_board=initial_board,
                                            individuals=individuals,
                                            direction=initial_direction)

    print('Pesos calculados: ', __weigths__)

    for generation_number in range(1, max_generations + 1):

        # Se obtiene la generación completa sin ordenar
        generation = generate(parents=generation,
                              direction=initial_direction,
                              mutation_chance=mutation_chance,
                              mat_shape=dimensions,
                              cross_type=cross_type)

        # Se seleccionan los mejores
        generation = replacement(generation, individuals)

        if generation[0].get_score() > current_best_score:
            optimal_origin_generation = generation_number
            current_best_score = generation[0].get_score()

        print_this_generation = generation_number % __print_frecuency__ == 0

        if __console_output__ and print_this_generation:
            print('\nGENERACIÓN: {:05}'.format(generation_number))
            for i in range(0, len(generation[:__print_per_generation__])):
                print(
                    '\tINDIVIDUO: {:05}'.format(i),
                    ' -> APTITUD: ' + str(generation[i].get_score())
                )

    if __console_output__:
        print('\nMÁS APTO ENCONTRADO: ')
        print(generation[0].get_array().reshape(starting_board.shape))
        print('\nAPTITUD DEL MEJOR ENCONTRADO:', generation[0].get_score())
        print('\nGENERACIÓN DEL MEJOR ENCONTRADO:',
              '{:05}'.format(optimal_origin_generation))

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
    [' ', ' ', ' ', ' ', ' ', ' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', ' '],
    [' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Z', ' ', ' ', ' ', ' ', ' ']]
starting_board = np.matrix(starting_board, object)
optimal = run_carrot_finder(initial_direction='izquierda',
                            individuals=15,
                            max_generations=500,
                            mutation_chance=80,
                            initial_board=starting_board,
                            cross_type=1, custom_seed=20)[0]
