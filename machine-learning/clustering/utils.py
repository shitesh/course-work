from matplotlib import pyplot as plt


def plot_cluster(dict_cluster, function_name=None):
    colors = list("rgbcmyk")
    markers = list('xo^+d')
    for key, value in dict_cluster.iteritems():
        x_coord = []
        y_coord = []
        for entry in value:
            x_coord.append(entry[0])
            y_coord.append(entry[1])
        plt.scatter(x_coord, y_coord, color=colors.pop(0), marker=markers.pop(0), s=75)
    if function_name:
        title = '%s : K-value=%s' %(function_name, len(dict_cluster))
    else:
        title = 'K-value=%s' % len(dict_cluster)
    plt.title(title)
    plt.savefig('images/%s.png' % title)
    plt.show()
    plt.clf()


def plot_likelihood(likelihood_list):
    for index, entry in enumerate(likelihood_list):
        plt.plot(range(len(entry)), entry, label='Iteration %s' % (index+1))
    plt.title('Log Likelihood values for 5 iterations')
    # plt.legend(loc='lower right')
    plt.xlabel("Number of iterations")
    plt.ylabel("Log Likelihood value")
    plt.savefig('images/GMM.png')
    plt.show()
    plt.clf()
