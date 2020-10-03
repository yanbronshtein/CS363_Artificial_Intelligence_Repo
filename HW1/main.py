from node import Node
from priority_queue import PriorityQueue
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
    4: (1, 0), blank: (1, 1), 8: (1, 2),
    3: (2, 0), 2: (2, 1), 1: (2, 2)
}


# find_matching_node(Node(easy_grid,True), list([Node(easy_grid,True),Node(medium_grid,True),Node(worst_grid,True)]))

# find_matching_node(Node(easy_grid,True), list([Node(medium_grid,True),Node(worst_grid,True)]))

# def a_star_search(start_grid, use_manhattan=False):
#     """
#     Create open list of nodes, initially containing only starting node
#     """
#     open_list = PriorityQueue()
#     first_node = Node(easy_grid, True)
#     open_list.insert(first_node)
#
#     '''
#     Create the closed list of nodes, initially empty
#     '''
#     closed_list = []
#     reached_goal_state = False
#     while open_list.size() > 0:
#         '''
#         Consider the best node in the open list (the node with the lowest f value)
#         '''
#         best_node = open_list.delete()
#         print(best_node)
#         if best_node.curr_grid == goal_grid:
#             # print("The goal has been reached")
#             reached_goal_state = True
#             break
#         else:
#             closed_list.append(best_node)
#             successors = best_node.generate_successors()
#             for successor in successors:
#                 match_in_closed = find_matching_node(successor, closed_list)
#                 match_in_open = find_matching_node(successor, open_list.p_queue)
#
#                 if match_in_closed is not None and best_node.g < match_in_closed.g:
#                     '''
#                     move the node from the closed list to the open list
#                     '''
#                     open_list.insert(successor)
#                     closed_list.remove(match_in_closed)  # Use find_matching_node to remove correct node
#
#                     '''update the neighbor with the new, lower g value'''
#                     successor.g = best_node.g
#
#                     '''change the neighbor's parent to our current node'''
#                     successor.parent_node = best_node
#                     # to here
#
#                 elif match_in_open is not None and best_node.g < match_in_open.g:  # if successor equivalent in
#                 open list and our current g value is lower than its
#                     successor.g = best_node.g
#                     open_list.p_queue.remove(match_in_open)
#
#                     pass
#                 else:
#                     open_list.insert(successor)
#
#     if not reached_goal_state:
#         print("Failed to reach goal")

# def a_star_search(start_grid, use_manhattan):
#     """
#     Create open list of nodes, initially containing only starting node
#     """
#     open_list = PriorityQueue()
#     first_node = Node(start_grid, goal_grid, use_manhattan)
#     open_list.insert(first_node)
#
#     '''
#     Create the closed list of nodes, initially empty
#     '''
#     closed_list = []
#     reached_goal_state = False
#     while open_list.size() > 0 and not reached_goal_state:
#         '''
#         Consider the best node in the open list (the node with the lowest f value)
#         '''
#         best_node = open_list.delete()
#         print(best_node)
#         if best_node.curr_grid == goal_grid:
#             # print("The goal has been reached")
#             reached_goal_state = True
#             break
#         else:
#             closed_list.append(best_node)
#
#             successors = best_node.generate_successors()
#             for successor in successors:
#
#                 match_in_closed = find_matching_node(successor, closed_list)
#                 match_in_open = find_matching_node(successor, open_list.p_queue)
#
#                 if match_in_closed is not None and best_node.g < match_in_closed.g:
#                     '''
#                     move the node from the closed list to the open list
#                     '''
#                     open_list.insert(successor)
#                     closed_list.remove(match_in_closed)  # Use find_matching_node to remove correct node
#
#                     '''update the neighbor with the new, lower g value'''
#                     successor.g = best_node.g
#
#                     '''change the neighbor's parent to our current node'''
#                     successor.parent_node = best_node
#                     # to here
#
#                 # if successor equivalent in open list and our current g value is lower than its
#                 elif match_in_open is not None and best_node.g < match_in_open.g:
#                     successor.g = best_node.g
#                     open_list.p_queue.remove(match_in_open)
#
#                     pass
#                 else:
#                     open_list.insert(successor)
#
#     if not reached_goal_state:
#         print("Failed to reach goal")

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


def trace_and_print(best_node: Node):
    node_ptr = best_node
    print_list = []
    while node_ptr.parent_node is not None:
        print_list.insert(0, node_ptr)
        node_ptr = node_ptr.parent_node
    for node in print_list:
        print(node)


def a_star_search(start_grid, use_manhattan):
    """
    Create open list of nodes, initially containing only starting node
    """
    open_list = PriorityQueue()
    first_node = Node(start_grid, goal_grid, use_manhattan)
    open_list.insert(first_node)

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
            trace_and_print(best_node)
            break
        else:

            closed_list.append(best_node)

            successors = best_node.generate_successors()
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
                    match_in_closed.parent_node = successor.parent_node
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



def branch_and_bound_search(start_grid, use_manhattan):
    p_queue = PriorityQueue()
    root = Node(start_grid, goal_grid, use_manhattan)
    p_queue.insert(root)

    while p_queue.size() > 0:
        min_node = p_queue.delete()
        if min_node.curr_grid == goal_grid:
            trace_and_print(min_node)
            break

        successors = min_node.generate_successors()
        for successor in successors:
            p_queue.insert(successor)








def main():
    # print("1. A* search using the heuristic function f*(n) = g(n) + h*(n), where h*(n) is the number of tiles out of "
    #       "place "
    #       "(not counting the blank).")
    # print("easy grid")
    # a_star_search(easy_grid, False)
    # print("medium grid")
    # a_star_search(medium_grid, False)
    # print("hard grid")
    # a_star_search(hard_grid, False)
    # print("worst grid")
    # a_star_search(worst_grid, False)

    # print(
    #     "2. A* search using the heuristic function f*(n) = g(n) + h*(n), where h*(n) is the number of tiles out of "
    #     "place")
    # print("easy grid")
    # a_star_search(easy_grid, True)
    # print("medium grid")
    # a_star_search(medium_grid, True)
    # print("hard grid")
    # a_star_search(hard_grid, True)
    # print("worst grid")
    # a_star_search(worst_grid, True)
    branch_and_bound(easy_grid, True)
if __name__ == '__main__':
    main()
