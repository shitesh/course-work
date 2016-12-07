import pandas as pd
import numpy as np
from svm import *
from svmutil import *


def get_data():
    train_df = pd.read_csv('data/phishing-train-features.txt', header=None, delimiter='\t')
    train_target = pd.read_csv('data/phishing-train-label.txt', header=None, delimiter='\t')
    test_df = pd.read_csv('data/phishing-test-features.txt', header=None, delimiter='\t')
    test_target = pd.read_csv('data/phishing-test-label.txt', header=None, delimiter='\t')

    train_target = train_target.transpose()[0]
    test_target = test_target.transpose()[0]

    return train_df, train_target, test_df, test_target


def preprocess_data(dataframe):
    index_numbers = [1, 6, 7, 13, 14, 25, 28]

    dict_mapping = {-1: [1, 0, 0], 0: [0, 1, 0], 1: [0, 0, 1]}

    dict_index = {}
    start_val = 30
    for col_num in index_numbers:
        dict_index[col_num] = [col_num]
        for index in xrange(2):
            dataframe[start_val] = 0
            dict_index[col_num].append(start_val)
            start_val += 1

    for col_index in index_numbers:
        for row_val in xrange(len(dataframe[col_index])):
            curr_val = dataframe[col_index][row_val]
            correct_value_list = dict_mapping[curr_val]

            for index, value in enumerate(dict_index[col_index]):
                dataframe[value][row_val] = correct_value_list[index]

    dataframe[dataframe == -1] = 0
    data_list = dataframe.values.tolist()
    return data_list


def run_best_kernel(rbf_c_value, best_gamma):
    train_df, train_target, test_df, test_target = get_data()
    train_list = preprocess_data(train_df)
    test_list = preprocess_data(test_df)

    problem = svm_problem(train_target, train_list)
    parameter = svm_parameter(['-c', rbf_c_value, '-g', best_gamma, '-q', '-t', RBF])
    model = svm_train(problem, parameter)
    labels, accuracy, p = svm_predict(test_target, test_list, model)
    print 'Test Accuracy: %s' % accuracy[0]


if __name__=='__main__':
    print 'Running RBF Kernel with C=16384 and gamma=0.25'
    run_best_kernel(16384, 0.25)
