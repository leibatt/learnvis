import os
import csv
import traceback
import numpy as np
from datasets.vis.vis_obj import Vis
from datasets.vis.vis_metadata import VisMetadata
from base import BaseExtractor,default_delim, default_quote

class MappingExtractor(BaseExtractor):
  '''
  Set of extraction functions for producing Vis objects from raw data files
  uses mapping files to traverse directories for data
  '''

  def __init__(self):
    BaseExtractor.__init__(self)

  #def extract(self,filename,delim=default_delim,quotechar=default_quote):
  def extract(self,ops):
    '''
    gets mapper data from a file, containing metadata about visualizations
    mapping.txt schema:
    source,url,data file location, vis type label, [column type/purpose lable, column index, column name] 

    Requried inputs:
      filename: name of file to retrieve mapping from

    Optional Inputs:
      delim: delimiter used in mapping file
      quotechar: character used to quote data in mapping file

    Args
      ops: dictionary of inputs, filename required
    Returns:
      list of visualization objects
    '''
    filename = ops['filename']
    delim = default_delim
    quotechar = default_quote

    if 'delim' in ops:
      delim = ops['delim']

    if 'quotechar' in ops:
      quotechar = ops['quotechar']


    #assumes no header in the mapper file
    mapper_data,hh = self.loadCSVRows(filename,delim=delim,quotechar=quotechar)
    vis_map = []
    for row in mapper_data:
      # print "row:",row
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
      raw_data,hh = self.loadCSVRows(location,delim=delim,quotechar='"',
                    usetuples=True,check_row_widths=True,ignore_bad_rows=True)
      if len(raw_data) <= 1: # don't add this if there's nothing in it
        continue


      msl = str(self.max_str_len(raw_data))
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

