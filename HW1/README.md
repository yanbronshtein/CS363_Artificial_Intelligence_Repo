# Artificial Intelligence Programming Assignment #1 Heuristic Search

***Make sure you have python version at least 3.6***
### Windows
The Python installers for Windows include pip. 
You should be able to access pip using:

`$py -m pip --version`


`$py -m pip install --upgrade pip`


**Run code:**
`python main.py`

### Linux and macOS
Debian and most other distributions include a python-pip package, if you want to use the Linux distribution-provided versions of pip see Installing pip/setuptools/wheel with Linux Package Managers.

You can also install pip yourself to ensure you have the latest version. It’s recommended to use the system pip to bootstrap a user installation of pip:

`python3 -m pip install --user --upgrade pip`
Afterwards, you should have the newest pip installed in your user site:

`$python3 -m pip --version`

**Run code:**
`python main.py`
## This project contains 3 files:
### main.py
This contains:
* the entire code for the 3 algorithms, <br>
* the hardcoded grid dictionaries for goal, easy, medium, hard, worst <br>
* trace_and_print() for printing
* find_matching_node() used for A*
* main() function that executes all the algorithms on all four start grids


### node.py
This contains:
** Node class
* a constructor that calculates f(), g(), and h() <br>
* generate_successors() which returns a list of the current node's children <br>
* generate_successor() helper which returns a child node
* calc_manhattan_heuristic() which calculates h() using the manhattan heuristic
* calc_misplaced_tiles_heuristic() which calculates h() using the misplaced tile heuristic

### priority_queue
** PriorityQueue class
* insert() to add a node to the queue
* delete() which removes the node with the lowest f() from the front of the queue
* size() which returns the size of the list
* print_queue() utility function
* has_node() returns if the node exists in the queue
