
def print_vis_info(vis_object):
  try:
    #each parsed visualization is stored as a Vis object
    print "first visualization:",vis_object
    
    #to get the data from the vis object:
    vis_data = vis_object.data
    print "data shape:",vis_data.shape
    
    #column names
    column_names = vis_data.dtype.names
    print "column names:", column_names
    col1 = column_names[0]
    
    #to get data for a particular column
    col1_data = vis_data[col1]
    #print "column 1 data:",col1_data.shape
    
    #to get data by row (row is returned as a tuple)
    row1_data = vis_data[0]
    #print "row 1 data:",row1_data.shape
    
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
  except:
    pass



# get the path to the datasets package
if __name__ == '__main__':
  import os, sys
  # get an absolute path to the directory that contains mypackage
  datasets_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))
  sys.path.append(os.path.normpath(os.path.join(datasets_dir, '..', '..')))
  from datasets import ManyEyesExtractor,VisDataset,Vis,VisMetadata
else:
  from .. import ManyEyesExtractor,VisDataset,Vis,VisMetadata


# VisDataset is basically a list of visualization objects
# it takes a directory as input to init, which it uses to retreive datasets
ex_ops = {'filename':'../../../data/manyeyes_crawler'}
v = VisDataset(ManyEyesExtractor,ex_ops)

#to get the visualizations, call getVisualizations function
visualizations = v.getVisualizations()


for i, vis_object in enumerate(visualizations):
  print_vis_info(vis_object)
  if i > 10: break
