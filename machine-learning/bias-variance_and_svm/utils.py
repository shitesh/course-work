import numpy as np
from numpy.linalg import pinv
import matplotlib.pyplot as plt

def filter_dataframes(dataframe1, feature_names):
    new_df1 = dataframe1[feature_names]
    return new_df1


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


def get_mean_error(y_correct, y_predicted, isMean=True):
    num_terms = len(y_correct)
    curr_sum = 0
    for index in xrange(len(y_correct)):
        curr_diff = abs(y_correct[index] - y_predicted[index])
        curr_diff = pow(curr_diff, 2)

        curr_sum += curr_diff
    if isMean:
        return curr_sum/num_terms
    return curr_sum

def draw_histogram(mse_list, folder_name, function_index):
    #print 'HISTOGRAM:\n'
    #print 'The histograms generated are stored in the "images" folder in the current directory.\n'


    function_names = ['g1(x) = 1', 'g2(x) = w0', 'g3(x) = w0+w1(x)', 'g4(x) = w0+ w1(x) + w2(x^2) ',
                      'g5(x) = w0+ w1(x) + w2(x^2) + w3(x^3)', 'g6(x) = w0+ w1(x) + w2(x^2) + w3(x^3) + w4(x^4)']

    plt.title('Function : %s' % function_names[function_index])
    plt.hist(mse_list, bins=10)
    plt.savefig('%s/%s.png' % (folder_name, function_names[function_index].split('=')[0]))
    plt.show()
    plt.clf()
    #print 'HISTOGRAM generation complete. Please visit the folder for images.\n\n'
