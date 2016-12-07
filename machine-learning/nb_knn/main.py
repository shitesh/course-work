import copy
import sys
import os
import pandas as pd
import scipy.stats
from knn import knn

current_path = os.path.dirname(sys.argv[0])
TRAIN_DATA = os.path.join(current_path, 'data/train.txt')
TEST_DATA = os.path.join(current_path, 'data/test.txt')


def read_file(file_location):
    column_names = ['id', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'target']
    df = pd.read_csv(file_location, header=None, index_col=0, names=column_names)
    return df


def initialise():
    train_df = read_file(TRAIN_DATA)
    test_df = read_file(TEST_DATA)

    return train_df, test_df


def calculate_accuracy(test_df, class_list, dict_prior, dict_std, dict_mean):
    num_rows = len(test_df)
    correct_results = 0
    for index, row in test_df.iterrows():

        #create prior values
        temp_prior = copy.deepcopy(dict_prior)
        for index2 in xrange(1, 10):
            feature_name = 'f%s' % index2
            for class_name in class_list:
                if row[feature_name] == 0 and dict_mean[(class_name, feature_name)] == 0 and dict_std[(class_name, feature_name)] == 0:
                    probab_value = 1
                else:
                    probab_value = scipy.stats.norm(dict_mean[(class_name, feature_name)], dict_std[(class_name, feature_name)]).pdf(row[feature_name])
                temp_prior[class_name] *= probab_value

        max_value = 0
        max_class = None
        for key, value in temp_prior.iteritems():
            if not max_class or value > max_value:
                max_value = value
                max_class = key

        if max_class == row['target']:
            correct_results += 1

    return float(correct_results)/num_rows


def naive_bayes(train_df, test_df):

    # calculate prior probabilities
    class_list = train_df['target'].unique()
    class_count = train_df['target'].value_counts()
    prob_dist = (class_count/class_count.sum())

    dict_prior = {}

    for class_name in class_list:
        dict_prior[class_name] = prob_dist[class_name]

    dict_mean = {}
    training_mean = train_df.groupby(['target']).mean()
    for index, row in training_mean.iterrows():
        for index2 in xrange(1, 10):
            dict_mean[(index, 'f%s' % index2)] = row['f%s' % index2]


    dict_std = {}
    training_std = train_df.groupby(['target']).std()
    for index, row in training_std.iterrows():
        for index2 in xrange(1, 10):
            dict_std[(index, 'f%s' % index2)] = row['f%s' % index2]

    # calculate accuracy of test data
    test_accuracy = calculate_accuracy(test_df, class_list, dict_prior, dict_std, dict_mean)
    train_accuracy = calculate_accuracy(train_df, class_list, dict_prior, dict_std, dict_mean)

    print 'TRAIN ACCURACY: %.4f' % (train_accuracy*100)
    print 'TEST ACCURACY: %.4f\n' % (test_accuracy*100)
    print '**************************************************************'

if __name__ == '__main__':
    train_df, test_df = initialise()
    print '\nNAIVE BAYES RESULTS (Accuracy in %) :\n'
    naive_bayes(train_df, test_df)
    knn(train_df, test_df)


