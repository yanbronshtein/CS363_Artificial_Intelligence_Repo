from node import Node
from priority_queue import PriorityQueue
from typing import List
import time
import sys
from concurrent.futures import ProcessPoolExecutor

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


# Warning: this does not terminate function if timeout
def timeout_five(fnc, *args, **kwargs):
    with ProcessPoolExecutor() as p:
        f = p.submit(fnc, *args, **kwargs)
        return f.result(timeout=5)


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


def trace_and_print(start_node: Node, result: Node, num_nodes_expanded, exec_time_str: str):
    node_ptr = result
    print_list = []
    while node_ptr.parent_node is not None:
        print_list.insert(0, node_ptr)
        node_ptr = node_ptr.parent_node

    print("Start:")
    print(start_node)
    for node in print_list:
        print(f"Move#: {node.g} {node.move_str}")
        print(node)

    print('Nodes expanded:', end=' ')
    print(num_nodes_expanded)
    print(exec_time_str)


# def a_star_search(start_grid: dict, use_manhattan):
#     """
#     Create open list of nodes, initially containing only starting node
#     """
#     start_time = time.perf_counter()
#     num_nodes_expanded = 0
#
#     open_list = PriorityQueue()
#     root = Node(start_grid, goal_grid, use_manhattan)
#     open_list.insert(root)
#
#     '''
#     Create the closed list of nodes, initially empty
#     '''
#     closed_list = dict()
#     seen_node = dict()
#     seen_node[str(root)] = root
#     while open_list.size() > 0:
#         '''
#         Consider the best node in the open list (the node with the lowest f value)
#         '''
#         num_nodes_expanded += 1
#         current_node = open_list.delete()
#         closed_list[str(current_node)] = current_node
#         if current_node.h == 0:
#             """
#             – 4. If n is a goal node exit successfully with a solution path obtained by
#             tracing back the root, best_node, num_nodes_expanded)
#             return best_node pointers from n to s.
#             """
#             end_time = time.perf_counter()
#             exec_time = end_time - start_time
#             exec_time_str = f'Execution Time: {exec_time:0.4f} seconds'
#
#             trace_and_print(root, current_node, num_nodes_expanded, exec_time_str)
#             return
#         else:
#
#             successors = current_node.generate_successors()
#             for successor in successors:
#                 temp_node = seen_node[str(successor)]
#                 # match_in_closed = find_matching_node(successor, closed_list)
#
#                 # if match_in_closed is not None and best_node.g < match_in_closed.g:
#                 if str(successor) in closed_list and successor.g < closed_list[str(successor)].g:
#                     temp_successor = closed_list[str(successor)]
#                     if successor.g < temp_successor.g:
#                         temp_successor.g = successor.g
#                         temp_successor.parent_node = current_node
#                         closed_list.pop(str(successor))
#                         open_list.insert(temp_successor)
#
#                     elif open_list.has_node(temp_node):
#                         if successor.g < temp_successor.g:
#                             temp_successor.g = successor.g
#                             temp_successor.parent_node = current_node
#                     else:
#                         open_list.insert(successor)



def a_star_search(start_grid: dict, use_manhattan):
    """
    Create open list of nodes, initially containing only starting node
    """
    start_time = time.perf_counter()
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
        best_node = open_list.delete()
        num_nodes_expanded += 1
        if best_node.curr_grid == goal_grid:
            """
            – 4. If n is a goal node exit successfully with a solution path obtained by
            tracing back the root, best_node, num_nodes_expanded)
            return best_node pointers from n to s.
            """
            end_time = time.perf_counter()
            exec_time = end_time - start_time
            exec_time_str = f'Execution Time: {exec_time:0.4f} seconds'

            trace_and_print(root, best_node, num_nodes_expanded, exec_time_str)
            break
        else:

            closed_list.append(best_node)

            successors = best_node.generate_successors()
            # Number of nodes expanded incremented by the size of the list returned by generate_successors
            # num_nodes_expanded += len(successors)
            for successor in successors:

                match_in_closed = find_matching_node(successor, closed_list)
                match_in_open = find_matching_node(successor, open_list.p_queue)

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

def depth_first_branch_and_bound_search(start_grid, use_manhattan, called_by_ida:bool):
    limit = INFINITY
    open_list = PriorityQueue()
    root = Node(start_grid, goal_grid, use_manhattan, '')
    open_list.insert(root)
    result_node = None
    min_node = None
    num_nodes_expanded = 0
    start_time = time.perf_counter()

    exec_time = 0
    exec_time_str = ''

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


    trace_and_print(root, result_node, num_nodes_expanded,exec_time_str)




def iterative_deepening_a_star_search(start_grid, use_manhattan):
    root = Node(curr_grid=start_grid, goal_grid=goal_grid, use_manhattan=use_manhattan, move_str='')
    limit = root.f
    goal_node_found = None
    num_nodes_expanded = 0
    start_time = time.perf_counter()
    exec_time_str = ''

    while goal_node_found is None:
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
                goal_node_found = current_node
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

        limit = evaluated_weight
    trace_and_print(root, goal_node_found,num_nodes_expanded,exec_time_str)




def main():
    # print("1. A* search using the heuristic function f*(n) = g(n) + h*(n), where h*(n) is the number of tiles out of "
    #       "place "
    #       "(not counting the blank).")
    # print("LEVEL:EASY")
    # a_star_search(start_grid=easy_grid, use_manhattan=False)
    # print("LEVEL:MEDIUM")
    # a_star_search(start_grid=medium_grid, use_manhattan=False)
    # print("LEVEL:HARD")
    # a_star_search(start_grid=hard_grid, use_manhattan=False)
    # print("LEVEL:WORST")
    a_star_search(start_grid=easy_grid, use_manhattan=False)
    # a_star_search(start_grid=worst_grid, use_manhattan=True)
    # depth_first_branch_and_bound_search(start_grid=worst_grid, use_manhattan=True,called_by_ida=False)
    # branch_and_bound_search(start_grid=easy_grid,use_manhattan=True)
    # iterative_deepening_a_star_search(start_grid=worst_grid,use_manhattan=True)

    # node_str = str(Node(curr_grid=easy_grid,goal_grid=goal_grid,use_manhattan=True, move_str=''))
    # print(node_str)
if __name__ == '__main__':
    main()
