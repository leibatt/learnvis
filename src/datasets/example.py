import datasets as d
# VisDataset is basically a list of visualizatio objects
# it takes a mapping file as input to init, which it uses to retreive datasets
v = d.VisDataset('/Volumes/E/mit/vis/code/learnvis-datasets/many_eyes/mapping.txt')

#to get the visualizations, call getVisualizations function
visualizations = v.getVisualizations()
print "visualizations:",visualizations

#each parsed visualization is stored as a Vis object
vis_object = visualizations[0]
print "first visualization:",vis_object

#to get the data from the vis object:
vis_data = vis_object.data
print "data:",vis_data

#column names
column_names = vis_data.dtype.names
print "column names:", column_names
col1 = column_names[0]

#to get data for a particular column
col1_data = vis_data[col1]
print "column 1 data:",col1_data

#to get data by row (row is returned as a tuple)
row1_data = vis_data[0]
print "row 1 data:",row1_data

#to get the metadata from the vis object:
vis_metadata = vis_object.metadata
print "metadata:",vis_metadata

#to get the indices of the columns used as axes in the visualization
axes = vis_metadata.axes
print "axes:",axes

#the columns are listed in order of precedence (so x-axis is at index 0 here)
x_axis = axes[0]
print "x axis:",x_axis

#to get the visualization type (y value):
y = vis_metadata.vistype
print "visualization type:",y

