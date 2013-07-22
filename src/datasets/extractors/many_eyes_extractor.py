import os
from datasets.vis.vis_obj import Vis
from datasets.vis.vis_metadata import VisMetadata
import csv
import numpy as np
from datasets.extractors.base import BaseExtractor,default_delim, default_quote

candidate_delimiters = ['\t',',']
numrows_min = 0

class ManyEyesExtractor(BaseExtractor):
  '''
  Set of extraction functions for producing Vis objects from Many Eyes raw data files.
  does a recursive walk down the given input directory for many eyes data.
  depends on the following directories to be contained in the input
  directory:

  metadata/
  rawfinaldatapages/
  '''

  def __init__(self):
    BaseExtractor.__init__(self)

  #def extract(self,dirname,delim=default_delim,quotechar=default_quote):
  def extract(self,ops):
    '''
      Required inputs:
      dirname: full path to directory containing many eyes data

      Optional inputs:
      delim: delimiter of data files in many eyes directory
      quotechar: character used to quote data in data files in many eyes directory

    Args
      ops: dictionary of inputs, filename required
    Returns:
      list of Vis objects
    '''
    dirname = ops['filename']
    delim = default_delim
    quotechar = default_quote

    if 'delim' in ops:
      delim = ops['delim']

    if 'quotechar' in ops:
      quotechar = ops['quotechar']

    # get list of [uid].txt files
    vis_map = []
    uids = []
    labels = {}
    metadata = os.path.join(dirname,'metadata')
    rawfinaldata = os.path.join(dirname,'rawfinaldatapages')
    try:
      uids = os.listdir(metadata)
    except Exception as e:
      print e
    
    total_parsed = 0
    total_headers = 0
    total_files = len(uids)

    for uid in uids:
      #print uid
      metadata_path = os.path.join(metadata,uid)
      data_path = os.path.join(rawfinaldata,uid)

      md,hh = self.loadCSVRows(metadata_path,delim=default_delim,
                  quotechar=default_quote,check_row_widths=False)
      if len(md) == 0: # throw out useless datasets
        #print "len of md is ",len(md)
        continue
      
      vistype = None
      # get vistype
      for line in md:
        if line[0] == 'vistype':
          l = line[1]
          vistype = l
          if l not in labels:
            labels[l] = 1
          else:
            labels[l] += 1

      #if vistype in ['Word_Cloud_Generator','Tag_Cloud']:
      #  continue


      d,hh = self.loadCSVRows(data_path,delim=default_delim,
                  quotechar=default_quote,check_row_widths=True,ignore_bad_rows=True)
      # len 1 data sets tend to be world clouds
      if len(d) <= numrows_min: # throw out useless datasets
        #print "len of d is ",len(d)
        continue

      arr = self.numpy_arr_csv(d)
      if arr is None:
        continue

      vis = Vis(data=arr)
      vis.metadata.vistype = l

      #print vis
      vis_map.append(vis)
      if hh:
        total_headers += 1
      total_parsed += 1
      #print "total headers:",total_headers,", total files parsed:",total_parsed, "uid:",uid
    print "successfully parsed %r out of %r files found" % (total_parsed,total_files)
    print "%r headers found" % (total_headers)
    print "labels: %r" % (labels)
    return vis_map


