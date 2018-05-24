# -----------------------------------------------------------------------------

import argparse
from tec.ic.ia.pc2.g03 import run

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
    parser.add_argument('--semilla', nargs=1, type=int)
    parser.add_argument('--politica', nargs=1, type=int)
    parser.add_argument('--mutaciones', nargs=1, type=int)
    parser.add_argument('--semilla', nargs=1, type=int)

    return parser.parse_args()


# -----------------------------------------------------------------------------


if __name__ == '__main__':
    print("ARGS: ")
    args = get_arguments()
    print(args)
    run(args)

# -----------------------------------------------------------------------------

