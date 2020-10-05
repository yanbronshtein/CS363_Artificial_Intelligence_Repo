from node import Node
from priority_queue import PriorityQueue
from typing import List
import numpy as np
import math
import sys

INFINITY = sys.maxsize
blank = 0
goal_grid = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    8: (1, 0), blank: (1, 1), 4: (1, 2),
    7: (2, 0), 6: (2, 1), 5: (2, 2)
}

# goal_grid = {
#     1: (0, 0), 2: (0, 1), 3: (0, 2),
#     4: (1, 0), 5: (1, 1), 6: (1, 2),
#     7: (2, 0), 8: (2, 1), blank: (2, 2)
# }
# Out of place 4
easy_grid = {
    1: (0, 0), 3: (0, 1), 4: (0, 2),
    8: (1, 0), 6: (1, 1), 2: (1, 2),
    7: (2, 0), blank: (2, 1), 5: (2, 2)
}

# easy_grid = {
#     1: (0, 0), 8: (0, 1), 2: (0, 2),
#     blank: (1, 0), 4: (1, 1), 3: (1, 2),
#     7: (2, 0), 6: (2, 1), 5: (2, 2)
# }
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
    4: (1, 0), blank: (1, 1), 8: (1, 2),
    3: (2, 0), 2: (2, 1), 1: (2, 2)
}


# find_matching_node(Node(easy_grid,True), list([Node(easy_grid,True),Node(medium_grid,True),Node(worst_grid,True)]))

# find_matching_node(Node(easy_grid,True), list([Node(medium_grid,True),Node(worst_grid,True)]))


# todo: reimplement
# todo: reimplement
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


def trace_and_print(start_node: Node, result: Node):
    node_ptr = result
    print_list = []
    while node_ptr.parent_node is not None:
        print_list.insert(0, node_ptr)
        node_ptr = node_ptr.parent_node
    print("Start Grid")
    print(start_node)
    for node in print_list:
        print('Move#:' + str(node.g) + ' ' + node.move_str)
        print(node)


# def a_star_search(start_grid: dict, use_manhattan: bool):
#     """
#     Create open list of nodes, initially containing only starting node
#     """
#     open_list = PriorityQueue()
#     first_node = Node(start_grid, goal_grid, use_manhattan, move_str='')
#     open_list.insert(first_node)
#
#     '''
#     Create the closed list of nodes, initially empty
#     '''
#     closed_list = list()
#     # closed_list = dict()
#
#
#     while open_list.size() > 0:
#         '''
#         Consider the best node in the open list (the node with the lowest f value)
#         '''
#         best_node = open_list.delete()
#
#         if best_node.curr_grid == goal_grid:
#             # print("The goal has been reached")
#             """
#             – 4. If n is a goal node exit successfully with a solution path obtained by
#             tracing back the pointers from n to s.
#             """
#             return best_node
#             # trace_and_print(first_node, best_node)
#         else:
#             #Move the current node to the closed list and consider all of its neighbors
#
#             for item in
#             closed_list.append(best_node)
#
#             successors = best_node.generate_successors_branch_and_bound()
#             # successors = best_node.generate_successors_branch_and_bound()
#             for successor in successors:
#
#                 if find_matching_node(successor, closed_list):
#                     match_in_closed = find_matching_node(successor, closed_list)
#                     if successor.g < match_in_closed.g:
#                         match_in_closed.f = successor.f
#                         match_in_closed.parent_node = successor.parent_node
#                         open_list.insert(match_in_closed)
#                         closed_list.remove(match_in_closed)
#                 elif find_matching_node(successor, closed_list):
#                     match_in_open = find_matching_node(successor, open_list.p_queue)
#                     if successor.g < match_in_open.g:
#                         match_in_open.g = successor.g
#                         match_in_open.parent_node = successor.parent_node
#                 else:
#                     open_list.insert(successor)


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


def trace_and_print(start_grid: Node, best_node: Node):
    node_ptr = best_node
    print_list = []
    while node_ptr.parent_node is not None:
        print_list.insert(0, node_ptr)
        node_ptr = node_ptr.parent_node
    print("Start Grid")
    print(start_grid)
    for node in print_list:
        print("Move #: " + str(node.g))
        print(node)




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


def trace_and_print(start_grid: Node, best_node: Node):
    node_ptr = best_node
    print_list = []
    while node_ptr.parent_node is not None:
        print_list.insert(0, node_ptr)
        node_ptr = node_ptr.parent_node
    print("Start Grid")
    print(start_grid)
    for node in print_list:
        print('Move #:' + str(node.g) + ' ' + node.move_str )
        print(node)


def a_star_search(start_grid: dict , use_manhattan):
    """
    Create open list of nodes, initially containing only starting node
    """
    open_list = PriorityQueue()
    root = Node(start_grid, goal_grid, use_manhattan)
    open_list.insert(root)

    '''
    Create the closed list of nodes, initially empty
    '''
    closed_list = []
    reached_goal_state = False
    while open_list.size() > 0:
        # open_list.print_queue()
        '''
        Consider the best node in the open list (the node with the lowest f value)
        '''
        best_node = open_list.delete()
        # print("best node")
        # print(best_node)
        # print(best_node)
        if best_node.curr_grid == goal_grid:
            # print("The goal has been reached")
            """
            – 4. If n is a goal node exit successfully with a solution path obtained by
            tracing back the pointers from n to s.
            """
            reached_goal_state = True
            trace_and_print(root, best_node)
            return best_node
            # trace_and_print(first_node, best_node)
            # break
        else:

            closed_list.append(best_node)

            successors = best_node.generate_successors_branch_and_bound()
            for successor in successors:

                match_in_closed = find_matching_node(successor, closed_list)
                match_in_open = find_matching_node(successor, open_list.p_queue)
                # open_list.print_queue()


                # if match_in_closed is not None and best_node.g < match_in_closed.g:
                if match_in_closed and successor.f < match_in_closed.f:
                    match_in_closed.f = successor.f
                    match_in_closed.parent_node = successor.parent_node
                    open_list.insert(match_in_closed)
                    closed_list.remove(match_in_closed)
                elif match_in_open and successor.f < match_in_open.f:
                    match_in_open.f = successor.f
                    match_in_open.parent_node = successor.parent_node

                else:
                    open_list.insert(successor)

    if not reached_goal_state:
        print("Failed to reach goal")



# def branch_and_bound(start_grid, use_manhattan):
#     Q = PriorityQueue()
#     Q.insert(Node(start_grid, goal_grid, use_manhattan))
#     L = np.inf #Initialize to infinity
#
#     while Q.size() > 0:
#         #Pull Q1, the first element in Q
#         Q1 = Q.delete()
#         if Q1.curr_grid == goal_grid:
#             reached_goal_state = True
#             trace_and_print(Q1)
#             L = np.min(Q1.f, old_cost)
#             break
#         else:
#             child_nodes = Q1.generate_successors()
#             #eliminate child_nodes which represent simple loops
#             for child in child_nodes:
#                 if child.f < L:
#                     Q.insert(child)
#
#     if not reached_goal_state:
#         print("Failed to reach goal")


# def branch_and_bound_search(start_grid, use_manhattan, limit=sys.maxsize):
#     p_queue = PriorityQueue()
#     root = Node(start_grid, goal_grid, use_manhattan,'')
#     p_queue.insert(root)
#     # L = sys.maxsize
#     min_node = None
#     while p_queue.size() > 0:
#         min_node = p_queue.delete()
#         if min_node.f >= limit:
#             continue
#         elif min_node.curr_grid == goal_grid:
#             if min_node.f < limit:
#                 L = min_node.f
#                 # trace_and_print(root, min_node)
#         else:
#             successors = min_node.generate_successors_branch_and_bound()
#
#             for successor in successors:
#                 if successor.f <= limit:
#                     p_queue.insert(successor)
#
#     trace_and_print(root, min_node)

def branch_and_bound_search(start_grid, use_manhattan, limit=INFINITY):
    p_queue = PriorityQueue()
    root = Node(start_grid, goal_grid, use_manhattan, '')
    p_queue.insert(root)
    min_node = None
    while p_queue.size() > 0:
        min_node = p_queue.delete()
        if min_node.f >= limit:
            continue
        elif min_node.curr_grid == goal_grid:
            if min_node.f < limit:
                limit = min_node.f
                # trace_and_print(root, min_node)
        else:
            successors = min_node.generate_successors_a_star()

            for successor in successors:
                if successor.f <= limit:
                    p_queue.insert(successor)

    return (min_node, limit)
    # trace_and_print(root, min_node)


def iterative_deepening_a_star_search(start_grid, use_manhattan):
    root = Node(curr_grid=start_grid, goal_grid=goal_grid, use_manhattan=use_manhattan, move_str='')
    limit = root.f
    goal_found = False
    closed_list = []
    result = None
    while True:
        closed_list.append(root)
        new_limit = INFINITY
        result = branch_and_bound_search(start_grid, use_manhattan, limit)  # this returns a tuple: (node, new_limit)
        new_limit = result[1]


def main():
    # print("1. A* search using the heuristic function f*(n) = g(n) + h*(n), where h*(n) is the number of tiles out of "
    #       "place "
    #       "(not counting the blank).")
    # print("easy grid")
    # a_star_search(start_grid=easy_grid, use_manhattan=False)
    # print("medium grid")
    # a_star_search(medium_grid, False)
    # print("hard grid")
    # a_star_search(hard_grid, False)
    print("worst grid")

    result = a_star_search(worst_grid, use_manhattan=True)


    # print(
    #     "2. A* search using the heuristic function f*(n) = g(n) + h*(n), where h*(n) is the number of tiles out of "
    #     "place")
    # print("easy grid")
    # a_star_search(start_grid=easy_grid, use_manhattan=True)
    # print("medium grid")
    # a_star_search(start_grid=medium_grid, use_manhattan=True)
    # print("hard grid")
    # a_star_search(start_grid=hard_grid, use_manhattan=True)
    # print("worst grid")
    # a_star_search(worst_grid, True)
    # branch_and_bound_search(easy_grid, True)

    # print("worst grid a star")
    # a_star_search(start_grid=worst_grid,use_manhattan=True)

    # print("easy grid branch and bound")
    # branch_and_bound_search(start_grid=easy_grid,use_manhattan=True)
    # print("medium grid branch and bound")
    # branch_and_bound_search(start_grid=medium_grid, use_manhattan=True)
    # print("hard grid branch and bound")
    # branch_and_bound_search(start_grid=hard_grid, use_manhattan=True)
    # print("worst grid branch and bound")
    # branch_and_bound_search(start_grid=worst_grid, use_manhattan=True)
    # print("easy grid a star")
    # a_star_search(start_grid=easy_grid, use_manhattan=True)

    # print("Branch and bound easy")
    # branch_and_bound_search(start_grid=worst_grid,use_manhattan=True)


if __name__ == '__main__':
    main()
