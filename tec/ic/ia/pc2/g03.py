# -----------------------------------------------------------------------------

import os
import sys

sys.path.append('..')
from tec.ic.ia.pc2.model.file_utils import *
from tec.ic.ia.pc2.model.a_estrella import a_estrella
from tec.ic.ia.pc2.model.genetic_algorithms import run_carrot_finder

# -----------------------------------------------------------------------------


def run(args):

    if args.tablero_inicial is None:
        filename = get_default_filename()
    else:
        filename = args.tablero_inicial[0]

    initial_board = read_file(filename)

    if args.a_estrella:
        return a_estrella(initial_board, args.vision[0], args.zanahoria[0])

    else:

        if args.derecha:
            initial_direction = 'derecha'
        elif args.izquierda:
            initial_direction = 'izquierda'
        elif args.arriba:
            initial_direction = 'arriba'
        else:
            initial_direction = 'abajo'

        return run_carrot_finder(initial_direction,
                                 args.individuos[0],
                                 args.generaciones[0],
                                 args.mutacion[0],
                                 initial_board,
                                 args.politica[0],
                                 args.semilla[0])

# -----------------------------------------------------------------------------
