##import tensorflow as tf
import os
from itertools import permutations
from string import ascii_lowercase

import numpy as np
import pandas as pd

np.set_printoptions(edgeitems=352, threshold=351648)
bigrams = {}
splitted_bigrams = {}
count = 0
encounters = {}
alpha_labels = dict()
words = []


def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    for indices in permutations(range(n), r):
        if sorted(indices) == list(indices):
            fragment = []
            for i in range(n):
                fragment.append('_')
            for j in indices:
                fragment[j] = pool[j]
            yield list(fragment)


def fragmentize_words(word):
    fragments = []
    for index in range(len(word) + 1):
        fragments = list(combinations(word, index))
        for syll in fragments:
            # print(syll)
            print(''.join(syll))

    fragments.append('')
    fragments.append('win')


def generate_colnames(length):
    for index in range(length):
        for c in sorted(ascii_lowercase):
            alpha_labels[c + "_" + str(index)] = 0
            # if word[index] == c:
            #   alpha_labels[c + str(index)] = 1
    return alpha_labels


def maybe_download(filename, expected_bytes):
    """make sure it's the right size."""
    statinfo = os.stat(filename)
    if statinfo.st_size == expected_bytes:
        print('Found and verified', filename)
        max_col_length = 0
        for line in open(filename):
            if len(line) > max_col_length:
                max_col_length = len(line)
            line = line.rstrip()
            words.append(line)
    else:
        print(statinfo.st_size)
        raise Exception(
            'Failed to verify ' + filename + '. Can you get to it with a browser?')

    generate_colnames(max_col_length)
    return filename


filename = maybe_download('1-1000.txt', 5835)

"""data = open('1-1000.txt', 'r').readlines()"""
data = open('1-1000.txt', 'r').read()  # should be simple plain text file"""
chars = list(set(data))
data_size, vocab_size = len(data), len(chars)
print('data has %d characters, %d unique.' % (data_size, vocab_size))
char_to_ix = {ch: i for i, ch in enumerate(chars)}
ix_to_char = {i: ch for i, ch in enumerate(chars)}

matrix = np.array(np.zeros((len(words), len(alpha_labels)))).reshape(len(words), len(alpha_labels))
row_names = [_ for _ in sorted(words)]
col_names = [_ for _ in sorted(alpha_labels.keys())]

df = pd.DataFrame(matrix, index=row_names, columns=col_names)

for row in df.index:
    for index in range(len(row)):
        for col in df.columns:
            letter = col.split("_")[0]
            letter_index = col.split("_")[1]
            if row[index] == letter and str(index) == letter_index:
                df.set_value(row, col, 1)

df.to_csv('fragment_vectors.csv', index=True, header=True, sep=' ')

output_file = open("fragment_vectors.txt", 'w')
output_file.write(str(matrix))
output_file.close()
