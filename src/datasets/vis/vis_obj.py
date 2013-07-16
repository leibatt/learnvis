from vis_metadata import VisMetadata
import numpy as np

class Vis:
  '''
  Visualization Object - container for data about visualizations
  '''

  def __init__(self,data,metadata=None,features=None):
    self.data = data
    self.metadata = VisMetadata()
    self.features = None
    if metadata is not None:
      self.metadata = metadata
    if features is not None:
      self.features = features

  def __repr__(self):
    return "Vis(column names: %s,%s)" % (self.data.dtype.names,self.metadata)

  def get_column_labels(self):
    '''
      return an array of strings representing the column labels
    '''
    return []

  def get_column_types(self):
    '''
    return an array of strings representing the column types
    '''
    return []


