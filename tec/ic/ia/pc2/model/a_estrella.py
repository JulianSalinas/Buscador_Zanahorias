# -----------------------------------------------------------------------------

import os
import queue
import numpy as np
from file_utils import *


# -----------------------------------------------------------------------------

def calc_distancia_lineal(pos, metas):
    """
    Funcion utlizada para asignar pesos al heuristico por medio de la distancia
    lineal entre una posicion determinada y el conjunto de objetivos meta

    :param pos: Es la posicion en la que se encuentra el conejo, representada
    como un arreglo [x, y]
    :param metas: lista con el conjunto de posiciones de las zanahorias
    de la forma [[x1, y1], ..., [Xn, Yn]]
    :return: lista de prioridad con las distancias del conejo hacia cada una de
    las zanahorias
    """

    distancias = queue.PriorityQueue()

    for meta in metas:
        distancia = abs(meta[0] - pos[0]) + abs(meta[1] - pos[1])
        distancias.put((distancia, meta))

    return distancias


# -----------------------------------------------------------------------------

def calc_submatriz_aux(matriz, pos_actual, rango_vision):
    """
    Funcion utilizada para el calculo de una submatriz que representa el rango
    de vision que tiene el conejo

    :param matriz: es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param pos_actual: posicion del conejo en el tablero, de la forma [x, y]
    :param rango_vision: es un numero que representa la cantidad de casillas
    que el conejo puede visualizar a su alrededor
    :return: sub matriz con n filas y m columnas, representando el rango
    de vision del conejo
    """

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

def calc_submatriz(matriz, pos_actual, rango_vision):
    """
    Funcion utilizada para el calculo de una submatriz que representa el rango
    de vision que tiene el conejo

    :param matriz: es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param pos_actual: posicion del conejo en el tablero, de la forma [x, y]
    :param rango_vision: es un numero que representa la cantidad de casillas
    que el conejo puede visualizar a su alrededor
    :return: sub matriz con n filas y m columnas, representando el rango
    de vision del conejo
    """
    sub_matriz = matriz.copy()

    zanahorias = calc_pos_simbolo(matriz, 'Z')

    z_visibles = delimitar_rango_vision(matriz, pos_actual, rango_vision)

    for i in z_visibles:
        zanahorias.remove(i)

    sub_matriz.put(zanahorias, ' ')

    return sub_matriz


# -----------------------------------------------------------------------------

def calc_pos_simbolo(matriz, simbolo):
    """
    Funcion empleada para determinar las posiciones de un determinado simbolo
    dentro de una matriz
    En este caso, se utiliza para determinar donde se encuentra el conejo, y
    tambien para saber donde estan las zanahorias

    :param matriz:  es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param simbolo: letra que se buscara dentro de la matriz, en el caso de las
    zanahorias seria la 'Z' y del conejo seria la 'C'
    :return: lista con el conjunto de posiciones del simbolo dentro
    de la matriz
    """

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
    """
    Funcion utilizada para desplazar el conejo dentro del tablero y hacer que
    se coma una zanahoria si es que encuentra una

    :param matriz: es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param pos_vieja: arreglo de la forma [x, y], representando la posicion
    vieja del conejo
    :param pos_nueva: arreglo de la forma [x, y], representando la posicion
    que debera ocupar el conejo dentro de la matriz
    :param simbolo_vacio: simbolo que sera asignado al espacio desocupado por
    el conejo
    :param simbolo_conejo: simbolo que sera asignado al nuevo espacio ocupado
    por el conejo
    :return: matriz actualizada con el simbolo del conejo desplazado
    """

    pos_x = pos_vieja[0]
    pos_y = pos_vieja[1]
    matriz[pos_x, pos_y] = simbolo_vacio

    pos_x = pos_nueva[0]
    pos_y = pos_nueva[1]
    matriz[pos_x, pos_y] = simbolo_conejo

    return matriz


# -----------------------------------------------------------------------------

def calc_pos_conejo(matriz, simbolo_conejo='C'):
    """
    Funcion utilizada para determinar en que posicion [x, y] se encuentra el
    conejo dentro de la matriz

    :param matriz: es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param simbolo_conejo: es el simbolo que tiene el conejo
    dentro de la matriz
    :return: posicion [x, y] del conejo dentro de la matriz
    """
    
    pos = []
    indices = calc_pos_simbolo(matriz, simbolo_conejo)

    if len(indices) > 0:
        pos = indices[0]

    return pos


# -----------------------------------------------------------------------------

def estados_sucesores(estado_actual):
    """
    Funcion utilizada para calcular el conjunto de direcciones a las que se
    puede desplazar el conejo Izq, Der, Top, Down

    :param estado_actual: posicion [x, y] en la que se encuentra el conejo
    :return: lista con el conjunto de direcciones a las que se puede desplazar
    el conejo
    """

    izq = [[estado_actual[0], estado_actual[1] - 1], 'IZQUIERDA']
    der = [[estado_actual[0], estado_actual[1] + 1], 'DERECHA']
    arriba = [[estado_actual[0] - 1, estado_actual[1]], 'ARRIBA']
    abajo = [[estado_actual[0] + 1, estado_actual[1]], 'ABAJO']

    sucesores = [izq, der, arriba, abajo]
    return sucesores


# -----------------------------------------------------------------------------

def calc_heuristico_min(heuristicos):
    """
    Funcion utilizada para calcular cual de todos los heuristicos es el mejor

    :param heuristicos: conjunto de valores que fueron determinados y sobre
    los que se determinara el mejor costo
    :return: valor del mejor costo
    """

    costo = 50

    if heuristicos.qsize() > 0:
        mejor_valor = heuristicos.get()
        costo = mejor_valor[0]

    return costo


# -----------------------------------------------------------------------------

def calc_mejor_sucesor(sucesores):
    """
    Funcion utilizada para determinar cual de todas las direcciones
    posibles es la mejor para hacer que el conejo de desplace

    :param sucesores: Conjunto de direcciones posibles a las que se puede
    desplazar el conejo
    :return: Mejor sucesor del conjunto de sucesores, indicando el costo, la
    etiqueta de direccion y la posicion a la que se debe desplazar
    """

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
    """
    Verifica si dada una posicion, el conejo llego o no a la meta, que seria
    basicamente localizar una zanahoria dentro del tablero

    :param matriz: es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param posicion: es un arreglo de la forma [x, y] que indica la posicion
    en la que se encuentra el conejo
    :param meta: es el caracter que se desea encontrar, o que indica que se
    llego a una meta
    :return: valor booleano indicando si encontro o no una zanahoria
    """

    eje_x = posicion[0]
    eje_y = posicion[1]

    if matriz[eje_x, eje_y] == meta:
        return True

    return False


# -----------------------------------------------------------------------------

def eliminar_sucesor_viejo(sucesores, sucesor_viejo):
    """
    Funcion utilizada para borrar un sucesor viejo del conjunto de sucesores
    que puede tener una detemrinada posicion

    :param sucesores: conjunto de direcciones a las que se puede
    dirigir el conejo
    :param sucesor_viejo: es el sucesor del cual provenia el conejo
    :return: conjunto de sucesores sin el sucesor viejo
    """

    sucesores = sucesores.tolist()
    if sucesor_viejo in sucesores:
        sucesores.remove(sucesor_viejo)

    sucesores = np.matrix(sucesores)

    return sucesores


# -----------------------------------------------------------------------------

def delimitar_rango_vision(matriz, pos_actual, rango_vision):
    """
    Elimina el conjunto de zanahorias que se encuentran fuera del rango de
    vision, esto para evitar que sean tomadas en cuenta

    :param matriz: es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param pos_actual: posicion [x, y] en la que se encuentra el conejo
    :param rango_vision: es un numero que indica la cantidad de casillas
    que puede ver el conejo a su alrededor
    :return: conjunto de zanahorias que se encuentran dentro del
    rango de vision
    """

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
    """
    Funcion utilizada para partir la matriz o tablero en dos secciones, arriba
    y abajo

    :param matriz: es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param pos_actual: posicion [x, y] en la que se encuentra el conejo
    :return: matriz superior e inferior, detemrinadas por un split de la matriz
    en la posicion en la que se encuentra el conejo
    """

    matriz_1 = matriz[:pos_actual[0], :]
    matriz_2 = matriz[pos_actual[0]:, :]
    return matriz_1, matriz_2


# -----------------------------------------------------------------------------

def split_vertical_matriz(matriz, pos_actual):
    """
    Funcion utilizada para partir la matriz o tablero en dos secciones, derecha
    e izquierda

    :param matriz: es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param pos_actual: posicion [x, y] en la que se encuentra el conejo
    :return: matriz izquierda y derecha, detemrinadas por un split de la matriz
    en la posicion en la que se encuentra el conejo
    """

    matriz_1 = matriz[:, :pos_actual[1]]
    matriz_2 = matriz[:, pos_actual[1]:]
    return matriz_1, matriz_2


# -----------------------------------------------------------------------------

def castigar_distancia(sucesores, zanahorias, pasos_actuales):
    """
    Funcion utilizada por el heuirstico para colocar un peso a cada direccion
    segun la distancia lineal de una posicion hacia la meta

    :param sucesores: es el conjunto de direcciones a las que puede desplazarse
    el conejo desde su posicion actual
    :param zanahorias: es una lista con el conjunto [x, y] de cada zanahoria
    dentro del rango de vision
    :param pasos_actuales: es la cantidad de pasos que ha dado el conejo
    :return: costo de cada uno de los posibles sucesores, con su respectiva
    posicion y etiqueta de direccion
    """

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

def castigar_emisferios(matriz, costo_sucesores, pos_actual, cant_zanahorias):
    """
    Funcion utilizada para castigar las direcciones donde se encuentran menos
    zanahorias

    :param matriz: es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param costo_sucesores: costo de cada uno de los posibles sucesores,
    con su respectiva posicion y etiqueta de direccion
    :param pos_actual: posicion que ocupa el conejo actualmente, es decir,
    antes de que se desplace
    :param cant_zanahorias: es l cantidad de zanahorias que le faltan por comer
    al conejo para verse satisfecho
    :return: costo de cada uno de los posibles sucesores, con su respectiva
    posicion y etiqueta de direccion
    """

    m_izq, m_der = split_vertical_matriz(matriz, pos_actual)
    m_arriba, m_abajo = split_horizontal_matriz(matriz, pos_actual)

    zanahorias_izq = calc_pos_simbolo(m_izq, 'Z')
    zanahorias_der = calc_pos_simbolo(m_der, 'Z')
    zanahorias_abajo = calc_pos_simbolo(m_abajo, 'Z')
    zanahorias_arriba = calc_pos_simbolo(m_arriba, 'Z')

    for i in costo_sucesores:
        dir_sucesor = i[1][1]
        if dir_sucesor == 'IZQUIERDA':
            if len(zanahorias_izq) < len(zanahorias_der) \
                    == cant_zanahorias:
                i[0] += 3
        elif dir_sucesor == 'DERECHA':
            if len(zanahorias_der) < len(zanahorias_izq) \
                    == cant_zanahorias:
                i[0] += 3
        elif dir_sucesor == 'ABAJO':
            if len(zanahorias_abajo) < len(zanahorias_arriba) \
                    == cant_zanahorias:
                i[0] += 3
        else:
            if len(zanahorias_arriba) < len(zanahorias_abajo) \
                    == cant_zanahorias:
                i[0] += 3

    return costo_sucesores


# -----------------------------------------------------------------------------

def castigar_esp_desconocido(costo_sucesores, forma_matriz):
    """
    Funcion utilizada para castigar los sucesores/direcciones que van a un
    espacio desconocido del tablero, es decir, que se intentan salir.

    :param costo_sucesores: costo de cada uno de los posibles sucesores,
    con su respectiva posicion y etiqueta de direccion
    :param forma_matriz: es el .shape del tablero, misma que indica las
    dimensiones que tiene el tablero
    :return: costo de cada uno de los posibles sucesores, con su respectiva
    posicion y etiqueta de direccion
    """

    for i in costo_sucesores:
        posicion = i[1][0]
        if (0 > posicion[0]) or (posicion[0] > forma_matriz[0] - 1) or\
                (0 > posicion[1]) or (posicion[1] > forma_matriz[1] - 1):
            i[0] += 100

    return costo_sucesores


# -----------------------------------------------------------------------------

def direccion_padre(direccion):
    """
    Determinar cual direccion es la del padre, en otras palabras, de cual
    provenia el conejo

    :param direccion: es la etiqueta con la direccion que llevo al conejo
    a estar donde se encuentra actualmente
    :return: direccion hacia el padre (la opuesta)
    """

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
    """
    Funcion utilizada para calcular el heuristico, misma que se encarga de
    colocar un costo al sucesor que dirige hacia el padre, esto si en la
    posicion no existian zanahorias

    :param costo_sucesores: costo de cada uno de los posibles sucesores,
    con su respectiva posicion y etiqueta de direccion
    :param direccion_vieja: es la etiqueta con la direccion que llevo al conejo
    a estar donde se encuentra actualmente
    :return: costo de cada uno de los posibles sucesores, con su respectiva
    posicion y etiqueta de direccion luego de penalizar por direccion del padre
    """

    if len(direccion_vieja) > 0 and direccion_vieja[0]:
        direccion = direccion_padre(direccion_vieja[1])

        for i in costo_sucesores:
            if i[1][1] == direccion:
                i[0] += 10

    return costo_sucesores


# -----------------------------------------------------------------------------

def calcular_heuristico(matriz, sucesores, zanahorias, pasos_actuales,
                        pos_actual, rango_vision, direccion_vieja,
                        cant_zanahorias):
    """
    Funcion utilizada para determinar el heuristico de un determinado
    movimiento, aplicando los diferentes tipos de castigo a cada direccion

    :param matriz: es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param sucesores: Conjunto de direcciones posibles a las que se puede
    desplazar el conejo
    :param zanahorias: es una lista con el conjunto [x, y] de cada zanahoria
    dentro del rango de vision
    :param pasos_actuales: es un numero que indica el costo acumulado hasta el
    momento, es decir la funcion g(n)
    :param pos_actual: posicion del conejo en el tablero, de la forma [x, y]
    :param rango_vision: es un numero que indica la cantidad de casillas
    que puede ver el conejo a su alrededor
    :param direccion_vieja: es la etiqueta con la direccion que llevo al conejo
    a estar donde se encuentra actualmente
    :param cant_zanahorias: es l cantidad de zanahorias que le faltan por comer
    al conejo para verse satisfecho
    :return: costo de cada uno de los posibles sucesores, con su respectiva
    posicion y etiqueta de direccion luego de penalizar por direccion
    """

    # Obtenemos una submatriz con el rango de vision del conejo
    matriz_visible = calc_submatriz(matriz, pos_actual, rango_vision)

    # Determinamos la forma de la matriz original
    m2 = np.matrix(matriz)
    forma_matriz = m2.shape

    # Castigamos segun la distancia lineal a las zanahorias
    costo_sucesores = castigar_distancia(sucesores, zanahorias, pasos_actuales)

    # Castigamos segun la region que tenga mas zanahorias
    costo_sucesores = castigar_emisferios(matriz_visible, costo_sucesores,
                                          pos_actual, cant_zanahorias)

    # Castigamos si el sucesor va a un espacio desconocido
    costo_sucesores = castigar_esp_desconocido(costo_sucesores, forma_matriz)

    # Castigamos la direccion padre si en la misma no existia zanahoria
    costo_sucesores = castigar_direccion_padre(costo_sucesores,
                                               direccion_vieja)

    return costo_sucesores


#  -----------------------------------------------------------------------------

def get_costos_direccion(costo_sucesores):
    """
    Funcion utilizada para extraer del arreglo de costos,
    cada uno de los mismo segun la direccion

    :param costo_sucesores: costo de cada uno de los posibles sucesores,
    con su respectiva posicion y etiqueta de direccion
    :return: costo de cada una de las posibles direcciones que puede tomar el
    conejo
    """

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


#  ----------------------------------------------------------------------------

def guardar_paso(pasos_actuales, matriz):

    folder = get_default_folder()
    folder = os.path.join(folder, "a_estrella")

    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = str(pasos_actuales).zfill(5) + ".txt"
    filename = os.path.join(folder, filename)
    save_file(filename, matriz)

#  ----------------------------------------------------------------------------


def a_estrella(matriz, rango_vision, cant_zanahorias):
    """
    Funcion principal del algoritmo A*, que recibe el tablero, el rango de
    vision y la cantidad de zanahorias meta, y con ello desplaza el conejo para
    lograr el objetivo de comerse todas las zanahorias

    :param matriz: es la matriz que representa el tablero por completo,
    de la forma [[fila1], [fila2], ..., [filaN]]
    :param rango_vision: es un numero que indica la cantidad de casillas
    que puede ver el conejo a su alrededor
    :param cant_zanahorias: es un numero que indica cuantas zanahorias debera
    comerse el conejo para darse por satisfecho
    :return: No existe retorno
    """

    pos_actual = calc_pos_conejo(matriz)
    pasos_actuales = 0
    direccion_vieja = []
    while cant_zanahorias > 0:
        # Aumentamos el  valor de g() para calcular los sucesores
        pasos_actuales += 1

        # Calculamos los estados a los que se puede desplazar el conejo
        sucesores = estados_sucesores(pos_actual)

        # Buscamos si hay zanahorias en el rango de vision
        zanahorias = delimitar_rango_vision(matriz, pos_actual, rango_vision)

        # Creamos una lista donde agregamos el calculo del heuristico
        # para cada sucesor, obteniendo [[costo_heuristico, sucesor],...]
        # Calculamos el heuristico para cada estado sucesor
        costo_sucesores = \
            calcular_heuristico(matriz, sucesores, zanahorias, pasos_actuales,
                                pos_actual, rango_vision, direccion_vieja,
                                cant_zanahorias)

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

        # Imprimimos los pasos ejecutados por el conejo
        costo_izq, costo_der, costo_arriba, costo_abajo = \
            get_costos_direccion(costo_sucesores)

        mejor_movimiento = mejor_sucesor[1][1]
        print('PASO: %s '
              '\tIZQUIERDA: %s'
              '\tDERECHA: %s'
              '\tARRIBA: %s'
              '\tABAJO: %s'
              '\tMOVIMIENTO: %s '
              % (str(pasos_actuales).zfill(5), str(costo_izq).ljust(5),
                 str(costo_der).ljust(5), str(costo_arriba).ljust(5),
                 str(costo_abajo).ljust(5), mejor_movimiento))
        guardar_paso(pasos_actuales, matriz)

    print('PASO: %s \tFINAL' % (str(pasos_actuales).zfill(5)))
    guardar_paso(pasos_actuales, matriz)


if __name__ == '__main__':

    test_matrix = np.matrix([
        [' ', ' ', ' ', ' ', 'C', ' ', 'Z'],
        [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'Z', ' ', ' ', 'Z', ' '],
        [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', 'Z', ' ', 'Z'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['Z', ' ', ' ', 'Z', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'Z', ' ', ' ', ' ', 'Z'],
        [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'Z', ' ', ' ', 'Z', ' '],
        [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'Z', ' ', ' ', 'Z', ' ', ' ']
    ])

    a_estrella(test_matrix, 2, 10)
