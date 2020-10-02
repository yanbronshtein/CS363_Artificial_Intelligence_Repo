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


class Node:
    def __init__(self, curr_grid: dict, use_manhattan: bool, parent_node=None):
        self.use_manhattan = use_manhattan
        self.curr_grid = curr_grid
        self.blank_pos = self.curr_grid[blank]  # Get Position of the blank
        if parent_node is not None:
            self.parent_node = parent_node
            self.g = parent_node.g + 1
            self.h = self.calc_manhattan_heuristic() if self.use_manhattan else self.calc_misplaced_tiles_heuristic()
            self.f = self.g + self.h
        else:
            self.g = 0
            self.h = 0
            self.f = 0

    def calc_misplaced_tiles_heuristic(self):
        # for coordinates in easy_grid.values():
        #     print(coordinates)
        misplaced_tiles = 0
        for (k1, v1), (k2, v2) in zip(self.curr_grid.items(), goal_grid.items()):
            # We don't care if the blank is out of place
            if k1 != k2 and k1 != 0:
                misplaced_tiles += 1

        return misplaced_tiles

    def calc_manhattan_heuristic(self):
        # for coordinates in easy_grid.values():
        total_manhattan_distance = 0
        for num in self.curr_grid:
            #     #We don't care if the blank is out of place
            if num != blank:
                total_manhattan_distance += (
                        abs(self.curr_grid[num][blank] - goal_grid[num][blank]) + (abs(self.curr_grid[num][1] -
                                                                                       goal_grid[num][1])))

        return total_manhattan_distance

    def generate_successors(self):
        row, col = self.blank_pos

        right = (row, col + 1)
        down = (row + 1, col)
        left = (row, col - 1)
        up = (row - 1, col)

        potential_moves = [right, down, left, up]

        for move in potential_moves:
            row, col = move
            if row > 2 or col > 2 or row < 0 or col < 0:
                potential_moves.remove(move)
        successors = []

        for move in potential_moves:
            successors.append(self.create_successor(move))

        return successors

    def create_successor(self, new_blank_pos: tuple):
        replace_key = -1
        new_grid = self.curr_grid.copy()
        for key in new_grid:
            if new_grid[key] == new_blank_pos:
                replace_key = key
                break
        new_grid[blank] = new_blank_pos  # Set the new position of the blank to be the new position
        new_grid[replace_key] = self.blank_pos  # Set the position of the replace_key to the old position of the blank
        return Node(new_grid, self.use_manhattan, self)

    def __repr__(self):
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


# class for Priority queue
class PriorityQueue:

    def __init__(self):
        self.queue = list()
        # if you want you can set a maximum size for the queue

    def insert(self, node: Node):
        # if queue is empty
        if self.size() == 0:
            # add the new node
            self.queue.append(node)
        else:
            # traverse the queue to find the right place for new node
            for x in range(self.size()):
                # if the priority of new node is greater
                if node.f >= self.queue[x].f:
                    # if we have traversed the complete queue
                    if x == (self.size() - 1):
                        # add new node at the end
                        self.queue.insert(x + 1, node)
                    else:
                        continue
                else:
                    self.queue.insert(x, node)
                    return True

    def delete(self) -> Node:
        # remove the first node from the queue
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)


def a_star_search(start_grid, use_manhattan=False):
    # Initialize the open list
    open_list = PriorityQueue()
    first_node = Node(easy_grid, True)
    open_list.insert(first_node)

    # Initialize the closed list
    closed_list = []

    q = open_list.delete()
    print(q)
    # print(type(q))
    successors = q.generate_successors()

    print("Hi")
    # while open_list:
    #     '''
    #     Find the node with the least f. Call it "q" Pop it off the list. I am using a priority queue so this is done
    #     automatically
    #     '''
    #     q = open_list.delete()
    #     print(type(q))
    #     '''
    #     Generate q's successors and set their parents to q
    #     # '''


a_star_search(easy_grid, True)

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
