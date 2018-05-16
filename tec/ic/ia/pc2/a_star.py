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

def get_submatriz(matriz, pos_actual, rango_vision):
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
# ------------------ Pruebas --------------------------------------------------
# -----------------------------------------------------------------------------
test_matrix = [
    ['Z','','','N','','','Z'],
    ['','Z','','N','','',''],
    ['G','','Z','','','C',''],
    ['','','Z','','','',''],
    ['A','B','','Z','','',''],
    ['Z','','','','','','Z']
]

matriz2 = np.arange(50).reshape(5,10)


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
      get_submatriz(test_matrix, posicion_actual, rango_vision))

print('\n---------- Posicion de las Zanahorias en la matriz ----------')
print('Matriz original: \n',test_matrix)
print('Posiciones:\n', calc_pos_simbolo(test_matrix, 'N'))
