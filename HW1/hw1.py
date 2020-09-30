import numpy as np
import pandas as pd
import sys
from queue import PriorityQueue
import itertools
# x and y coordinates with top left corner as origin
goal_grid = {
    1:(0,0), 2:(1,0), 3: (2,0),
    8:(0,1), 0:(1,1), 4: (2,1),
    7:(0,2), 6:(1,2), 5: (2,2)
}

#Out of place 4
easy_grid = {
    1:(0,0), 3:(1,0), 4: (2,0),
    8:(0,1), 6:(1,1), 2: (2,1),
    7:(0,2), 0:(1,2), 5: (2,2)
}
#Out of place 5
medium_grid = {
    2:(0,0), 8:(1,0), 1: (2,0),
    0:(0,1), 4:(1,1), 3: (2,1),
    7:(0,2), 6:(1,2), 5: (2,2)
}

#Out of place 7
hard_grid = {
    2:(0,0), 8:(1,0), 1: (2,0),
    4:(0,1), 6:(1,1), 3: (2,1),
    0:(0,2), 7:(1,2), 5: (2,2)
}

#out of place
worst_grid = {
    5:(0,0), 6:(1,0), 7: (2,0),
    4:(0,1), 0:(1,1), 8: (2,1),
    3:(0,2), 2:(1,2), 1: (2,2)
}

#use easy and goal
def calc_out_of_place_tiles(start_grid):
    # for coordinates in easy_grid.values():
    #     print(coordinates)
    num_out_of_place_tiles = 0
    for (k1, v1), (k2,v2) in zip(start_grid.items(), goal_grid.items()):
        #We don't care if the blank is out of place
        if k1 != k2 and k1!= 0 :
            num_out_of_place_tiles += 1
        print("start:" + str(k1), str(v1))
        print("goal:" + str(k2), str(v2))

    print("Out of place:" + str(num_out_of_place_tiles))


# calc_out_of_place_tiles(worst_grid)


def calc_sum_manhattan_distance(start_grid):
    # for coordinates in easy_grid.values():
    #     print(coordinates)
    distance = 0
    for (k1, v1), (k2,v2) in zip(start_grid.items(), goal_grid.items()):
        #We don't care if the blank is out of place
        if k1 != 0:
            distance += (abs(v1[0] - v2[0]) + abs(v1[1] - v2[1]))


    print("sum of manhattan distance" + str(distance))
'''
def state:
    matrix
    parent node
    g(n)
    h_manhattan
    h_regular
    

'''



# def calculateManhattan(initial_state):
#     initial_config = initial_state
#     manDict = 0
#     for i,item in enumerate(initial_config):
#         prev_row,prev_col = int(i/ 3) , i % 3
#         goal_row,goal_col = int(item /3),item % 3
#         manDict += abs(prev_row-goal_row) + abs(prev_col - goal_col)
#     return manDict
#
#
#
# class state:
#     def __init__(self,matrix, parent_node):
#
# def h_manhattan(node1,node2):
#
# def h(node):
#     pass
#
# def f(node):
#     # returns number
#     pass
#
# def g(node):
#     pass
#
# def a_star_search(start_state, goal_state, heuristic='not_manhattan'):
#     open_list = PriorityQueue()
#
#     open_list.put()
#
#
#     heuristic = str(heuristic).lower()
#
#     if heuristic == 'manhattan':
#         pass
#     else:
#         pass
#
#     #dicts for the nodes todo: do I really need this?
#     f = {}
#     g = {}
#     h = {}
#
#     while open_list:
#         curr_state = open_list
#
#     # while open_list :
#     #     curr_
#
#
#
# def print_state(state):
#     print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in state]))
#
#
#
# def main():
#     start_state_str = input("Please enter the start state as a comma separated vector excluding '<' and '>'. "
#                             "For blank type b:\n"
#                             "Ex: <1,2,3,4,5,6,7,8,b>\n")
#     goal_state_str = input("Please enter the goal state as a comma separated vector excluding '<' and '>'. "
#                            "For blank type b:\n"
#                            "Ex: <1,2,3,4,5,6,7,8,b>\n")
#     # print(start_state_str)
#     start_state = np.reshape(start_state_str.split(","), (3,3))
#     goal_state = np.reshape(goal_state_str.split(","), (3,3))
#     # print(start_state)
#     # print_state(start_state, goal_state)
#
#
# if __name__ == '__main__':
#     main()
