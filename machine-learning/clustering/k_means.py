import csv
import math
import random
import sys
from utils import *
from gmm import gmm
from kernel_k_means import kernel_k_means


def get_distance(point1, point2):
    sum_val = 0
    for index in xrange(len(point1)):
        sum_val += pow(point1[index]-point2[index], 2)
    return math.sqrt(sum_val)


def get_center(input_list):
    length = len(input_list)
    num_ele = len(input_list[0])
    center = [0] * num_ele

    for entry in input_list:
        for index2 in xrange(len(entry)):
            center[index2] += entry[index2]

    for index in xrange(len(center)):
        center[index] /= length
    return tuple(center)


def create_cluster(data_points, centroid_list):
    dict_cluster =  {}
    for entry in centroid_list:
        dict_cluster[entry] = []

    for point in data_points:
        min_dist = sys.maxint
        cluster = None
        for centroid in centroid_list:
            distance = get_distance(centroid, point)
            if distance < min_dist:
                min_dist = distance
                cluster = centroid
        dict_cluster[cluster].append(point)

    return dict_cluster


def get_k_means_cluster(data_points, k):
    centroid_set = set()
    while len(centroid_set) < k:
        centroid_set.add(tuple(random.choice(data_points)))

    centroid_list = list(centroid_set)
    centroid_list.sort()
    dict_cluster = create_cluster(data_points, centroid_list)
    prev_centroid_list = None

    count = 0
    while prev_centroid_list != centroid_list:
        count += 1
        prev_centroid_list = centroid_list
        centroid_list = []
        for entry in prev_centroid_list:
            points = dict_cluster[entry]
            new_centroid = get_center(points)
            centroid_list.append(new_centroid)
        centroid_list.sort()
        dict_cluster = create_cluster(data_points, centroid_list)
    return dict_cluster


def k_means():
    k_value_list = [2, 3, 5]
    file = open('data/hw5_blob.csv', 'r')
    reader = csv.reader(file)
    blob_data_points = []

    for row in reader:
        blob_data_points.append((float(row[0]), float(row[1])))

    for k_value in k_value_list:
        dict_cluster = get_k_means_cluster(blob_data_points, k_value)
        plot_cluster(dict_cluster, 'K-means(blob)')

    file = open('data/hw5_circle.csv', 'r')
    reader = csv.reader(file)
    circle_data_points = []

    for row in reader:
        circle_data_points.append((float(row[0]), float(row[1])))

    for k_value in k_value_list:
        dict_cluster = get_k_means_cluster(circle_data_points, k_value)
        plot_cluster(dict_cluster, 'K-means(circle)')


if __name__ == '__main__':
    print 'K Means:'
    k_means()
    print '***************************************************************'
    print 'Starting Kernel K Means:'
    kernel_k_means()
    print '***************************************************************'
    print 'Starting GMM:'
    best_log_likelihood, best_mean, best_covariance = gmm()
    for index in xrange(len(best_mean)):
        print 'Cluster:%s' % (index+1)
        print '\tMean: %s' % best_mean[index]
        print '\tCovariance: %s\n' % best_covariance[index]
    print '***************************************************************'
