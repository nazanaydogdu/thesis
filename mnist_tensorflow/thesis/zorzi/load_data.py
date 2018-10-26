import np_utils as np_utils

from itertools import permutations
import numpy as np


def load_data():
    raw_text = 'ABCDEF'
    raw_input = []
    alphabet = []

    for x in list(permutations(raw_text, 3)):
        raw_input.append("".join(x))  # 120 words like ABC ABD ABF

    for letter in range(65, 91):
        alphabet.append(chr(letter))

    matrix = np.array(np.zeros((3, len(alphabet))), dtype=int)

    for word in raw_input:
        matrix_new = np.array(np.zeros((3, len(alphabet))), dtype=int)
        for i in range(3):
            matrix_new[i, ord(word[i]) - 65] = 1;
        final_matrix = np.concatenate((matrix, matrix_new), axis=1)
        matrix = final_matrix;

    matrix = np.delete(matrix, np.s_[0:26], axis=1)
    np.savetxt("rawdata.csv", matrix, fmt="%d", delimiter=",")
    return matrix

print(load_data())