
# coding: utf-8

#------------------------------------------------------------
## P05 - Plotting maps with basemap
#------------------------------------------------------------
# This section introduces the basemap package, which allows geospatial data to be plotted on maps.

#------------------------------------------------------------
#### Setting up

#%% -----------
# Import modules + check versions
import os  # for changing directories
import sys  # checking python version
import pandas as pd  # gives us dataframes
import numpy as np  # arrays and maths
import matplotlib.pyplot as plt  # plotting figures
from mpl_toolkits.basemap import Basemap  # plotting maps
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
#### Get some data

#%% -----------
# Load up the Global Volcanism Programme data from section P04
gvp = pd.read_csv('GVP_Volcano_List.csv')
gvp.dropna(subset=['Latitude', 'Longitude', 'Elevation (m)'], inplace=True)  # Drop any rows without data
lat = gvp['Latitude'].tolist()
lon = gvp['Longitude'].tolist()
elev = gvp['Elevation (m)'].tolist()


#%% -----------
# Plot the data as a normal scatter plot to check
plt.scatter(lon, lat, c='black')


#------------------------------------------------------------
#### Prepare a basemap

#%% -----------
# Create the map canvas
fig = plt.figure(figsize=(11, 8))
# Robinson projection.  lon_0 is central longitude.
# resolution = 'c' means use crude resolution coastlines.
m = Basemap(projection='robin',lon_0=180,resolution='c')

#  Decorate the map by adding continents and grid lines
m.drawcoastlines(linewidth=0.75)
m.fillcontinents(color='0.9')
parallels = m.drawparallels(np.arange(-90.,120.,30.), labels=[0, 1, 0, 0])
meridians = m.drawmeridians(np.arange(0.,360.,60.), labels=[0, 0, 0, 1])

#  Plot the data
x, y = m(lon, lat)  # Convert the latitudes and longitudes into map coordintes
m.scatter(x, y, s=30, c='red', edgecolor='red', alpha=0.8,  # Alpha is transparency
          marker='^', zorder=3)  # zorder brings points to top layer
plt.savefig('Ring_of_fire.png')


#------------------------------------------------------------
## Exercises
#------------------------------------------------------------
#%% -----------
#  1. Use c=elev and cmap='jet' to colour volcanoes by elevation, using m.colorbar to make a key.
#  2. Plot onto the etopo background (see http://matplotlib.org/basemap/users/examples.html?highlight=gallery)
#  3. Make a zoomed map showing Iceland's volcanoes.  Lambert Conformal Conic is a good projection for this.

