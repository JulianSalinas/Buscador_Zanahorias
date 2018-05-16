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
    n_cols = len(matriz[0])
    n_filas = len(matriz)

    x_min = max(0, pos_actual[0] - rango_vision)
    x_max = min(n_filas, pos_actual[0] + rango_vision + 1)

    y_min = max(0, pos_actual[1] - rango_vision)
    y_max = min(n_cols, pos_actual[1] + rango_vision + 1)

    sub_matriz = matriz[x_min:x_max, y_min:y_max]

    return sub_matriz


# -----------------------------------------------------------------------------
test_matrix = [
    ['Z', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', 'Z', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', 'Z', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', 'Z', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', 'Z', 'Z', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', 'Z', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', 'C', '', '', '', '', '', '', '', '', '', '', 'Z', '']
]

matriz2 = np.arange(50).reshape(5,10)


test_matrix = np.matrix(test_matrix)

valores = np.nonzero(test_matrix == 'Z')

# print(valores[0])

distancias = calc_heuristico([1, 2], [[0,3], [3,0], [3,1]])

print('---------- Heuristicos ----------')
for i in range(distancias.qsize()):
    x = distancias.get()
    print('valor: ', x[0], ' - Meta: ', x[1])

print('\n---------- Sub Matriz ----------')
print('Matriz original: \n',matriz2)

print('\nSubMatriz: \n', get_submatriz(matriz2, [2,7], 1))