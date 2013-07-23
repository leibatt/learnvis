import os
import csv
import numpy as np
from vis_obj import Vis
from vis_metadata import VisMetadata

default_delim = '\t'
default_quote = '"'

class VisDataset():
  '''
  Dataset containing an array of Vis objects
  '''

  def __init__(self,extractor,extractor_ops):
    '''
    Args
      extractor: extractor class used to retrieve the vis objects
      extractor_ops: dictionary of inputs to extractor.
    '''
    self.visualizations = []
    self.extractor = extractor()
    self.visualizations = self.extractor.extract(extractor_ops)

  def __repr__(self):
    '''
    prints the stored list of visualization objects
    '''
    s = "["
    for i,vis in enumerate(self.visualizations):
      s += str(vis)
      s += ","
    s += "]"
    return s

  def getVisualizations(self):
    '''
    returns the list of visualizations retreived from the mapping file 
    '''
    return self.visualizations

  def reload(self,extractor_ops):
    self.visualizations = self.extractor.extract(extractor_ops)


