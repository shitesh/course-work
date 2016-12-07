import numpy as np
from numpy.linalg import pinv, det
import math
import sys
from utils import *
from scipy.stats import multivariate_normal

# def get_multivariate_norm(input_vec, mean, co_variance):
#     for i in xrange(len(co_variance)):
#         if co_variance[i, i] <= sys.float_info[3]:  # min float
#             co_variance[i, i] = sys.float_info[3]
#     diff_vec = np.matrix(input_vec - mean)
#     covariance_inverse = pinv(co_variance)
#     num_dimensions = len(input_vec)
#     value = (2.0*math.pi)**(-num_dimensions/2.0) * (1.0/math.sqrt(det(co_variance))) * math.exp(-0.5 * (diff_vec * covariance_inverse
#                                                                                    * diff_vec.transpose()))
#     return value


def get_covariance(input_data, mu_list, probability_values=None):
    dict_covariance = {}
    for index, mu_val in enumerate(mu_list):
        covar_value = np.matrix(np.diag(np.zeros(len(input_data[0]), np.float64)))
        for index2, row in enumerate(input_data):
            value = np.matrix(row-mu_val).transpose()*np.matrix(row-mu_val)
            if probability_values:
                value = probability_values[index2][index] * value
            covar_value += value
        dict_covariance[index] = covar_value
    return dict_covariance


def gmm():
    k_value = 3
    file = open('data/hw5_blob.csv', 'r')
    input_data = np.loadtxt(file, delimiter=',')
    likelihood_list = []

    best_log_likelihood = -1*sys.maxint
    best_mean, best_covariance, best_probab_dist = None, None, None

    for total_iteration in xrange(5):
        print 'Iteration Number: %s' %(total_iteration+1)
        likelihood_list.append([])
        mu_list = input_data[np.random.choice(input_data.shape[0], k_value, replace=False)]
        dict_covariance = get_covariance(input_data, mu_list)
        for key, value in dict_covariance.iteritems():
            dict_covariance[key] /= len(input_data)
        probability_list = np.array([1.0/k_value for index in xrange(k_value)])
        iteration_count = 0

        old_likelihood_val, new_likelihood_val = None, 0.0
        num_match = 0
        while (old_likelihood_val != new_likelihood_val or num_match < 5) and iteration_count < 100:
            if old_likelihood_val == new_likelihood_val:
                num_match += 1

            old_likelihood_val = new_likelihood_val
            new_likelihood_val = 0.0

            cluster_responsibility = np.zeros(k_value)
            new_mu_list = np.zeros_like(mu_list)
            all_probability_values = []
            for element in input_data:
                probab_cluster_list = []
                likelihood_val = 0.0
                for cluster_index in xrange(k_value):
                    norm_val = multivariate_normal.pdf(element, mu_list[cluster_index], dict_covariance[cluster_index])
                    norm_val *= probability_list[cluster_index]
                    likelihood_val += norm_val
                    probab_cluster_list.append(norm_val)
                probab_array = np.array(probab_cluster_list)
                probab_array = probab_array/probab_array.sum() # ric - probability that point belongs to class
                all_probability_values.append(probab_array)

                new_likelihood_val += math.log(likelihood_val)
                cluster_responsibility += probab_array  # sum over all probabilities and then divide to get new one

                for index, entry in enumerate(probab_array):
                    new_mu_list[index] += (entry * element) # summation ric*x_i

            likelihood_list[-1].append(new_likelihood_val)
            if new_likelihood_val > best_log_likelihood:
                best_log_likelihood = new_likelihood_val
                best_mean = mu_list
                best_covariance = dict_covariance
                best_probab_dist = all_probability_values

            probability_list = cluster_responsibility/cluster_responsibility.sum() # m_c/m
            for index in xrange(len(cluster_responsibility)):
                new_mu_list[index] /= cluster_responsibility[index] # divide by m_c

            mu_list = new_mu_list
            dict_covariance = get_covariance(input_data, mu_list, all_probability_values)
            for index in xrange(len(cluster_responsibility)):
                dict_covariance[index] /= cluster_responsibility[index] # divide by m_c

            iteration_count += 1

    print 'plotting now'
    plot_likelihood(likelihood_list)

    dict_cluster = {0: [], 1:[], 2:[]}
    for index in xrange(len(input_data)):
        max_index = best_probab_dist[index].argmax()
        dict_cluster[max_index].append(input_data[index])
    print 'created cluster: plotting now'
    plot_cluster(dict_cluster, 'Best GMM:')
    return best_log_likelihood, best_mean, best_covariance

