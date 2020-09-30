import numpy as np
import pandas as pd
import sys
from queue import PriorityQueue
import itertools

# x and y coordinates with top left corner as origin
goal_grid = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    8: (1, 0), 0: (1, 1), 4: (1, 2),
    7: (2, 0), 6: (2, 1), 5: (2, 2)
}

# Out of place 4
easy_grid = {
    1: (0, 0), 3: (0, 1), 4: (0, 2),
    8: (1, 0), 6: (1, 1), 2: (1, 2),
    7: (2, 0), 0: (2, 1), 5: (2, 2)
}
# Out of place 5
medium_grid = {
    2: (0, 0), 8: (0, 1), 1: (0, 2),
    0: (1, 0), 4: (1, 1), 3: (1, 2),
    7: (2, 0), 6: (2, 1), 5: (2, 2)
}

# Out of place 7
hard_grid = {
    2: (0, 0), 8: (0, 1), 1: (0, 2),
    4: (1, 0), 6: (1, 1), 3: (1, 2),
    0: (2, 0), 7: (2, 1), 5: (2, 2)
}

# out of place
worst_grid = {
    5: (0, 0), 6: (0, 1), 7: (0, 2),
    4: (1, 0), 0: (1, 1), 8: (1, 2),
    3: (2, 0), 2: (2, 1), 1: (2, 2)
}

# use easy and goal


'''
def state:
    matrix
    parent node
    g(n)
    h_manhattan
    h_regular
    

'''


class Node:
    def __init__(self, curr_grid, use_manhattan, parent_node=None):
        if parent_node:
            self.parent_node = parent_node
            self.g = parent_node.g + 1
            self.h = self.calc_manhattan_heuristic(self.curr_grid) if use_manhattan else self.calc_misplaced_tiles_heuristic(self.curr_grid)
            self.f = self.g + self.h
            self.curr_grid = curr_grid
        else:
            self.g = 0
            self.h = 0
            self.f = 0
            self.curr_grid = curr_grid



    def get_f(self):
        return self.f
    def calc_misplaced_tiles_heuristic(self, curr_grid):
        # for coordinates in easy_grid.values():
        #     print(coordinates)
        misplaced_tiles = 0
        for (k1, v1), (k2, v2) in zip(curr_grid.items(), goal_grid.items()):
            # We don't care if the blank is out of place
            if k1 != k2 and k1 != 0:
                misplaced_tiles += 1
            print("start:" + str(k1), str(v1))
            print("goal:" + str(k2), str(v2))

        return misplaced_tiles

    # calc_out_of_place_tiles(worst_grid)

    def calc_manhattan_heuristic(self, curr_grid):
        # for coordinates in easy_grid.values():
        #     print(coordinates)
        total_manhattan_distance = 0
        for num in curr_grid:
            #     #We don't care if the blank is out of place
            if num != 0:
                total_manhattan_distance += (
                        abs(curr_grid[num][0] - goal_grid[num][0]) + (abs(curr_grid[num][1] - goal_grid[num][1])))

        return total_manhattan_distance

    #String representation of Node for printing purposes
    def __repr__(self):
        arr = np.empty([3,3],np.int)
        for num in self.curr_grid:
            row,col = self.curr_grid[num]
            # print(num)
            arr[row,col] = num
            # print(arr[row,col])
        # print(arr)
        return '\n'.join(['\t'.join([str(cell) for cell in row]) for row in arr])

    # def __repr__(self):
    #     arr = []
    #     for num in self.curr_grid:
    #         row, col = self.curr_grid[num]
    #         arr[row, col] = num
    #
    #     arr.astype(int)
    #     print(arr)
    #     return '\n'.join(['\t'.join([str(cell) for cell in row]) for row in arr])


def a_star_search(start_grid, use_manhattan=False):
    #Initialize the open list
    open_list = PriorityQueue()
    start_node = Node(start_grid,use_manhattan)
    open_list.put((start_node.get_f(),start_node))
    #Initialize the closed list
    closed_list = []

    while open_list:
        '''
        Find the node with the least f. Call it "q" Pop it off the list. I am using a priority queue so this is done
        automatically
        '''
        q = open_list.get()
        print(q[1])
        '''
        Generate q's successors and set their parents to q
        '''

a_star_search(easy_grid)


    # while open_list :
    #     curr_
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
