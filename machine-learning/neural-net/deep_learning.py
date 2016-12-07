from utils import *
import time

def preprocessing():
    train_data, train_label, test_data, test_label = loaddata('data/MiniBooNE_PID.txt')
    train_data, test_data = normalize(train_data, test_data)
    return train_data, train_label, test_data, test_label


def linear_activation():
    global train_data, train_label, test_data, test_label, num_features, num_output

    print 'LINEAR ACTIVATION: \n'
    print 'Initial Architecture:'
    architecture_list = [[num_features, num_output], [num_features, 50, num_output], [num_features, 50, 50, num_output],
                         [num_features, 50, 50, 50, num_output]]
    start_time = time.time()
    testmodels(train_data, train_label, test_data, test_label, architecture_list, actfn='linear', last_act='softmax',
               sgd_lr=0.001)
    end_time = time.time()
    print 'Time Taken: %s sec\n' % (end_time-start_time)
    print 'Large Architecture:'
    architecture_list = [[num_features, 50, num_output], [num_features, 500, num_output], [num_features, 500, 300, num_output],
                         [num_features, 800, 500, 300, num_output], [num_features, 800, 800, 500, 300, num_output]]
    start_time = time.time()
    testmodels(train_data, train_label, test_data, test_label, architecture_list, actfn='linear', last_act='softmax',
               sgd_lr=0.001)
    end_time = time.time()
    print 'Time Taken: %s sec\n' % (end_time-start_time)


def sigmoid_activation():
    global train_data, train_label, test_data, test_label, num_features, num_output
    print 'SIGMOID ACTIVATION:\n'
    architecture_list = [[num_features, 50, num_output], [num_features, 500, num_output], [num_features, 500, 300, num_output],
                     [num_features, 800, 500, 300, num_output], [num_features, 800, 800, 500, 300, num_output]]
    start_time = time.time()
    testmodels(train_data, train_label, test_data, test_label, architecture_list, actfn='sigmoid', last_act='softmax',
               sgd_lr=0.001)
    end_time = time.time()
    print 'Time Taken: %s sec\n' % (end_time-start_time)


def relu_activation():
    global train_data, train_label, test_data, test_label, num_features, num_output
    print 'RELU ACTIVATION:\n'
    architecture_list = [[num_features, 50, num_output], [num_features, 500, num_output], [num_features, 500, 300, num_output],
                         [num_features, 800, 500, 300, num_output], [num_features, 800, 800, 500, 300, num_output]]
    start_time = time.time()
    testmodels(train_data, train_label, test_data, test_label, architecture_list, actfn='relu', last_act='softmax',
               sgd_lr=5*pow(10, -4))
    end_time = time.time()
    print 'Time Taken: %s sec\n' % (end_time-start_time)


def l2_regularization():
    global train_data, train_label, test_data, test_label, num_features, num_output
    print 'L2-REGULARIZATION: \n'
    architecture_list = [[num_features, 800, 500, 300, num_output]]
    regularization_params = [pow(10, -7), 5*pow(10, -7), pow(10, -6), 5*pow(10, -6), pow(10, -5)]
    testmodels(train_data, train_label, test_data, test_label, architecture_list, actfn='relu', last_act='softmax',
               sgd_lr=5*pow(10, -4), reg_coeffs=regularization_params)


def early_stopping():
    global train_data, train_label, test_data, test_label, num_features, num_output
    print 'EARLY STOPPING and L2-REGULARIZATION:\n'
    architecture_list = [[num_features, 800, 500, 300, num_output]]
    regularization_params = [pow(10, -7), 5 * pow(10, -7), pow(10, -6), 5 * pow(10, -6), pow(10, -5)]

    best_config = testmodels(train_data, train_label, test_data, test_label, architecture_list, actfn='relu',
                             last_act='softmax', sgd_lr=5*pow(10, -4), reg_coeffs=regularization_params, EStop=True)
    return best_config


def sgd_with_weight_decay():
    global train_data, train_label, test_data, test_label, num_features, num_output
    print 'SGD WITH WEIGHT DECAY:\n'
    architecture_list = [[num_features, 800, 500, 300, num_output]]
    decay_list = [pow(10, -5), 5*pow(10, -5), pow(10, -4), 3*pow(10, -4), 7*pow(10, -4), pow(10, -3)]
    regularization_coeff = [5*pow(10, -7)]

    best_config = testmodels(train_data, train_label, test_data, test_label, architecture_list, actfn='relu',
                             last_act='softmax', sgd_lr=pow(10, -5), reg_coeffs=regularization_coeff, num_epoch=100,
                             sgd_decays=decay_list)
    return best_config


def momentum(decay_val):
    global train_data, train_label, test_data, test_label
    print 'MOMENTUM: \n'
    momentum_coeff = [0.99, 0.98, 0.95, 0.9, 0.85]
    best_decay = [decay_val]
    architecture_list = [[num_features, 800, 500, 300, num_output]]
    best_config = testmodels(train_data, train_label, test_data, test_label, architecture_list, actfn='relu',
                             last_act='softmax', num_epoch=50, sgd_lr=pow(10, -5), sgd_Nesterov=True,
                             sgd_moms=momentum_coeff, sgd_decays=best_decay)
    return best_config


def combination(coeff, decay, momentum_val):
    global train_data, train_label, test_data, test_label, num_features, num_output
    print 'COMBINATION: \n'
    best_decay = [decay]
    regularization_coeff = [coeff]
    best_momentum = [momentum_val]
    architecture_list = [[num_features, 800, 500, 300, num_output]]
    testmodels(train_data, train_label, test_data, test_label, architecture_list, actfn='relu', last_act='softmax',
               num_epoch=100, batch_size=1000, sgd_lr=pow(10, -5), sgd_Nesterov=True, sgd_moms=best_momentum,
               EStop=True, sgd_decays=best_decay, reg_coeffs=regularization_coeff)


def grid_search_cross_validation():
    global train_data, train_label, test_data, test_label, num_features, num_output
    print 'GRID SEARCH CROSS VALIDATION: \n'
    architecture_list = [[num_features, 50, num_output], [num_features, 500, num_output], [num_features, 500, 300, num_output],
                         [num_features, 800, 500, 300, num_output], [num_features, 800, 800, 500, 300, num_output]]
    regularization_params = [pow(10, -7), 5 * pow(10, -7), pow(10, -6), 5 * pow(10, -6), pow(10, -5)]
    momentum_coeff = [0.99]
    decay_list = [pow(10, -5), 5*pow(10, -5), pow(10, -4)]
    testmodels(train_data, train_label, test_data, test_label, architecture_list, actfn='relu', last_act='softmax',
               num_epoch=100, sgd_lr=pow(10, -5), sgd_Nesterov=True, sgd_moms=momentum_coeff, EStop=True,
               reg_coeffs=regularization_params, sgd_decays=decay_list)


if __name__ == '__main__':
    train_data, train_label, test_data, test_label =  preprocessing()
    # train_data = train_data[:100]
    # train_label = train_label[:100]
    # test_data = test_data[:100]
    # test_label = test_label[:100]
    num_features = 50
    num_output = 2
    print '***************************************************************'
    linear_activation()
    print '***************************************************************'
    sigmoid_activation()
    print '***************************************************************'
    relu_activation()
    print '***************************************************************'
    l2_regularization()
    print '***************************************************************'
    x, best_reg_coeff, y, z, a, b = early_stopping()
    print '***************************************************************'
    x, y, best_decay, a, b, c = sgd_with_weight_decay()
    print '***************************************************************'
    x, y, z, best_momentum, a, b = momentum(best_decay)
    print '***************************************************************'
    print 'Best: Coefficient: %s, Decay: %s, Momentum: %s' % (best_reg_coeff, best_decay, best_momentum)
    combination(best_reg_coeff, best_decay, best_momentum)
    print '***************************************************************'
    grid_search_cross_validation()
    print '***************************************************************'
