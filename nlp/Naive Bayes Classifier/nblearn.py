import csv
import glob
import math
import os
import sys
import re

DEPTH_PATTERN = '/*/*/*'
dict_word_frequency = {}
dict_class_word_count = {}
dict_class_file_probability = {}
STRING_FORMATTING_PATTERN = "-+|\.+|,|/|'m|'d|'re|'ve"

# if more classes are there, just input here
DICT_CLASS_INDEX = {
    'positive': 0,
    'negative': 1,
    'truthful': 2,
    'deceptive': 3
}


STOP_WORD_LIST = ['a','about','above','across','after','afterwards','again','against','all','almost','alone','along','already',
             'also','although','always','am','among','amongst','amoungst','amount','an','and','another','any','anyhow','anyone','anything',
             'anyway','anywhere','are','around','as','at','back','be','became','because','become','becomes','becoming','been','before','beforehand',
             'behind','being','below','beside','besides','between','beyond','bill','both','bottom','but','by','call','can','cannot','cant','co','computer',
             'con','could','couldnt','cry','de','describe','detail','do','done','down','due','during','each','eg','eight','either','eleven','else',
             'elsewhere','empty','enough','etc','even','ever','every','everyone','everything','everywhere','except','few','fifteen','fify','fill','find',
             'fire','first','five','for','former','formerly','forty','found','four','from','front','full','further','get','give','go','had','has','hasnt',
             'have','he','hence','her','here','hereafter','hereby','herein','hereupon','hers','herse"','him','himse"','his','how','however','hundred','i',
             'ie','if','in','inc','indeed','interest','into','is','it','its','itse"','keep','last','latter','latterly','least','less','ltd','made','many',
             'may','me','meanwhile','might','mill','mine','more','moreover','most','mostly','move','much','must','my','myse"','name','namely','neither',
             'never','nevertheless','next','nine','no','nobody','none','noone','nor','not','nothing','now','nowhere','of','off','often','on','once','one',
             'only','onto','or','other','others','otherwise','our','ours','ourselves','out','over','own','part','per','perhaps','please','put','rather','re',
             'same','see','seem','seemed','seeming','seems','serious','several','she','should','show','side','since','sincere','six','sixty','so','some',
             'somehow','someone','something','sometime','sometimes','somewhere','still','such','system','take','ten','than','that','the','their','them',
             'themselves','then','thence','there','thereafter','thereby','therefore','therein','thereupon','these','they','thick','thin','third','this',
             'those','though','three','through','throughout','thru','thus','to','together','too','top','toward','towards','twelve','twenty','two','un',
             'under','until','up','upon','us','very','via','was','we','well','were','what','whatever','when','whence','whenever','where','whereafter',
             'whereas','whereby','wherein','whereupon','wherever','whether','which','while','whither','who','whoever','whole','whom','whose','why','will',
             'with','within','without','would','yet','you','your','yours','yourself','yourselves']


def calculate_probability():
    global dict_class_word_count, dict_word_frequency, dict_class_file_probability

    total_num_files = sum(dict_class_file_probability.values())
    for key, value in dict_class_file_probability.iteritems():
        probability = 0
        if value:
            probability = math.log(float(dict_class_file_probability[key]) / total_num_files)
        dict_class_file_probability[key] = probability

    total_word_count = len(dict_word_frequency)
    for word, class_frequency_list in dict_word_frequency.iteritems():
        probability_list = []
        for index, value in enumerate(class_frequency_list):
            probability = math.log(float(value+1)/(dict_class_word_count[index] + total_word_count))
            probability_list.append(probability)
        dict_word_frequency[word] = probability_list


def write_file(output_file='nbmodel.txt'):
    global dict_word_frequency, dict_class_file_probability

    file = open(output_file, 'w')
    csv_writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    # first write class level probabilities
    for key, value in dict_class_file_probability.iteritems():
        row = [key, value]
        csv_writer.writerow(row)

    for word, probability_list in dict_word_frequency.iteritems():
        row = [word]
        row.extend(probability_list)
        csv_writer.writerow(row)

    file.close()


def process_word(line):
    line = re.sub(STRING_FORMATTING_PATTERN, ' ', line)
    word_list = line.split(' ')
    word_list = [word.strip() for word in word_list]

    word_list = list(set(word_list) - set(STOP_WORD_LIST))

    final_list = []
    for word in word_list:
        if word.isdigit():
            continue
        word = word.replace("'s", '')
        word = re.sub('^[^a-zA-Z]+|[^a-zA-Z]+$', '', word)
        if word:
            final_list.append(word.lower())
    return final_list


def process_line(line, class_list):
    global dict_word_frequency, dict_class_word_count, dict_class_probability, DICT_CLASS_INDEX

    num_classes = len(DICT_CLASS_INDEX)
    word_list = process_word(line.strip())

    for word in word_list:
        # update word frequency for each class
        class_frequency_list = dict_word_frequency.setdefault(word, [0]*num_classes)
        for class_index in class_list:
            class_frequency_list[class_index] += 1
            if not class_index in dict_class_word_count:
                dict_class_word_count[class_index] = 0
            dict_class_word_count[class_index] += 1


def process_file(file_path, class_list):
    file_obj = open(file_path, 'r')
    for line in file_obj:
        process_line(line.strip(), class_list)

    file_obj.close()


def process_directory(input_directory_location):
    global dict_class_file_probability, DEPTH_PATTERN
    training_directories_pattern = '%s%s' %(input_directory_location, DEPTH_PATTERN)
    training_directories = glob.glob(training_directories_pattern)

    for directory in training_directories:
        class_list = []

        for key, index in DICT_CLASS_INDEX.iteritems():
            if key in directory:
                class_list.append(index)

        for file_name in os.listdir(directory):
            for class_index in class_list:
                dict_class_file_probability[class_index] += 1

            process_file(os.path.join(directory, file_name), class_list)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python nblearn.py <word>'
        sys.exit(1)

    for key, value in DICT_CLASS_INDEX.iteritems():
        dict_class_file_probability[value] = 0

    input_directory_location = sys.argv[1]
    process_directory(input_directory_location)
    write_file('frequency_count.txt')
    calculate_probability()
    write_file()
