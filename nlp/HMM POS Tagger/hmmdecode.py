import csv
import sys

MODEL_FILE = 'hmmmodel.txt'
OUTPUT_FILE = 'hmmoutput.txt'
dict_transition = {}
dict_emission = {}

def read_model_parameters():
    """Reads the model file and updates the transition and emission dictionaries.

    transition dictionary - {start_tag: {to_tag1: probability, to_tag2: probability...}
    emission_dictionary - {word: {tag1: probability, tag2: probability.. }
    """
    global MODEL_FILE, dict_transition, dict_emission

    file = open(MODEL_FILE, 'r')
    csv_reader = csv.reader(file, delimiter=',')

    row = csv_reader.next()
    while row[0] != '<emission_end>':# TODO: rethink if this is good identifier or something else should be taken
        if row[0] in dict_emission:
            dict_emission[row[0]][row[1]] = float(row[2])
        else:
            dict_emission[row[0]] = {row[1]: float(row[2])}

        row = csv_reader.next()

    row = csv_reader.next()
    while row:
        if row[0] in dict_transition:
            dict_transition[row[0]][row[1]] = float(row[2])
        else:
            dict_transition[row[0]] = {row[1]: float(row[2])}
        row = csv_reader.next()


def process_line(line):
    tokens = line.split()
    prev_tag = 'start'

    # TODO: implement the main logic here


    out_line = None
    return out_line


def process_file(file_path):
    """Processes the input file.

    For each line calls the process_line function (which returns the tagged line) and writes the returned value in
    output file.
    """
    global OUTPUT_FILE
    file = open(file_path, 'r')

    out_file = open(OUTPUT_FILE, 'w')

    for line in file:
        line = line.strip()
        out_line = process_line(line)
        out_file.write('%s\n' % out_line)

    out_file.close()


if __name__ == '__main__':
    file_path = sys.argv[1]
    read_model_parameters()
    process_file(file_path)