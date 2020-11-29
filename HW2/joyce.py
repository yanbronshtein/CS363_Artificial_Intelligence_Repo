# Author: Joyce Tan
import math

def read_data(filename):
    dataset = {}
    missing = {}
    with open(filename) as file:
        for line in file:
            line = line.split()
            if line[0] != 'Gender':
                gender = line[0]
                weight = line[1]
                height = line[2]
                if gender != '-':
                    if (gender, weight, height) in dataset:
                        dataset[(gender, weight, height)] += 1
                    else:
                        dataset[(gender, weight, height)] = 1
                else:
                    if ('-', weight, height) in missing:
                        missing[('-', weight, height)] += 1
                    else:
                        missing[('-', weight, height)] = 1

    return dataset, missing


def prior_parameter(g0, w0_given_g0, w0_given_g1, h0_given_g0, h0_given_g1):
    prior_prob = {}
    prior_prob[('0', 'd', 'd')] = g0
    prior_prob[('1', 'd', 'd')] = 1 - g0
    prior_prob[('0', '0', 'd')] = w0_given_g0
    prior_prob[('0', '1', 'd')] = 1 - w0_given_g0
    prior_prob[('1', '0', 'd')] = w0_given_g1
    prior_prob[('1', '1', 'd')] = 1 - w0_given_g1
    prior_prob[('0', 'd', '0')] = h0_given_g0
    prior_prob[('0', 'd', '1')] = 1 - h0_given_g0
    prior_prob[('1', 'd', '0')] = h0_given_g1
    prior_prob[('1', 'd', '1')] = 1 - h0_given_g1

    return prior_prob


def E_step(missing_data, curr_param):
    estimated_data = {}

    for tuple in missing_data:
        numerator, denominator = 0, 0

        # estimate p(gender|weight=0,height=0)
        if tuple == ('-', '0', '0'):
            numerator = curr_param[('0', 'd', 'd')] * curr_param[('0','0','d')] * curr_param[('0', 'd', '0')]
            for i in range(2):
                g = str(i)
                denominator += curr_param[(g, 'd', 'd')] * curr_param[(g,'0','d')] * curr_param[(g, 'd', '0')]
            estimated_data[('0', '0', '0')] = (numerator/denominator) * missing_data[('-', '0', '0')]
            estimated_data[('1', '0', '0')] = 1 - estimated_data[('0', '0', '0')]

        # estimate p(gender|weight=0,height=1)
        elif tuple == ('-', '0', '1'):
            numerator = curr_param[('0', 'd', 'd')] * curr_param[('0', '0', 'd')] * curr_param[('0', 'd', '1')]
            for i in range(2):
                g = str(i)
                denominator += curr_param[(g, 'd', 'd')] * curr_param[(g, '0', 'd')] * curr_param[(g, 'd', '1')]
            estimated_data[('0', '0', '1')] = (numerator/denominator) * missing_data[('-', '0', '1')]
            estimated_data[('1', '0', '1')] = 1 - estimated_data[('0', '0', '1')]

        # estimate p(gender|weight=1,height=0)
        elif tuple == ('-', '1', '0'):
            numerator = curr_param[('0', 'd', 'd')] * curr_param[('0', '1', 'd')] * curr_param[('0', 'd', '0')]
            for i in range(2):
                g = str(i)
                denominator += curr_param[(g, 'd', 'd')] * curr_param[(g, '1', 'd')] * curr_param[(g, 'd', '0')]
            estimated_data[('0', '1', '0')] = (numerator/denominator) * missing_data[('-', '1', '0')]
            estimated_data[('1', '1', '0')] = 1 - estimated_data[('0', '1', '0')]

        # estimate p(gender|weight=1,height=1)
        else:
            numerator = curr_param[('0', 'd', 'd')] * curr_param[('0', '1', 'd')] * curr_param[('0', 'd', '1')]
            for i in range(2):
                g = str(i)
                denominator += curr_param[(g, 'd', 'd')] * curr_param[(g, '1', 'd')] * curr_param[(g, 'd', '1')]
            estimated_data[('0', '1', '1')] = (numerator/denominator) * missing_data[('-', '1', '1')]
            estimated_data[('1', '1', '1')] = 1 - estimated_data[('0', '1', '1')]

    return estimated_data


def M_step(given_data, missing_data, prior_param):
    new_param = {}
    estimated_data = E_step(missing_10, prior_param)

    # calculate p(gender=0) and p(gender=1)
    numerator, denominator = 0, 0
    for tuple in given_data:
        denominator += given_data[tuple]
        if tuple[0] == '0':
            numerator += given_data[tuple]
    for tuple in estimated_data:
        denominator += estimated_data[tuple]
        if tuple[0] == '0':
            numerator += estimated_data[tuple]
    new_param[('0', 'd', 'd')] = numerator/denominator
    new_param[('1', 'd', 'd')] = 1 - new_param[('0', 'd', 'd')]

    # calculate p(weight=0|gender=0) and p(weight=1|gender=0)
    numerator, denominator = 0, 0
    for tuple in given_data:
        if tuple[0] == '0':
            denominator += given_data[tuple]
            if tuple[1] == '0':
                numerator += given_data[tuple]
    for tuple in estimated_data:
        if tuple[0] == '0':
            denominator += estimated_data[tuple]
            if tuple[1] == '0':
                numerator += estimated_data[tuple]
    new_param[('0', '0', 'd')] = numerator/denominator
    new_param[('0', '1', 'd')] = 1 - new_param[('0', '0', 'd')]

    # calculate p(weight=0|gender=1) and p(weight=1|gender=1)
    numerator, denominator = 0, 0
    for tuple in given_data:
        if tuple[0] == '1':
            denominator += given_data[tuple]
            if tuple[1] == '0':
                numerator += given_data[tuple]
    for tuple in estimated_data:
        if tuple[0] == '1':
            denominator += estimated_data[tuple]
            if tuple[1] == '0':
                numerator += estimated_data[tuple]
    new_param[('1', '0', 'd')] = numerator/denominator
    new_param[('1', '1', 'd')] = 1 - new_param[('1', '0', 'd')]

    # calculate p(height=0|gender=0) and p(height=1|gender=0)
    numerator, denominator = 0, 0
    for tuple in given_data:
        if tuple[0] == '0':
            denominator += given_data[tuple]
            if tuple[2] == '0':
                numerator += given_data[tuple]
    for tuple in estimated_data:
        if tuple[0] == '0':
            denominator += estimated_data[tuple]
            if tuple[2] == '0':
                numerator += estimated_data[tuple]
    new_param[('0', 'd', '0')] = numerator/denominator
    new_param[('0', 'd', '1')] = 1 - new_param[('0', 'd', '0')]

    # calculate p(height=0|gender=1) and p(height=1|gender=1)
    numerator, denominator = 0, 0
    for tuple in given_data:
        if tuple[0] == '1':
            denominator += given_data[tuple]
            if tuple[2] == '0':
                numerator += given_data[tuple]
    for tuple in estimated_data:
        if tuple[0] == '1':
            denominator += estimated_data[tuple]
            if tuple[2] == '0':
                numerator += estimated_data[tuple]
    new_param[('1', 'd', '0')] = numerator/denominator
    new_param[('1', 'd', '1')] = 1 - new_param[('1', 'd', '0')]

    return new_param

prior_param = prior_parameter(0.7, 0.8, 0.4, 0.7, 0.3)

dataset_10, missing_10 = read_data('hw2dataset_30.txt')
# dataset_30, missing_30 = read_data('hw2dataset_30.txt')
# dataset_50, missing_50 = read_data('hw2dataset_50.txt')
# dataset_70, missing_70 = read_data('hw2dataset_70.txt')
# dataset_100, missing_100 = read_data('hw2dataset_100.txt')

print("given data:", dataset_10)
print("missing data:", missing_10)

expected_data10 = E_step(missing_10, prior_param)
print("estimated data:", expected_data10)
M_step_data10 = M_step(dataset_10, missing_10, prior_param)
print("new param:", M_step_data10)