
# coding: utf-8

#------------------------------------------------------------
## P01 - Handling from multiple files
#------------------------------------------------------------
# This section revises how to read files and write functions.  It shows how to apply the same code to multiple files.  Examples of curve-fitting are used.

#------------------------------------------------------------
#### Setting up

#%% -----------
# Import modules + check versions
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
#Inline plots for IPython notebooks
#%matplotlib inline
print 'Python: ' + sys.version
print 'Pandas: ' + pd.__version__
print 'Numpy: ' + np.__version__
from matplotlib import __version__ as mplv
print 'Matplotlib: ' + mplv

# Setup working directory
wdir = '/home/jsteven5/Desktop/python4geoscientists'
os.chdir(wdir)


#------------------------------------------------------------
#### The **os** module

#%% -----------
#  Get current directory
os.getcwd()


#%% -----------
#  Join folder and file names to create new paths, using correct separator for your operating system
datadir = os.path.join( wdir, 'data_files' )
print datadir


#%% -----------
#  Extract file name from a full path
filepath = '/long/path/to/myfile.txt'
os.path.basename(filepath)


#%% -----------
#  List directory contents
filelist = os.listdir(datadir)
filelist


#%% -----------
#  List data files
datafiles = []
for filename in filelist:
    if filename.endswith('.data'):
        datafiles.append(filename)
datafiles.sort()
datafiles


#------------------------------------------------------------
#### Reading the datafiles

#%% -----------
#  A simple script to read a data file
x = []
y = []
filepath = os.path.join(datadir, 'Sample001.data')
f = open(filepath, 'rt')
groupline = f.readline()  # Skip first line
for line in f.readlines():
    cols = line.split(',')
    x.append(cols[0])
    y.append(cols[1])
x = np.array(x, dtype=float)
y = np.array(y, dtype=float)
print x
print y


#%% -----------
#  Code that is often reused can be put in a function.
def read_data_file(filepath):
    """Reads a SampleXXX.data file, returning x and y as numpy arrays."""
    x = []
    y = []
    f = open(filepath, 'rt')
    groupline = f.readline()  # Skip first line
    for line in f.readlines():
        cols = line.split(',')
        x.append(cols[0])
        y.append(cols[1])
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    return x, y


#%% -----------
#  Read a data file using the function
filepath = os.path.join(datadir, 'Sample001.data')
x, y = read_data_file(filepath)
print x
print y


#%% -----------
#  Plot the data
plt.scatter(x, y)


#------------------------------------------------------------
#### Calculating the best fit line

#%% -----------
#  Use the linregress function from the scipy.stats module
slope, intercept, r_value, p_value, std_err = linregress(x, y)
os.path.basename(filename)
#  See https://mkaz.com/2012/10/10/python-string-format/ for string format hints
results_text = """
Filename: {filename}
Slope: {slope:.2f}
Intercept: {intercept:.2f}
R-squared: {r2:.2f}
""".format(filename=filename,slope=slope, intercept=intercept, r2=r_value**2)
print results_text


#%% -----------
#  Calculate coordinates for the ends of the best fit line.
fitted_x = np.array([x.min(), x.max()])  # Take these from the original data
fitted_y = slope*fitted_x + intercept


#%% -----------
#  Plot the best fit line
plt.scatter(x, y)
plt.plot(fitted_x, fitted_y, 'r-')


#%% -----------
#  Code that is reused can be put into a function
def calculate_best_fit(x, y):
    """Uses linear regression to calculate best fit line, returning fitted X and Y arrays for plotting."""
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    fitted_x = np.array([x.min(), x.max()])
    fitted_y = slope*fitted_x + intercept   
    return fitted_x, fitted_y


#------------------------------------------------------------
#### Combine functions into single plotting function

#%% -----------
#  Function to plot figure
def plot_sample_fit(filepath):
    """Reads data file, calculates fit to x and y, plots and saves figure."""
    x, y = read_data_file(filepath)  # Uses previous function
    fitted_x, fitted_y = calculate_best_fit(x, y)  # Uses previous function
    plt.figure()
    plt.plot(x, y, 'o')
    plt.plot(fitted_x, fitted_y, '-rx', label='Fitted')
    plt.ylim(0, 80)
    plt.xlabel('x')
    plt.ylabel('y')
    filename = os.path.basename(filepath)
    plt.title(filename[:-5])
    figure_filename = filename.replace('.data', '.png')
    plt.savefig(figure_filename)
    plt.close()
    return


#%% -----------
#  Plot all files
for datafile in datafiles:
    print datafile
    datafilepath = os.path.join(datadir, datafile)
    plot_sample_fit(datafilepath)


#------------------------------------------------------------
## Exercises
#------------------------------------------------------------
#%% -----------
#  1. Modify plot_sample_fit to save your figures as pdf files
#  2. Modify the calculate_best_fit so that it also returns results_text
#  3. Modify plot_sample_fit to use plt.text to write results_text onto your graph
#  4. The data belong to two groups (open a Sample file to see).  What is the average
#     gradient and intercept of each group?

