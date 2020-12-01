import os
import sys
import math

try:
    import matplotlib.pyplot as plt
except:
    os.system("pip install matplotlib")


# starting parameters

iterations = 0
log_likelihood_list = []

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
    # print(file_obj)
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
        # data_dict[line] = 1 if line not in data_dict else data_dict[line] + 1  # Put each line as the key and the
        # value is the frequency

        # unique_vowels = {i for i in quote if i in 'aeiou'}
    return data_dict


'''
P(G|W,H) = P(G,W,H) / P(W,H)
P(G,W,H) = P(G)*P(W|G)*P(H|G)
P(W,H) = SUM_OVER_G( P(G)*P(W|G)*P(H|G) ) 

'''


def e_step(theta_dict, filename):
    data_dict = parse_data(filename)
    expected_data_dict = data_dict.copy()
    for entry in data_dict:
        # estimate p(gender|weight=0,height=0)
        if entry == ('-', '0', '0'):
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
        elif entry == ('-', '0', '1'):
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

        # estimate p(gender|weight=1,height=0)
        elif entry == ('-', '1', '0'):
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

        # estimate p(gender|weight=1,height=1)
        elif entry == ('-', '1', '1'):
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

        else:
            # raise Exception("The entry ", entry, " is invalid")
            continue
    return expected_data_dict


def theta_parameters(gender_0, weight_0_given_gender_0, weight_0_given_gender_1, height_0_given_gender_0,
                     height_0_given_gender1):
    return dict({
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


def m_step(theta_dict, filename):
    global iterations
    iterations += 1
    new_param = dict()
    expected_data_dict = e_step(theta_dict, filename)

    # calculate p(gender=0) and p(gender=1)
    n, d = 0, 0

    for key in expected_data_dict:
        if key[0] == '-':
            continue
        else:
            d += expected_data_dict[key]
            if key[0] == '0':
                n += expected_data_dict[key]
    new_param[('0', 'x', 'x')] = n / d
    new_param[('1', 'x', 'x')] = 1 - new_param[('0', 'x', 'x')]

    # calculate p(weight=0|gender=0) and p(weight=1|gender=0)
    n, d = 0, 0

    for key in expected_data_dict:
        if key[0] == '-':
            continue
        else:
            if key[0] == '0':
                d += expected_data_dict[key]
                if key[1] == '0':
                    n += expected_data_dict[key]
    new_param[('0', '0', 'x')] = n / d
    new_param[('0', '1', 'x')] = 1 - new_param[('0', '0', 'x')]

    # calculate p(weight=0|gender=1) and p(weight=1|gender=1)
    n, d = 0, 0
    for key in expected_data_dict:
        if key[0] == '-':
            continue
        else:
            if key[0] == '1':
                d += expected_data_dict[key]
                if key[1] == '0':
                    n += expected_data_dict[key]
    new_param[('1', '0', 'x')] = n / d
    new_param[('1', '1', 'x')] = 1 - new_param[('1', '0', 'x')]

    # calculate p(height=0|gender=0) and p(height=1|gender=0)
    n, d = 0, 0
    for key in expected_data_dict:
        if key[0] == '-':
            continue
        else:
            if key[0] == '0':
                d += expected_data_dict[key]
                if key[2] == '0':
                    n += expected_data_dict[key]
    new_param[('0', 'x', '0')] = n / d
    new_param[('0', 'x', '1')] = 1 - new_param[('0', 'x', '0')]

    # calculate p(height=0|gender=1) and p(height=1|gender=1)
    n, d = 0, 0
    for key in expected_data_dict:
        if key[0] == '-':
            continue
        else:
            if key[0] == '1':
                d += expected_data_dict[key]
                if key[2] == '0':
                    n += expected_data_dict[key]
    new_param[('1', 'x', '0')] = n / d
    new_param[('1', 'x', '1')] = 1 - new_param[('1', 'x', '0')]

    # print("iteration #", iterations)
    convergence = check_convergence(theta_dict, new_param, 0.0001)

    if convergence:
        print("Final conditional probability tables:")
        # print_conditional_prob(new_param)
    else:
        # print("new parameters:", new_param)
        m_step(new_param, filename)


# def check_convergence(curr_param, new_param, threshold):
#     print("current parameters:", curr_param)
#     for tuple in curr_param:
#         difference = abs(curr_param[tuple] - new_param[tuple])
#         print("difference:", difference)
#         if difference <= threshold:
#             continue
#         else:
#             return False
#
#     return True

def check_convergence(curr_param, new_param, threshold):
    # print("current parameter:", curr_param)
    # print("new parameter:", new_param)
    log_likelihood_curr_param, log_likelihood_new_param = 0, 0
    for key in curr_param:
        if curr_param[key] == 0.0 or new_param[key] == 0.0:
            continue
        else:
            log_likelihood_curr_param += math.log(curr_param[key])
            log_likelihood_new_param += math.log(new_param[key])

    log_likelihood_list.append(log_likelihood_new_param)

    difference = abs(log_likelihood_curr_param - log_likelihood_new_param)
    print("Log likelihood current_param", log_likelihood_curr_param)
    print("Log likelihood new_param", log_likelihood_new_param)

    print("change of log likelihood:", difference)

    return difference <= threshold


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


sys.setrecursionlimit(2000)

filename1 = 'hw2dataset_100.txt'

theta_dict = theta_parameters(gender_0=0.7, weight_0_given_gender_0=0.8,
                              weight_0_given_gender_1=0.4, height_0_given_gender_0=0.7, height_0_given_gender1=0.3)
log_prob = 0
for key in theta_dict:
    log_prob += math.log(theta_dict[key])

log_likelihood_list.append(log_prob)

print("yoyo")
# m_step(theta_dict, 0, filename1)
m_step(theta_dict, filename1)
Y = log_likelihood_list
print(Y)

# X = [i for i in range(1, len(Y) + 1)]
# print(X)
plt.plot(Y)
plt.title("Yoyograph")
plt.xlabel("#Iterations")
plt.ylabel("Log likelihood")


plt.show()
print(iterations)
