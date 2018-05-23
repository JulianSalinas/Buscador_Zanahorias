# -----------------------------------------------------------------------------

import argparse
from tec.ic.ia.pc2.model.file_utils import *

# -----------------------------------------------------------------------------


def get_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('--genetico', action='store_true')
    parser.add_argument('--a-estrella', action='store_true')

    parser.add_argument('--abajo', action='store_true')
    parser.add_argument('--arriba', action='store_true')
    parser.add_argument('--derecha', action='store_true')
    parser.add_argument('--izquierda', action='store_true')

    parser.add_argument('--vision', nargs=1, type=int)
    parser.add_argument('--zanahoria', nargs=1, type=int)
    parser.add_argument('--individuos', nargs=1, type=int)
    parser.add_argument('--generaciones', nargs=1, type=int)
    parser.add_argument('--tablero-inicial', nargs=1, type=str)

    return parser.parse_args()


# -----------------------------------------------------------------------------


if __name__ == '__main__':

    print("ARGS: ")
    args = get_arguments()

    if args.tablero_inicial is None:
        filename = get_default_filename()
    else:
        filename = args.tablero_inicial[0]

    matrix = read_file(filename)

    print(matrix)

# -----------------------------------------------------------------------------

