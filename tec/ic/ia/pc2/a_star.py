import queue
import numpy as np


# -----------------------------------------------------------------------------

def calc_distancia_lineal(pos, metas):
    distancias = queue.PriorityQueue()

    for meta in metas:
        distancia = abs(meta[0] - pos[0]) + abs(meta[1] - pos[1])
        distancias.put((distancia, meta))

    return distancias


# -----------------------------------------------------------------------------

def calc_submatriz(matriz, pos_actual, rango_vision):
    matriz = np.matrix(matriz)
    n_cols = matriz.shape[1]
    n_filas = matriz.shape[0]

    x_min = max(0, pos_actual[0] - rango_vision)
    x_max = min(n_filas, pos_actual[0] + rango_vision + 1)

    y_min = max(0, pos_actual[1] - rango_vision)
    y_max = min(n_cols, pos_actual[1] + rango_vision + 1)

    sub_matriz = matriz[x_min:x_max, y_min:y_max]

    return sub_matriz


# -----------------------------------------------------------------------------

def calc_pos_simbolo(matriz, simbolo):
    indices = []
    arreglo_indices = np.nonzero(matriz == simbolo)
    if len(arreglo_indices) > 0:
        eje_x = arreglo_indices[0]
        eje_y = arreglo_indices[1]

        for index in range(len(eje_x)):
            indices.append([eje_x[index], eje_y[index]])

    return indices


# -----------------------------------------------------------------------------

def desplazar_conejo(matriz, pos_vieja, pos_nueva, simbolo_vacio=' ',
                     simbolo_conejo='C'):
    pos_x = pos_vieja[0]
    pos_y = pos_vieja[1]
    matriz[pos_x, pos_y] = simbolo_vacio

    pos_x = pos_nueva[0]
    pos_y = pos_nueva[1]
    matriz[pos_x, pos_y] = simbolo_conejo

    return matriz


# -----------------------------------------------------------------------------

def calc_pos_conejo(matriz, simbolo_conejo='C'):
    pos = []
    indices = calc_pos_simbolo(matriz, simbolo_conejo)

    if len(indices) > 0:
        pos = indices[0]

    return pos


# -----------------------------------------------------------------------------

def estados_sucesores(estado_actual):
    izq = [[estado_actual[0], estado_actual[1] - 1], 'IZQUIERDA']
    der = [[estado_actual[0], estado_actual[1] + 1], 'DERECHA']
    arriba = [[estado_actual[0] - 1, estado_actual[1]], 'ARRIBA']
    abajo = [[estado_actual[0] + 1, estado_actual[1]], 'ABAJO']

    sucesores = [izq, der, arriba, abajo]
    return sucesores


# -----------------------------------------------------------------------------

def calc_heuristico_min(heuristicos):
    costo = 9999

    if heuristicos.qsize() > 0:
        mejor_valor = heuristicos.get()
        meta = mejor_valor[1]
        costo = mejor_valor[0]

    return costo


# -----------------------------------------------------------------------------

def calc_mejor_sucesor(sucesores):
    mejor_sucesor = sucesores[0]
    for sucesor in sucesores:
        costo_sucesor = sucesor[0]
        costo_mejor = mejor_sucesor[0]
        if costo_sucesor < costo_mejor:
            mejor_sucesor = sucesor
        elif costo_sucesor == costo_mejor:
            if np.random.choice([True, False]):
                mejor_sucesor = sucesor

    return mejor_sucesor


# -----------------------------------------------------------------------------

def verificar_meta(matriz, posicion, meta='Z'):
    eje_x = posicion[0]
    eje_y = posicion[1]

    if matriz[eje_x, eje_y] == meta:
        return True

    return False


# -----------------------------------------------------------------------------

def eliminar_sucesor_viejo(sucesores, sucesor_viejo):
    sucesores = sucesores.tolist()
    if sucesor_viejo in sucesores:
        sucesores.remove(sucesor_viejo)

    sucesores = np.matrix(sucesores)

    return sucesores


# -----------------------------------------------------------------------------

def delimitar_rango_vision(matriz, pos_actual, rango_vision):
    zanahorias = calc_pos_simbolo(matriz, 'Z')
    zanahorias_res = []

    for zanahoria in zanahorias:
        if (pos_actual[0] - rango_vision <= zanahoria[0] <=
                pos_actual[0] + rango_vision):
            if (pos_actual[1] - rango_vision <= zanahoria[1] <=
                    pos_actual[1] + rango_vision):
                zanahorias_res.append(zanahoria)

    return zanahorias_res


# -----------------------------------------------------------------------------

def split_horizontal_matriz(matriz, pos_actual):
    matriz_1 = matriz[:pos_actual[0], :]
    matriz_2 = matriz[pos_actual[0]:, :]
    return matriz_1, matriz_2


# -----------------------------------------------------------------------------

def split_vertical_matriz(matriz, pos_actual):
    matriz_1 = matriz[:, :pos_actual[1]]
    matriz_2 = matriz[:, pos_actual[1]:]
    return matriz_1, matriz_2


# -----------------------------------------------------------------------------

def castigar_distancia(sucesores, zanahorias, pasos_actuales):
    costo_sucesores = []

    for sucesor in sucesores:
        if len(zanahorias) > 0:
            # Determinamos pesos segun la distancia lineal
            heuristicos = calc_distancia_lineal(sucesor[0], zanahorias)
            costo_heuristico = calc_heuristico_min(heuristicos)
        else:
            costo_heuristico = 15

        costo_total = pasos_actuales + costo_heuristico
        costo_sucesores.append([costo_total, sucesor])

    return costo_sucesores


# -----------------------------------------------------------------------------

def castigar_emisferios(matriz, costo_sucesores, pos_actual):
    m_izq, m_der = split_vertical_matriz(matriz, pos_actual)
    m_arriba, m_abajo = split_horizontal_matriz(matriz, pos_actual)

    zanahorias_izq = calc_pos_simbolo(m_izq, 'Z')
    zanahorias_der = calc_pos_simbolo(m_der, 'Z')
    zanahorias_abajo = calc_pos_simbolo(m_abajo, 'Z')
    zanahorias_arriba = calc_pos_simbolo(m_arriba, 'Z')

    for i in costo_sucesores:
        dir_sucesor = i[1][1]
        if dir_sucesor == 'IZQUIERDA':
            if len(zanahorias_izq) < len(zanahorias_der):
                i[0] += 10
        elif dir_sucesor == 'DERECHA':
            if len(zanahorias_der) < len(zanahorias_izq):
                i[0] += 10
        elif dir_sucesor == 'ABAJO':
            if len(zanahorias_abajo) < len(zanahorias_arriba):
                i[0] += 10
        else:
            if len(zanahorias_arriba) < len(zanahorias_abajo):
                i[0] += 10

    return costo_sucesores


# -----------------------------------------------------------------------------

def castigar_esp_desconocido(costo_sucesores, forma_matriz):

    for i in costo_sucesores:
        posicion = i[1][0]
        if (0 > posicion[0] > forma_matriz[0] - 1) or\
                (0 > posicion[1] > forma_matriz[1] - 1):
            i[1][0] += 999

    return costo_sucesores


# -----------------------------------------------------------------------------

def direccion_padre(direccion):
    if direccion == 'IZQUIERDA':
        dir_padre = 'DERECHA'
    elif direccion == 'DERECHA':
        dir_padre = 'IZQUIERDA'
    elif direccion == 'ABAJO':
        dir_padre = 'ARRIBA'
    else:
        dir_padre = 'ABAJO'

    return dir_padre


# -----------------------------------------------------------------------------

def castigar_direccion_padre(costo_sucesores, direccion_vieja):

    if len(direccion_vieja) > 0 and direccion_vieja[0]:
        dir = direccion_padre(direccion_vieja[1])

        for i in costo_sucesores:
            if i[1][1] == dir:
                i[0] += 50

    return costo_sucesores


# -----------------------------------------------------------------------------

def calcular_heuristico(matriz, sucesores, zanahorias, pasos_actuales,
                        pos_actual, rango_vision, direccion_vieja):
    # Obtenemos una submatriz con el rango de vision del conejo
    matriz_visible = calc_submatriz(matriz, pos_actual, rango_vision)

    # Determinamos la forma de la matriz original
    m2 = np.matrix(matriz)
    forma_matriz = m2.shape

    # Castigamos segun la distancia lineal a las zanahorias
    costo_sucesores = castigar_distancia(sucesores, zanahorias, pasos_actuales)

    # Castigamos segun la region que tenga mas zanahorias
    costo_sucesores = castigar_emisferios(matriz_visible, costo_sucesores,
                                          pos_actual)

    # Castigamos si el sucesor va a un espacio desconocido
    costo_sucesores = castigar_esp_desconocido(costo_sucesores, forma_matriz)

    # Castigamos la direccion padre si en la misma no existia zanahoria
    costo_sucesores = castigar_direccion_padre(costo_sucesores,
                                               direccion_vieja)

    return costo_sucesores


#  -----------------------------------------------------------------------------

def get_costos_direccion(costo_sucesores):
    costo_izq = costo_der = costo_arriba = costo_abajo = 0

    for i in costo_sucesores:
        sucesor = i[1]
        if sucesor[1] == 'IZQUIERDA':
            costo_izq = i[0]
        elif sucesor[1] == 'DERECHA':
            costo_der = i[0]
        elif sucesor[1] == 'ABAJO':
            costo_abajo = i[0]
        else:
            costo_arriba = i[0]

    return costo_izq, costo_der, costo_arriba, costo_abajo


#  -----------------------------------------------------------------------------

def a_estrella(matriz, rango_vision, cant_zanahorias):
    pos_actual = calc_pos_conejo(matriz)
    pasos_actuales = 0
    direccion_vieja = []
    while cant_zanahorias > 0:

        # Calculamos los estados a los que se puede desplazar el conejo
        sucesores = estados_sucesores(pos_actual)

        # Buscamos si hay zanahorias en el rango de vision
        zanahorias = delimitar_rango_vision(matriz, pos_actual, rango_vision)

        # Creamos una lista donde agregamos el calculo del heuristico
        # para cada sucesor, obteniendo [[costo_heuristico, sucesor],...]
        # Calculamos el heuristico para cada estado sucesor
        costo_sucesores = \
            calcular_heuristico(matriz, sucesores, zanahorias, pasos_actuales,
                                pos_actual, rango_vision, direccion_vieja)

        # Calculamos cual de todos es el mejor sucesor
        mejor_sucesor = calc_mejor_sucesor(costo_sucesores)
        pos_nueva = mejor_sucesor[1][0]

        # Verificamos si el movimiento llega a una zanahoria(meta),
        # si es asi se resta una zanahoria como comida
        if verificar_meta(matriz, pos_nueva):
            cant_zanahorias -= 1
            direccion_vieja = [False, mejor_sucesor[1][1]]
        else:
            direccion_vieja = [True, mejor_sucesor[1][1]]

        # Desplazamos el conejo hacia la mejor direccion en el tablero
        desplazar_conejo(matriz, pos_actual, pos_nueva)

        # Actualizamos la posicion actual del conejo
        pos_actual = pos_nueva

        # Aumentamos el  valor de g() para calcular los sucesores
        pasos_actuales += 1

        # Imprimimos los pasos ejecutados por el conejo
        costo_izq, costo_der, costo_arriba, costo_abajo = \
            get_costos_direccion(costo_sucesores)

        mejor_movimiento = mejor_sucesor[1][1]
        print('PASO: %s '
              'IZQUIERDA: %d  DERECHA: %d  ARRIBA: %d  ABAJO: %d MOVIMIENTO: '
              '%s ' % (str(pasos_actuales).zfill(5), costo_izq, costo_der,
                       costo_arriba, costo_abajo, mejor_movimiento))

    print('PASO: %s FINAL' % (str(pasos_actuales).zfill(5)))


# -----------------------------------------------------------------------------
# ------------------ Pruebas --------------------------------------------------
# -----------------------------------------------------------------------------

test_matrix = [
    [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
    [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
    ['G', ' ', 'Z', ' ', ' ', 'Z', ' '],
    [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
    ['A', 'B', ' ', ' ', ' ', 'C', ' '],
    ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
]

matriz2 = np.arange(50).reshape(5, 10)

test_matrix = np.matrix(test_matrix)

print('---------- Heuristicos ----------')
distancias = calc_distancia_lineal([1, 2], [[0, 3], [3, 0], [3, 1]])
print('Heuristico min:\t', calc_heuristico_min(distancias))
for i in range(distancias.qsize()):
    x = distancias.get()
    print('valor: ', x[0], ' - Meta: ', x[1])

print('\n---------- Sub Matriz ----------')
posicion_actual = [4, 1]
rango_vision = 1
print('Matriz original: \n', test_matrix)
print('\nSubMatriz: \n',
      calc_submatriz(test_matrix, posicion_actual, rango_vision))

print('\n---------- Posicion de las Zanahorias en la matriz ----------')
print('Matriz original: \n', test_matrix)
print('Posiciones:\n', calc_pos_simbolo(test_matrix, 'Z'))

print('\n---------- Calcular posicion del conejo en la matriz ----------')
print('Posicion del conejo:\n', calc_pos_conejo(test_matrix))

# print('\n---------- Desplazar conejo en la matriz ----------')
# pos_vieja = [0, 0]
# pos_nueva = [0, 1]
# print('Movimiento Realizado\n',
#       desplazar_conejo(test_matrix, pos_vieja, pos_nueva))

print('\n---------- Eliminar sucesor viejo----------\n')
print(eliminar_sucesor_viejo(test_matrix, ['A', 'B', ' ', 'Z', ' ', ' ', ' ']))

print('\n---------- Conjunto de estados sucesores ----------\n')
pos_actual = [2, 2]
print('Estado Actual:\t', pos_actual)
print('Estados Sucesores:\n', estados_sucesores(pos_actual))

print('\n---------- SPLIT HORIZONTAL ----------\n')
m1, m2 = split_horizontal_matriz(test_matrix, pos_actual)
print('MatrizArriba:\n', m1)
print('MatrizAbajo:\n', m2)

print('\n---------- SPLIT VERTICAL ----------\n')
m1, m2 = split_vertical_matriz(test_matrix, pos_actual)
print('MatrizI<q:\n', m1)
print('MatrizDer:\n', m2)

print('\n---------- FUNCION A ESTRELLA ----------\n')
a_estrella(test_matrix, 3, 5)
