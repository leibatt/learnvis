# 7/23/2013

To Dos:

* Eugene: Simple transformation script to detect if tables need to be 
  folded/unfolded
* Leilani: Filter data to those that have headers and rank them
* Ted: Get the Exhibit data
* All: Need instructions on how to code the data sets

Looking at many eyes visualizations

* line graphs may be rendering multiple columns rather than grouping a single column
* bar chart where instead of group on color, each sub-bar is a separate column
* data can be transposed -- 0005adc4-2f18-11e0-8962-000255111976
* May render multiple groups/columns, but only care(pick as default) a subset.
* title may specify which columns are "interesting"
* map plot of (states, number) -> scatter plot
* need a "hirearchical" test 


#7/16/2013

Harness is working!

To Dos:

   * Eugene will cc Leilani on Jeff Heer Revision email convo
   * Ted will get Exhibit data loading into the harness
   * Leilani will make her data parsing code easier to use and modularized
   * Leilani will follow up on many eyes scripting info to get more visualizations



#7/9/2013

## Architecture

The overall data flow is:

    cur data files   ----                  /---> compute_fetaures --
                         \--> vizObject ---                         \--> harness
    other data files ----                  \---> compute_label  ----/

#### cur data files

data files that we currently have (many eyes etc).  Creates a viz object

Currently, a dataset contains:

1. metadata.txt
2. data.txt
3. schema.txt
4. image.png


#### other data files

for the future.  can ignore now


#### VizObject: contains data for the many-eyes stuff
the data will be stored in a numpy structured array:
http://docs.scipy.org/doc/numpy/user/basics.rec.html

**vis.data**

Relational data in structured numpy array.  

```
vis.data.dtype.names # column names
vis.data[COLNAME]    # column of data
```

**vis.features**

f(x) e.g., "pie chart"

**vis.metadata**

metadata.txt encoded 

#### compute_features:

takes a relational table (numpy array) as input, and generates a dictionary of features

see `feature_extractor.py` and `features/`

#### compute_label:

takes `vis.metadata` object as input and return f(x) e.g., "pie chart"

#### harness:

takes list of `(x axis features, y axis features, label)` as input and train/tests/returns a model
