import node


class PriorityQueue:

    def __init__(self):
        """
        This constructor creates an empty list for the Priority Queue
        """
        self.p_queue = []

    def insert(self, node: node) -> bool:
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

    def delete(self) -> node:
        """
        This method removes the first node in the queue
        :return: removed element
        """

        return self.p_queue.pop(0)


    def size(self):
        """
        :return: The length of the internal list
        """
        return len(self.p_queue)

    def print_queue(self):
        print("queue start")
        for elem in self.p_queue:
            print(elem)

        print("queue end")

