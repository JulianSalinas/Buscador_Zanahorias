
import numpy as np

from random import seed
from time import time
from unittest import TestCase

from model.genetic_algorithms import *


class TestGeneticAlgorithms(TestCase):

    def test_gen_in_list(self):
        """
        :return: Sin retorno
        """
        gen = Gen(np.array([' ', ' ', 'C', ' ', ' ', ' ', 'Z', 'Z', ' '],
                           dtype=object))
        gen2 = Gen(np.array([' ', ' ', 'C', ' ', ' ', ' ', 'Z', 'Z', ' '],
                            dtype=object))
        gen3 = Gen(np.array([' ', ' ', 'C', ' ', ' ', ' ', ' ', 'Z', ' '],
                            dtype=object))

        gen_list = [gen2, gen3]

        self.assertTrue(gen_in_list(gen, gen_list))

    def test_direction_to_arrow(self):
        """
        :return: Sin retorno
        """
        directions = ['arriba', 'abajo', 'izquierda', 'derecha']
        expected_results = ['A', 'V', '<', '>']
        real_results = [direction_to_arrow()[d] for d in directions]

        self.assertEqual(expected_results, real_results)

    def test_a_idx_to_m_idx(self):
        """
        :return: Sin retorno
        """
        matrix_shapes = [(4, 3), (2, 5)]
        expected_results = [(3, 0), (1, 4)]
        real_results = [a_idx_to_m_idx(9, ms) for ms in matrix_shapes]

        self.assertEqual(expected_results, real_results)

    def test_initialization(self):
        """
        :return: Sin retorno
        """
        matrix = np.matrix([[1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 9]])

        generation, matrix_shape = initialization(matrix, 3, 'arriba', False)

        # Se cambia el valor de otro objeto para asegurar que son instancias
        # aparte
        generation[1].get_array()[1] = 3

        self.assertEqual(generation[0].get_array()[1], 2)

    def test_cross(self):
        """
        :return: Sin retorno
        """
        parent1 = Gen(np.array(['A', 'B', 'C', 'D', 'E', 'F', '7', '8', '9']))
        parent2 = Gen(np.array(['1', '2', '3', '4', '5', '6', 'G', 'H', 'I']))

        seed(7)

        childs = cross(parent1, parent2, 1)

        expected_results = list()
        expected_results.append(['1', '2', '3',
                                 '4', '5', '6',
                                 '7', '8', '9'])

        expected_results.append(['A', 'B', 'C',
                                 'D', 'E', 'F',
                                 'G', 'H', 'I'])

        real_results = [c.get_array().tolist() for c in childs]
        seed(time())

        self.assertEqual(expected_results, real_results)

    def test_mutation(self):
        """
        :return: Sin retorno
        """
        gen = Gen(np.array([' ', ' ', 'C', ' ', ' ', ' ', 'Z', 'Z', ' '],
                           dtype=object))

        seed(1)
        mutation1, _ = mutate(gen, 20)  # Inserción de una flecha
        seed(2)
        mutation2, _ = mutate(gen, 20)  # Inserción de una flecha
        seed(2)
        mutation3, _ = mutate(mutation2, 20)  # Cambio de dirección de flecha

        real_results = list()
        real_results.append(mutation1.get_array().tolist())
        real_results.append(mutation2.get_array().tolist())

        expected_results = list()
        expected_results.append([' ', 'A', 'C', ' ', ' ', ' ', 'Z', 'Z', ' '])
        expected_results.append([' ', '<', 'C', ' ', ' ', ' ', 'Z', 'Z', ' '])

        self.assertEqual(real_results, expected_results)

        seed(time())