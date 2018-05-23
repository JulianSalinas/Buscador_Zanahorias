
from unittest import TestCase
from model.a_estrella import *


# -----------------------------------------------------------------------------

class TestAEstrella(TestCase):

    """
    Clase encargada de probar funciones y fragmentos importantes de código para
    el modulo modelo.a_estrella
    """

    # -------------------------------------------------------------------------

    def test_calc_distancia_lineal(self):

        """
        Prueba la funcionalidad de distancia lineal, entre un punto y el
        conjunto de metas a las que se puede dirigir el conejo, que serian las
        zanahorias que se encuentran dentro del rango de vision

        Entradas: No aplica

        Resultado esperado: Las distancias del punto[1,2] a las zanahorias son:
            [1,2] - [0,3] = 2
            [1,2] - [3,0] = 4
            [1,2] - [3,1] = 3

        @return Sin retorno
        """

        distancias = calc_distancia_lineal([1, 2], [[0, 3], [3, 0], [3, 1]])

        distancia_1 = distancias.get()
        distancia_1 = distancia_1[0]

        distancia_2 = distancias.get()
        distancia_2 = distancia_2[0]

        distancia_3 = distancias.get()
        distancia_3 = distancia_3[0]

        self.assertEqual(distancia_1, 2)
        self.assertEqual(distancia_2, 3)
        self.assertEqual(distancia_3, 4)

    # -------------------------------------------------------------------------

    def test_sub_matriz(self):

        """
        Se encarga de probar la funcionalidad de obtener una submatriz
        segun el rango de vision que tiene el conejo dentro del tablero.

        Entradas: No aplica

        Resultado esperado: En este caso se prueba con una matriz de 6x7.
        El conejo se encuentra en la posicion [2,1] y al tener un rango
        de vision de 1 se espera obtener una submatriz que va desde el punto
        [1,0] al [3,2]

        @return Sin retorno
        """

        test_matrix = np.matrix([
            [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
            [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
            [' ', 'C', 'Z', ' ', ' ', 'Z', ' '],
            [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
        ])

        posicion_actual = [2, 1]
        rango_vision = 1

        sub_matriz = calc_submatriz(test_matrix, posicion_actual, rango_vision)

        sub_matriz_real = [
            [' ', 'Z', ' '],
            [' ', 'C', 'Z'],
            [' ', ' ', 'Z']
        ]

        self.assertTrue(sub_matriz.tolist(), sub_matriz_real)

    # -------------------------------------------------------------------------

    def test_posicion_zanahorias(self):

        """
        Se encarga de probar la funcion de extraer posiciones, esto para
        cada zanahoria que se encuentra en la matriz que ve el conejo en un
        punto determinado.
        Es decir, si en la matriz se encuentran tres zanahorias, las mismas
        deberian retornarse como una lista con valores [x,y] que representan
        la posicion de cada una de estas.

        Entradas: No Aplica

        Resultado esperado:
            En una lista con la forma

                test_matrix = [
                    [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
                    [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
                    [' ', 'C', 'Z', ' ', ' ', 'Z', ' '],
                    [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
                ]

            Los valores obtenidos deben ser:
                [[0, 6], [1, 1], [2, 2], [2, 5], [3, 2], [5, 0], [5, 3]]

        @return Sin retorno
        """

        test_matrix = np.matrix([
            [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
            [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
            [' ', 'C', 'Z', ' ', ' ', 'Z', ' '],
            [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
        ])

        pos_zanahorias = calc_pos_simbolo(test_matrix, 'Z')

        pos_reales = [[0, 6], [1, 1], [2, 2], [2, 5], [3, 2], [5, 0], [5, 3]]

        self.assertEqual(pos_zanahorias, pos_reales)

    # -------------------------------------------------------------------------

    def test_posicion_conejo(self):

        """
        Se encarga de probar la funcion de extraer la posicion del conejo
        que se encuentra en la matriz/tablero de juego

        Entradas: No Aplica

        Resultado esperado:
            El resultado esperado es un punto [x,y] representando los indices
            donde se encuentra ubicado el conejo dentro del tablero

            En este caso, para la matriz de prueba  que aparece a continuación:

            test_matrix = [
                [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
                [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
                [' ', 'C', 'Z', ' ', ' ', 'Z', ' '],
                [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
            ]

            La posicion del conejo es [2,1]

        @return Sin retorno
        """

        test_matrix = np.matrix([
            [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
            [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
            [' ', 'C', 'Z', ' ', ' ', 'Z', ' '],
            [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
        ])

        pos_conejo = calc_pos_conejo(test_matrix)

        pos_real = [2, 1]

        self.assertEqual(pos_conejo, pos_real)

    # -------------------------------------------------------------------------

    def test_desplazar_conejo(self):
        """
        Lo que se pretende en esta prueba, es verificar la funcion de
        desplazamiento del conejo, es decir, poner moverlo de una ubicacion
        [x1, y1] a [x2, y2], reemplazando el valor de la casilla [x1, y1] por
        el simbolo de vacio ' ', y además agregando el simbolo de conejo en
        la casilla [x2, y2]

        Entradas: No Aplica

        Resultado esperado:
            Para la matriz:

            test_matrix = [
                [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
                [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
                [' ', 'C', 'Z', ' ', ' ', 'Z', ' '],
                [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
            ]

            Se espera que el conejo de desplace la ubicacion:
                pos_vieja = [2, 1] ---> pos_nueva = [1, 1]

            Teniendo como resultado la matriz:
            [
                [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
                [' ', 'C', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', 'Z', ' ', ' ', 'Z', ' '],
                [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
            ]

        @return Sin retorno
        """
        test_matrix = np.matrix([
            [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
            [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
            [' ', 'C', 'Z', ' ', ' ', 'Z', ' '],
            [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
        ])

        pos_vieja = [2, 1]
        pos_nueva = [1, 1]

        matriz_desplazada = desplazar_conejo(test_matrix, pos_vieja, pos_nueva)

        matriz_real = [
            [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
            [' ', 'C', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'Z', ' ', ' ', 'Z', ' '],
            [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
        ]

        self.assertEqual(matriz_desplazada.tolist(), matriz_real)

    # -------------------------------------------------------------------------

    def test_estados_sucesores(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """

        pos_actual = [2, 2]

        sucesores_aux = estados_sucesores(pos_actual)
        sucesores = []
        for i in sucesores_aux:
            sucesores.append(i[0])

        sucesores_reales = [[2, 1], [2, 3], [1, 2], [3, 2]]

        self.assertEqual(sucesores, sucesores_reales)

    # -------------------------------------------------------------------------

    def test_split_horizontal(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """

        test_matrix = np.matrix([
            [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
            [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
            [' ', 'C', 'Z', ' ', ' ', 'Z', ' '],
            [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
        ])

        pos_actual = [2, 1]

        m_arriba = [
            [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
            [' ', 'Z', ' ', ' ', ' ', ' ', ' ']
        ]

        m_abajo = [
            [' ', 'C', 'Z', ' ', ' ', 'Z', ' '],
            [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
        ]

        m1, m2 = split_horizontal_matriz(test_matrix, pos_actual)

        self.assertEqual(m1.tolist(), m_arriba)
        self.assertEqual(m2.tolist(), m_abajo)

    # -------------------------------------------------------------------------

    def test_split_vertical(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """
        test_matrix = np.matrix([
            [' ', ' ', ' ', ' ', ' ', ' ', 'Z'],
            [' ', 'Z', ' ', ' ', ' ', ' ', ' '],
            [' ', 'C', 'Z', ' ', ' ', 'Z', ' '],
            [' ', ' ', 'Z', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['Z', ' ', ' ', 'Z', ' ', ' ', ' ']
        ])

        pos_actual = [2, 1]
        m_izq = [
            [' '],
            [' '],
            [' '],
            [' '],
            [' '],
            ['Z']
        ]

        m_der = [
            [' ', ' ', ' ', ' ', ' ', 'Z'],
            ['Z', ' ', ' ', ' ', ' ', ' '],
            ['C', 'Z', ' ', ' ', 'Z', ' '],
            [' ', 'Z', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'Z', ' ', ' ', ' ']
        ]

        m1, m2 = split_vertical_matriz(test_matrix, pos_actual)

        self.assertEqual(m1.tolist(), m_izq)
        self.assertEqual(m2.tolist(), m_der)

    # -------------------------------------------------------------------------

    def test_calcular_mejor_sucesor(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """
        self.assertEqual(sucesor, sucesor_real)

    # -------------------------------------------------------------------------

    def test_verificar_meta(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """
        self.assertEqual(meta, meta_real)

    # -------------------------------------------------------------------------

    def test_delimitar_rango_vision(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """
        self.assertEqual(rango, rango_real)

    # -------------------------------------------------------------------------

    def test_castigar_distancia(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """
        self.assertEqual(costo_sucesores, costo_sucesores_real)

    # -------------------------------------------------------------------------

    def test_castigar_emisferios(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """
        self.assertEqual(costo_sucesores, costo_sucesores_real)

    # -------------------------------------------------------------------------

    def test_castigar_espacio_desconocido(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """
        self.assertEqual(costo_sucesores, costo_sucesores_real)

    # -------------------------------------------------------------------------

    def test_castigar_direccion_padre(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """
        self.assertEqual(costo_sucesores, costo_sucesores_real)

    # -------------------------------------------------------------------------

    def test_direccion_padre(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """
        self.assertEqual(costo_sucesores, costo_sucesores_real)

    # -------------------------------------------------------------------------

    def test_costos_direccion(self):
        """
        Entradas:
        Resultado esperado:

        @return Sin retorno
        """
        self.assertEqual(costo_sucesores, costo_sucesores_real)
