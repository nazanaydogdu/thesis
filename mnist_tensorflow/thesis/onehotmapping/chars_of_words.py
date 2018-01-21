##import tensorflow as tf
import os

import numpy as np
import pandas as pd

np.set_printoptions(edgeitems=352, threshold=351648)
bigrams = {}
splitted_chars = {}
count = 0
encounters = {}


def extract_chars(word):
    bigram_list = []
    for char in word:
        bigram_list.append(char)
        ##if tmp != "#":
        if str(char) in encounters:
            encounters[char] += 1
        else:
            encounters[char] = 1
    bigrams[word] = bigram_list
    return bigram_list


def read_file(filename, expected_bytes):
    """make sure it's the right size."""
    statinfo = os.stat(filename)
    if statinfo.st_size == expected_bytes:
        print('Found and verified', filename)
        count = 0
        for line in open(filename):
            count += 1
            new_line = ""
            line = line.rstrip()
            new_line += line + " "
            new_line += str(extract_chars(line)) + " "
    else:
        print(statinfo.st_size)
        raise Exception(
            'Failed to verify ' + filename + '. Can you get to it with a browser?')
    return filename


filename = read_file('rass2007.txt', 4796)

# Write bigrams to output file:
output_file = open("chars.txt", 'w')

for bigram in bigrams:
    splitted_bigram = bigrams[bigram]
    splitted_chars[bigram] = bigram
    output_file.write(
        bigram + " " + "#" + bigram + "#" + " " + str(splitted_bigram) + " " + str(len(splitted_bigram)) + "\n")
    count += len(splitted_bigram)
output_file.write(str(count))
output_file.close()

output_file = open("char_encounters.txt", 'w')

for bigram in encounters:
    encounter_no = encounters[bigram]
    output_file.write(bigram + " " + str(encounter_no) + "\n")
output_file.close()

alphabet = []
for index in range(1, 11):
    for letter in range(65, 91):
        alphabet.append(chr(letter) + str(index))

matrix = np.array(np.zeros((len(splitted_chars.values()), len(alphabet)))).reshape(596, 260)
row_names = [_ for _ in sorted(splitted_chars.values())]
col_names = [_ for _ in alphabet]

df = pd.DataFrame(matrix, index=row_names, columns=col_names)

for row in df.index:
    row_list = list(row)
    row_index = 1;
    for rows in row_list:
        df.set_value(row, rows + str(row_index), 1)
        row_index +=1

df.to_csv('char_df.csv', index=True, header=True, sep=' ')

output_file = open("char_matrix.txt", 'w')
output_file.write(str(matrix))
output_file.close()
