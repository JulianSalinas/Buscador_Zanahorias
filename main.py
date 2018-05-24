# -----------------------------------------------------------------------------

import argparse
from tec.ic.ia.pc2.g03 import run

# -----------------------------------------------------------------------------


def get_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('--genetico', action='store_true')
    parser.add_argument('--a-estrella', action='store_true')
    parser.add_argument('--tablero-inicial', nargs=1, type=str)

    # Para --a-estrella
    parser.add_argument('--vision', nargs=1, type=int, default=[3])
    parser.add_argument('--zanahoria', nargs=1, type=int, default=[2])

    # Para --genetico
    parser.add_argument('--abajo', action='store_true')
    parser.add_argument('--arriba', action='store_true')
    parser.add_argument('--derecha', action='store_true')
    parser.add_argument('--izquierda', action='store_true')
    parser.add_argument('--individuos', nargs=1, type=int, default=[15])
    parser.add_argument('--generaciones', nargs=1, type=int, default=[100])
    parser.add_argument('--semilla', nargs=1, type=int, default=[10])
    parser.add_argument('--politica', nargs=1, type=int, default=[1])
    parser.add_argument('--mutaciones', nargs=1, type=int, default=[5])
    return parser.parse_args()


# -----------------------------------------------------------------------------


if __name__ == '__main__':

    args = get_arguments()

    if not (args.a_estrella or args.genetico):
        print("Debe específicar --a-estrella o --genetico")

    elif args.genetico:

        if not (args.derecha or args.izquierda or args.arriba or args.abajo):
            print("Debe indicar la posición actual "
                  "--derecha, --izquierda, --arriba o --abajo")

    run(get_arguments())

# -----------------------------------------------------------------------------

