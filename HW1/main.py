
import numpy as np

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


class Node:
    def __init__(self, curr_grid, use_manhattan, parent_node=None):
        if parent_node is not None:
            self.parent_node = parent_node
            self.g = parent_node.g + 1
            self.h = self.calc_manhattan_heuristic(
                self.curr_grid) if use_manhattan else self.calc_misplaced_tiles_heuristic(self.curr_grid)
            self.f = self.g + self.h
            self.curr_grid = curr_grid
        else:
            self.g = 0
            self.h = 0
            self.f = 0
            self.curr_grid = curr_grid

    @staticmethod
    def calc_misplaced_tiles_heuristic(curr_grid):
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

    @staticmethod
    def calc_manhattan_heuristic(curr_grid):
        # for coordinates in easy_grid.values():
        #     print(coordinates)
        total_manhattan_distance = 0
        for num in curr_grid:
            #     #We don't care if the blank is out of place
            if num != 0:
                total_manhattan_distance += (
                        abs(curr_grid[num][0] - goal_grid[num][0]) + (abs(curr_grid[num][1] - goal_grid[num][1])))

        return total_manhattan_distance

    def __repr__(self):
        arr = np.empty([3, 3], np.int)
        for num in self.curr_grid:
            row, col = self.curr_grid[num]
            arr[row, col] = num
        return '\n'.join(['\t'.join([str(cell) for cell in row]) for row in arr])


# class for Priority queue
class PriorityQueue:

    def __init__(self):
        self.queue = list()
        # if you want you can set a maximum size for the queue

    def insert(self, node):
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

    def delete(self):
        # remove the first node from the queue
        return self.queue.pop(0)

    # def show(self):
    #     for x in self.queue:
    #         print (str(x.info) + " - " + str(x.f))

    def size(self):
        return len(self.queue)


pQueue = PriorityQueue()
# node1 = Node("C", 3)
# node2 = Node("B", 2)
# node3 = Node("A", 1)
# node4 = Node("Z", 26)
# node5 = Node("Y", 25)
# node6 = Node("L", 12)

# node1 = Node()
# node2 = Node("B", 2)
# node3 = Node("A", 1)
# node4 = Node("Z", 26)
# node5 = Node("Y", 25)
# node6 = Node("L", 12)


node1 = Node(easy_grid, True)
node2 = Node(medium_grid, True)
node3 = Node(hard_grid, True)
pQueue.insert(node1)
pQueue.insert(node2)
pQueue.insert(node3)

print(pQueue.delete())

print()

print(pQueue.delete())
# pQueue.show()
