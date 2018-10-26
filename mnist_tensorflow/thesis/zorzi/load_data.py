import np_utils as np_utils

from itertools import permutations
import numpy as np
import pandas as pd

raw_text = 'ABCDEF'
raw_input = []
enum_input = []


chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
for x in list(permutations(raw_text, 3)):
    raw_input.append("".join(x)) #120 words like ABC ABD ABF
    '''enum_input.append([char_to_int[char] for char in "".join(x)])'''

'''np.savetxt("rawvocab.csv", raw_input, fmt="%s", delimiter=",")'''


n_chars = len(raw_text)
'''enum_input = enum_input / float(n_chars)
X = np_utils.to_categorical(enum_input)'''

alphabet = []
for letter in range(65, 91):
    alphabet.append(chr(letter))

matrix = np.array(np.zeros((3, len(alphabet))), dtype=int)
row_names = [_ for _ in sorted(range(3))]
col_names = [_ for _ in alphabet]

df = pd.DataFrame(matrix, index=row_names, columns=col_names)

for word in raw_input:
    #dfTemp = df.copy();
    matrix_new = np.array(np.zeros((3, len(alphabet))), dtype=int)
    for i in range(3):
        #dfTemp.set_value(i, word[i], 1)
        matrix_new[i, ord(word[i])-65] = 1;
        #df.set_value(i, word[i], 1)
    #pd.concat([df, dfTemp], axis=1)
    #pd.concat([df, df], axis=1)
    final_matrix = np.concatenate((matrix, matrix_new), axis=1)
    matrix = final_matrix;
matrix = np.delete(matrix, np.s_[0:26], axis=1)
np.savetxt("rawdata.csv", matrix, fmt="%d", delimiter=",")



print()

