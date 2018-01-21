import tensorflow as tf
import os

import numpy as np
from sklearn.neural_network import BernoulliRBM

np.set_printoptions(edgeitems=352, threshold=351648)
bigrams = {}
words = {}
splitted_bigrams = {}
count = 0
encounters = {}

def readFile(filename):
    data = open(filename, 'r').read() # should be simple plain text file
    chars = list(set(data))
    chars.remove('\n')
    data_size, char_size = len(data), len(chars)
    print('data has %d characters, %d unique.' % (data_size, char_size))
    return chars


chars = readFile('onehotmapping/rass2007.txt')
char_to_ix = {ch: i for i, ch in enumerate(chars)}
ix_to_char = {i: ch for i, ch in enumerate(chars)}

matrix = np.array(np.zeros((len(words), 260))).reshape(999, 260)
row_names = [_ for _ in sorted(words.values())]
#col_names = [_ for _ in sorted(encounters)]

df = pd.DataFrame(matrix, index=row_names)

for row in df.index:
    row_list = row.split("  --  ")[1].split(",")
    for rows in row_list:
        rows = rows.replace("[", "").replace("]", "").replace(" ", "")
        rows = rows[1:-1]
        for col in df.columns:
            if rows == col:
                df.set_value(row, col, 1)

df.to_csv('one_hot.csv', index=True, header=True, sep=' ')

output_file = open("one_hot.txt", 'w')
output_file.write(str(matrix))
output_file.close()
