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
# ------------------ Pruebas --------------------------------------------------
# -----------------------------------------------------------------------------

test_matrix = [
    ['','','','N','','','Z'],
    ['','Z','','N','','',''],
    ['G','','Z','','','Z',''],
    ['','','Z','','','',''],
    ['A','B','','Z','','',''],
    ['Z','','','','','','C']
]

matriz2 = np.arange(50).reshape(5, 10)


test_matrix = np.matrix(test_matrix)

print('---------- Heuristicos ----------')
distancias = calc_heuristico([1, 2], [[0,3], [3,0], [3,1]])
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
print('Posiciones:\n', calc_pos_simbolo(test_matrix, 'N'))


print('\n---------- Calcular posicion del conejo en la matriz ----------')
print('Posicion del conejo:\n', calc_pos_conejo(test_matrix))


print('\n---------- Desplazar conejo en la matriz ----------')
pos_vieja = [0, 0]
pos_nueva = [0, 1]
print('Movimiento Realizado\n',
      desplazar_conejo(test_matrix, pos_vieja, pos_nueva))
