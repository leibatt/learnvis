
#7/16/2013

Harness is working!

To Dos:

   * Eugene will cc Leilani on Jeff Heer Revision email convo
   * Ted will get Exhibit data loading into the harness
     * Note: you will need to easy_install thrift for this to work
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
