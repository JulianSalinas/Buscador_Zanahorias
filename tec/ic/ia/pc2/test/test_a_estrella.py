
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
        Entradas:
        Resultado esperado:

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

        pos_zanahorias = calc_pos_simbolo(test_matrix, 'Z')

        pos_reales = [[0, 6], [1, 1], [2, 2], [2, 5], [3, 2], [5, 0], [5, 3]]

        self.assertEqual(pos_zanahorias, pos_reales)

    # -------------------------------------------------------------------------

    def test_posicion_conejo(self):

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

        pos_conejo = calc_pos_conejo(test_matrix)

        pos_real = [2, 1]

        self.assertEqual(pos_conejo, pos_real)

    # -------------------------------------------------------------------------

    def test_desplazar_conejo(self):
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
