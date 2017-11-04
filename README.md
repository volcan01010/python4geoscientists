# python4geoscientists

*IPython notebooks demonstrating Python methods for common (geo)science tasks*

The purpose of these notebooks is to highlight how Python can be applied to
solve common problems in geoscience data processing.  These include:

1.  Automatically processing data from multiple files
2.  Dealing with time-series data
3.  Working with database-style data tables
4.  Plotting data on maps

They assume some familiarity with Python and the scientific processing stack
e.g. understanding the difference between a list and a numpy array.  There are
links to suggested reading below that will get you up to speed if you are
completely new to Python.


## Installing dependencies

Run the following command to install the dependencies for these exercises:

```
pip install jupyter pandas matplotlib numpy scipy
```

Jupyter notebooks, Pandas and other libraries are commonly installed as standard with scientific Python distributions.  The [Anaconda Distribution](https://www.anaconda.com/download/) is a popular example.  

The `4_plotting_maps.ipynb` file requires the _basemap_ package.  It requires the GEOS library, so is not always available in pip.  To install on a Debian/Ubuntu-based Linux system, run the following:

```
sudo apt install libgeos-3.5.1 libgeos-dev python3-dev
pip install https://github.com/matplotlib/basemap/archive/v1.1.0.tar.gz
```

## Using the notebooks

Download and start the notebooks by running the following:

```
git clone https://github.com/volcan01010/python4geoscientists.git
cd python4geoscientists
jupyter notebook
```

Your web browser should open at the correct page.  It is recommended to run through the notebooks in order.  You can step through the notebooks with <ctrl-enter>.  At each step, experiment with changing values or adding things to plots.  At the end of each notebook are exercises to try to see how well you have understood what you have seen.


## Data sources

The examples contain data from:
+  [Global Volcanism Program](http://www.volcano.si.edu/list_volcano_holocene.cfm)
+  [CIA World Factbook](https://www.cia.gov/library/publications/the-world-factbook/) downloaded from [Google Fusion tables](https://www.google.com/fusiontables/DataSource?snapid=134490) 


## Getting help

The following links point to useful information:

+    [Scipy Lecture Notes](http://www.scipy-lectures.org/): I highly recommend these tutorials as a starting point for learning Python for science.
+    [The Python Tutorial](http://docs.python.org/3/tutorial/): The 'official' tutorial is good from a programming perspective.  The first 5 chapters are important for beginners.
+    [Matplotlib gallery](http://matplotlib.org/gallery.html): Look for a plot you like, then check out the source code.
+    [Python String Format Cookbook](https://mkaz.com/2012/10/10/python-string-format/): Reference for string format codes.
+    [strftime.org](http://strftime.org): Reference for datetime string format codes.


## Further reading

If you liked this, you can find similar geoscience / volcano / software
goodness by following me at [@volcan01010 on
Twitter](https://www.twitter.com/volcan01010) or by reading the [volcan01010
blog](http://all-geo.org/volcan01010).

> These notebooks were originally created in 2014 for a workshop at Edinburgh
> University's School of GeoSciences.  Please feel free to use, modify,
> distribute and update them as you want.  Just include a link back here.  See
> (MIT) LICENSE files for details.
