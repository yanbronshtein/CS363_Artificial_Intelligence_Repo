from typing import List

import numpy as np

blank = 0
goal_grid = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    8: (1, 0), blank: (1, 1), 4: (1, 2),
    7: (2, 0), 6: (2, 1), 5: (2, 2)
}
# Out of place 4
easy_grid = {
    1: (0, 0), 3: (0, 1), 4: (0, 2),
    8: (1, 0), 6: (1, 1), 2: (1, 2),
    7: (2, 0), blank: (2, 1), 5: (2, 2)
}
# Out of place 5
medium_grid = {
    2: (0, 0), 8: (0, 1), 1: (0, 2),
    blank: (1, 0), 4: (1, 1), 3: (1, 2),
    7: (2, 0), 6: (2, 1), 5: (2, 2)
}
# Out of place 7
hard_grid = {
    2: (0, 0), 8: (0, 1), 1: (0, 2),
    4: (1, 0), 6: (1, 1), 3: (1, 2),
    blank: (2, 0), 7: (2, 1), 5: (2, 2)
}

# out of place
worst_grid = {
    5: (0, 0), 6: (0, 1), 7: (0, 2),
    4: (1, 0), 0: (1, 1), 8: (1, 2),
    3: (2, 0), 2: (2, 1), 1: (2, 2)
}


class Node:

    def __init__(self, curr_grid: dict, use_manhattan: bool, parent_node=None):
        """
        Constructor for state in 8 puzzle
        :param curr_grid: 3x3 dictionary with key the number and value the tuple for coordinates in the grid
        :param use_manhattan: if set to true calculates h using manhattan heuristic. Otherwise use misplaced tiles
        :param parent_node: parent of the current node
        """
        self.use_manhattan = use_manhattan
        self.curr_grid = curr_grid
        self.blank_pos = self.curr_grid[blank]  # Get Position of the blank

        # If the current node has a parent, calculate g,h, and f. Else, initialize f,g, and h to 0
        if parent_node is not None:
            self.parent_node = parent_node
            self.g = parent_node.g + 1
            self.h = self.calc_manhattan_heuristic() if self.use_manhattan else self.calc_misplaced_tiles_heuristic()
            self.f = self.g + self.h
        else:
            self.g = 0
            self.h = 0
            self.f = 0

    def calc_misplaced_tiles_heuristic(self) -> int:
        """
        This method uses the misplaced tile heuristic that compares the position of each number in the current state
        grid to that in the goal state grid
        :return: total number of misplaced tiles
        """

        # Iterate through each grid represented by a dictionary.
        # We only care about checking the position of the non-blank numbers.
        misplaced_tiles = 0
        for (k1, v1), (k2, v2) in zip(self.curr_grid.items(), goal_grid.items()):
            # We don't care if the blank is out of place
            if k1 != k2 and k1 != blank:
                misplaced_tiles += 1

        return misplaced_tiles

    def calc_manhattan_heuristic(self) -> int:
        """
        This method uses the manhattan heuristic that calculates the sum of all the manhattan distances
        between the tiles in the current grid and the goal grid.
        The manhattan distance is defined as the  distance between two points measured along axes at right angles
         see: https://xlinux.nist.gov/dads/HTML/manhattanDistance.html
        :return: sum total of manhattan distances
        """
        total_manhattan_distance = 0
        for num in self.curr_grid:
            if num != blank:
                total_manhattan_distance += (
                        abs(self.curr_grid[num][blank] - goal_grid[num][blank]) + (abs(self.curr_grid[num][1] -
                                                                                       goal_grid[num][1])))

        return total_manhattan_distance

    def generate_successors(self) -> list:
        """
        This method generates all possible moves for the blank tile
        :return: A list of Node objects representing the resulting grids after the available moves are applied
        """

        row, col = self.blank_pos
        # Definition of moves available.
        right = (row, col + 1)
        down = (row + 1, col)
        left = (row, col - 1)
        up = (row - 1, col)

        potential_moves = [right, down, left, up]

        # Remove moves that result in the tile moving out of the bounds of the grid
        for move in potential_moves:
            row, col = move
            if row > 2 or col > 2 or row < 0 or col < 0:
                potential_moves.remove(move)

        # Generate all the valid grid configurations after the valid moves are applied and append them to
        # the successor list
        successors = []
        for move in potential_moves:
            successors.append(self.create_successor(move))

        return successors

    def create_successor(self, new_blank_pos: tuple):
        """
        This method creates a new node containing the grid configuration reflecting the blank tile move.
        This involves swapping the blank tile with the adjacent tile
        :param new_blank_pos: tuple containing the new coordinates of the blank tile
        :return: Node containing the new grid configuration
        """
        # Determine the number currently located in the desired position of the blank tile
        tile_to_replace = -1
        new_grid = self.curr_grid.copy()
        for key in new_grid:
            if new_grid[key] == new_blank_pos:
                tile_to_replace = key
                break

        # Swap the positions of the blank and the replaced tile
        new_grid[blank] = new_blank_pos
        new_grid[tile_to_replace] = self.blank_pos  # Set the position of the replaced number to the old position of the blank
        return Node(new_grid, self.use_manhattan, self)

    def __repr__(self):
        """
        Generates the string representation of the Node object grid for printing purposes
        :return: string representation
        """
        arr = np.empty([3, 3], np.int)
        for num in self.curr_grid:
            row, col = self.curr_grid[num]
            arr[row, col] = num

        return_str = ''
        #todo: range(3) or range(2)
        for i in range(3):
            for j in range(3):
                return_str += str(arr[i, j]) + ' '

            return_str += '\n'

        return return_str



class PriorityQueue:

    def __init__(self):
        """
        This constructor creates an empty list for the Priority Queue
        """
        self.p_queue = []

    def insert(self, node: Node) -> bool:
        """
        This method inserts a node into the priority queue.
        If the internal list is empty, the new node is appended.
        Otherwise, find the right place for node depending on the value of f determined either by the manhattan or
        misplaced tile heuristics
        :param node: Node to be inserted
        :return: whether the node was successfully inserted
        """
        if self.size() == 0:
            self.p_queue.append(node)
        else:
            # Iterate through entire list.
            # If the f value is at least that of the current node:
            #   If we are at the end, append the node. Else keep iterating
            # Else insert the node right before the current node
            for i in range(self.size()):

                if node.f >= self.p_queue[i].f:
                    if i == (self.size() - 1):
                        self.p_queue.insert(i + 1, node)
                    else:
                        continue
                else:
                    self.p_queue.insert(i, node)
                    return True

    def delete(self) -> Node:
        """
        This method removes the first node in the queue
        :return: removed element
        """
        try:
            return self.p_queue.pop(0)
        except IndexError:
            pass

    def size(self):
        """
        :return: The length of the internal list
        """
        return len(self.p_queue)


def find_matching_node(node: Node, node_list: List[Node]) -> Node:
    """
    This function attempts to find the first node with a matching grid. In anticipation of duplicates,
    this function breaks after the first match, ignoring all others.
    :param node_list: list of nodes
    :type node: Node
    :return match or None
    """
    match = None
    for item in node_list:
        if node.curr_grid == item.curr_grid:
            match = item
            break
    return match

# find_matching_node(Node(easy_grid,True), list([Node(easy_grid,True),Node(medium_grid,True),Node(worst_grid,True)]))

find_matching_node(Node(easy_grid,True), list([Node(medium_grid,True),Node(worst_grid,True)]))

def a_star_search(start_grid, use_manhattan=False):
    """
    Create open list of nodes, initially containing only starting node
    """
    open_list = PriorityQueue()
    first_node = Node(easy_grid, True)
    open_list.insert(first_node)

    '''
    Create the closed list of nodes, initially empty
    '''
    closed_list = []
    reached_goal_state = False
    while open_list.size() > 0:
        '''
        Consider the best node in the open list (the node with the lowest f value)
        '''
        best_node = open_list.delete()

        if best_node.curr_grid == goal_grid:
            print("The goal has been reached")
            reached_goal_state = True
            break
        else:
            closed_list.append(best_node)
            successors = best_node.generate_successors()
            for successor in successors:
                if successor.curr_grid in list(map(lambda x:x.curr_grid,closed_list)) and best_node.g < successor.g:
                    # ... and best_node.g< x(successor.curr_grid, closed_list):
                    '''
                    move the node from the closed list to the open list
                    '''
                    open_list.insert(successor)
                    closed_list.remove(successor)
                    '''
                    #open_list.insert(successor)
                    #closed_list.remove(x(successor.curr_grid, closed_list)) removing olde less iffecient route to succesor 
                    #delete from here
                    '''
                    '''update the neighbor with the new, lower g value'''
                    successor.g = best_node.g

                    '''change the neighbor's parent to our current node'''
                    successor.parent_node = best_node
                    #to here
                elif True: #if successor equivlent in open list and our current g value is lower tthan its
                    #remove equivlent node from open list
                    #add successor to open list
                    pass
                else:
                    open_list.insert(successor)

    if not reached_goal_state:
        print("Failed to reach goal")
    # Initialize the closed list
    # todo: Create a function that takes a grid and a list of node objects and returns the node object with the
    #matching grid
    q = open_list.delete()
    print(q)
    # print(type(q))
    successors = q.generate_successors()

    for successor in successors:
        if successor.curr_grid == goal_grid:
            print("Goal reached")
            break
        else:
            successor.g = q.g


# a_star_search(easy_grid, True)
