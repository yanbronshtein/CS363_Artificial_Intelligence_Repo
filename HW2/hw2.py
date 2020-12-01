import os
import sys
import math

try:
    import matplotlib.pyplot as plt
    import pandas as pd
except ImportError:
    os.system("pip install matplotlib")
    os.system("pip install pandas")



class EM:
    def __init__(self, gender_0, weight_0_given_gender_0, weight_0_given_gender_1, height_0_given_gender_0,
                 height_0_given_gender1, filename: str, threshold):
        self.threshold = threshold
        self.iterations = 0
        self.log_likelihood_list = list()
        sys.setrecursionlimit(2000)

        self.theta_dict = dict({
            ('0', 'x', 'x'): gender_0,
            ('1', 'x', 'x'): 1 - gender_0,
            ('0', '0', 'x'): weight_0_given_gender_0,
            ('0', '1', 'x'): 1 - weight_0_given_gender_0,
            ('1', '0', 'x'): weight_0_given_gender_1,
            ('1', '1', 'x'): 1 - weight_0_given_gender_1,
            ('0', 'x', '0'): height_0_given_gender_0,
            ('0', 'x', '1'): 1 - height_0_given_gender_0,
            ('1', 'x', '0'): height_0_given_gender1,
            ('1', 'x', '1'): 1 - height_0_given_gender1
        })

        log_prob = 0
        for key in self.theta_dict:
            log_prob += math.log(self.theta_dict[key])

        self.log_likelihood_list.append(log_prob)
        self.filename = filename
        self.m_step(self.theta_dict, self.filename)

    def e_step(self, theta_dict, filename):
        data_dict = parse_data(filename)
        expected_data_dict = data_dict.copy()
        entry_options = [
            ('-', '1', '1'),
            ('-', '1', '0'),
            ('-', '0', '0'),
            ('-', '0', '1')
        ]

        for entry in data_dict:
            # estimate p(gender|weight=1,height=1)
            if entry == entry_options[0]:
                d = 0
                n = theta_dict[('0', 'x', 'x')] * theta_dict[('0', '1', 'x')] * theta_dict[('0', 'x', '1')]

                d += theta_dict[('0', 'x', 'x')] * theta_dict[('0', '1', 'x')] * theta_dict[('0', 'x', '1')]
                d += theta_dict[('1', 'x', 'x')] * theta_dict[('1', '1', 'x')] * theta_dict[('1', 'x', '1')]

                if ('0', '1', '1') in expected_data_dict:
                    expected_data_dict[('0', '1', '1')] += (n / d) * expected_data_dict[('-', '1', '1')]
                else:
                    expected_data_dict[('0', '1', '1')] = (n / d) * expected_data_dict[('-', '1', '1')]

                if ('1', '1', '1') in expected_data_dict:
                    expected_data_dict[('1', '1', '1')] += (1 - (n / d)) * expected_data_dict[('-', '1', '1')]
                else:
                    expected_data_dict[('1', '1', '1')] = (1 - (n / d)) * expected_data_dict[('-', '1', '1')]

                    # estimate p(gender|weight=1,height=0)
            elif entry == entry_options[1]:
                d = 0
                n = theta_dict[('0', 'x', 'x')] * theta_dict[('0', '1', 'x')] * theta_dict[('0', 'x', '0')]

                d += theta_dict[('0', 'x', 'x')] * theta_dict[('0', '1', 'x')] * theta_dict[('0', 'x', '0')]
                d += theta_dict[('1', 'x', 'x')] * theta_dict[('1', '1', 'x')] * theta_dict[('1', 'x', '0')]

                if ('0', '1', '0') in expected_data_dict:
                    expected_data_dict[('0', '1', '0')] += (n / d) * expected_data_dict[('-', '1', '0')]
                else:
                    expected_data_dict[('0', '1', '0')] = (n / d) * expected_data_dict[('-', '1', '0')]

                if ('1', '1', '0') in expected_data_dict:
                    expected_data_dict[('1', '1', '0')] += (1 - (n / d)) * expected_data_dict[('-', '1', '0')]
                else:
                    expected_data_dict[('1', '1', '0')] = (1 - (n / d)) * expected_data_dict[('-', '1', '0')]


            # estimate p(gender|weight=0,height=0)
            elif entry == entry_options[2]:
                d = 0
                n = theta_dict[('0', 'x', 'x')] * theta_dict[('0', '0', 'x')] * theta_dict[('0', 'x', '0')]

                d += theta_dict[('0', 'x', 'x')] * theta_dict[('0', '0', 'x')] * theta_dict[('0', 'x', '0')]
                d += theta_dict[('1', 'x', 'x')] * theta_dict[('1', '0', 'x')] * theta_dict[('1', 'x', '0')]

                if ('0', '0', '0') in expected_data_dict:
                    expected_data_dict[('0', '0', '0')] += (n / d) * expected_data_dict[('-', '0', '0')]
                else:
                    expected_data_dict[('0', '0', '0')] = (n / d) * expected_data_dict[('-', '0', '0')]

                if ('1', '0', '0') in expected_data_dict:
                    expected_data_dict[('1', '0', '0')] += (1 - (n / d)) * expected_data_dict[('-', '0', '0')]
                else:
                    expected_data_dict[('1', '0', '0')] = (1 - (n / d)) * expected_data_dict[('-', '0', '0')]

                    # estimate p(gender|weight=0,height=1)
            elif entry == entry_options[3]:
                d = 0
                n = theta_dict[('0', 'x', 'x')] * theta_dict[('0', '0', 'x')] * theta_dict[('0', 'x', '1')]

                d += theta_dict[('0', 'x', 'x')] * theta_dict[('0', '0', 'x')] * theta_dict[('0', 'x', '1')]
                d += theta_dict[('1', 'x', 'x')] * theta_dict[('1', '0', 'x')] * theta_dict[('1', 'x', '1')]

                if ('0', '0', '1') in expected_data_dict:
                    expected_data_dict[('0', '0', '1')] += (n / d) * expected_data_dict[('-', '0', '1')]
                else:
                    expected_data_dict[('0', '0', '1')] = (n / d) * expected_data_dict[('-', '0', '1')]

                if ('1', '0', '1') in expected_data_dict:
                    expected_data_dict[('1', '0', '1')] += (1 - (n / d)) * expected_data_dict[('-', '0', '1')]
                else:
                    expected_data_dict[('1', '0', '1')] = (1 - (n / d)) * expected_data_dict[('-', '0', '1')]

            else:
                continue
        return expected_data_dict

    def m_step(self, theta_dict, filename):
        # global iterations
        self.iterations += 1
        new_param_dict = dict()
        expected_data_dict = self.e_step(theta_dict, filename)

        # calculate p(gender=0) and p(gender=1)
        n = 0
        d = 0

        for key in expected_data_dict:
            if key[0] == '-':
                continue
            else:
                d += expected_data_dict[key]
                if key[0] == '0':
                    n += expected_data_dict[key]
        new_param_dict[('0', 'x', 'x')] = n / d
        new_param_dict[('1', 'x', 'x')] = 1 - new_param_dict[('0', 'x', 'x')]

        # calculate p(weight=0|gender=0) and p(weight=1|gender=0)
        n = 0
        d = 0

        for key in expected_data_dict:
            if key[0] == '-':
                continue
            else:
                if key[0] == '0':
                    d += expected_data_dict[key]
                    if key[1] == '0':
                        n += expected_data_dict[key]
        new_param_dict[('0', '0', 'x')] = n / d
        new_param_dict[('0', '1', 'x')] = 1 - new_param_dict[('0', '0', 'x')]

        # calculate p(weight=0|gender=1) and p(weight=1|gender=1)
        n = 0
        d = 0
        for key in expected_data_dict:
            if key[0] == '-':
                continue
            else:
                if key[0] == '1':
                    d += expected_data_dict[key]
                    if key[1] == '0':
                        n += expected_data_dict[key]
        new_param_dict[('1', '0', 'x')] = n / d
        new_param_dict[('1', '1', 'x')] = 1 - new_param_dict[('1', '0', 'x')]

        # calculate p(height=0|gender=0) and p(height=1|gender=0)
        n = 0
        d = 0
        for key in expected_data_dict:
            if key[0] == '-':
                continue
            else:
                if key[0] == '0':
                    d += expected_data_dict[key]
                    if key[2] == '0':
                        n += expected_data_dict[key]
        new_param_dict[('0', 'x', '0')] = n / d
        new_param_dict[('0', 'x', '1')] = 1 - new_param_dict[('0', 'x', '0')]

        # calculate p(height=0|gender=1) and p(height=1|gender=1)
        n = 0
        d = 0
        for key in expected_data_dict:
            if key[0] == '-':
                continue
            else:
                if key[0] == '1':
                    d += expected_data_dict[key]
                    if key[2] == '0':
                        n += expected_data_dict[key]
        new_param_dict[('1', 'x', '0')] = n / d
        new_param_dict[('1', 'x', '1')] = 1 - new_param_dict[('1', 'x', '0')]

        if self.has_converged(theta_dict, new_param_dict, self.threshold):
            print("Total Iterations", self.iterations)
            print("Final conditional probability tables:")
            print_conditional_prob(new_param_dict)
        else:
            self.m_step(new_param_dict, filename)

    def has_converged(self, curr_param_dict, new_param_dict, threshold):
        log_likelihood_curr_param = 0
        log_likelihood_new_param = 0
        for key in curr_param_dict:
            if curr_param_dict[key] == 0.0 or new_param_dict[key] == 0.0:
                continue
            else:
                log_likelihood_curr_param += math.log(curr_param_dict[key])
                log_likelihood_new_param += math.log(new_param_dict[key])

        self.log_likelihood_list.append(log_likelihood_new_param)

        difference = math.fabs(log_likelihood_curr_param - log_likelihood_new_param)
        if difference <= self.threshold:
            return True
        else:
            return False

"""
Hint: E-step of the EM algorithm is essentially estimating the probabilities of different 
values of Gender given that we know a person’s Weight and Height, i.e., 
P(Gender | Weight, Height), and use these estimations as if they are our (expected) counts.

P(Gender | Weight, Height) = [P(Weight|Gender) * P(Height|Gender) * P(Gender)] / P(Weight,Height)
"""


def parse_data(filename):
    file_obj = open(filename, 'r')
    data_dict = dict()
    for line in file_obj.readlines():
        line = line.strip().split()  # Trim and tokenize line
        if line[0] == "Gender":  # Skip the first line with the labels
            continue
        line_tuple = tuple(line)
        if line_tuple in data_dict:
            data_dict[line_tuple] += 1
        else:
            data_dict[line_tuple] = 1

    return data_dict


'''
P(G|W,H) = P(G,W,H) / P(W,H)
P(G,W,H) = P(G)*P(W|G)*P(H|G)
P(W,H) = SUM_OVER_G( P(G)*P(W|G)*P(H|G) ) 

'''


def print_conditional_prob(param_dict):

    for key in param_dict:
        if key[0] == '0':
            if key[1] == '0' and key[2] == 'x':
                print("p(weight=0|gender=0):", param_dict[('0', '0', 'x')])
            elif key[1] == '1' and key[2] == 'x':
                print("p(weight=1|gender=0):", param_dict[('0', '1', 'x')])
            elif key[1] == 'x' and key[2] == '0':
                print("p(height=0|gender=0):", param_dict[('0', 'x', '0')])
            elif key[1] == 'x' and key[2] == '1':
                print("p(height=1|gender=0):", param_dict[('0', 'x', '1')])
            else:
                print("p(gender=0):", param_dict[('0', 'x', 'x')])
        else:
            if key[1] == '0' and key[2] == 'x':
                print("p(weight=0|gender=1):", param_dict[('1', '0', 'x')])
            elif key[1] == '1' and key[2] == 'x':
                print("p(weight=1|gender=1):", param_dict[('1', '1', 'x')])
            elif key[1] == 'x' and key[2] == '0':
                print("p(height=0|gender=1):", param_dict[('1', 'x', '0')])
            elif key[1] == 'x' and key[2] == '1':
                print("p(height=1|gender=1):", param_dict[('1', 'x', '1')])
            else:
                print("p(gender=1):", param_dict[('1', 'x', 'x')])



def main():
    files = [
        'hw2dataset_10.txt',
        'hw2dataset_30.txt',
        'hw2dataset_50.txt',
        'hw2dataset_70.txt',
        'hw2dataset_100.txt'

    ]

    em_10_percent = EM(gender_0=0.7, weight_0_given_gender_0=0.8,
                       weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3,
                       filename=files[0], threshold=0.0001)
    em_30_percent = EM(gender_0=0.7, weight_0_given_gender_0=0.8,
                       weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3,
                       filename=files[1], threshold=0.0001)

    #
    em_50_percent = EM(gender_0=0.7, weight_0_given_gender_0=0.8,
                       weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3,
                       filename=files[2], threshold=0.0001)

    #
    em_70_percent = EM(gender_0=0.7, weight_0_given_gender_0=0.8,
                       weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3,
                       filename=files[3], threshold=0.0001)
    #
    em_100_percent = EM(gender_0=0.7, weight_0_given_gender_0=0.8,
                        weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3,
                        filename=files[4], threshold=0.0001)



    # plt.plot(Y)
    # plt.title("Yoyograph")
    # plt.xlabel("#Iterations")
    # plt.ylabel("Log likelihood")
    #
    # plt.show()


if __name__ == '__main__':
    main()