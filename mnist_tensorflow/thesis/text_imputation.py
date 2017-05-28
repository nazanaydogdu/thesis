#!/usr/bin/env python

import random
from collections import Counter
from optparse import OptionParser


def create_vocab(vocab_list, size, filename):
    """ Creates a vocabulary that is at max size 'size' using the words
    that were collected while created a training dataset.  We keep top
    'size' most frequent words and replace all other words with a unique
    token 'UUUNKKK'. """

    print("Creating vocabulary file")
    counts = Counter(vocab_list)
    to_keep = dict(counts.most_common(size))
    uuunkkk_count = len(vocab_list) - sum(to_keep.values())
    total_words = len(vocab_list)
    vocab_file = open(filename, 'w')
    vocab_file.write('%s\t%.9f\n' % (str('UUUNKKK'), float(uuunkkk_count) / float(total_words)))
    for word in to_keep.keys():
        vocab_file.write('%s\t%.9f\n' % (str(word), float(to_keep[word]) / float(total_words)))
    vocab_file.close()
    # Return final vocab list
    final_vocab = set()
    final_vocab = final_vocab.union(set(to_keep.keys()))
    final_vocab.add('UUUNKKK')
    return final_vocab


def create_training(dataset_size, vocab_size, max_sentence_size, min_sentence_size=3):
    """ Creates a training dataset that is 80 percent of the total dataset_size.
    Only sentences that have at least 'min_sentence_size' words and at max
    'max_sentence_size' words will be kept. """

    print("Creating training dataset, (80 percent of the datatset), with maximum")
    print("sentence size: %d and minimum sentence size: %d and maximum dataset size: %d" % (
        min_sentence_size, max_sentence_size, dataset_size))
    output_filename = 'training_total_' + str(dataset_size) + '_max_' + str(max_sentence_size) \
                      + '_min_' + str(min_sentence_size) + '.txt'
    output_file = open(output_filename, 'w')
    input_file = open('train_v2.txt', 'r')
    vocab = []
    max_lines = 0.80 * dataset_size
    last_line_read = 0
    while max_lines > 0:
        line = input_file.readline().strip().lower()
        last_line_read += 1
        # Check sentence size
        sentence_size = len(line.split())
        if (sentence_size >= min_sentence_size) and (sentence_size <= max_sentence_size):
            # Add the words to the vocabulary
            for word in line.split():
                vocab.append(word)
            # Add the line to the output file
            output_file.write('%s\n' % line)
            max_lines -= 1
    output_file.close()
    input_file.close()
    # Create the vocabulary file
    vocab_filename = 'vocab_total_' + str(dataset_size) + '_max_' \
                     + str(max_sentence_size) + '_min_' + str(min_sentence_size) + '.txt'
    final_vocab = create_vocab(vocab, vocab_size, vocab_filename)
    return final_vocab, last_line_read


def create_dev_or_test(
        vocab, last_line_read, dataset_size, max_sentence_size,
        min_sentence_size=0, is_dev=True):
    """ Creates a development or test dataset that is 10 percent of the total dataset_size.
    Only sentences that have at least 'min_sentence_size' words and at max
    'max_sentence_size' words will be kept. """

    if is_dev:
        print("Creating dev dataset, (10 percent of the datatset), with maximum")
        print("sentence size: %d and minimum sentence size: %d and maximum dataset size: %d" % (
            min_sentence_size, max_sentence_size, dataset_size))
        output_filename = 'dev_total_' + str(dataset_size) + '_max_' \
                          + str(max_sentence_size) + '_min_' + str(min_sentence_size) + '.txt'
        gold_output_filename = 'dev_total_' + str(dataset_size) + '_max_' \
                               + str(max_sentence_size) + '_min_' + str(min_sentence_size) + '_gold.txt'
    else:
        print("Creating test dataset, (10 percent of the datatset), with maximum")
        print("sentence size: %d and minimum sentence size: %d and maximum dataset size: %d" % (
            min_sentence_size, max_sentence_size, dataset_size))
        output_filename = 'test_total_' + str(dataset_size) + '_max_' \
                          + str(max_sentence_size) + '_min_' + str(min_sentence_size) + '.txt'
        gold_output_filename = 'test_total_' + str(dataset_size) + '_max_' \
                               + str(max_sentence_size) + '_min_' + str(min_sentence_size) + '_gold.txt'

    output_file = open(output_filename, 'w')
    gold_output_file = open(gold_output_filename, 'w')
    input_file = open('train_v2.txt', 'r')
    # Read file until last_line read to avoid reading same lines as training (or dev) set
    lines_read = 0
    while lines_read < last_line_read:
        line = input_file.readline()
        lines_read += 1
    max_lines = 0.10 * dataset_size
    while max_lines > 0:
        line = input_file.readline().strip().lower()
        last_line_read += 1
        # Check sentence size
        sentence_size = len(line.split())
        if (sentence_size >= min_sentence_size) and (sentence_size <= max_sentence_size):
            # Remove a random word
            words = line.split()
            index = random.randint(1, len(words) - 2)
            popped_word = words[index]
            if popped_word not in vocab:
                words[index] = 'UUUNKKK'
            # Add the actual sentence to the gold file
            gold_output_file.write('%s\n' % (" ".join(words)))
            words.pop(index)
            # Add sentence with word popped to file
            output_file.write('%s\n' % (" ".join(words)))
            max_lines -= 1
    output_file.close()
    gold_output_file.close()
    input_file.close()
    return last_line_read


def get_options():
    """ Get command-line options. """
    parser = OptionParser()
    parser.add_option('-b', '--maxSentenceSize', type='int', dest='max_sentence_size',
                      help='maximum number of words in the sentence to be kept in the dataset', default='100')
    parser.add_option('-s', '--minSentenceSize', type='int', dest='min_sentence_size',
                      help='minimum number of words in the sentence to be kept in the dataset', default='3')
    parser.add_option('-d', '--datasetSize', type='int', dest='dataset_size',
                      help='number of sentences to keep in the datasets', default='1000000')
    parser.add_option('-v', '--vocabSize', type='int', dest='vocab_size',
                      help='number of words to keep in the vocabulary')
    options, _ = parser.parse_args()
    return options


def main():
    options = get_options()
    print('Running with options:', options)
    vocab, last_line_read = create_training(options.dataset_size, options.vocab_size, options.max_sentence_size,
                                            options.min_sentence_size)
    last_line_read = create_dev_or_test(vocab, last_line_read, options.dataset_size, options.max_sentence_size,
                                        options.min_sentence_size, True)
    create_dev_or_test(vocab, last_line_read, options.dataset_size, options.max_sentence_size,
                       options.min_sentence_size, False)


if __name__ == '__main__':
    main()
