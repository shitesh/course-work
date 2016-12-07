import numpy as np
import random
import sys
from utils import *


def get_kernel_matrix(input_data):
    square_val = np.square(input_data)
    square_sum = square_val[:, 0]  +square_val[:, 1]
    square_sum_mat = np.asmatrix(square_sum)
    k_matrix = np.dot(square_sum_mat.transpose(), square_sum_mat)
    return k_matrix


def kernel_k_means():
    k_value = 2
    input_data = np.loadtxt('data/hw5_circle.csv', delimiter=',')
    kernel_matrix = get_kernel_matrix(input_data)

    rank_list = [-1] * len(input_data)
    cluster1_centre = random.randint(0, len(input_data))
    rank_list[cluster1_centre] = 0
    cluster2_centre = random.randint(0, len(input_data))

    while cluster2_centre == cluster1_centre:
        cluster2_centre = random.randint(0, len(input_data))
    rank_list[cluster2_centre] = 1

    cluster_changed = True
    updated_rank_list = rank_list
    count = 0
    while cluster_changed:
        count += 1
        # print count
        rank_list = updated_rank_list
        cluster_changed = False
        # group all points belonging to a cluster
        dict_cluster_elements = {0: [], 1: []}
        for index in xrange(len(rank_list)):
            if rank_list[index] != -1:
                dict_cluster_elements[rank_list[index]].append(index)
        # compute the sum of kernel function values between all points belonging to a cluster
        dict_cluster_kernel_sum = {0: 0, 1: 0}
        for cluster_index, value in dict_cluster_elements.iteritems():
            for element in value:
                for element2 in value:
                    dict_cluster_kernel_sum[cluster_index] += kernel_matrix[element, [element2]]
        # print dict_cluster_kernel_sum

        for index in xrange(len(input_data)):
            distance_vec = [-1] * k_value
            for cluster_index in xrange(k_value):
                value1 = kernel_matrix[index, [index]]
                value2 = 0
                for index2 in dict_cluster_elements[cluster_index]:
                    value2 += kernel_matrix[index, [index2]]

                cluster_length = len(dict_cluster_elements[cluster_index])
                distance_vec[cluster_index] = value1 - 2 * value2/cluster_length + dict_cluster_kernel_sum[cluster_index] / (cluster_length ** 2)

            min_index, min_value = 0, sys.maxint
            for i in xrange(len(distance_vec)):
                if distance_vec[i] < min_value:
                    min_value = distance_vec[i]
                    min_index = i

            if updated_rank_list[index] != min_index:
                updated_rank_list[index] = min_index
                cluster_changed = True

    dict_cluster = {0: [], 1: []}
    for index in xrange(len(updated_rank_list)):
        dict_cluster[updated_rank_list[index]].append(input_data[index])
    plot_cluster(dict_cluster, 'Kernel K-means(circle)')
