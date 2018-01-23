##import tensorflow as tf
import os

import numpy as np
import pandas as pd
from itertools import chain, combinations
import csv

np.set_printoptions(edgeitems=352, threshold=351648)
chars = {}
splitted_chars = {}
count = 0
encounters = {}


def extract_chars(word):
    char_list = []
    for char in word:
        char_list.append(char)
        ##if tmp != "#":
        if str(char) in encounters:
            encounters[char] += 1
        else:
            encounters[char] = 1
    chars[word] = char_list
    return char_list

my_list = pd.read_csv('test_words.csv', delimiter=',')

for i in my_list:
    extract_chars(i)


# Write chars to output file:
output_file = open("chars.txt", 'w')

for char in chars:
    splitted_char = chars[char]
    splitted_chars[char] = char
    output_file.write(
        char + " " + "#" + char + "#" + " " + str(splitted_char) + " " + str(len(splitted_char)) + "\n")
    count += len(splitted_char)
output_file.write(str(count))
output_file.close()

alphabet = []
for index in range(1, 11):
    for letter in range(65, 91):
        alphabet.append(chr(letter) + str(index))

matrix = np.array(np.zeros((len(splitted_chars.values()), len(alphabet)))).reshape(640, 260)
row_names = [_ for _ in sorted(splitted_chars.values())]
col_names = [_ for _ in alphabet]

df = pd.DataFrame(matrix, index=row_names, columns=col_names)

for row in df.index:
    row_list = list(row)
    row_index = 1;
    for rows in row_list:
        df.set_value(row, rows + str(row_index), 1)
        row_index +=1

df.to_csv('char_df.csv', index=True, header=True, sep=',')

output_file = open("char_matrix.txt", 'w')
output_file.write(str(matrix))
output_file.close()
