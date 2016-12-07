import numpy as np
import pandas as pd
from utils import *
from kernel_svm import *

DICT_INDEX_FUNCTION_NAMES = {0: 'g1(x) = 1', 1: 'g2(x) = w0', 2: 'g3(x) = w0+w1(x)', 3: 'g4(x) = w0+ w1(x) + w2(x^2) ',
                      4: 'g5(x) = w0+ w1(x) + w2(x^2) + w3(x^3)', 5: 'g6(x) = w0+ w1(x) + w2(x^2) + w3(x^3) + w4(x^4)'}


def get_target(element):
    return_ele = 2 * pow(element, 2)
    error_val = np.random.normal(0, 0.1, size=1)
    return return_ele+error_val[0]


def get_samples(num_datasets, num_samples):
    all_sample_list = []
    all_target_list = []

    for index in xrange(num_datasets):
        temp_list = np.random.uniform(-1, 1, num_samples)
        sample_list = []
        target_list = []
        for element in temp_list:
            sample_list.append([1, element])
            target_list.append(get_target(element))

        column_list = ['f0', 'x']
        dataset = pd.DataFrame(sample_list, columns=column_list)

        dataset['x^2'] = dataset['x']*dataset['x']
        dataset['x^3'] = dataset['x^2']*dataset['x']
        dataset['x^4'] = dataset['x^3']*dataset['x']

        all_sample_list.append(dataset)
        all_target_list.append(np.array(target_list))

    return all_sample_list, all_target_list


def linear_regression(train_df, train_target, lambda_val=0.0):
    theta_df = get_theta_values(train_df, train_target, lambda_val)
    y_train_predicted = theta_df.dot(train_df.transpose())

    return theta_df, y_train_predicted


def generate_features(x, index):
    return_list = []
    for i in xrange(index):
        return_list.append(x**i)
    return np.array(return_list)


def calculate_bias_variance(theta_values, function_order):
    bias_value = 0
    total_variance = 0
    for x in np.linspace(-1, 1, 1000):
        correct_y = 2 * pow(x, 2)
        if function_order == 0:
            y_pred_sum = 100
            features = []
        else:
            y_pred_sum = 0
            features = generate_features(x, function_order)
            for theta in theta_values:
                y_pred_sum += theta.dot(features.transpose())
        y_avg = y_pred_sum/100
        bias_value += pow(y_avg - correct_y, 2)

        variance = 0
        if function_order != 0:
            for theta in theta_values:
                y_pred = theta.dot(features.transpose())
                variance += pow(y_pred - y_avg, 2)
        variance /= 100
        total_variance += variance

    print '\tBIAS: %s' % (bias_value/1000)
    print '\tVariance: %s\n' % (total_variance/1000)


def get_bias_variance(all_dataset, all_target, sample_size, histogram_folder_name):
    global DICT_INDEX_FUNCTION_NAMES
    column_list = ['constant']
    column_list.extend(all_dataset[0].columns)

    for index, element in enumerate(column_list):
        mse_list = []
        theta_values = []
        feature_names = column_list[1: index+1]

        print 'FUNCTION NAME : %s\n' % DICT_INDEX_FUNCTION_NAMES[index]
        for index2 in xrange(len(all_dataset)):
            dataset = all_dataset[index2]
            target = all_target[index2]

            if element == 'constant':
                y_predicted = [1]*len(target)
                mse_error = get_mean_error(target, y_predicted)
                mse_list.append(mse_error)
            else:
                train_df = filter_dataframes(dataset, feature_names)
                theta_df, y_predicted = linear_regression(train_df, target)
                theta_values.append(theta_df)
                mse_list.append(get_mean_error(target, y_predicted))

        draw_histogram(mse_list, histogram_folder_name, index)

        calculate_bias_variance(theta_values, index)


def linear_reg():
    print 'LINEAR REGRESSION WITHOUT REGULARIZATION:\n'
    print 'The histograms plotted here are also saved in the folders in present directory. The plots with sample size ' \
          '10 are stored in folder named "sample_size_10_images" and plots for sample size 100 are stored in folder ' \
          'named "sample_size_100_images"\n'

    dataset, target = get_samples(100, 10)
    print 'SAMPLE SIZE: 10\n'
    get_bias_variance(dataset, target, 10, 'sample_size_10_images')
    print '***************************************************************'

    dataset, target = get_samples(100, 100)
    print 'SAMPLE SIZE: 100\n'
    get_bias_variance(dataset, target, 100, 'sample_size_100_images')
    print '***************************************************************'

    linear_reg_with_regularization(dataset, target)


def linear_reg_with_regularization(dataset, target):
    print 'LINEAR REGRESSION WITH REGULARIZATION:\n'
    feature_names = ['f0', 'x', 'x^2']
    training_list = []
    for entry in dataset:
        training_list.append(filter_dataframes(entry, feature_names))
    lambda_values = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]
    for lambda_val in lambda_values:
        print 'LAMBDA VALUE: %s\n' %(lambda_val)
        theta_values = []
        for index, train_df in enumerate(training_list):
            theta_df, y_predicted = linear_regression(train_df, target[index], lambda_val)
            theta_values.append(theta_df)
        calculate_bias_variance(theta_values, 3)


if __name__=='__main__':
    linear_reg()
    print '***************************************************************'
    print 'Running SVM kernels now\n'
    svm_main()