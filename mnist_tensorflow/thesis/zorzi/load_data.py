from itertools import permutations
import numpy as np


def load_data():
    raw_text = 'ABCDEF'
    raw_input = []
    alphabet = []
    letter_size = 3

    for x in list(permutations(raw_text, 3)):
        raw_input.append("".join(x))  # 120 words like ABC ABD ABF

    for letter in range(65, 91):
        alphabet.append(chr(letter))

    matrix = np.array(np.zeros((letter_size, len(alphabet))), dtype=int)
    input_data = np.array(np.zeros((1, letter_size*len(alphabet))), dtype=int)
    targets = np.array(np.zeros((1, len(raw_input))), dtype=int)

    for word in raw_input:
        matrix_new = np.array(np.zeros((letter_size, len(alphabet))), dtype=int)
        for i in range(letter_size):
            matrix_new[i, ord(word[i]) - 65] = 1
        final_flat_matrix = np.concatenate((input_data, np.ravel(matrix_new).reshape(1,letter_size*len(alphabet))), axis=0)
        input_data = final_flat_matrix
        final_matrix = np.concatenate((matrix, matrix_new), axis=1)
        matrix = final_matrix

    for i in range(len(raw_input)):
        target = np.array(np.zeros((1, len(raw_input))), dtype=int)
        target[0, i] = 1
        final_targets = np.concatenate((targets, target), axis=0)
        targets = final_targets

    input_data = np.delete(input_data, (0), axis=0)
    targets = np.delete(targets, (0), axis=0)
    matrix = np.delete(matrix, np.s_[0:len(alphabet)], axis=1)

    return input_data, targets