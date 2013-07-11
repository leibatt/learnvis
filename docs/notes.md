
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

* **vis.data**: relational data in numpy array. Should also include column labels
* **vis.features**: f(x) e.g., "pie chart"
* **vis.metadata**: metadata.txt encoded 

#### compute_features:

takes a relational table (numpy array) as input, and generates a dictionary of features

see `feature_extractor.py` and `features/`

#### compute_label:

takes `vis.metadata` object as input and return f(x) e.g., "pie chart"

#### harness:

takes `(x axis features, y axis features, f(x))` as input and generates a model

