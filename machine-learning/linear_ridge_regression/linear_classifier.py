from numpy.linalg import pinv
import pandas as pd
import numpy as np
from utils import *
import operator
import itertools
import sys


def get_pearson_coeff():
    dict_pearson_coeff = {}

    print 'PEARSON CORRELATION: \n'
    for feature_name in feature_names[1:]:
        pearson_coeff = pearson(train_df[feature_name], train_target)
        print '\t%s : %.4f' % (feature_name, pearson_coeff)
        dict_pearson_coeff[feature_name] = abs(pearson_coeff)
    print '***************************************************************'

    return dict_pearson_coeff


def get_theta_values(train_df, train_target, lambda_val=0.0):
    theta_df = train_df.transpose()
    theta_df = theta_df.dot(train_df)
    if lambda_val:
        identity_matrix = np.identity(len(theta_df))
        identity_matrix *= lambda_val
        theta_df = theta_df + identity_matrix

    theta_df = pinv(theta_df)
    theta_df = theta_df.dot(train_df.transpose())
    theta_df = theta_df.dot(train_target)
    return theta_df


def linear_regression(train_df, train_target, test_df, test_target, print_res=True):
    theta_df = get_theta_values(train_df, train_target)
    y_train_predicted = theta_df.dot(train_df.transpose())
    y_test_predicted = theta_df.dot(test_df.transpose())

    if print_res:
        print '\nLINEAR REGRESSION (Mean Squared Error):\n'
        print '\tTraining: %.4f' % get_mean_error(train_target, y_train_predicted)
        print '\tTest: %.4f' % get_mean_error(test_target, y_test_predicted)
        print '***************************************************************'

    return get_mean_error(train_target, y_train_predicted), get_mean_error(test_target, y_test_predicted)


def ridge_regression():
    lambda_value_list = [0.01, 0.1, 1.0]
    print '\nRIDGE REGRESSION (Mean Squared Error):\n'

    for lambda_val in lambda_value_list:
        theta_df = get_theta_values(train_df, train_target, lambda_val)
        y_train_predicted = theta_df.dot(train_df.transpose())
        y_test_predicted = theta_df.dot(test_df.transpose())

        print 'Lambda value: %s' % lambda_val
        print '\t Training: %.4f' % get_mean_error(train_target, y_train_predicted)
        print '\t Test: %.4f\n' % get_mean_error(test_target, y_test_predicted)
    print '***************************************************************'


def find_avg_mse_k_fold(k_folds, lambda_val):
    mse_list = []
    for index, fold in enumerate(k_folds):
        test_fold = fold
        train_fold = pd.concat(k_folds[:index] + k_folds[index+1:])

        test_fold_target = test_fold['target'].tolist()
        train_fold_target = train_fold['target'].tolist()

        train_fold = train_fold.drop('target', axis=1)
        test_fold = test_fold.drop('target', axis=1)

        theta_df = get_theta_values(train_fold, train_fold_target, lambda_val)
        y_test_predicted = theta_df.dot(test_fold.transpose())
        mse_list.append(get_mean_error(test_fold_target, y_test_predicted))
    return sum(mse_list)/10.0


def find_optimum_lambda(start_value, end_value):
    k_folds = get_k_folds(train_df, train_target)
    optimum_lambda = None
    optimum_mse = sys.maxint


    print 'Ridge Regression with Cross-Validation\n'

    print 'Chosen Step Size: 0.01\n'
    print 'As the number of values processed is large, results for only a few lambda values will be displayed. The ' \
          'entire results are stored in a filed named "lambda_value_mse.csv" in the present directory.'
    print 'Starting processing now: '
    lambda_mse_list = []

    min_cross_validation_mse = (None, sys.maxint, None)

    for lambda_val in np.arange(start_value, end_value, 0.01):
        validation_mse_val = find_avg_mse_k_fold(k_folds, lambda_val)
        theta_df = get_theta_values(train_df, train_target, lambda_val)
        y_test_predicted = theta_df.dot(test_df.transpose())

        mean_error_test = get_mean_error(test_target, y_test_predicted)
        if lambda_val in [1.0001, 2.0001, 3.0001, 4.0001, 5.0001, 6.0001, 7.0001, 8.0001, 9.0001]:
            print '\t Lambda Value: %s \t Average cross validation MSE: %.4f \t Test MSE: %.4f' %(lambda_val, validation_mse_val, mean_error_test)

        if validation_mse_val < min_cross_validation_mse[1]:
            min_cross_validation_mse = (lambda_val, validation_mse_val, mean_error_test)
        lambda_mse_list.append((lambda_val, validation_mse_val, mean_error_test))

    print '\nThe optimum value of lambda based on lowest average cross validation MSE is:'
    print '\t Lambda Value: %s \t Average cross validation MSE : %.4f \t Test MSE: %.4f' % (min_cross_validation_mse[0], min_cross_validation_mse[1], min_cross_validation_mse[2])



    file = open('lambda_value_mse.csv', 'w')
    file.write('LAMBDA VALUE, CROSS VALIDATION ERROR, TEST MSE\n')
    for entry in lambda_mse_list:
        file.write('%s, %s, %s\n' % (entry[0], entry[1], entry[2]))
    file.close()
    print '\nSave complete. Please check the file for complete results.\n'
    print '***************************************************************'


def basic_correlation(dict_pearson_coeff):
    sorted_dict = sorted(dict_pearson_coeff.items(), key=operator.itemgetter(1), reverse=True)

    print '4 FEATURES WITH HIGHEST CORRELATION: %s' % (','.join(entry[0] for entry in sorted_dict[:4]))

    sliced_feature_names = [entry[0] for entry in sorted_dict[:4]]
    curr_train, curr_test = filter_dataframes(train_df, test_df, sliced_feature_names)
    linear_regression(curr_train, train_target, curr_test, test_target)


def selection_with_brute_force():
    combinations = list(itertools.combinations(feature_names[1:], 4))

    best_features = []
    best_test_mse = None
    min_train_mse = sys.maxint

    for entry in combinations:
        curr_train, curr_test = filter_dataframes(train_df, test_df, entry)
        train_mse, test_mse = linear_regression(curr_train, train_target, curr_test, test_target, False)

        if train_mse < min_train_mse:
            min_train_mse = train_mse
            best_features = entry
            best_test_mse = test_mse

    print 'SELECTION OF 4 FEATURES(BRUTE FORCE):\n'
    print '\tFeatures : %s' %(', '.join(best_features))
    print '\t TRAINING MSE: %.4f' % min_train_mse
    print '\t TEST MSE: %.4f' % best_test_mse
    print '***************************************************************'


def selection_based_on_residue():
    feature_list = [get_max_coeff(train_df, train_target, feature_names[1:])]

    while len(feature_list) < 4:
        new_train_df, new_test_df = filter_dataframes(train_df, test_df, feature_list)
        theta_df = get_theta_values(new_train_df, train_target)
        y_train_predicted = theta_df.dot(new_train_df.transpose())
        residue_val = train_target - y_train_predicted
        feature_list.append(get_max_coeff(train_df, residue_val, feature_names[1:], feature_list))

    print 'RESIDUE BASED SELECTION:\n'
    print 'FEATURES : %s' % (','.join(feature_list))

    curr_train, curr_test = filter_dataframes(train_df, test_df, feature_list)
    linear_regression(curr_train, train_target, curr_test, test_target)


def polynomial_coeff_selection():
    poly_train_df = copy.deepcopy(train_df)
    poly_test_df = copy.deepcopy(test_df)

    count = 1
    column_name_list = []
    for index in xrange(1, len(feature_names)):
        feature1 = feature_names[index]
        for index2 in xrange(index, len(feature_names)):
            feature2 = feature_names[index2]

            column_name = 'f%s' % count
            column_name_list.append(column_name)

            poly_train_df[column_name] = poly_train_df[feature1] * poly_train_df[feature2]
            poly_test_df[column_name] = poly_test_df[feature1] * poly_test_df[feature2]

            count += 1

    print 'POLYNOMIAL FEATURE SELECTION:'
    standardize_data(poly_train_df, poly_test_df, column_name_list)
    linear_regression(poly_train_df, train_target, poly_test_df, test_target)



if __name__=='__main__':
    train_df, train_target, test_df, test_target, feature_names = get_data()


    print 'DATA ANALYSIS: \n'
    draw_histograms(train_df)
    dict_pearson_coeff = get_pearson_coeff()

    standardize_data(train_df, test_df, feature_names[1:])
    linear_regression(train_df, train_target, test_df, test_target)
    ridge_regression()
    find_optimum_lambda(0.0001, 10)
    basic_correlation(dict_pearson_coeff)
    selection_with_brute_force()
    selection_based_on_residue()
    polynomial_coeff_selection()

