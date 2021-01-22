To run this tool:

Pre-requisites installed (commonly already installed):
- Python 3.7 or later
- Pip (comes with python)
- Google Chrome or any other webbrowser supporting HTML-5

Python modules installation:
Some python modules need to be imported for the tool to function:
  Importing modules can be done in the following way:
	- open a command console by searching for 'cmd' in the windows search bar, or terminal
	- run the following commands to install the following modules:
		0 - 'Bokeh' 	 - 'pip install Bokeh'	     - framework for the visualisation tool in python
		1 - 'Pandas' 	 - 'pip install pandas'	     - toolkit for parsing and processing data in python

	- the following modules should have come pre-installed with python, but if not, these must be installed:
		2 - 'math' 	 - 'pip install math'	     - toolkit for advanced calculation in python
		3 - 'numpy' 	 - 'pip install numpy'	     - libary of different constants and types of numbers
		4 - 'itertools'  - 'pip install itertools'   - toolkit for working with iterables in python
		5 - 'collections'- 'pip install collections' - module containing advanced structures to hold information in python

Any other dependencies should have been handled by pip

To RUN the tool:
1. Open a command console
2. Navigate to the directory where the tool is located in the command console
	(This can be done by using the '>>>dir [relative or absolute path]' command
3. Run the tool using '>>>bokeh serve --show JBI100_GUI.py'
	(This will open a new browser tab with the tool.)
	(NOTE: Should the tool not open, make sure that no other script is occupying a localhost:5006 connection in the background)