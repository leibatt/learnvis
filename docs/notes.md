# 10/18/2013

Progress:
* Ted: Added config file, logging, and configurable dataset loader, added CHI template
* Aditya: gained a better sense for whats going on in the code
* Eugene:
* Leilani: Made headway on the introduction, and wrote bulleted outline for intro/paper in general

Immediate Tasks
* Ted:
  * Continue to fix harness
  * make a lat/long classifier
* Eugene:
  * write importer for R dataset
* Leilani:
  * make intro/outline available
  * finish intro
  * talk to Mike about venue
  * find a way to scrape additional metadata from many eyes
  * Add features to the harness and measure their performance (optional)
* Aditya:
  * 

Ideas for how the model will work
* main classifier:
  * start with a brute-force approach
  * for each table:
    * enumerate all possible pairs of colums
      * enumerate all possible chart types
        * how good is this pair of axes and chart type together?
* optional (do this later)
  * one to learn for a given visualization type, what columns make the best axes
* We could make implicit negatives (i.e. the choices the user did not pick)
  * we have a lot of negatives and not as many positives
    * could subsample the negatives
    * could re-weight error objective
      * weight false-negatives more harshly than false-positives

# 9/27/2013

Immediate Tasks
* Ted: Fix harness to output sane numbers
* Eugene: write importer for R dataset
* Leilani: pick deadlines for things
  * SIGMOD?
  * WWW?
  * UIST
* Leilani: write skeleton/outline for our future paper
  * try to write the introduction
  * doesn’t need to be polished, bullets are okay
  * scope out space we are addressing
    * narrow down the problem space we are addressing to a few sentences


# 8/15/2013

DoneDid

* Ted: added logging to the project.  Harness is currently not reading visdata objects.
* Eugene: composed data request emails to hadley, jeff.  Ted copy/pasted to GVis/manyeyes folks
* Leilani: added manyeyes+socrata scrapers to repo

TODOS

* Ted: get harness running to predict maps and word clouds
* Eugene: do nothing.  my job here is done
* Leilani: add to socrata scraper to extract more vis spec structure

# 7/23/2013

To Dos:

* Eugene: Simple transformation script to detect if tables need to be 
  folded/unfolded
* Leilani: Filter data to those that have headers and rank them
* Ted: Run a test with exihibit to make sure data import is returning everything in the right shape
* All: Need instructions on how to code the data sets

Meeting summary

* Decomposed problem into data-cleaning/formatting --> model-learning
* data-cleaning is a separate task that we should hand perform, but both are necessary for learnvis to be useful
* Looked at a number of many-eyes visualizations that Joshua scraped for us, considered strategies for
  * hand labeling datasets
  * how to code the data while labeling
  * interfaces to make labeling fast (e.g., show the vis, sample of the dataset, and a simple form)

Some observations while looking at many eyes visualizations in datasets/manyeyes_crawler/

* line graphs may be rendering multiple columns rather than grouping a single column
* bar chart where instead of group on color, each sub-bar is a separate column
* data can be transposed -- 0005adc4-2f18-11e0-8962-000255111976
* May render multiple groups/columns, but only care(pick as default) a subset.
* title may specify which columns are "interesting"
* map plot of (states, number) -> scatter plot
* need a "hirearchical" test 
* exhibit data importer done. needs testing. 
  * you need to easy_install thrift for this to work
  * right now it whitelists only maps(latlng) and timelines(start, end), since the other vis types are too complicated for us at the moment
  * it is SLOWWWWWW. partly because thrift isn't that fast. partly because it's a lot of data  that has to be changed from graph form to table form
  * one problem is that a lot of these datasets are hierarchical or graphical, rather than tabular, but I'm crushing them into tabular form. unsure if this is going to cause a problem with us learning bad weights for features as a result. (e.g., this will impact the number of NULLs.)


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
