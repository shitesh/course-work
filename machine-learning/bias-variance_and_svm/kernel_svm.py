import pandas as pd
import numpy as np
from svm import *
from svmutil import *
import time


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


def linear_svm(train_df, train_target):
    print 'LINEAR KERNEL:\n'
    for index in xrange(-6, 3):
        print '\nC value: 4^(%s)' %(index)
        parameter = svm_parameter(['-c', pow(4, index), '-v', '3', '-q', '-t', 0])
        problem = svm_problem(train_target, train_df)
        start_time = time.time()
        accuracy = svm_train(problem, parameter)
        end_time = time.time()
        print 'Average Time Taken: %s sec' %((end_time-start_time)/3.0)

def polynomial_kernel(train_df, train_target):
    print 'POLYNOMIAL KERNEL:\n'

    best_accuracy = 0
    best_c_value = 0
    best_degree = 0

    for c_value in xrange(-3, 8):
        for degree in xrange(1, 4):
            print 'C value: 4^{%s} Degree: %s' %(c_value, degree)
            parameter = svm_parameter(['-c', pow(4, c_value), '-v', '3', '-d', degree, '-q', '-t', POLY])
            problem = svm_problem(train_target, train_df)
            start_time = time.time()
            accuracy = svm_train(problem, parameter)
            end_time = time.time()
            print 'Average Time Taken: %s sec\n' %((end_time-start_time)/3.0)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_c_value = pow(4, c_value)
                best_degree = degree

    return best_accuracy, best_c_value, best_degree


def rbf_kernel(train_df, train_target):
    print 'RBF KERNEL:\n'
    best_accuracy = 0
    best_c_value = 0
    best_gamma_val = 0

    for c_value in xrange(-3, 8):
        for index in xrange(-7, 0):
            gamma_val = pow(4, index)
            print 'C value: 4^{%s} Gamma: 4^{%s}' %(c_value, index)
            parameter = svm_parameter(['-c', pow(4, c_value), '-v', '3', '-g', gamma_val, '-q', '-t', RBF])
            problem = svm_problem(train_target, train_df)
            start_time = time.time()
            accuracy = svm_train(problem, parameter)
            end_time = time.time()
            print 'Average Time Taken: %s sec\n' %((end_time-start_time)/3.0)
            if accuracy >= best_accuracy:
                best_accuracy = accuracy
                best_c_value = pow(4, c_value)
                best_gamma_val = gamma_val

    return best_accuracy, best_c_value, best_gamma_val


def compare_poly_rbf(train_list, train_target, test_list, test_target):
    poly_best_accuracy, poly_c_value, best_degree = polynomial_kernel(train_list, train_target)
    print '***************************************************************'
    rbf_best_accuracy, rbf_c_value, best_gamma = rbf_kernel(train_list, train_target)
    print '***************************************************************\n\n'
    if poly_best_accuracy > rbf_best_accuracy:
        print 'BEST KERNEL: Polynomial Kernel'
        print 'C value: %s Degree: %s' %(poly_c_value, best_degree)
        parameter = svm_parameter(['-c', poly_c_value, '-d', best_degree, '-q', '-t', POLY])
        problem = svm_problem(train_target, train_list)
        model = svm_train(problem, parameter)
        labels, accuracy, p = svm_predict(test_target, test_list, model)
        print accuracy

    else:
        print 'BEST KERNEL: RBF\n'
        print 'C value: %s Gamma: %s\n' %(rbf_c_value, best_gamma)
        problem = svm_problem(train_target, train_list)
        parameter = svm_parameter(['-c', rbf_c_value, '-g', best_gamma, '-q', '-t', RBF])
        model = svm_train(problem, parameter)
        labels, accuracy, p = svm_predict(test_target, test_list, model)
        print 'Test Accuracy: %s' % accuracy[0]


def svm_main():
    train_df, train_target, test_df, test_target = get_data()
    train_list = preprocess_data(train_df)
    test_list = preprocess_data(test_df)
    linear_svm(train_list, train_target)
    print '***************************************************************'
    compare_poly_rbf(train_list, train_target, test_list, test_target)


if __name__=='__main__':
    svm_main()
