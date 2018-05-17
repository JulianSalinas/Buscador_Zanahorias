import queue
import numpy as np


# -----------------------------------------------------------------------------

def calc_heuristico(pos, metas):
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

def desplazar_conejo(matriz, pos_vieja, pos_nueva, simbolo_vacio='',
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

def a_estrella(matriz, rango_vision, cant_zanahorias):
    pos_actual = calc_pos_conejo(matriz)
    pasos_actuales = 0

    while cant_zanahorias > 0:

        # Obtenemos una submatriz con el rango de vision del conejo
        # matriz_visible = calc_submatriz(matriz, pos_actual, rango_vision)

        # Calculamos los estados a los que se puede desplazar el conejo
        sucesores = estados_sucesores(pos_actual)

        # Buscamos si hay zanahorias en el rango de vision
        # zanahorias = calc_pos_simbolo(matriz_visible, 'Z')
        zanahorias = calc_pos_simbolo(matriz, 'Z')

        # Creamos una lista donde agregamos el calculo del heuristico
        # para cada sucesor, obteniendo [[costo_heuristico, sucesor],...]
        costo_sucesores = []

        # Calculamos el heuristico para cada estado sucesor
        for sucesor in sucesores:
            if len(zanahorias) > 0:
                heuristicos = calc_heuristico(sucesor[0], zanahorias)
                costo_heuristico = calc_heuristico_min(heuristicos)
            else:
                costo_heuristico = 999

            costo_total = pasos_actuales + costo_heuristico
            costo_sucesores.append([costo_total, sucesor])

        # Calculamos cual de todos es el mejor sucesor
        mejor_sucesor = calc_mejor_sucesor(costo_sucesores)
        pos_nueva = mejor_sucesor[1][0]

        # Verificamos si el movimiento llega a una zanahoria(meta),
        # si es asi se resta una zanahoria como comida
        if verificar_meta(matriz, pos_nueva):
            cant_zanahorias -= 1

        # Desplazamos el conejo hacia la mejor direccion en el tablero
        desplazar_conejo(matriz, pos_actual, pos_nueva)

        # Actualizamos la posicion actual del conejo
        pos_actual = pos_nueva

        # Aumentamos el  valor de g() para calcular los sucesores
        pasos_actuales += 1

        # Imprimimos los pasos ejecutados por el conejo
        costo_izq = 0
        costo_der = 0
        costo_arriba = 0
        costo_abajo = 0

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

        mejor_movimiento = mejor_sucesor[1][1]
        print('PASO: %s '
              'IZQUIERDA: %d  DERECHA: %d  ARRIBA: %d  ABAJO: %d MOVIMIENTO: %s'
              % (str(pasos_actuales).zfill(5), costo_izq, costo_der,
                 costo_arriba, costo_abajo, mejor_movimiento))

    print('PASO: %s FINAL' % (str(pasos_actuales).zfill(5)))


# -----------------------------------------------------------------------------
# ------------------ Pruebas --------------------------------------------------
# -----------------------------------------------------------------------------

test_matrix = [
    ['','','','N','','','Z'],
    ['','Z','','N','','',''],
    ['G','','Z','','','Z',''],
    ['','','Z','','','',''],
    ['A','B','','','','C',''],
    ['Z','','','Z','','','']
]

matriz2 = np.arange(50).reshape(5, 10)


test_matrix = np.matrix(test_matrix)

print('---------- Heuristicos ----------')
distancias = calc_heuristico([1, 2], [[0,3], [3,0], [3,1]])
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
print('Matriz original: \n',test_matrix)
print('Posiciones:\n', calc_pos_simbolo(test_matrix, 'Z'))


print('\n---------- Calcular posicion del conejo en la matriz ----------')
print('Posicion del conejo:\n', calc_pos_conejo(test_matrix))


# print('\n---------- Desplazar conejo en la matriz ----------')
# pos_vieja = [0, 0]
# pos_nueva = [0, 1]
# print('Movimiento Realizado\n',
#       desplazar_conejo(test_matrix, pos_vieja, pos_nueva))

print('\n---------- Eliminar sucesor viejo----------\n')
print(eliminar_sucesor_viejo(test_matrix, ['A','B','','Z','','','']))

print('\n---------- Conjunto de estados sucesores ----------\n')
pos_actual = [2, 2]
print('Estado Actual:\t', pos_actual)
print('Estados Sucesores:\n', estados_sucesores(pos_actual))

print('\n---------- FUNCION A ESTRELLA ----------\n')
a_estrella(test_matrix, 2, 1)
