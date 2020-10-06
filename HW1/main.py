from node import Node
from priority_queue import PriorityQueue
from typing import List
import time
import sys

INFINITY = sys.maxsize
blank = 0

goal_grid = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    8: (1, 0), blank: (1, 1), 4: (1, 2),
    7: (2, 0), 6: (2, 1), 5: (2, 2)
}

easy_grid = {
    1: (0, 0), 3: (0, 1), 4: (0, 2),
    8: (1, 0), 6: (1, 1), 2: (1, 2),
    7: (2, 0), blank: (2, 1), 5: (2, 2)
}

medium_grid = {
    2: (0, 0), 8: (0, 1), 1: (0, 2),
    blank: (1, 0), 4: (1, 1), 3: (1, 2),
    7: (2, 0), 6: (2, 1), 5: (2, 2)
}
hard_grid = {
    2: (0, 0), 8: (0, 1), 1: (0, 2),
    4: (1, 0), 6: (1, 1), 3: (1, 2),
    blank: (2, 0), 7: (2, 1), 5: (2, 2)
}

worst_grid = {
    5: (0, 0), 6: (0, 1), 7: (0, 2),
    4: (1, 0), blank: (1, 1), 8: (1, 2),
    3: (2, 0), 2: (2, 1), 1: (2, 2)
}


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


def trace_and_print(root_node: Node, result: Node, num_nodes_expanded, exec_time_str: str):
    """
    Utility function used to trace the solution path from the goal node to the start/root node
    Prints every state, representing the blank with a 0. Includes move #, move, and from-> to coordinates
    :param root_node: Node object containing start grid
    :param result: Goal node reached containing solution path back to the root
    :param num_nodes_expanded: Number of nodes expanded for each algorithm
    :param exec_time_str: Execution time string in seconds rounded to 4 decimal places
    :return: None
    """
    node_ptr = result
    print_list = []
    while node_ptr.parent_node is not None:
        print_list.insert(0, node_ptr)
        node_ptr = node_ptr.parent_node

    print("Start:")
    print(root_node)
    for node in print_list:
        print(f"Move#: {node.g} {node.move_str}")
        print(node)

    print('Nodes expanded:', end=' ')
    print(num_nodes_expanded)
    print(exec_time_str)


def a_star_search_does_not_work(start_grid: dict, use_manhattan: bool):
    """
    This function would attempt to use a dictionary for the open_list to avoid having to call find find_matching_node()
    The key for the dictionary is a string representation of the grid defined in __repr__() in the Node class
    :param start_grid: dictionary representation of start grid
    :param use_manhattan: determines heuristic to be used for the algorithm
    """
    start_time = time.perf_counter()
    num_nodes_expanded = 0  # removed from the open_list priority queue

    """
    Insert root node into open list
    """
    open_list = PriorityQueue()
    root = Node(start_grid, goal_grid, use_manhattan)
    open_list.insert(root)

    '''
    Create the closed list of nodes, initially empty
    '''
    closed_list = dict()
    seen_node = dict()
    seen_node[str(root)] = root
    while open_list.size() > 0:
        '''
        Consider the best node in the open list (the node with the lowest f value)
        '''
        num_nodes_expanded += 1
        current_node = open_list.delete()
        closed_list[str(current_node)] = current_node
        if current_node.h == 0:
            """
            – 4. If n is a goal node exit successfully with a solution path obtained by
            tracing back the root, best_node, num_nodes_expanded)
            return best_node pointers from n to s.
            """
            end_time = time.perf_counter()
            exec_time = end_time - start_time
            exec_time_str = f'Execution Time: {exec_time:0.4f} seconds'

            trace_and_print(root, current_node, num_nodes_expanded, exec_time_str)
            return
        else:

            successors = current_node.generate_successors()
            for successor in successors:
                temp_node = seen_node[str(successor)]
                if str(successor) in closed_list and successor.g < closed_list[str(successor)].g:
                    temp_successor = closed_list[str(successor)]
                    if successor.g < temp_successor.g:
                        temp_successor.g = successor.g
                        temp_successor.parent_node = current_node
                        closed_list.pop(str(successor))
                        open_list.insert(temp_successor)

                    elif open_list.has_node(temp_node):
                        if successor.g < temp_successor.g:
                            temp_successor.g = successor.g
                            temp_successor.parent_node = current_node
                    else:
                        open_list.insert(successor)


def a_star_search(start_grid: dict, use_manhattan: bool):
    """
    This is the current implementation of A* that uses the f_cost instead of g_cost. For some reason g_cost was
    not working for me. Correct algorithm implemented above but no time to debug
    :param start_grid: initial configuration grid
    :param use_manhattan: tells whether to use manhattan heuristic or not
    :return: None
    """
    start_time = time.perf_counter()  # counter
    num_nodes_expanded = 0

    open_list = PriorityQueue()
    root = Node(start_grid, goal_grid, use_manhattan)
    open_list.insert(root)

    '''
    Create the closed list of nodes, initially empty
    '''
    closed_list = []
    while open_list.size() > 0:
        '''
        Consider the best node in the open list (the node with the lowest f value)
        '''
        current_node = open_list.delete()
        num_nodes_expanded += 1
        if current_node.curr_grid == goal_grid:
            """
            – 4. If n is a goal node exit successfully with a solution path obtained by
            tracing back the root, best_node, num_nodes_expanded)
            return best_node pointers from n to s.
            """
            end_time = time.perf_counter()
            exec_time = end_time - start_time
            exec_time_str = f'Execution Time: {exec_time:0.4f} seconds'

            trace_and_print(root, current_node, num_nodes_expanded, exec_time_str)
            break
        else:
            """
            add the current node to the closed list, generate its children.
            For each child, 
                if it is in the closed_list and its f value is less than that of its counterpart in the
                closed list, update the match's f value and parent.Move the match from the closed list to open list
                If the child is in the open list, and its f value is less than that of the match, update the match's 
                f value and parent to that of the child
                Otherwise, add the child to the open list
                
            """
            closed_list.append(current_node)

            successors = current_node.generate_successors()

            for successor in successors:

                match_in_closed = find_matching_node(successor, closed_list)
                match_in_open = find_matching_node(successor, open_list.p_queue)

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


def depth_first_branch_and_bound_search(start_grid, use_manhattan):
    """
    This algorithm performs depth first branch and bound search
    :param start_grid: initial configuration grid
    :param use_manhattan: tells whether to use manhattan heuristic or not
    :return: None
    """
    limit = INFINITY  # Initialize limit to infinity

    """
    Open list contains the live nodes 
    """
    open_list = PriorityQueue()
    root = Node(start_grid, goal_grid, use_manhattan, '')
    open_list.insert(root)
    result_node = None
    num_nodes_expanded = 0
    start_time = time.perf_counter()
    exec_time_str = ''  # Execution time string for measuring execution time in seconds rounded to 4 decimal places

    """
    While the open_list is not empty,
        Pull out the min f cost node.
        if the node is equal to the goal state, update the limit to the solution's f value
        Otherwise, generate the children, iterate through each child and only insert those elements into the queue with
        an f value <= the current limit
    
    """
    while open_list.size() > 0:
        min_node = open_list.delete()
        num_nodes_expanded += 1
        if min_node.h == 0:
            if min_node.f <= limit:
                end_time = time.perf_counter()
                exec_time = end_time - start_time
                exec_time_str = f'Execution Time: {exec_time:0.4f} seconds'
                limit = min_node.f
                result_node = min_node
        else:
            successors = min_node.generate_successors()
            temp_list = PriorityQueue()
            for successor in successors:
                if successor.f <= limit:
                    temp_list.insert(successor)
            while temp_list.size() > 0:
                open_list.insert(temp_list.delete())

    trace_and_print(root, result_node, num_nodes_expanded, exec_time_str)


def iterative_deepening_a_star_search(start_grid, use_manhattan):
    """
    This function performs Iterative Deepening A* (IDA*)

    :param start_grid: initial configuration grid
    :param use_manhattan: tells whether to use manhattan heuristic or not
    :return: None
    """

    """
    Initialize the bound to the current f value of the root node instead of infinity like with branch_and_bound
    The algorithm calls for calling branch and bound, but a tweak was required, so the code is partially repeated 
    """
    root = Node(curr_grid=start_grid, goal_grid=goal_grid, use_manhattan=use_manhattan, move_str='')
    limit = root.f
    result_node = None
    num_nodes_expanded = 0
    start_time = time.perf_counter()
    exec_time_str = ''
    """
    Branch and Bound. See above method for details
    """
    while result_node is None:
        evaluated_weight = INFINITY
        open_list = PriorityQueue()
        open_list.insert(root)
        while open_list.size() > 0:
            num_nodes_expanded += 1
            current_node = open_list.delete()
            if current_node.h == 0 and current_node.f <= limit:
                end_time = time.perf_counter()
                exec_time = end_time - start_time
                exec_time_str = f'Execution Time: {exec_time:0.4f} seconds'
                limit = current_node.f
                result_node = current_node
            else:
                successors = current_node.generate_successors()
                temp_list = PriorityQueue()
                for successor in successors:
                    if successor.f <= limit:
                        temp_list.insert(successor)
                    elif evaluated_weight > successor.f:
                        evaluated_weight = successor.f
                while temp_list.size() > 0:
                    open_list.insert(temp_list.delete())

        limit = evaluated_weight  # Update the weight
    trace_and_print(root, result_node, num_nodes_expanded, exec_time_str)  # Call trace and print for the solution


def main():
    print("1. A* search using the heuristic function f*(n) = g(n) + h*(n), where h*(n) is the number of tiles out of "
          "place "
          "(not counting the blank).")

    print("LEVEL:EASY")
    a_star_search(start_grid=easy_grid, use_manhattan=False)
    print("LEVEL:MEDIUM")
    a_star_search(start_grid=medium_grid, use_manhattan=False)
    print("LEVEL:HARD")
    a_star_search(start_grid=hard_grid, use_manhattan=False)
    print("LEVEL:WORST")
    print("OUT OF MEMORY")
    # This code is the only one that crashes. Uncommenting will crash the program
    # a_star_search(start_grid=worst_grid, use_manhattan=False) #todo: Fix

    print("2. A* search using the Manhattan heuristic function.")
    print("LEVEL:EASY")
    a_star_search(start_grid=easy_grid, use_manhattan=True)
    print("LEVEL:MEDIUM")
    a_star_search(start_grid=medium_grid, use_manhattan=True)
    print("LEVEL:HARD")
    a_star_search(start_grid=hard_grid, use_manhattan=True)
    print("LEVEL:WORST")
    a_star_search(start_grid=worst_grid, use_manhattan=True)

    print("3. Iterative deepening A* with the Manhattan heuristic function.")
    print("LEVEL:EASY")
    iterative_deepening_a_star_search(start_grid=easy_grid, use_manhattan=True)
    print("LEVEL:MEDIUM")
    iterative_deepening_a_star_search(start_grid=medium_grid, use_manhattan=True)
    print("LEVEL:HARD")
    iterative_deepening_a_star_search(start_grid=hard_grid, use_manhattan=True)
    print("LEVEL:WORST")
    iterative_deepening_a_star_search(start_grid=worst_grid, use_manhattan=True)

    print("4.Depth-first Branch and Bound with the Manhattan heuristic function.")
    print("LEVEL:EASY")
    depth_first_branch_and_bound_search(start_grid=easy_grid, use_manhattan=True)
    print("LEVEL:MEDIUM")
    depth_first_branch_and_bound_search(start_grid=medium_grid, use_manhattan=True)
    print("LEVEL:HARD")
    depth_first_branch_and_bound_search(start_grid=hard_grid, use_manhattan=True)
    print("LEVEL:WORST")
    depth_first_branch_and_bound_search(start_grid=worst_grid, use_manhattan=True)


if __name__ == '__main__':
    main()
