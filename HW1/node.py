import numpy as np
from typing import List
blank = 0


class Node:

    def __init__(self, curr_grid: dict, goal_grid: dict, use_manhattan: bool, parent_node=None):
        """
        Constructor for state in 8 puzzle
        :param curr_grid: 3x3 dictionary with key the number and value the tuple for coordinates in the grid
        :param use_manhattan: if set to true calculates h using manhattan heuristic. Otherwise use misplaced tiles
        :param parent_node: parent of the current node
        """
        self.curr_grid = curr_grid
        self.blank_pos = self.curr_grid[blank]  # Get Position of the blank
        self.goal_grid = goal_grid
        self.use_manhattan = use_manhattan
        self.parent_node = parent_node
        self.move_type = ''
        # If the current node has a parent, calculate g,h, and f. Else, initialize f,g, and h to 0
        if self.parent_node is not None:
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
        for (k1, v1), (k2, v2) in zip(self.curr_grid.items(), self.goal_grid.items()):
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

                        abs(self.curr_grid[num][0] - self.goal_grid[num][0]) + (abs(self.curr_grid[num][1] -
                                                                                            self.goal_grid[num][1])))

        return total_manhattan_distance

    def generate_successors(self):
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

        # A column value of 3 is illegal for a right move
        if right[1] > 2:
            potential_moves.remove(right)

        # A row value of 3 is illegal for a down move
        if down[0] > 2:
            potential_moves.remove(down)

        # A column value of -1 is illegal for a left move
        if left[1] < 0:
            potential_moves.remove(left)

        # A row value of -1 is illegal for an up move
        if up[0] < 0:
            potential_moves.remove(up)

        # Remove moves that result in the tile moving out of the bounds of the grid
        # for move in potential_moves:
        #     row, col = move
        #     # if row > 2 or col > 2 or row < 0 or col < 0:
        #     #             #     potential_moves.remove(move)
        #     if row > 2:
        #         potential_moves.remove(move)

        # for move in potential_moves:
        #     if col > 2:
        #         potential_moves.remove(move)
        #     if row > 2:
        #         potential_moves.remove(move)
        #     if col < 0:
        #         potential_moves.remove(move)
        #     if row < 0:
        #         potential_moves.remove(move)
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
        # print("Inside create successor. new_blank_pos")
        # print(new_blank_pos)
        for key in new_grid:
            if new_grid[key] == new_blank_pos:
                tile_to_replace = key
                break

        # Swap the positions of the blank and the replaced tile
        new_grid[blank] = new_blank_pos
        # Set the position of the replaced number to the old position of the blank

        new_grid[tile_to_replace] = self.blank_pos
        return Node(new_grid, self.goal_grid, self.use_manhattan, self)

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
        for i in range(3):
            for j in range(3):
                return_str += str(arr[i, j]) + ' '

            return_str += '\n'

        return return_str
