import csv
import glob
import os
import re
import sys


DEPTH_PATTERN = '/*/*/*'
DICT_INDEX_CLASS = {
    0: 'positive',
    1: 'negative',
    2: 'truthful',
    3: 'deceptive',
}
# each group can only contain two class index
CLASS_GROUPING = [(2, 3), (0, 1)]
dict_class_file_probability = {}
dict_word_probability = {}
STRING_FORMATTING_PATTERN = "-+|\.+|,|/|'m|'d|'re|'ve"


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


def populate_entries(input_location='nbmodel.txt'):
    global dict_class_file_probability, dict_word_probability
    file_obj = open(input_location, 'r')
    csv_reader = csv.reader(file_obj, delimiter=',')

    count = 0
    for row in csv_reader:
        count += 1
        if count > 4:
            break
        dict_class_file_probability[int(row[0])] = float(row[1])

    for row in csv_reader:
        dict_word_probability[row[0]] = [float(row[i]) for i in xrange(1, 5)]


    file_obj.close()


def process_line(line):
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


def get_class_name(file_path):
    global dict_class_file_probability, dict_word_probability, DICT_INDEX_CLASS
    file_obj = open(file_path, 'r')

    # initialise priors here, value at index i represents probability of class DICT_INDEX[i]
    probability_value_list = [0] * len(dict_class_file_probability)
    for index, value in dict_class_file_probability.iteritems():
        probability_value_list[index] = value

    word_list = []
    for line in file_obj:
        word_list.extend(process_line(line.strip()))

    file_obj.close()

    for word in word_list:
        if word in dict_word_probability:
            word_probability_list = dict_word_probability[word]
            for index, value in enumerate(word_probability_list):
                # if value is not present for a class, we are ignoring it
                if value != 0:
                    probability_value_list[index] += value

    class_name_list = []
    for group in CLASS_GROUPING:
        max_class_index = 0
        max_probability = -1 * sys.maxint
        for class_id in group:
            if probability_value_list[class_id] == 0:
                continue

            if probability_value_list[class_id] > max_probability:
                max_probability = probability_value_list[class_id]
                max_class_index = class_id

        class_name_list.append(DICT_INDEX_CLASS[max_class_index])

    return class_name_list


def process_directory(directory_path, out_file_location='nboutput.txt'):
    global DEPTH_PATTERN

    out_file = open(out_file_location, 'w')

    test_directories_pattern = '%s%s' % (directory_path, DEPTH_PATTERN)
    test_directories = glob.glob(test_directories_pattern)

    for directory in test_directories:
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            class_name_list = get_class_name(file_path)
            class_names = ' '.join(class_name_list)
            out_file.write('%s %s\n' % (class_names, file_path))

    out_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python nbclassify.py <path>'
        sys.exit(1)

    populate_entries()
    process_directory(sys.argv[1])
