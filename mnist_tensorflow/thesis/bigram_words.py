##import tensorflow as tf
import os

import numpy as np
import pandas as pd

np.set_printoptions(edgeitems=352, threshold=351648)
bigrams = {}
splitted_bigrams = {}
count = 0
encounters = {}


def extract_bigrams(word):
    bigram_list = []
    tmp = "#"
    for char in word:
        bigram_list.append(tmp + char)
        ##if tmp != "#":
        if str(tmp + char) in encounters:
            encounters[tmp + char] += 1
        else:
            encounters[tmp + char] = 1
        tmp = char
    bigram_list.append(tmp + "#")
    if str(tmp + "#") in encounters:
        encounters[tmp + "#"] += 1
    else:
        encounters[tmp + "#"] = 1
    bigrams[word] = bigram_list
    return bigram_list


def maybe_download(filename, expected_bytes):
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
            new_line += str(extract_bigrams(line)) + " "
    else:
        print(statinfo.st_size)
        raise Exception(
            'Failed to verify ' + filename + '. Can you get to it with a browser?')
    return filename


filename = maybe_download('1-1000.txt', 5835)

# Write bigrams to output file:
output_file = open("bigrams.txt", 'w')

for bigram in bigrams:
    splitted_bigram = bigrams[bigram]
    splitted_bigrams[bigram] = bigram + "  --  " + str(splitted_bigram)
    output_file.write(
        bigram + " " + "#" + bigram + "#" + " " + str(splitted_bigram) + " " + str(len(splitted_bigram)) + "\n")
    count += len(splitted_bigram)
output_file.write(str(count))
output_file.close()

output_file = open("encounters.txt", 'w')

for bigram in encounters:
    encounter_no = encounters[bigram]
    output_file.write(bigram + " " + str(encounter_no) + "\n")
output_file.close()

matrix = np.array(np.zeros((len(splitted_bigrams.values()), len(encounters)))).reshape(999, 352)
row_names = [_ for _ in sorted(splitted_bigrams.values())]
col_names = [_ for _ in sorted(encounters)]

df = pd.DataFrame(matrix, index=row_names, columns=col_names)

for row in df.index:
    row_list = row.split("  --  ")[1].split(",")
    for rows in row_list:
        rows = rows.replace("[", "").replace("]", "").replace(" ", "")
        rows = rows[1:-1]
        for col in df.columns:
            if rows == col:
                df.set_value(row, col, 1)

df.to_csv('df.csv', index=True, header=True, sep=' ')

output_file = open("matrix.txt", 'w')
output_file.write(str(matrix))
output_file.close()
