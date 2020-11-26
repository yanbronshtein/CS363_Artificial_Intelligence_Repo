import zipfile
import os
import shutil

# starting parameters
theta_gender_is_M = 0.7
theta_weight_gt_130_given_gender_is_M = 0.8
theta_weight_gt_130_given_gender_isF = 0.4
theta_height_gt_55_given_gender_is_M = 0.7
theta_height_gt_5_given_gender_is_F = 0.3
threshold = 0.0001

"""
Hint: E-step of the EM algorithm is essentially estimating the probabilities of different 
values of Gender given that we know a person’s Weight and Height, i.e., 
P(Gender | Weight, Height), and use these estimations as if they are our (expected) counts.

P(Gender | Weight, Height) = [P(Weight|Gender) * P(Height|Gender) * P(Gender)] / P(Weight,Height)
"""


# def parse_data(filename):
# current_dir = os.getcwd()+ "/Bronshtein_Yaniv_AS_2"  # Get current working directory
# current_dir = os.getcwd()  # Get current working directory
# my_working_dir = current_dir + "/Bronshtein_Yaniv_AS_2"
# if not os.path.isdir(my_working_dir):
#     os.mkdir(my_working_dir)
#
# with zipfile.ZipFile(current_dir + '/data_assign2.zip', 'r') as zip_ref:
#     shutil.move(zip_ref.extract(), my_working_dir)


# parse_data('data_assign2.zip')
def parse_data(filename):
    file_obj = open(filename, 'r')
    print(file_obj)
    data_dict = {}
    for line in file_obj.readlines():
        line = line.strip().split()  # Trim and tokenize line
        if line[0] == "Gender":  # Skip the first line with the labels
            continue
        line_tuple = tuple(line)
        if line_tuple in data_dict:
            data_dict[line_tuple] += 1
        else:
            data_dict[line_tuple] = 1
        # data_dict[line] = 1 if line not in data_dict else data_dict[line] + 1  # Put each line as the key and the
        # value is the frequency


        # unique_vowels = {i for i in quote if i in 'aeiou'}
    return data_dict



parse_data('hw2dataset_10.txt')
