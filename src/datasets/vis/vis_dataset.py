import os
from datasets.base import BaseDataset
from vis_obj import Vis
from vis_metadata import VisMetadata
import csv
import numpy as np

default_delim = '\t'
default_quote = '"'

class VisDataset(BaseDataset):
  '''
  Dataset containing an array of Vis objects
  '''

  def __init__(self,filename,delim=default_delim,quotechar=default_quote):
    '''
    Args
      filename: location of mapping.txt file to parse to retrieve datasets
    '''
    BaseDataset.__init__(self)
    self.visualizations = loadMapper(filename,delim=delim,quotechar=quotechar)

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

  def changeMapping(filename,delim=default_delim,quotechar=default_quote):
    self.visualizations = loadMapper(filename,delim=delim,quotechar=quotechar)

def loadMapper(filename,delim,quotechar):
  '''
  gets mapper data from a file, containing metadata about visualizations
  mapping.txt schema:
  source,url,data file location, vis type label, [column type/purpose lable, column index, column name] 
  Args
    filename: name of file to retrieve mapping from
    delim: delimiter used in mapping file
    quotechar: character used to quote data in mapping file
  Returns:
    list of visualization objects
  '''
  #assumes no header in the mapper file
  mapper_data = loadCSVRows(filename,delim=delim,quotechar=quotechar)
  vis_map = []
  for row in mapper_data:
    #print "row:",row
    source = row.pop(0) # index 0
    url = row.pop(0) # index 1
    location = row.pop(0) # index 2
    head,tail = os.path.split(filename)
    location = os.path.join(head, location)
    label = row.pop(0) # index 3
    delim = ','
    if location[len(location)-4:] == '.tsv' or location[len(location)-8:] == 'data.txt':
      delim = '\t'
    #assumes there is a header
    raw_data = loadCSVRows(location,delim=delim,quotechar='"',usetuples=True)
    if len(raw_data) <= 1: # don't add this if there's nothing in it
      continue


    msl = str(max_str_len(raw_data))
    column_names = raw_data[0]
    numcols = len(column_names)
    raw_data = raw_data[1:] # remove column names from data
    #print "raw_data:",raw_data
    dt = []
    for i,f in enumerate(column_names):
      dt.append('S'+msl)
    #print "dt:",dt,",format:",(','.join(dt))
    data = np.array(raw_data,dtype=','.join(dt)) # create structured array of strings
    data.dtype.names = tuple(column_names)
    #print "data:",data
    #print "source:",source,", url:",url,",location:",location,",label:",label
    # only vis aesthetics info is left
    indexes = {'g':[],'p':[],'s':[],'c':[]}
    column_names = []
    for i in range(len(row)/3):
      base = i * 3
      indexes[row[base]].append(int(row[base+1]))
      column_names.append(row[base+2])
    #print indexes

    #build vis object
    vis = Vis(data=data)
    vis.metadata.vistype = label
    vis.metadata.url = url
    vis.metadata.axes = []

    for i,axis in enumerate(indexes['g']):
      vis.metadata.axes.append(axis)

    for i,axis in enumerate(indexes['p']):
      vis.metadata.axes.append(axis)

    if len(indexes['s']) > 0:
      vis.metadata.scaling = indexes['s'][0]

    if len(indexes['c']) > 0:
      vis.metadata.color = indexes['c'][0]

    vis_map.append(vis)
  print "successfuly loaded %d files" % (len(vis_map))
  return vis_map

def loadCSVRows(filename,delim,quotechar,usetuples=False):
  '''
  Parses delimiter-separated files and produces list of lists
  Args
    filename: name of file to retrieve data from
    delim: delimiter of file
    quotechar: character used to quote data
    usetuples: whether to store each row as tuples or lists
  Returns:
    list of lists containing data from file
  '''

  rowtype = list
  if usetuples:
    rowtype = tuple
  data = []
  try:
    with open(filename,'rb') as csvfile:
      filereader = csv.reader(csvfile,delimiter=delim,quotechar=quotechar)
      for row in filereader: # just take whatever's in the row
        #print "row:",row
        data.append(rowtype(row))
  except Exception as e:
    print "something bad happened. aborting load of file '%s'" % (filename)
    print e
    pass
  return data

def max_str_len(data):
  '''
  Args
    data: assumed to be a list of lists or list of tuples
  '''
  return max(len(max(item,key=len)) for item in (row for row in data))



