from sklearn.datasets import load_boston
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import copy


def get_data():
    feature_names = ['f0']
    boston_data = load_boston()

    train_data = []
    train_target = []
    test_data = []
    test_target = []

    for index in xrange(len(boston_data.data)):
        temp_list = [1]
        temp_list.extend(boston_data.data[index])
        if index % 7 == 0:
            test_data.append(temp_list)
            test_target.append(boston_data.target[index])
        else:
            train_data.append(temp_list)
            train_target.append(boston_data.target[index])

    feature_names.extend(boston_data.feature_names)

    train_df = pd.DataFrame(train_data, columns=feature_names)
    test_df = pd.DataFrame(test_data, columns=feature_names)

    train_target = np.array(train_target)
    test_target = np.array(test_target)
    return train_df, train_target, test_df, test_target, feature_names


def standardize_data(train_df, test_df, column_names):
    for feature_name in column_names:
        test_df[feature_name] = (test_df[feature_name]-train_df[feature_name].mean())/train_df[feature_name].std()
        train_df[feature_name] = (train_df[feature_name]-train_df[feature_name].mean())/train_df[feature_name].std()


def get_k_folds(train_df, train_target):
    copy_train_df = copy.deepcopy(train_df)
    copy_train_df['target'] = train_target

    train_shuffle = copy_train_df
    k_folds = []
    length = len(train_shuffle)

    incr_value = (length/10) + 1
    start_val = 0
    for index in xrange(1, 11):
        if index <= 3:
            k_folds.append(train_shuffle[start_val:start_val+incr_value])
        else:
            incr_value = (length/10)
            k_folds.append(train_shuffle[start_val: start_val+incr_value])
        start_val += incr_value

    return k_folds


def pearson(X, Y):
    sum1 = sum(X)
    sum2 = sum(Y)
    squares1 = sum([n * n for n in X])
    squares2 = sum([n * n for n in Y])
    product_sum = 0
    for i in range(len(X)):
        product_sum += X[i]*Y[i]
    size = len(X)
    numerator = product_sum - ((sum1 * sum2) / size)
    denominator = math.sqrt((squares1 - (sum1 * sum1) / size) * (squares2 - (sum2 * sum2) / size))
    if denominator == 0:
        return 0
    return numerator / denominator


def get_mean_error(y_correct, y_predicted):
    num_terms = len(y_correct)
    curr_sum = 0
    for index in xrange(len(y_correct)):
        curr_diff = abs(y_correct[index] - y_predicted[index])
        curr_diff = pow(curr_diff, 2)

        curr_sum += curr_diff
    return curr_sum/num_terms


def draw_histograms(train_df):
    print 'HISTOGRAM:\n'
    print 'The histograms generated are stored in the "images" folder in the current directory.\n'

    for column in train_df.columns[1:]:
        attr = train_df[column]
        plt.title('Feature Name: %s' % column)
        plt.hist(attr, bins=10)
        plt.savefig('images/%s.png' % column)
        plt.clf()
        #plt.show()
    print 'HISTOGRAM generation complete. Please visit the folder for images.\n\n'


def filter_dataframes(dataframe1, dataframe2, feature_names):
    feature_list = ['f0']
    feature_list.extend(feature_names)

    new_df1 = dataframe1[feature_list]
    new_df2 = dataframe2[feature_list]

    return new_df1, new_df2


def get_max_coeff(train_df, target, feature_names, skip_feature_list=None):

    max_coeff = -1
    req_feature = None

    for feature_name in feature_names:
        if skip_feature_list and feature_name in skip_feature_list:
            continue

        pearson_coeff = abs(pearson(train_df[feature_name], target))
        if pearson_coeff> max_coeff:
            max_coeff = pearson_coeff
            req_feature = feature_name

    return req_feature