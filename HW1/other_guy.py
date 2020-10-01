class Node(object):
    def __init__(self, title, i, j):
        self.title = title
        self.i = str(i)
        self.j = str(j)
        self.f = 0
        self.g = 0
        self.h = 0
        # no neighbors at first
        self.neighbors = []

    def __str__(self):
        return '<' + self.title + '>'

    def __repr__(self):
        character = 'W' if self.title == '#' else 'O'
        return '<' + self.i + ' ' + self.j + ' ' + self.title + ', ' + str(len(self.neighbors))+'>'

from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: object = field()

q = PriorityQueue()
n = Node('a', 0, 0)
n.f = 1
n2 = Node('b', 0, 0)
n2.f = 0
n3 = Node('c', 0, 0)
n3.f = 2
q.put(PrioritizedItem(n.f, n))
q.put(PrioritizedItem(n2.f, n2))
q.put(PrioritizedItem(n3.f, n3))
print(q.get())
print(q.get())
print(q.get())