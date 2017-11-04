
# coding: utf-8

#------------------------------------------------------------
## 04 - Querying data tables with Pandas
#------------------------------------------------------------
# This tutorial covers database-like features of the Pandas module.  It adds new objects: Dataframes, which are tables of data, and Series, which represent a single column or row.  These can analyse tables of data within Python using similar operations to those provided by Structured Query Language ([SQL](https://en.wikipedia.org/wiki/SQL)), which is used with relational database management systems.  Here, we will query the [Global Volcanism Program](http://www.volcano.si.edu/list_volcano_holocene.cfm)'s spreadsheet of Holocene volcanoes.  Many of the queries are based on the _Generate volcano trivia with this SQLite tutorial_ blog [post](http://www.volcano.si.edu/list_volcano_holocene.cfm). 

#------------------------------------------------------------
#### Setting up

#%% -----------
# Import modules + check versions
import os  # for changing directories
import sys  # checking python version
import pandas as pd  # gives us dataframes
import numpy as np  # arrays and maths
import matplotlib.pyplot as plt  # plotting figures
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
#### Import and check the data

#%% -----------
# Pandas' read_csv command has lots of options for dealing with headers, footers etc.
gvp = pd.read_csv('GVP_Volcano_List.csv')


#%% -----------
# Check the column names.
print gvp.columns


#%% -----------
# View the first 5 entries
gvp.head()


#%% -----------
# View the last 2 entries
gvp.tail(2)


#------------------------------------------------------------
#### Accessing data

#%% -----------
# Access individual columns as Pandas series using Python dictionary syntax.
gvp['Last Known Eruption'].tail()


#%% -----------
#  Get summary statistics for a column
print gvp['Elevation (m)'].describe()


#%% -----------
# Data rows can be sliced based on their position
gvp[150:155]


#%% -----------
# Using the index and the '.loc' command gives more meaningful access to the rows
gvp_names = gvp.set_index('Volcano Name')  # Make a copy with the Name column as the index
gvp_names.loc['Hekla']  # What information is there on Hekla?


#%% -----------
# The '.loc' command accepts lists of rows and columns
gvp_names.loc[['Fuji', 'Etna'], 'Elevation (m)']  # Which is taller, Fuji or Etna?


#%% -----------
#  True/False (Boolean) indexing can be used to perform SQL-like 'WHERE' queries.
gvp_names.loc[gvp_names['Country'] == 'Iceland', ['Latitude', 'Longitude']]  # Where are Iceland's volcanoes?


#------------------------------------------------------------
#### Manipulating data within the columns

#%% -----------
# Add extra columns using dictionary assignment notation
gvp_names['Elevation (km)'] = gvp_names['Elevation (m)']/1000.0
gvp_names['Elevation (km)'].head()


#%% -----------
#  Operations on Series that contains text strings are done with the .str.????? commands
gvp_regions = gvp['Region']
print(gvp_regions.str.upper().head())
print(gvp_regions.str.replace('and', '&').head())
print(gvp_regions.str.contains('Asia').head())


#%% -----------
#  Use the .map method to apply a function to every entry in a column
def extract_year(year_string):
    """Drops the CE or BCE suffix from a date, e.g. '2015 CE', returning an integer.
    This allows sorting and indexing by the numerical value of the year."""
    if year_string == 'Unknown':
        return None
    year = year_string.split()[0]
    suffix = year_string.split()[1]
    if suffix == 'CE':
        return int(year)
    elif suffix == 'BCE':
        return -1 * int(year)
    else:
        raise ValueError('Cannot parse {} as eruption year.'.format(year_string))

gvp['Last Known Eruption Year'] = gvp['Last Known Eruption'].map(extract_year)  # Applying functions to change values
gvp_years = gvp.dropna(subset=['Last Known Eruption Year']).set_index('Last Known Eruption Year').sort_index()
gvp_years.loc[1914:1919, ['Volcano Name', 'Country']]  # Volcanoes that began erupting during the First World War.


#------------------------------------------------------------
## Exercises
#------------------------------------------------------------
#%% -----------
#  1. How many volcanoes are in Spain?
#  2. Which is further north, Cotopaxi or Kilimanjaro?


#------------------------------------------------------------
#### Database-like analysis

#%% -----------
#  Perform SQL-like SELECT and ORDER BY operations
gvp_names['Elevation (m)'].order(ascending=False).head(10)


#%% -----------
#  Perform SQL-like GROUP BY operations
country_counts = gvp_names.groupby('Country').size()  # Count the number of volcanoes per country
country_counts.order(ascending=False).head(10)  # Top 10 most volcanically active countries


#%% -----------
#  Plot results of groupby operations
type_sizes = gvp.groupby('Primary Volcano Type')['Elevation (m)'].mean()
type_sizes.plot(kind='bar')
plt.ylabel('Mean elevation (m)')


#%% -----------
#  Use the pd.merge function to perform SQL-like JOINs of data tables
factbook = pd.read_csv('factbook_extracts.csv')
# CIA World Factbook data modified from https://www.google.com/fusiontables/DataSource?snapid=134490
gvp_factbook = pd.merge(gvp, factbook, left_on='Country', right_on='Country', how='inner')
print gvp_factbook.columns


#%% -----------
#  Perform queries using data from both tables
low_gdp_cutoff = 5000
low_gdp_volcanoes = gvp_factbook.loc[gvp_factbook['GDP per capita ($ PPP)'] < low_gdp_cutoff]
print '\n%d of %d volcanoes are in countries with GDP per capita <$%d.\n' % (
       len(low_gdp_volcanoes), len(gvp), low_gdp_cutoff)


#%% -----------
#  What is the mean life expectancy in the GVP-defined regions?
gvp_factbook_regions = gvp_factbook.groupby('Region')
gvp_factbook_regions['Life expectancy at birth'].mean().order(ascending=False)


#------------------------------------------------------------
#### Exporting data

#%% -----------
#  A Pandas Series (single column or row) can be exported as a list
iceland_volcanoes = gvp_names.loc[gvp_names['Country'] == 'Iceland', ['Latitude', 'Longitude']] 
volcano_names = iceland_volcanoes.index.tolist()
print(volcano_names)


#%% -----------
#  Convert a column to a list
volcano_latitudes = iceland_volcanoes['Latitude'].tolist()
print(volcano_latitudes)


#%% -----------
#  Convert a row to a list
askja_lat_lon = iceland_volcanoes.loc['Askja'].tolist()
print(askja_lat_lon)


#%% -----------
#  A Pandas Dataframe (multiple columns) can be exported as a dictionary of lists
iceland_latlons = iceland_volcanoes[['Longitude', 'Latitude']]
iceland_latlons = iceland_latlons.to_dict('list')
print(iceland_latlons)


#%% -----------
#  Data can be exported to files with .to_csv, .to_excel, .to_latex commands.
#  There are options to control the format of dates and floating point numbers.
iceland_volcanoes = gvp_names.loc[gvp_names['Country'] == 'Iceland', ['Latitude', 'Longitude']]
iceland_volcanoes.to_csv('Icelandic_volcano_locations.csv', float_format='%.2f')


#------------------------------------------------------------
## Exercises
#------------------------------------------------------------
#%% -----------
#  1. Export a csv file with a list of the names and locations of stratovolcanoes over 2500 m in South America.
#  2. What proportion of countries list volcanoes as a natural hazard?  (hint .str.contains('volcan.*')

