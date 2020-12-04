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
import sys
import math

# Importing non-standard libraries that require pip to install
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

    def __init__(self, gender_0, weight_0_given_gender_0, weight_0_given_gender_1, height_0_given_gender_0,
                 height_0_given_gender1, filename: str, threshold):
        """
        Default constructor for EM class
        :param gender_0:  P(Gender=0)
        :param weight_0_given_gender_0: P(Weight=0|Gender=0)
        :param weight_0_given_gender_1: P(Weight=0|Gender=1)
        :param height_0_given_gender_0: P(height=0|Gender=0)
        :param height_0_given_gender1: P(height=0|Gender=1)
        :param filename: File of this form:"hw2dataset_{%missing_data}.txt"
        :param threshold: Threshold for convergence
        """
        self.threshold = threshold  # Threshold for convergence testing
        self.iterations = 0  # Stores the number of iterations of the EM algorithm
        self.log_likelihood_list = list()  # List to store log_likelihoods for a given iteration of EM
        # sys.setrecursionlimit(2000)  # Recursion limit necessary to avoid the error: "RecursionError:
        # maximum recursion depth exceeded while calling a Python object"

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

        self.operations = [
            'A',  # Compute P(Gender=0) and P(Gender=1)
            'B',  # Compute P(Weight=0|Gender=0) and P(Weight=1|Gender=0)
            'C',  # Compute P(Weight=0|Gender=1) and P(Weight=1|Gender=1)
            'D',  # Compute P(Height=0|Gender=0) and P(Height=1|Gender=0)
            'E',  # Compute P(Height=0|Gender=1) and P(Height=1|Gender=1)
        ]

        # Calculate the first log probability and append to log_likelihood list
        # log_prob = 0
        # for key in self.theta_dict:
        #     log_prob += math.log(self.theta_dict[key])
        # self.log_likelihood_list.append(log_prob)

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
        :param filename:
        :return:
        """
        # self.iterations += 1
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
        :param curr_param_dict: Current learned parameters for the given Bayesian Network
        :param new_param_dict: Newly learned parameters for the given Bayesian Network
        :param threshold: Threshold provided by the user for halting EM algorithm
        :return: True if it is time to halt the EM algorithm and False otherwise
        """

        # print("iteration#:", self.iterations)
        # print("curr_param_dict")
        # print(curr_param_dict)

        # print("new_param_dict")
        # print(new_param_dict)
        log_likelihood_curr_param = 0
        log_likelihood_new_param = 0
        for key in data_dict:
            g, w, h = key
            prob_using_curr_param_dict = 0
            prob_using_new_param_dict = 0
            # if key is ('-', W, H) then calculate log(P(W,H))
            if g == '-':
                # P(W,H) = sum_of_G P(G) * P(W|G) * P(H|G) using probabilities from the previous probability dict
                prob_using_curr_param_dict += curr_param_dict[('0', 'x', 'x')] * curr_param_dict[('0', w, 'x')] * \
                                              curr_param_dict[('0', 'x', h)]
                prob_using_curr_param_dict += curr_param_dict[('1', 'x', 'x')] * curr_param_dict[('1', w, 'x')] * \
                                              curr_param_dict[('1', 'x', h)]
                # P(W,H) = sum_of_G P(G) * P(W|G) * P(H|G) using probabilities from the new probability dict
                prob_using_new_param_dict += new_param_dict[('0', 'x', 'x')] * new_param_dict[('0', w, 'x')] * \
                                             new_param_dict[('0', 'x', h)]
                prob_using_new_param_dict += new_param_dict[('1', 'x', 'x')] * new_param_dict[('1', w, 'x')] * \
                                             new_param_dict[('1', 'x', h)]

            # else key is a complete data (G,W,H) then calculate log(P(G,W,H))
            else:
                # P(G,W,H) = P(G) * P(W|G) * P(H|G) using probabilities from the previous probability dict
                prob_using_curr_param_dict = curr_param_dict[(g, 'x', 'x')] * curr_param_dict[(g, w, 'x')] * \
                                             curr_param_dict[(g, 'x', h)]
                # P(G,W,H) = P(G) * P(W|G) * P(H|G) using probabilities from the new probability dict
                prob_using_new_param_dict = new_param_dict[(g, 'x', 'x')] * new_param_dict[(g, w, 'x')] * \
                                            new_param_dict[(g, 'x', h)]
                # add log(P(G,W,H)) to the total log probabilities

            # add log(P(W,H)) to the total log probabilities
            log_likelihood_curr_param += math.log(prob_using_curr_param_dict) * data_dict[key]
            log_likelihood_new_param += math.log(prob_using_new_param_dict) * data_dict[key]

        if self.iterations == 1:
            self.log_likelihood_list.append(log_likelihood_curr_param)

        self.log_likelihood_list.append(log_likelihood_new_param)

        # print("prob_using_curr_param_dict", prob_using_curr_param_dict)

        delta_log_likelihood = math.fabs(log_likelihood_curr_param - log_likelihood_new_param)
        # print("log_likelihood_curr_param", log_likelihood_curr_param)
        # print("log_likelihood_new_param", log_likelihood_new_param)
        # print("delta:", delta_log_likelihood)
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

        print("filename:", self.filename)
        print("total iterations:", self.iterations)
        print("----------------------------------------Gender Table----------------------------------------")
        gender_df["P(Gender=0)"] = [param_dict[('0', 'x', 'x')]]
        gender_df["P(Gender=1)"] = [param_dict[('1', 'x', 'x')]]
        print(gender_df.to_string(index=False))
        print("--------------------------------------------------------------------------------------------")
        print("----------------------------------------Weight|Gender Table---------------------------------")

        weight_given_gender_df["P(Weight=0|Gender=0)"] = [param_dict[('0', '0', 'x')]]
        weight_given_gender_df["P(Weight=1|Gender=0)"] = [param_dict[('0', '1', 'x')]]
        weight_given_gender_df["P(Weight=0|Gender=1)"] = [param_dict[('1', '0', 'x')]]
        weight_given_gender_df["P(Weight=1|Gender=1)"] = [param_dict[('1', '1', 'x')]]
        print(weight_given_gender_df.to_string(index=False))
        print("--------------------------------------------------------------------------------------------")

        print("----------------------------------------Height|Gender Table---------------------------------")

        height_given_gender_df["P(Height=0|Gender=0)"] = [param_dict[('0', 'x', '0')]]
        height_given_gender_df["P(Height=1|Gender=0)"] = [param_dict[('0', 'x', '1')]]
        height_given_gender_df["P(Height=0|Gender=1)"] = [param_dict[('1', 'x', '0')]]
        height_given_gender_df["P(Height=1|Gender=1)"] = [param_dict[('1', 'x', '1')]]
        print(height_given_gender_df.to_string(index=False))

        print(
            "--------------------------------------------------------------------------------------------")
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


def main():
    # List of files
    files = [
        'hw2dataset_10.txt',
        'hw2dataset_30.txt',
        'hw2dataset_50.txt',
        'hw2dataset_70.txt',
        'hw2dataset_100.txt'

    ]
    """
    Create an EM() object for each of the hw2dataset files
    """

    em_10 = EM(gender_0=0.7, weight_0_given_gender_0=0.8,
               weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3,
               filename=files[0], threshold=0.0001)

    print("likelihoodlist")
    print(em_10.log_likelihood_list)
    em_10.log_likelihood_list = None
    em_30 = EM(gender_0=0.7, weight_0_given_gender_0=0.8,
               weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3,
               filename=files[1], threshold=0.0001)

    print("likelihoodlist")
    print(em_30.log_likelihood_list)
    em_30.log_likelihood_list = None

    em_50 = EM(gender_0=0.7, weight_0_given_gender_0=0.8,
               weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3,
               filename=files[2], threshold=0.0001)

    print("likelihoodlist")
    print(em_50.log_likelihood_list)
    em_50.log_likelihood_list = None

    em_70 = EM(gender_0=0.7, weight_0_given_gender_0=0.8,
               weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3,
               filename=files[3], threshold=0.0001)

    print("likelihoodlist")
    print(em_70.log_likelihood_list)

    em_70.log_likelihood_list = None

    em_100 = EM(gender_0=0.7, weight_0_given_gender_0=0.8,
                weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3,
                filename=files[4], threshold=0.0001)

    print("likelihoodlist")
    print(em_100.log_likelihood_list)
    em_100.log_likelihood_list = None


if __name__ == '__main__':
    main()
