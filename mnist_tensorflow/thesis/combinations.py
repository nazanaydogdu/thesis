# from itertools import combinations
from itertools import permutations


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


# print(list(combinations("win", 1)))
fragmentize_words("win")
