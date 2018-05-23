# -----------------------------------------------------------------------------

import os
import pandas as pd

# -----------------------------------------------------------------------------


def get_default_folder():
    folder = os.path.split(__file__)[0]
    folder = os.path.split(folder)[0]
    folder = os.path.abspath(folder)
    return os.path.join(folder, 'files')

# -----------------------------------------------------------------------------


def get_default_filename():
    folder = get_default_folder()
    return os.path.join(folder, "testing_file.txt")

# -----------------------------------------------------------------------------


def save_file(filename, data):
    filename = fix_filename(filename)
    data = pd.DataFrame(data)
    data.to_csv(open(filename, "w"), header=False, index=False, sep=",")

# -----------------------------------------------------------------------------


def read_file(filename):
    filename = fix_filename(filename)
    return pd.read_csv(open(filename, "r")).values


# -----------------------------------------------------------------------------


def fix_filename(filename):
    has_folder = os.path.split(filename)[0] is not ""
    if not has_folder:
        folder = get_default_folder()
        filename = os.path.join(folder, filename)
    return filename

# -----------------------------------------------------------------------------


test_matrix = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Z', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'C', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
]

# -----------------------------------------------------------------------------


if __name__ == '__main__':

    test_filename = get_default_filename()
    save_file(test_filename, test_matrix)
    test_matrix = read_file(test_filename)
    print(test_matrix)

    for i in range(0, 1000):
        print(get_step_filename(i))

# -----------------------------------------------------------------------------
