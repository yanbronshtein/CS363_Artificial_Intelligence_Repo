import zipfile
import os
import shutil

# starting parameters


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


def e_step(data_dict, parameter_set):
    for key in data_dict:
        # estimate p(gender|weight=0,height=0)
        if key == ('-', '0', '0'):
            pass

        elif key == ('-', '0', '1'):
            pass

        elif key == ('-', '1', '0'):
            pass
        elif key == ('-', '1', '1'):
            pass
        else:
            raise Exception("The data", key, "is not formatted correctly")


def theta_parameters(gender_0, weight_0_given_gender_0, weight_0_given_gender_1, height_0_given_gender_0,
                     height_0_given_gender1):
    return {
        ('0', 'd', 'd'): gender_0,
        ('1', 'd', 'd'): 1 - gender_0, ('0', '0', 'd'): weight_0_given_gender_0,
        ('0', '1', 'd'): 1 - weight_0_given_gender_0,
        ('1', '0', 'd'): weight_0_given_gender_1,
        ('1', '1', 'd'): 1 - weight_0_given_gender_1, ('0', 'd', '0'): height_0_given_gender_0,
        ('0', 'd', '1'): 1 - height_0_given_gender_0,
        ('1', 'd', '0'): height_0_given_gender1,
        ('1', 'd', '1'): 1 - height_0_given_gender1
    }


data_dict = parse_data('hw2dataset_10.txt')
theta = theta_parameters(gender_0=0.7, weight_0_given_gender_0=0.8,
                         weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3)
e_step(data_dict=data_dict, parameter_set=theta)
