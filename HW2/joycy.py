# Author: Joyce Tan
import math
import os

try:
    import matplotlib.pyplot as plt
except ImportError:
    os.system("pip install matplotlib")

# this method reads a dataset file and puts rows of complete data and rows of missing data into their respective dict
# param: filename: name of dataset file
# return: dict of complete data and dict of missing
def read_data(filename):
    complete_data = {} # key: (G, W, H), value: count of (G, W, H)
    missing_data = {} # key: ('-', W, H), value: count of ('-', W, H), value of gender is missing
    with open(filename) as file:
        for line in file:
            line = line.split()
            if line[0] != 'Gender':
                gender, weight, height = line
                if gender != '-':
                    if (gender, weight, height) in complete_data:
                        complete_data[(gender, weight, height)] += 1
                    else:
                        complete_data[(gender, weight, height)] = 1
                else:
                    if ('-', weight, height) in missing_data:
                        missing_data[('-', weight, height)] += 1
                    else:
                        missing_data[('-', weight, height)] = 1

    return complete_data, missing_data


# this method puts prior probabilities into a dict and returns the dict
# params: g0: P(G=0), w0_given_g0: P(W=0|G=0), w0_given_g1: P(W=0|G=1), h0_given_g0: P(H=0|G=0), h0_given_g1: P(H=0|G=1)
def prior_parameter(g0, w0_given_g0, w0_given_g1, h0_given_g0, h0_given_g1):
    prior_param = {('0', ' ', ' '): g0, ('1', ' ', ' '): 1 - g0, ('0', '0', ' '): w0_given_g0,
                  ('0', '1', ' '): 1 - w0_given_g0, ('1', '0', ' '): w0_given_g1, ('1', '1', ' '): 1 - w0_given_g1,
                  ('0', ' ', '0'): h0_given_g0, ('0', ' ', '1'): 1 - h0_given_g0, ('1', ' ', '0'): h0_given_g1,
                  ('1', ' ', '1'): 1 - h0_given_g1}

    return prior_param

# this method calculates the log likelihood for iteration#0 using the prior parameters and returns a list with the log
# likelihood of iteration#0. This list will be used to keep track of log likelihoods during each iteration of the EM
# algorithm then used to generate the plot iteration# vs log likelihood
# param: complete_data: dict of complete data, key: (G, W, H), value: count of (G, W, H)
# param: missing_data: dict of missing data, key: ('-', W, H), value: count of ('-', W, H)
# param: prior_prob: dict of prior probabilities
def calc_log_prob_iteration0(complete_data, missing_data, prior_prob):
    log_likelihood_list = []
    total_log_likelihood = 0

    # for each complete data row in the given dataset calculate log likelihood
    for data in complete_data:
        g = data[0]
        w = data[1]
        h = data[2]
        # P(G,W,H) = P(G) * P(W|G) * P(H|G) using probabilities from the prior probability tables
        prob_data_using_prior_prob = prior_prob[(g, ' ', ' ')] * prior_prob[(g, w, ' ')] * prior_prob[(g, ' ', h)]
        # add log(P(G,W,H)) to the total log likelihood
        total_log_likelihood += math.log(prob_data_using_prior_prob)

    # for each missing data row in the given dataset calculate log likelihood
    for data in missing_data:
        w = data[1]
        h = data[2]
        prob_data_using_prior_prob = 0
        # for G=0 and G=1
        for i in range(2):
            g = str(i)
            # P(W,H) = sum_of_G P(G) * P(W|G) * P(H|G) using probabilities from the previous probability tables
            prob_data_using_prior_prob += prior_prob[(g, ' ', ' ')] * prior_prob[(g, w, ' ')] * prior_prob[(g, ' ', h)]
            # add log(P(W,H)) to the total log likelihood
            total_log_likelihood += math.log(prob_data_using_prior_prob)

    log_likelihood_list.append(total_log_likelihood)

    return log_likelihood_list

# this method performs the E-step in the EM algorithm and returns a dict of the estimated data
# param: missing_data: dict of missing data, key: ('-', W, H), value: count of ('-', W, H)
# param: curr_prob: dict of conditional probability tables used for calculations in E-step in the current iteration
def E_step(missing_data, curr_prob):
    estimated_data = {} # key: (G, W, H), value: expected count of (G, W, H)

    # for each missing data row in the given dataset calculate P(G|W,H)
    for data in missing_data:
        weight = data[1]
        height = data[2]
        prob_G0_given_W_H = calc_prob_G0_given_W_H(data, curr_prob)
        estimated_data[('0', weight, height)] = prob_G0_given_W_H * missing_data[data]
        estimated_data[('1', weight, height)] = (1 - prob_G0_given_W_H) * missing_data[data]

    return estimated_data


# this method calculates P(G=0|W,H) and returns the probability of P(G=0|W,H)
# param: data: data tuple (G, W, H)
# param: curr_prob: dict of conditional probability tables used for calculations in E-step in the current iteration
def calc_prob_G0_given_W_H(data, curr_prob):
    w = data[1]
    h = data[2]
    numerator, denominator = 0, 0

    # numerator = P(G=0) * P(W|G=0) * P(H|G=0)
    numerator = curr_prob[('0', ' ', ' ')] * curr_prob[('0', w, ' ')] * curr_prob[('0', ' ', h)]
    # denominator = sum_of_G P(G) * P(W|G) * P(H|G)
    for i in range(2):
        g = str(i)
        denominator += curr_prob[(g, ' ', ' ')] * curr_prob[(g, w, ' ')] * curr_prob[(g, ' ', h)]

    return numerator/denominator


# this method performs the M-step in the EM algorithm
# param: complete_data: dict of complete data, key: (G, W, H), value: count of (G, W, H)
# param: missing_data: dict of missing data, key: ('-', W, H), value: count of ('-', W, H)
# param: curr_prob: dict of conditional probability tables used for calculations in E-step in the current iteration
# param: iterations: count of the current iteration
# param: filename: name of dataset file
# param: log_likelihood_list: list to keep track of log likelihoods during each iteration of the EM algorithm
def M_step(complete_data, missing_data, curr_prob, iterations, filename, log_likelihood_list):
    iterations += 1 # increase the iteration by 1 every time M_step is called
    new_prob = {} # dict for the new conditional probability tables that will be calculated in the M-step
    estimated_data = E_step(missing_data, curr_prob) # call E-step method to get dict of estimated data

    # calculate P(G=0) and P(G=1) using counts from complete_data and expected counts from estimated_data
    numerator, denominator = 0, 0
    for data in complete_data:
        denominator += complete_data[data]
        if data[0] == '0':
            numerator += complete_data[data]
    for data in estimated_data:
        denominator += estimated_data[data]
        if data[0] == '0':
            numerator += estimated_data[data]
    new_prob[('0', ' ', ' ')] = numerator / denominator
    new_prob[('1', ' ', ' ')] = 1 - new_prob[('0', ' ', ' ')]

    # calculate P(W=0|G=0) and P(W=1|G=0) using counts from complete_data and expected counts from estimated_data
    numerator, denominator = 0, 0
    for data in complete_data:
        if data[0] == '0':
            denominator += complete_data[data]
            if data[1] == '0':
                numerator += complete_data[data]
    for data in estimated_data:
        if data[0] == '0':
            denominator += estimated_data[data]
            if data[1] == '0':
                numerator += estimated_data[data]
    new_prob[('0', '0', ' ')] = numerator / denominator
    new_prob[('0', '1', ' ')] = 1 - new_prob[('0', '0', ' ')]

    # calculate P(W=0|G=1) and P(W=1|G=1) using counts from complete_data and expected counts from estimated_data
    numerator, denominator = 0, 0
    for data in complete_data:
        if data[0] == '1':
            denominator += complete_data[data]
            if data[1] == '0':
                numerator += complete_data[data]
    for data in estimated_data:
        if data[0] == '1':
            denominator += estimated_data[data]
            if data[1] == '0':
                numerator += estimated_data[data]
    new_prob[('1', '0', ' ')] = numerator / denominator
    new_prob[('1', '1', ' ')] = 1 - new_prob[('1', '0', ' ')]

    # calculate P(H=0|G=0) and P(H=1|G=0) using counts from complete_data and expected counts from estimated_data
    numerator, denominator = 0, 0
    for data in complete_data:
        if data[0] == '0':
            denominator += complete_data[data]
            if data[2] == '0':
                numerator += complete_data[data]
    for data in estimated_data:
        if data[0] == '0':
            denominator += estimated_data[data]
            if data[2] == '0':
                numerator += estimated_data[data]
    new_prob[('0', ' ', '0')] = numerator / denominator
    new_prob[('0', ' ', '1')] = 1 - new_prob[('0', ' ', '0')]

    # calculate P(H=0|G=1) and P(H=1|G=1) using counts from complete_data and expected counts from estimated_data
    numerator, denominator = 0, 0
    for data in complete_data:
        if data[0] == '1':
            denominator += complete_data[data]
            if data[2] == '0':
                numerator += complete_data[data]
    for data in estimated_data:
        if data[0] == '1':
            denominator += estimated_data[data]
            if data[2] == '0':
                numerator += estimated_data[data]
    new_prob[('1', ' ', '0')] = numerator / denominator
    new_prob[('1', ' ', '1')] = 1 - new_prob[('1', ' ', '0')]

    print("iteration #", iterations)
    convergence, new_log_likelihood_list = check_convergence(complete_data, missing_data, curr_prob, new_prob, 0.0001, log_likelihood_list)

    # if convergence then print out # of iterations and final conditional probability tables
    if convergence:
        # print("iteration #", iterations)
        print("Final conditional probability tables:")
        print_conditional_prob(new_prob)
        # print(new_log_likelihood_list)
        # generate_graph(filename, new_log_likelihood_list)
    # if not convergence do another iteration of the EM algorithm using the new conditional probability tables
    else:
        M_step(complete_data, missing_data, new_prob, iterations, filename, new_log_likelihood_list)


# this method checks change of log likelihood between two iterations to determine convergence
# returns true if change of log likelihood between two iterations is less than or equal to the threshold and
# returns the current log likelihood list
# param: complete_data: dict of complete data, key: (G, W, H), value: count of (G, W, H)
# param: missing_data: dict of missing data, key: ('-', W, H), value: count of ('-', W, H)
# param: prev_prob: dict of conditional probability tables produced from the previous iteration
# param: new_prob: dict of new conditional probability tables produced from the current iteration
# param: threshold: threshold for change of log likelihood to determine convergence
def check_convergence(complete_data, missing_data, prev_prob, new_prob, threshold, log_likelihood_list):
    print("previous prob:", prev_prob)
    print("new_prob:", new_prob)
    total_log_likelihood_prev_prob, total_log_likelihood_new_prob = 0, 0

    # for each complete data row (G, W, H) in the given dataset calculate log likelihood
    for data in complete_data:
        g, w, h = data
        # P(G,W,H) = P(G) * P(W|G) * P(H|G) using probabilities from the previous probability tables
        prob_data_using_prev_prob = prev_prob[(g, ' ', ' ')] * prev_prob[(g, w, ' ')] * prev_prob[(g, ' ', h)]
        # P(G,W,H) = P(G) * P(W|G) * P(H|G) using probabilities from the new probability tables
        prob_data_using_new_prob = new_prob[(g, ' ', ' ')] * new_prob[(g, w, ' ')] * new_prob[(g, ' ', h)]
        # add log(P(G,W,H)) to the total log likelihoods
        total_log_likelihood_prev_prob += math.log(prob_data_using_prev_prob) * complete_data[data]
        total_log_likelihood_new_prob += math.log(prob_data_using_new_prob) * complete_data[data]

    # for each missing data row ('-', W, H) in the given dataset calculate log likelihood
    for data in missing_data:
        w = data[1]
        h = data[2]
        prob_data_using_prev_prob, prob_data_using_new_prob = 0, 0

        # for G=0 and G=1
        for i in range(2):
            g = str(i)
            # P(W,H) = sum_of_G P(G) * P(W|G) * P(H|G) using probabilities from the previous probability tables
            prob_data_using_prev_prob += prev_prob[(g, ' ', ' ')] * prev_prob[(g, w, ' ')] * prev_prob[(g, ' ', h)]
            # P(W,H) = sum_of_G P(G) * P(W|G) * P(H|G) using probabilities from the new probability tables
            prob_data_using_new_prob += new_prob[(g, ' ', ' ')] * new_prob[(g, w, ' ')] * new_prob[(g, ' ', h)]
            # add log(P(W,H)) to the total log likelihoods
            total_log_likelihood_prev_prob += math.log(prob_data_using_prev_prob) * missing_data[data]
            total_log_likelihood_new_prob += math.log(prob_data_using_new_prob) * missing_data[data]

    # add the new log likelihood of current iteration to the log likelihood list
    log_likelihood_list.append(total_log_likelihood_new_prob)

    # calculate change in log likelihood
    difference = abs(total_log_likelihood_prev_prob - total_log_likelihood_new_prob)
    print("curr log prob:", total_log_likelihood_prev_prob)
    print("new log prob:", total_log_likelihood_new_prob)
    print("difference:", difference)

    return difference <= threshold, log_likelihood_list


# this method prints out the conditional probability table
# param: param_dict: dict of conditional probability table
def print_conditional_prob(param_dict):
    for data in param_dict:
        if data[0] == '0':
            if data[1] == '0' and data[2] == ' ':
                print("p(weight=0|gender=0):", param_dict[('0', '0', ' ')])
            elif data[1] == '1' and data[2] == ' ':
                print("p(weight=1|gender=0):", param_dict[('0', '1', ' ')])
            elif data[1] == ' ' and data[2] == '0':
                print("p(height=0|gender=0):", param_dict[('0', ' ', '0')])
            elif data[1] == ' ' and data[2] == '1':
                print("p(height=1|gender=0):", param_dict[('0', ' ', '1')])
            else:
                print("p(gender=0):", param_dict[('0', ' ', ' ')])
        else:
            if data[1] == '0' and data[2] == ' ':
                print("p(weight=0|gender=1):", param_dict[('1', '0', ' ')])
            elif data[1] == '1' and data[2] == ' ':
                print("p(weight=1|gender=1):", param_dict[('1', '1', ' ')])
            elif data[1] == ' ' and data[2] == '0':
                print("p(height=0|gender=1):", param_dict[('1', ' ', '0')])
            elif data[1] == ' ' and data[2] == '1':
                print("p(height=1|gender=1):", param_dict[('1', ' ', '1')])
            else:
                print("p(gender=1):", param_dict[('1', ' ', ' ')])


# this method generates a plot of iteration # vs log likelihoods
# param: filename: name of dataset file
# param: log_likelihood_list: list of log likelihoods from each iteration in the EM algorithm
def generate_graph(filename, log_likelihood_list):
    plt.plot(log_likelihood_list)
    plt.title(filename)
    plt.xlabel("Iteration #")
    plt.ylabel("Log Likelihood")
    plt.show()


# g0 = float(input("Enter p(gender=0): "))
# w0_given_g0 = float(input("Enter p(weight=0|gender=0): "))
# w0_given_g1 = float(input("Enter p(weight=0|gender=1): "))
# h0_given_g0 = float(input("Enter p(height=0|gender=0): "))
# h0_given_g1 = float(input("Enter p(height=0|gender=1): "))

# prior_prob = prior_parameter(g0, w0_given_g0, w0_given_g1, h0_given_g0, h0_given_g1)
prior_prob = prior_parameter(0.7, 0.8, 0.4, 0.7, 0.3)

complete_data10, missing_data10 = read_data('hw2dataset_10.txt')
complete_data30, missing_data30 = read_data('hw2dataset_30.txt')
complete_data50, missing_data50 = read_data('hw2dataset_50.txt')
complete_data70, missing_data70 = read_data('hw2dataset_70.txt')
complete_data100, missing_data100 = read_data('hw2dataset_100.txt')

log_likelihood_list_dataset10 = calc_log_prob_iteration0(complete_data10, missing_data10, prior_prob)
log_likelihood_list_dataset30 = calc_log_prob_iteration0(complete_data30, missing_data30, prior_prob)
log_likelihood_list_dataset50 = calc_log_prob_iteration0(complete_data50, missing_data50, prior_prob)
log_likelihood_list_dataset70 = calc_log_prob_iteration0(complete_data70, missing_data70, prior_prob)
log_likelihood_list_dataset100 = calc_log_prob_iteration0(complete_data100, missing_data100, prior_prob)

print('hw2dataset_10.txt')
M_step(complete_data10, missing_data10, prior_prob, 0, 'hw2dataset_10.txt', log_likelihood_list_dataset10)
# print('\nhw2dataset_30.txt')
# M_step(complete_data30, missing_data30, prior_prob, 0, 'hw2dataset_30.txt', log_likelihood_list_dataset30)
# print('\nhw2dataset_50.txt')
# M_step(complete_data50, missing_data50, prior_prob, 0, 'hw2dataset_50.txt', log_likelihood_list_dataset50)
# print('\nhw2dataset_70.txt')
# M_step(complete_data70, missing_data70, prior_prob, 0, 'hw2dataset_70.txt', log_likelihood_list_dataset70)
# print('\nhw2dataset_100.txt')
# M_step(complete_data100, missing_data100, prior_prob, 0, 'hw2dataset_100.txt', log_likelihood_list_dataset100)
