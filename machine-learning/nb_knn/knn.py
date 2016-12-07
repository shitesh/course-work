import operator
import pandas as pd
from scipy.spatial import distance


def get_class_name(input_list):
    dict_class = {}

    for entry in input_list:
        if entry[1] in dict_class:
            dict_class[entry[1]] += 1
        else:
            dict_class[entry[1]] = 1

    sorted_dict = sorted(dict_class.items(), key=operator.itemgetter(1), reverse=True)
    potential_return_value = sorted_dict[0]

    if len(sorted_dict) > 1 and sorted_dict[1][1] == potential_return_value[1]:
        #repeat case
        temp_list = []
        for entry in sorted_dict:
            if entry[1] == potential_return_value[1]:
                temp_list.append(entry[0])

        for entry in input_list:
            if entry[1] in temp_list:
                return entry[1]
    # non repeat case - return class with max count
    return potential_return_value[0]


def update_metrics(dict_accuracy, metric_list, actual_class):
    for key, value in dict_accuracy.iteritems():
        class_name = get_class_name(metric_list[:key])
        if class_name == actual_class:
            dict_accuracy[key] += 1


def compute_accuracy(train_df, test_df, is_train=False):
    dict_accuracy_l1_k = {1: 0, 3: 0, 5: 0, 7: 0}

    dict_accuracy_l2_k = {1: 0, 3: 0, 5: 0, 7: 0}

    for index, row in test_df.iterrows():
        l1_metrics = []
        l2_metrics = []
        for index2, next_row in train_df.iterrows():
            #if tuple(row[:-1]) == tuple(next_row[:-1]):
            if is_train and index2 == index:
                continue
            l1_metrics.append((distance.cityblock(row[:-1], next_row[:-1]), next_row['target']))
            l2_metrics.append((distance.euclidean(row[:-1], next_row[:-1]), next_row['target']))

        l1_metrics.sort()
        l2_metrics.sort()

        update_metrics(dict_accuracy_l1_k, l1_metrics, row['target'])
        update_metrics(dict_accuracy_l2_k, l2_metrics, row['target'])

    total_rows = len(test_df)
    if is_train:
        total_rows -= 1

    for key, value in dict_accuracy_l1_k.iteritems():
        print '\nK == %s' % key
        print '    Manhattan(L1) accuracy = %.4f' % (float(value)*100/total_rows)
        print '    Eucledian(L2) accuracy = %.4f' % (float(dict_accuracy_l2_k[key])*100/total_rows)


def knn(train_df, test_df):
    #print len(train_df)
    #train_df = train_df.drop_duplicates()
    #print len(train_df)

    for index in xrange(1, 10):
        feature_name = 'f%s' % index
        test_df[feature_name] = (test_df[feature_name]-train_df[feature_name].mean())/train_df[feature_name].std()
        train_df[feature_name] = (train_df[feature_name]-train_df[feature_name].mean())/train_df[feature_name].std()

    print '\nKNN RESULTS (Accuracy in %) :'
    print '****************TRAINING DATA*********************************'
    compute_accuracy(train_df, train_df, True)
    print '\n******************TEST DATA***********************************'
    compute_accuracy(train_df, test_df)
