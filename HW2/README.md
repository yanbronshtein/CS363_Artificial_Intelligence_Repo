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
`python3 hw2.py`
In the terminal you will see the 3 tables generated for the 5 files
You will also have pyplots popup. You must exit out the pyplots one at a time to observe them
The program will not terminate until you have exited all 5 pyplots
## This project contains 1 file:
### hw2.py
This contains:
* the EM class with the e_step(), m_step(), compute_new_params(), has_converged(), print_em_results(), 
and generate_graph() methods  <br>
* parse_data() function for parsing the data set text files
* main() function that executes the EM algorithm for the 5 files
* hw2dataset_10.txt, hw2dataset_30.txt, hw2dataset_50.txt, hw2dataset_70.txt, hw2dataset_100.txt 


