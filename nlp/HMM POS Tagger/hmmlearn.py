# Reads an input file and generate transition probabilities for different tags and emission probabilities for words
import sys
import csv

OUTPUT_FILE_LOCATION = 'hmmmodel.txt'
dict_transition = {}
dict_emission = {}
tag_set = set()


def update_emission_count(word, tag):
    """ Updates the emission count dictionary.

    The dictionary contains data in the form {'word' : {'tag1': count, 'tag2': count , 'total_count': total number of times word has occured}}
    """

    global dict_emission, tag_set

    tag_set.add(tag)
    if word in dict_emission:
        if tag in dict_emission[word]:
            dict_emission[word][tag] += 1
        else:
            dict_emission[word][tag] = 1
        dict_emission[word]['total_count'] += 1
    else:
        dict_emission[word] = {tag: 1, 'total_count': 1}


def update_transition_count(start_tag, end_tag):
    """Updates the transition count dictionary.

    The dictionary stores data in the form {'start_tag': {'to_tag1': count, 'to_tag2': count, 'total_count': total number of times start_tag is present}}
    """
    global dict_transition
    if start_tag in dict_transition:
        if end_tag in dict_transition[start_tag]:
            dict_transition[start_tag][end_tag] += 1
        else:
            dict_transition[start_tag][end_tag] = 1
        dict_transition[start_tag]['total_count'] += 1
    else:
        dict_transition[start_tag] = {end_tag: 1, 'total_count': 1}


def calculate_probabilities():
    """Updates emission and transition dictionary to change value from count to probability.

    To handle add one smoothing in transition, a separate tag 'others' is created at each start tag level which contains
    the probability value of all the transitions not observed in training data.
    """

    global dict_emission, dict_transition, tag_set

    total_num_tags = len(tag_set)

    # calculate transition probabilities
    for key, value in dict_transition.iteritems():
        total_count = value['total_count']
        del value['total_count']

        for tag, count in value.iteritems():
            value[tag] = float(count+1)/(total_count+total_num_tags)

        value['others'] = 1.0/(total_count+total_num_tags)

    # todo: do we really need these
    for tag in tag_set:
        if tag not in dict_transition:
            dict_transition[tag] = {'others': 1.0/total_num_tags}

    # calculate emission probabilities
    for key, value in dict_emission.iteritems():
        total_word_count = value['total_count']
        del value['total_count']

        for tag, count in value.iteritems():
            value[tag] = float(count)/total_word_count


def write_file():
    """Writes the transition and emission probabilities to a file so that it can be used in next step.

    """
    global dict_emission, dict_transition, OUTPUT_FILE_LOCATION
    out_file = open(OUTPUT_FILE_LOCATION, 'w')
    csv_writer = csv.writer(out_file, delimiter=',')

    for word, tag_dict in dict_emission.iteritems():
        for tag, probability in tag_dict.iteritems():
            csv_writer.writerow([word, tag, probability])

    csv_writer.writerow(['<emission_end>'])
    for start_tag, transition_dict in dict_transition.iteritems():
        for tag, probability in transition_dict.iteritems():
            csv_writer.writerow([start_tag, tag, probability])

    out_file.close()


def process_file(input_path):
    file = open(input_path, 'r')

    for line in file:
        line = line.strip()
        tokens = line.split()
        prev_tag = 'start'
        for token in tokens:
            word, tag = token.rsplit('/', 1)
            update_emission_count(word, tag)
            update_transition_count(prev_tag, tag)
            prev_tag = tag


if __name__ == '__main__':
    input_path = sys.argv[1]
    process_file(input_path)
    calculate_probabilities()
    write_file()