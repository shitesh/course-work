import codecs
import os
import sys
import math


def increment_dict(input_dict, key):
    if key in input_dict:
        input_dict[key] += 1
    else:
        input_dict[key] = 1


def get_n_grams(sentence, n=1):
    temp_dict = {}
    for index in xrange(0, len(sentence)-n+1):
        n_gram = tuple(sentence[index: index+n])
        increment_dict(temp_dict, n_gram)

    return temp_dict


def update_dict(dict1, dict2):
    for key, value in dict2.iteritems():
        if key not in dict1:
            dict1[key] = value
        else:
            dict1[key] = max(value, dict1[key])


def get_brevity_panelty(candidate_text, reference_text):
    candidate_len = 0
    reference_len = 0

    for index, candidate in enumerate(candidate_text):
        candidate_len += len(candidate)
        current_reference_len = 0
        min_len_difference = sys.maxint

        for reference in reference_text:
            if abs(len(reference[index])-len(candidate)) < min_len_difference:
                min_len_difference = len(reference[index])-len(candidate)
                current_reference_len = len(reference[index])

        reference_len += current_reference_len

    penalty = min(1.0, math.exp(1.0 - float(reference_len)/candidate_len))

    return penalty


def compute_blue_score(candidate_text, reference_text):
    numerical_part = 0

    for n_gram_index in xrange(1, 5):
        numerator_val = 0
        denominator_val = 0

        for index, candidate in enumerate(candidate_text):
            reference_n_gram_dict = {}

            for reference in reference_text:
                update_dict(reference_n_gram_dict, get_n_grams(reference[index], n_gram_index))

            candidate_n_gram_dict = get_n_grams(candidate, n_gram_index)

            for key, value in candidate_n_gram_dict.iteritems():
                if key in reference_n_gram_dict:
                    numerator_val += min(value, reference_n_gram_dict[key])

            denominator_val += len(candidate) - n_gram_index + 1

        numerical_part += math.log(numerator_val) - math.log(denominator_val)

    brevity_penalty = get_brevity_panelty(candidate_text, reference_text)
    bleu_score = brevity_penalty * math.exp(numerical_part/4)

    return bleu_score


def process_file(file_path):
    file = codecs.open(file_path, 'r', encoding='utf-8')

    all_text = []
    for line in file:
        words = line.strip().split()
        all_text.append(words)

    return all_text

def process_directory(directory_path):
    reference_text = list()
    for file_name in os.listdir(directory_path):
        file_text = process_file(os.path.join(directory_path, file_name))
        reference_text.append(file_text)

    return reference_text


if __name__ == '__main__':
    candidate_file = sys.argv[1]
    if os.path.isdir(sys.argv[2]):
        reference_text = process_directory(sys.argv[2])
    else:
        reference_text = list()
        reference_text.append(process_file(sys.argv[2]))

    candidate_text = process_file(sys.argv[1])
    bleu_score = compute_blue_score(candidate_text, reference_text)
    out_file = open('bleu_out.txt', 'w')
    out_file.write('%s' % bleu_score)
    out_file.close()
