
# coding: utf-8

#------------------------------------------------------------
## P03 - Time series analysis with Pandas
#------------------------------------------------------------
# This tutorial introduces the time-series analysis features of Python.  It add the Datetime object, which handles calculations involving periods of time.  The Pandas module introduces two new objects: Dataframes, which are tables of data, and Series, which represent a single column or row.  In this section, we take advantage Pandas' datetime-based indexing to process time-series data.

#------------------------------------------------------------
#### Setting up

#%% -----------
# Import modules + check versions
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
# Inline plots for IPython notebooks
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
#### Creating datetime objects

#%% -----------
#  Directly enter year, month, day, hour etc.
dt.datetime(1955, 11, 12, 22, 4, 0)


#%% -----------
#  Read from formatted text string (See strftime.org for codes)
dt.datetime.strptime('26 October 1985, 01:21:59 am', '%d %B %Y, %I:%M:%S %p')


#%% -----------
#  Get current time from function
dt.datetime.now()


#------------------------------------------------------------
#### Timedelta objects represent time spans

#%% -----------
#  Timedelta objects represent the difference between to datetimes.
departure = dt.datetime.strptime('26 October 1985, 01:21:59 am', '%d %B %Y, %I:%M:%S %p')
delta = dt.datetime.now() - departure
print delta


#%% -----------
#  You can define timedelta based on number of days, seconds and microseconds.  (Why not months or years?)
delta = dt.timedelta(1, 1, 1)
print delta


#%% -----------
#  You can specify them by named keys
delta = dt.timedelta(seconds=864000)
print delta


#%% -----------
#  The total_seconds() function converts into seconds.  (Python 2.7)
delta = dt.timedelta(1, 1, 1)
print delta.total_seconds()


#------------------------------------------------------------
#### Extracting information from datetime objects

#%% -----------
#  Year, month, day etc. are attributes of the object
arrival = dt.datetime(1955, 11, 12, 22, 4, 0)
print arrival.year
print arrival.hour


#%% -----------
#  There are methods calculate number of days since Jan 01, 1 A.D.
print arrival.toordinal()


#%% -----------
#  Or the day of the week (Monday = 0)
print arrival.weekday()


#%% -----------
#  The .strftime method writes a string in the specified format
arrival.strftime('%Y-%m-%d %H:%M:%S')


#------------------------------------------------------------
#### Datetime Exercises

#%% -----------
#  1. Was Marty McFly's journey Back to the Future (departure and arrival times are defined above)
#     longer or shorter than if he had travelled to now?
#  2. When will you be (or were you) 1 billion seconds old?
#  3. Change the arrival.strftime() string to write the arrival date as "04 minutes past 10 on 12 November 1955".


#------------------------------------------------------------
#### Loading time series data in Pandas

# This example uses temperatures of steam vents (fumaroles) on the crater of Volcán de Colima, Mexico, as measured by infrared camera during a night in 2006.

#%% -----------
#  Create a Pandas dataframe reading data from a .csv file.  It can translate dates into datetime objects
infraredData = pd.read_csv('InfraredCameraData.csv', parse_dates=[0])
infraredData.set_index('DateTime', inplace=True)  # Set the datetime column as the index
infraredData.head(10)  # Print the first 10 values


#%% -----------
#  Plot the time series.
infraredData.plot()
plt.savefig('graph.png')


#%% -----------
#  Extract a column as a data series with dictionary-like notation
e_flank = infraredData['EFlankAvg']
e_flank.head()


#%% -----------
#  Extract 1 minute worth of rows by slicing the index with datetimes
rows = infraredData[dt.datetime(2006, 5, 23, 4, 0):dt.datetime(2006, 5, 23, 4, 1)]
rows


#%% -----------
#  Find the row corresponding to the explosion (max temperature)
explosion_status = infraredData['CraterMax'] == infraredData['CraterMax'].max()
explosion_status


#%% -----------
#  Extract the timestamp
explosion_time = infraredData.index[explosion_status]  # Get index values where explosion_status is True
explosion_time[0]  # Extract the first (only) value


#%% -----------
#  Add a column for the 2-minute rolling mean of the CraterMax temperature
rolling_mean = pd.rolling_mean(infraredData, window=24)  # 24 x 5 second intervals
infraredData['CraterMaxRolling'] = rolling_mean['CraterMax']
infraredData.plot()


#------------------------------------------------------------
#### Calculating the cloud-free mean fumarole temperatures

#%% -----------
#  Use time index slicing to select time when data unaffected by sunlight or explosions.
night = infraredData['2006-05-23 02:50':'2006-05-23 05:50']
night.plot()


#%% -----------
#  Drop data where clouds obscure the crater
no_clouds = night[night['CraterMax'] > 28]
no_clouds.plot()


#%% -----------
#  Resample to take 2 minute maximum values, dropping other cloud noise
max_2mins = no_clouds.resample('2min', how='max')
max_2mins.plot()
max_2mins.describe()  # Statistics for temperatures unaffected by clouds or explosions


#------------------------------------------------------------
## Exercises
#------------------------------------------------------------
#%% -----------
#  1. What percentage of the original data have we used in the max_2mins data?
#  2. Drop data within 10 minutes of explosion_time from infraredData

