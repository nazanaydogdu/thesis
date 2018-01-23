from itertools import chain, combinations
import csv

finalCharList = []
words = {}


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)  # allows duplicate elements
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def augment(word):
    charList = list(word)
    finalCharList.append(''.join(charList))
    stuff = range(len(charList))
    for i, combo in enumerate(powerset(stuff)):
        if(len(combo) > 0):
            newCharList = charList.copy()
            for j in combo:
                newCharList[j] = '_'
            finalCharList.append(''.join(newCharList))
    return finalCharList


def read_file(filename):
    print('Found and verified', filename)
    for line in open(filename):
        line = line.rstrip()
        words[line] = line
        for i in augment(line):
            words[i] = i

    with open("test_words.csv", 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
        wr.writerow(finalCharList)


read_file('test.txt')