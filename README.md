learnvis
========
features.py -- computes features given data from
mapper.py -- script that takes a mapping.txt file, parses it for data locations, computes features over the data
and stores them in a separate output file
loader.py -- has utilities for reading in and parsing data files specified by the mapper file
mydate.py -- utility functions for working with dates
traverse.py -- script given a directory and output filename, recursively explores the directory and
produces features for all '.tsv' and '.csv' files.
visdata.py -- contains a class used to store information about individual data sets
run.py -- this is an old script used to do what the scripts above do for a specific file. I don't
know if this script still works.

I installed Graphviz and used scikit-learn to build a quick decision tree to sanity check. Using
graphviz means I can export the decision tree into a readable tree format. I did not write a script
for how to do this (not sure why I didn't). Info is here:
http://scikit-learn.org/stable/modules/tree.html

You just need the features in matrix form (I think numpy matrices are fine), and a separate 1 column
matrix with the labels. I think mapper.py is the script I used. traverse.py looks like it may work
too, but it's a bit older so I'm not sure.
