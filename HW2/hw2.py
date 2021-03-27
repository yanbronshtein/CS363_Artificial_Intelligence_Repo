"""
This program implements the EM(Expectation Maximization) algorithm for learning parameters for a simple Bayesian
network from missing data
E-step of the EM algorithm is essentially estimating the probabilities of different
values of Gender given that we know a person’s Weight and Height, i.e.,
P(Gender | Weight, Height), and use these estimations as if they are our (expected) counts.

P(Gender | Weight, Height) = [P(Weight|Gender) * P(Height|Gender) * P(Gender)] / P(Weight,Height)
"""

__author___ = "Yaniv Bronshtein"
__version__ = "1.0"

# Standard libraries
import os
import math
import random

# Importing non-standard libraries that require pip to install
from typing import List

try:
    import matplotlib.pyplot as plt
    import pandas as pd
except ImportError:
    os.system("pip3 install matplotlib")
    os.system("pip3 install pandas")

"""
This class implements Expectation Maximization
"""


class EM:

    def __init__(self, g_0, w_0_given_g_0, w0_given_g0_1, h_0_given_g_0,
                 h_0_given_g1, filename: str, threshold, make_graph=False):
        """
        Default constructor for EM class
        :param g_0:  P(Gender=0)
        :param w_0_given_g_0: P(Weight=0|Gender=0)
        :param w0_given_g0_1: P(Weight=0|Gender=1)
        :param h_0_given_g_0: P(height=0|Gender=0)
        :param h_0_given_g1: P(height=0|Gender=1)
        :param filename: File of this form:"hw2dataset_{%missing_data}.txt"
        :param threshold: Threshold for convergence
        :param make_graph Tells EM whether to generate matplotlib or not
        """
        self.make_graph = make_graph
        self.threshold = threshold  # Threshold for convergence testing
        self.iterations = 0  # Stores the number of iterations of the EM algorithm
        self.log_likelihood_list = []  # List to store log_likelihoods for a given iteration of EM

        self.known_data_options = [
            ('0', 'x', 'x'),
            ('1', 'x', 'x'),

            ('0', '0', 'x'),
            ('0', '1', 'x'),

            ('1', '0', 'x'),
            ('1', '1', 'x'),

            ('0', 'x', '0'),
            ('0', 'x', '1'),

            ('1', 'x', '0'),
            ('1', 'x', '1')
        ]

        self.theta_dict = dict({  # Dictionary that stores the initial parameters and their complements in a dictionary
            ('0', 'x', 'x'): g_0,
            ('1', 'x', 'x'): 1 - g_0,

            ('0', '0', 'x'): w_0_given_g_0,
            ('0', '1', 'x'): 1 - w_0_given_g_0,

            ('1', '0', 'x'): w0_given_g0_1,
            ('1', '1', 'x'): 1 - w0_given_g0_1,

            ('0', 'x', '0'): h_0_given_g_0,
            ('0', 'x', '1'): 1 - h_0_given_g_0,

            ('1', 'x', '0'): h_0_given_g1,
            ('1', 'x', '1'): 1 - h_0_given_g1
        })

        self.operations = [
            'A',  # Compute P(Gender=0) and P(Gender=1)
            'B',  # Compute P(Weight=0|Gender=0) and P(Weight=1|Gender=0)
            'C',  # Compute P(Weight=0|Gender=1) and P(Weight=1|Gender=1)
            'D',  # Compute P(Height=0|Gender=0) and P(Height=1|Gender=0)
            'E',  # Compute P(Height=0|Gender=1) and P(Height=1|Gender=1)
        ]

        self.filename = filename
        self.m_step(self.theta_dict, self.filename)  # Call m_step to begin the algorithm

    def e_step(self, data_dict, theta_dict):
        """
        This method calculates the expectation for the current step to be used during the m-step using the following
        formulas
        P(Gender|Weight,Height) = P(Gender,Weight,Height) / P(Weight,Height)
        P(Gender,Weight,Height) = P(Gender)*P(Weight|Gender)*P(Height|Gender)
        P(Weight,Height) = SUM_OVER_Gender( P(Gender)*P(Weight|Gender)*P(Height|Gender) )

        :param theta_dict: current parameters
        :param filename: Name of file to be parsed
        :return: Dictionary of expected values
        """
        # data_dict = parse_data(filename)
        expected_data_dict = data_dict.copy()  # At this point contains the current frequencies for tuples
        # All possible missing data tuples
        entry_options = [
            ('-', '1', '1'),
            ('-', '1', '0'),
            ('-', '0', '0'),
            ('-', '0', '1')
        ]

        for entry in data_dict:
            # estimate p(gender|Weight=1,Height=1)
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

            # estimate P(Gender|Weight=1,Height=0)
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

            # estimate P(Gender|Weight=0,Height=0)
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

            # estimate P(Gender|Weight=0,Height=1)
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
        """
        This method computes
        :param theta_dict: dictionary of current parameters to be updated in the e_step
        :param filename: data set
        :return:recursive call to m_step or call to print results
        """
        data_dict = parse_data(filename)
        expected_data_dict = self.e_step(data_dict, theta_dict)  # Calculate the expectations

        # Computer the new parameters
        new_param_dict = self.compute_new_params(expected_data_dict=expected_data_dict, new_param_dict=dict(),
                                                 op_index=-1)

        # Check if it is time to halt the EM algorithm. Call print_em_results() if that is the case

        self.iterations += 1

        has_converged = self.has_converged(data_dict, theta_dict, new_param_dict, self.threshold)
        if has_converged:
            self.print_em_results(new_param_dict)
        else:
            self.m_step(new_param_dict, filename)

    def compute_new_params(self, expected_data_dict, new_param_dict, op_index):
        """
        This recursive method computes the probabilities necessary for the tables Gender, Weight|Gender,
        and Height|Gender
        :param expected_data_dict: Current expectations
        :param new_param_dict: new_parameters, Initially this is usually empty dictionary
        :param op_index: index of operation to be performed in operations list. Initially this is usually -1
        :return: updated new_param_dict after all operations have been performed
        """
        n = 0
        d = 0
        if op_index + 1 >= len(self.operations):
            return new_param_dict

        op_index += 1

        for key in expected_data_dict:
            # If the first element is '-' we are looking at missing data; skip
            if key[0] == '-':
                continue
            else:  # Calculate the numerator and denominator depending on the operation
                if self.operations[op_index] == 'A':
                    d += expected_data_dict[key]
                    if key[0] == '0':
                        n += expected_data_dict[key]
                elif self.operations[op_index] == 'B':
                    if key[0] == '0':
                        d += expected_data_dict[key]
                        if key[1] == '0':
                            n += expected_data_dict[key]
                elif self.operations[op_index] == 'C':
                    if key[0] == '1':
                        d += expected_data_dict[key]
                        if key[1] == '0':
                            n += expected_data_dict[key]
                elif self.operations[op_index] == 'D':
                    if key[0] == '0':
                        d += expected_data_dict[key]
                        if key[2] == '0':
                            n += expected_data_dict[key]
                elif self.operations[op_index] == 'E':
                    if key[0] == '1':
                        d += expected_data_dict[key]
                        if key[2] == '0':
                            n += expected_data_dict[key]
                else:
                    break

        if self.operations[op_index] == 'A':
            new_param_dict[self.known_data_options[0]] = n / d
            new_param_dict[self.known_data_options[1]] = 1 - new_param_dict[self.known_data_options[0]]

        elif self.operations[op_index] == 'B':
            new_param_dict[self.known_data_options[2]] = n / d
            new_param_dict[self.known_data_options[3]] = 1 - new_param_dict[self.known_data_options[2]]

        elif self.operations[op_index] == 'C':
            new_param_dict[self.known_data_options[4]] = n / d
            new_param_dict[self.known_data_options[5]] = 1 - new_param_dict[self.known_data_options[4]]

        elif self.operations[op_index] == 'D':
            new_param_dict[self.known_data_options[6]] = n / d
            new_param_dict[self.known_data_options[7]] = 1 - new_param_dict[self.known_data_options[6]]

        elif self.operations[op_index] == 'E':
            new_param_dict[self.known_data_options[8]] = n / d
            new_param_dict[self.known_data_options[9]] = 1 - new_param_dict[self.known_data_options[8]]

        return self.compute_new_params(expected_data_dict, new_param_dict, op_index)

    def has_converged(self, data_dict, curr_param_dict, new_param_dict, threshold):
        """
        This method determines whether to stop the EM algorithm. It calculates the difference of log_likelihoods
        between the current learned parameters and the newly learned parameters.
        If the difference is under the threshold, the method returns True
        :param data_dict: dict containing data necessary
        :param curr_param_dict: Current learned parameters for the given Bayesian Network
        :param new_param_dict: Newly learned parameters for the given Bayesian Network
        :param threshold: Threshold provided by the user for halting EM algorithm
        :return: True if it is time to halt the EM algorithm and False otherwise
        """

        log_likelihood_curr_param = 0
        log_likelihood_new_param = 0
        for key in data_dict:
            g, w, h = key
            prob_using_curr_param_dict = 0
            prob_using_new_param_dict = 0
            # if key starts with '-' we must compute log(P(W,H))
            if g == '-':
                # P(W,H) = SUM OVER G of P(G) * P(W|G) * P(H|G) using probabilities from the current param dict
                prob_using_curr_param_dict += curr_param_dict[('0', 'x', 'x')] * curr_param_dict[('0', w, 'x')] * \
                                              curr_param_dict[('0', 'x', h)]
                prob_using_curr_param_dict += curr_param_dict[('1', 'x', 'x')] * curr_param_dict[('1', w, 'x')] * \
                                              curr_param_dict[('1', 'x', h)]
                # P(W,H) = SUM OVER G of  P(G) * P(W|G) * P(H|G) using probabilities from the new param dict
                prob_using_new_param_dict += new_param_dict[('0', 'x', 'x')] * new_param_dict[('0', w, 'x')] * \
                                             new_param_dict[('0', 'x', h)]
                prob_using_new_param_dict += new_param_dict[('1', 'x', 'x')] * new_param_dict[('1', w, 'x')] * \
                                             new_param_dict[('1', 'x', h)]

            # else key is a complete data (G,W,H) then calculate log(P(G,W,H))
            else:
                # Compute P(G,W,H) using probabilities from the current param dict
                prob_using_curr_param_dict = curr_param_dict[(g, 'x', 'x')] * curr_param_dict[(g, w, 'x')] * \
                                             curr_param_dict[(g, 'x', h)]
                # Compute P(G,W,H) using probabilities from the new param dict
                prob_using_new_param_dict = new_param_dict[(g, 'x', 'x')] * new_param_dict[(g, w, 'x')] * \
                                            new_param_dict[(g, 'x', h)]

            # Increment by log(P(W,H)) to the total log probabilities
            log_likelihood_curr_param += math.log(prob_using_curr_param_dict) * data_dict[key]
            log_likelihood_new_param += math.log(prob_using_new_param_dict) * data_dict[key]

        # In the first iteration, we must add the curr log likelihood in addition to the new log_likelihood
        if self.iterations == 1:
            self.log_likelihood_list.append(log_likelihood_curr_param)
        self.log_likelihood_list.append(log_likelihood_new_param)

        delta_log_likelihood = math.fabs(log_likelihood_curr_param - log_likelihood_new_param)

        if delta_log_likelihood <= threshold:
            return True
        else:
            return False

    def print_em_results(self, param_dict):
        """
        This method creates a DataFrame for each of the three tables required:
        Gender Table, Weight|Gender Table, and Height|Gender Table and prints the DataFrames as strings
        After the printing is done, generate_graph() is called to create the Log Likelihood vs Iterations pyplot
        :param param_dict: Dictionary of Final learned parameters
        :return: None
        """
        gender_df = pd.DataFrame()
        weight_given_gender_df = pd.DataFrame()
        height_given_gender_df = pd.DataFrame()

        print("total iterations:", self.iterations)
        print("----------------------------------------Gender Table----------------------------------------")
        gender_df["P(Gender=0)"] = [param_dict[('0', 'x', 'x')]]
        gender_df["P(Gender=1)"] = [param_dict[('1', 'x', 'x')]]
        print(gender_df.to_string(index=False))
        print("\n")
        print("----------------------------------------Weight|Gender Table---------------------------------")

        weight_given_gender_df["P(Weight=0|Gender=0)"] = [param_dict[('0', '0', 'x')]]
        weight_given_gender_df["P(Weight=1|Gender=0)"] = [param_dict[('0', '1', 'x')]]
        weight_given_gender_df["P(Weight=0|Gender=1)"] = [param_dict[('1', '0', 'x')]]
        weight_given_gender_df["P(Weight=1|Gender=1)"] = [param_dict[('1', '1', 'x')]]
        print(weight_given_gender_df.to_string(index=False))
        print("\n")
        print("----------------------------------------Height|Gender Table---------------------------------")

        height_given_gender_df["P(Height=0|Gender=0)"] = [param_dict[('0', 'x', '0')]]
        height_given_gender_df["P(Height=1|Gender=0)"] = [param_dict[('0', 'x', '1')]]
        height_given_gender_df["P(Height=0|Gender=1)"] = [param_dict[('1', 'x', '0')]]
        height_given_gender_df["P(Height=1|Gender=1)"] = [param_dict[('1', 'x', '1')]]
        print(height_given_gender_df.to_string(index=False))
        print("\n")
        # print(
        #     "--------------------------------------------------------------------------------------------")
        if self.make_graph:
            self.generate_graph()

    def generate_graph(self):
        """
        This method prints the Log Likelihood vs Iterations of the EM algorithm for the given
        file that the EM algorithm is run on
        :return: None
        """
        plt.plot(self.log_likelihood_list, color='magenta', marker='o')
        plt.title(self.filename)
        plt.xlabel("#Iterations")
        plt.ylabel("Log likelihood")
        plt.show()


def parse_data(filename):
    """
    This function parses the given dataset files and stores all the tuples in a dictionary
    :param filename: String file name
    :return: populated dictionary
    """
    file_obj = open(filename, 'r')
    data_dict = dict()  # Create an empty dictionary for reading in the data key=tuple val=frequency
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


def generate_probabilities():
    """
    This function uses random.uniform() method from python's random library to generate 5 probabilities
    to be used as input for two test cases
    :return:
    """
    x = []
    for i in range(5):
        x.append(random.uniform(0, 1))
    return x


def create_prior_prob_df(list_of_prob: List[float]):
    """
    Given list of 5 probabilities
    create the data frame and return the stringified version of it
    :param list_of_prob: list of 5 probabilities
    :return: Stringified dataframe
    """
    df = pd.DataFrame()
    df["P(Gender=0)"] = [list_of_prob[0]]
    df["P(Weight=0|Gender=0)"] = [list_of_prob[1]]
    df["P(Weight=0|Gender=1)"] = [list_of_prob[2]]
    df["P(Height=0|Gender=0)"] = [list_of_prob[3]]
    df["P(Height=0|Gender=1)"] = [list_of_prob[4]]
    return df.to_string(index=False)


def main():
    # List of files
    f = [
        'hw2dataset_10.txt',
        'hw2dataset_30.txt',
        'hw2dataset_50.txt',
        'hw2dataset_70.txt',
        'hw2dataset_100.txt'
    ]

    """
    Give prior probabilities
    """
    given_probs = [0.7, 0.8, 0.4, 0.7, 0.3]
    """
       Random probabilities
    """
    test_1_probs = generate_probabilities()
    test_2_probs = generate_probabilities()


    """
    Non-random probabilities
    """
    test_3_probs = [0.1, 0.1, 0.1, 0.1, 0.1]
    test_4_probs = [0.9, 0.9, 0.9, 0.9, 0.9]
    test_5_probs = [0.5, 0.5, 0.5, 0.5, 0.5]

    """
    Prior Probability Type
    """
    print_str = [
        "Provided",
        "Test Case #1",
        "Test Case #2",
        "Test Case #3",
        "Test Case #4",
        "Test Case #5",

    ]
    """
    hw2_dataset_10.txt
    """

    print("filename", f[0])
    print(print_str[0])
    print(create_prior_prob_df(given_probs))
    em_10 = EM(g_0=given_probs[0], w_0_given_g_0=given_probs[1],
               w0_given_g0_1=given_probs[2], h_0_given_g_0=given_probs[3], h_0_given_g1=given_probs[4],
               filename=f[0], threshold=0.0001, make_graph=True)

    # print(print_str[1])
    # print(create_prior_prob_df(test_1_probs))
    # test_1_em_10 = EM(g_0=test_1_probs[0], w_0_given_g_0=test_1_probs[1],
    #                   w0_given_g0_1=test_1_probs[2], h_0_given_g_0=test_1_probs[3], h_0_given_g1=test_1_probs[4],
    #                   filename=f[0], threshold=0.0001)
    #
    # print(print_str[2])
    # print(create_prior_prob_df(test_2_probs))
    # test_2_em_10 = EM(g_0=test_2_probs[0], w_0_given_g_0=test_2_probs[1],
    #                   w0_given_g0_1=test_2_probs[2], h_0_given_g_0=test_2_probs[3], h_0_given_g1=test_2_probs[4],
    #                   filename=f[0], threshold=0.0001)
    #
    # print(print_str[3])
    # print(create_prior_prob_df(test_3_probs))
    # test_3_em_10 = EM(g_0=test_3_probs[0], w_0_given_g_0=test_3_probs[1],
    #                   w0_given_g0_1=test_3_probs[2], h_0_given_g_0=test_3_probs[3], h_0_given_g1=test_3_probs[4],
    #                   filename=f[0], threshold=0.0001)
    #
    # print(print_str[4])
    # print(create_prior_prob_df(test_4_probs))
    # test_4_em_10 = EM(g_0=test_4_probs[0], w_0_given_g_0=test_4_probs[1],
    #                   w0_given_g0_1=test_4_probs[2], h_0_given_g_0=test_4_probs[3], h_0_given_g1=test_4_probs[4],
    #                   filename=f[0], threshold=0.0001)
    #
    # print(print_str[5])
    # print(create_prior_prob_df(test_5_probs))
    # test_5_em_10 = EM(g_0=test_5_probs[0], w_0_given_g_0=test_5_probs[1],
    #                   w0_given_g0_1=test_5_probs[2], h_0_given_g_0=test_5_probs[3], h_0_given_g1=test_5_probs[4],
    #                   filename=f[0], threshold=0.0001)
    #
    # """
    #      hw2_dataset_30.txt
    # """
    # print("****************************************************************************************************")
    # print("filename", f[1])
    # print(print_str[0])
    # print(create_prior_prob_df(given_probs))
    # em_30 = EM(g_0=0.7, w_0_given_g_0=0.8,
    #            w0_given_g0_1=0.4, h_0_given_g_0=0.7, h_0_given_g1=0.3,
    #            filename=f[1], threshold=0.0001, make_graph=True)
    #
    # print(print_str[1])
    # print(create_prior_prob_df(test_1_probs))
    # test_1_em_30 = EM(g_0=test_1_probs[0], w_0_given_g_0=test_1_probs[1],
    #                   w0_given_g0_1=test_1_probs[2], h_0_given_g_0=test_1_probs[3], h_0_given_g1=test_1_probs[4],
    #                   filename=f[1], threshold=0.0001)
    #
    # print(print_str[2])
    # print(create_prior_prob_df(test_2_probs))
    # test_2_em_30 = EM(g_0=test_2_probs[0], w_0_given_g_0=test_2_probs[1],
    #                   w0_given_g0_1=test_2_probs[2], h_0_given_g_0=test_2_probs[3], h_0_given_g1=test_2_probs[4],
    #                   filename=f[1], threshold=0.0001)
    #
    # print(print_str[3])
    # print(create_prior_prob_df(test_3_probs))
    # test_3_em_30 = EM(g_0=test_3_probs[0], w_0_given_g_0=test_3_probs[1],
    #                   w0_given_g0_1=test_3_probs[2], h_0_given_g_0=test_3_probs[3], h_0_given_g1=test_3_probs[4],
    #                   filename=f[1], threshold=0.0001)
    #
    # print(print_str[4])
    # print(create_prior_prob_df(test_4_probs))
    # test_4_em_30 = EM(g_0=test_4_probs[0], w_0_given_g_0=test_4_probs[1],
    #                   w0_given_g0_1=test_4_probs[2], h_0_given_g_0=test_4_probs[3], h_0_given_g1=test_4_probs[4],
    #                   filename=f[1], threshold=0.0001)
    #
    # print(print_str[5])
    # print(create_prior_prob_df(test_5_probs))
    # test_5_em_30 = EM(g_0=test_5_probs[0], w_0_given_g_0=test_5_probs[1],
    #                   w0_given_g0_1=test_5_probs[2], h_0_given_g_0=test_5_probs[3], h_0_given_g1=test_5_probs[4],
    #                   filename=f[1], threshold=0.0001)
    #
    # """
    #     hw2_dataset_50.txt
    # """
    # print("****************************************************************************************************")
    # print("filename", f[2])
    # print(print_str[0])
    # print(create_prior_prob_df(given_probs))
    # em_50 = EM(g_0=0.7, w_0_given_g_0=0.8,
    #            w0_given_g0_1=0.4, h_0_given_g_0=0.7, h_0_given_g1=0.3,
    #            filename=f[2], threshold=0.0001, make_graph=True)
    #
    # print(print_str[1])
    # print(create_prior_prob_df(test_1_probs))
    # test_1_em_50 = EM(g_0=test_1_probs[0], w_0_given_g_0=test_1_probs[1],
    #                   w0_given_g0_1=test_1_probs[2], h_0_given_g_0=test_1_probs[3], h_0_given_g1=test_1_probs[4],
    #                   filename=f[2], threshold=0.0001)
    #
    # print(print_str[2])
    # print(create_prior_prob_df(test_2_probs))
    # test_2_em_50 = EM(g_0=test_2_probs[0], w_0_given_g_0=test_2_probs[1],
    #                   w0_given_g0_1=test_2_probs[2], h_0_given_g_0=test_2_probs[3], h_0_given_g1=test_2_probs[4],
    #                   filename=f[2], threshold=0.0001)
    #
    # print(print_str[3])
    # print(create_prior_prob_df(test_3_probs))
    # test_3_em_50 = EM(g_0=test_3_probs[0], w_0_given_g_0=test_3_probs[1],
    #                   w0_given_g0_1=test_3_probs[2], h_0_given_g_0=test_3_probs[3], h_0_given_g1=test_3_probs[4],
    #                   filename=f[2], threshold=0.0001)
    #
    # print(print_str[4])
    # print(create_prior_prob_df(test_4_probs))
    # test_4_em_50 = EM(g_0=test_4_probs[0], w_0_given_g_0=test_4_probs[1],
    #                   w0_given_g0_1=test_4_probs[2], h_0_given_g_0=test_4_probs[3], h_0_given_g1=test_4_probs[4],
    #                   filename=f[2], threshold=0.0001)
    #
    # print(print_str[5])
    # print(create_prior_prob_df(test_5_probs))
    # test_5_em_50 = EM(g_0=test_5_probs[0], w_0_given_g_0=test_5_probs[1],
    #                   w0_given_g0_1=test_5_probs[2], h_0_given_g_0=test_5_probs[3], h_0_given_g1=test_5_probs[4],
    #                   filename=f[2], threshold=0.0001)
    #
    # """
    #     hw2_dataset_70.txt
    # """
    # print("****************************************************************************************************")
    #
    # print("filename", f[3])
    # print(print_str[0])
    # print(create_prior_prob_df(given_probs))
    # em_70 = EM(g_0=0.7, w_0_given_g_0=0.8,
    #            w0_given_g0_1=0.4, h_0_given_g_0=0.7, h_0_given_g1=0.3,
    #            filename=f[3], threshold=0.0001, make_graph=True)
    #
    # print(print_str[1])
    # print(create_prior_prob_df(test_1_probs))
    # test_1_em_70 = EM(g_0=test_1_probs[0], w_0_given_g_0=test_1_probs[1],
    #                   w0_given_g0_1=test_1_probs[2], h_0_given_g_0=test_1_probs[3], h_0_given_g1=test_1_probs[4],
    #                   filename=f[3], threshold=0.0001)
    #
    # print(print_str[2])
    # print(create_prior_prob_df(test_2_probs))
    # test_2_em_70 = EM(g_0=test_2_probs[0], w_0_given_g_0=test_2_probs[1],
    #                   w0_given_g0_1=test_2_probs[2], h_0_given_g_0=test_2_probs[3], h_0_given_g1=test_2_probs[4],
    #                   filename=f[3], threshold=0.0001)
    #
    # print(print_str[3])
    # print(create_prior_prob_df(test_3_probs))
    # test_3_em_70 = EM(g_0=test_3_probs[0], w_0_given_g_0=test_3_probs[1],
    #                   w0_given_g0_1=test_3_probs[2], h_0_given_g_0=test_3_probs[3], h_0_given_g1=test_3_probs[4],
    #                   filename=f[3], threshold=0.0001)
    #
    # print(print_str[4])
    # print(create_prior_prob_df(test_4_probs))
    # test_4_em_70 = EM(g_0=test_4_probs[0], w_0_given_g_0=test_4_probs[1],
    #                   w0_given_g0_1=test_4_probs[2], h_0_given_g_0=test_4_probs[3], h_0_given_g1=test_4_probs[4],
    #                   filename=f[3], threshold=0.0001)
    #
    # print(print_str[5])
    # print(create_prior_prob_df(test_5_probs))
    # test_5_em_70 = EM(g_0=test_5_probs[0], w_0_given_g_0=test_5_probs[1],
    #                   w0_given_g0_1=test_5_probs[2], h_0_given_g_0=test_5_probs[3], h_0_given_g1=test_5_probs[4],
    #                   filename=f[3], threshold=0.0001)
    #
    # """
    #     hw2_dataset_100.txt
    # """
    # print("****************************************************************************************************")
    # print("filename", f[4])
    # print(print_str[0])
    # print(create_prior_prob_df(given_probs))
    # em_100 = EM(g_0=0.7, w_0_given_g_0=0.8,
    #             w0_given_g0_1=0.4, h_0_given_g_0=0.7, h_0_given_g1=0.3,
    #             filename=f[4], threshold=0.0001, make_graph=True)
    #
    # print(print_str[1])
    # print(create_prior_prob_df(test_1_probs))
    # test_1_em_100 = EM(g_0=test_1_probs[0], w_0_given_g_0=test_1_probs[1],
    #                    w0_given_g0_1=test_1_probs[2], h_0_given_g_0=test_1_probs[3], h_0_given_g1=test_1_probs[4],
    #                    filename=f[4], threshold=0.0001)
    #
    # print(print_str[2])
    # print(create_prior_prob_df(test_2_probs))
    # test_2_em_100 = EM(g_0=test_2_probs[0], w_0_given_g_0=test_2_probs[1],
    #                    w0_given_g0_1=test_2_probs[2], h_0_given_g_0=test_2_probs[3], h_0_given_g1=test_2_probs[4],
    #                    filename=f[4], threshold=0.0001)
    #
    # print(print_str[3])
    # print(create_prior_prob_df(test_3_probs))
    # test_3_em_100 = EM(g_0=test_3_probs[0], w_0_given_g_0=test_3_probs[1],
    #                    w0_given_g0_1=test_3_probs[2], h_0_given_g_0=test_3_probs[3], h_0_given_g1=test_3_probs[4],
    #                    filename=f[4], threshold=0.0001)
    #
    # print(print_str[4])
    # print(create_prior_prob_df(test_4_probs))
    # test_4_em_100 = EM(g_0=test_4_probs[0], w_0_given_g_0=test_4_probs[1],
    #                    w0_given_g0_1=test_4_probs[2], h_0_given_g_0=test_4_probs[3], h_0_given_g1=test_4_probs[4],
    #                    filename=f[4], threshold=0.0001)
    #
    # print(print_str[5])
    # print(create_prior_prob_df(test_5_probs))
    # test_5_em_100 = EM(g_0=test_5_probs[0], w_0_given_g_0=test_5_probs[1],
    #                    w0_given_g0_1=test_5_probs[2], h_0_given_g_0=test_5_probs[3], h_0_given_g1=test_5_probs[4],
    #                    filename=f[4], threshold=0.0001)


if __name__ == '__main__':
    main()
