import csv
import sys
import math
import codecs

MODEL_FILE = 'hmmmodel.txt'
OUTPUT_FILE = 'hmmoutput.txt'
dict_transition = {}
dict_emission = {}
tag_set = set()

def read_model_parameters():
    """Reads the model file and updates the transition and emission dictionaries.

    transition dictionary - {start_tag: {to_tag1: probability, to_tag2: probability...}
    emission_dictionary - {word: {tag1: probability, tag2: probability.. }
    """
    global MODEL_FILE, dict_transition, dict_emission

    file = codecs.open(MODEL_FILE, 'r', encoding='utf-8')

    line = file.readline()
    line = line.strip()
    while line != '\x01emission\x01end\x01':
        row = line.strip().split('\x01')
        if row[0] in dict_emission:
            dict_emission[row[0]][row[1]] = math.log(float(row[2])) # handling floating point underflow case
        else:
            dict_emission[row[0]] = {row[1]: math.log(float(row[2]))}

        line = file.readline()
        line = line.strip()

    for line in file:
        row = line.strip().split('\x01')
        tag_set.add(row[0])
        if row[0] in dict_transition:
            dict_transition[row[0]][row[1]] = math.log(float(row[2]))
        else:
            dict_transition[row[0]] = {row[1]: math.log(float(row[2]))}



def process_token(word, prev_state_dict, state_source_list):
    """For each word, returns a dictionary of tags and associated probabilities.

    If word is present in training data, all the tags which have transition defined from previous states are considered
    as next states with emission probability set as 1.
    If word is present in training data, and there is no transition defined from previous state to possible tags to word,
    then the default value present in 'others' is considered as transition probability.
    """

    global dict_emission, dict_transition, tag_set
    word_tag_dict = {}
    if word not in dict_emission: # unknown word case
        for tag in tag_set:
            if tag != 'others':
                word_tag_dict[tag] = 0.0 # log value of probability as 0

    else: # word present in dict_emission
        word_tag_dict = dict_emission[word]

    # now the main calculation starts
    dict_word_probability = {}  # contains each possible tag for the word with associated probabilities
    dict_state_source = {}  # source of a given tag, that is which tag of previous state is source of current tag
    for prev_tag, prev_probability in prev_state_dict.iteritems():
        for tag, emission_probability in word_tag_dict.iteritems():
            if tag in dict_transition[prev_tag]:
                transition_probability = dict_transition[prev_tag][tag]
            else:
                transition_probability = dict_transition[prev_tag]['others']

            state_probability = prev_probability + emission_probability + transition_probability

            if tag not in dict_word_probability or state_probability > dict_word_probability[tag]:
                dict_word_probability[tag] = state_probability
                dict_state_source[tag] = prev_tag

    state_source_list.append(dict_state_source)
    return dict_word_probability


def process_line(line):
    """Process each line and return the POS tagged version of the line.

    Implements Viterbi algorithm using backtracking to find out the the best sequence of POS tags for the given line.
    """
    state_source_list = []
    tokens = line.split()
    # this probability here is actually 1, but as we are using addition while calculating probabilities, so setting the
    # value as log(1) = 0.0
    state_probability_list = {'start': 0.0}

    for word in tokens:
        probability_list = process_token(word, state_probability_list, state_source_list)
        state_probability_list = probability_list

    tag_list = []
    max_value, best_tag = -1*sys.maxint, None

    for key, value in state_probability_list.iteritems():
        if value > max_value:
            max_value = value
            best_tag = key

    tag_list.append(best_tag)
    prev_tag = best_tag
    for index in xrange(len(state_source_list)-1, 0, -1):
        tag = state_source_list[index][prev_tag]
        tag_list.append(tag)
        prev_tag = tag

    tag_list.reverse()
    out_tokens = []
    for index, word in enumerate(tokens):
        out_tokens.append('%s/%s' % (word, tag_list[index]))

    out_line = ' '.join(out_tokens)
    return out_line


def process_file(file_path):
    """Processes the input file.

    For each line calls the process_line function (which returns the tagged line) and writes the returned value in
    output file.
    """
    global OUTPUT_FILE
    file = codecs.open(file_path, 'r', encoding='utf-8')

    out_file = codecs.open(OUTPUT_FILE, 'w', encoding='utf-8')

    for line in file:
        line = line.strip()
        out_line = process_line(line)
        out_file.write('%s\n' % out_line)

    out_file.close()


if __name__ == '__main__':
    file_path = sys.argv[1]
    read_model_parameters()
    process_file(file_path)
