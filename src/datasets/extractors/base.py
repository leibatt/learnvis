import csv
from csv import Sniffer
import numpy as np

default_delim = '\t'
default_quote = '"'
default_colname = 'f'
sniff_sample = 4096

class BaseExtractor():
  def __init__(self):
    self.default_delim = '\t'
    self.default_quote = '"'

  def extract(self,ops):
    return []

  def loadCSVRows(self,filename,delim,quotechar,usetuples=False,
                  check_row_widths=False,ignore_bad_rows=True):
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
    hh = False
    row_widths = -1
    try:
      with open(filename,'rb') as csvfile:
        filereader = csv.reader(csvfile,delimiter=delim,quotechar=quotechar)

        # look for headers
        try:
          hh = Sniffer().has_header(csvfile.read(sniff_sample))
        except:
          pass
        csvfile.seek(0)

        if check_row_widths:
          for row in filereader:
            if len(row) == 0: # don't add empty lines to the data set
              continue
            elif row_widths == -1:
              row_widths = len(row) # this is what we'll use to match rows
            elif len(row) != row_widths: # not all rows match
              if ignore_bad_rows: # if ignoring bad rows, just omit
                continue
              else:
                data = [] # reset data
                break
            data.append(rowtype(row))
        else:
          for row in filereader: # just take whatever's in the row
            data.append(rowtype(row))
    except Exception as e:
      print "something bad happened. aborting load of file '%s'" % (filename)
      print e
      pass
    return data,hh

  def max_str_len_across_rows(self,data):
    '''
    Args
      data: assumed to be a list of lists or list of tuples
    '''
    returnval = 0
    if len(data) > 0:
      returnval = max(self.max_str_len(row) for row in data)
    return returnval

  def max_str_len_per_col(self,data):
    if len(data) == 0:
      return []
    maxvals = [0] * len(data[0])
    for row in data:
      for i,item in enumerate(row):
        maxvals[i] = max(len(item),maxvals[i],1)
    return maxvals

  def max_str_len(self,arr):
    returnval = 0
    if len(arr) > 0:
      returnval = len(max(arr,key=len))
    return returnval

  def min_str_len(self,arr):
    returnval = len(min(arr,key=len))
    return returnval

  def numpy_arr_csv(self,csv_data,hh=True):
    '''
    Turns output from loadCSVRows into a numpy structured array of strings.
    If the data has headers, they can be accessed using data.dtype.names.
    If not, names will be f0, f1, f2, etc.
    Args
      csv_data: list of lists representing rows of column data
      hh: boolean flag representing whether column names are present 
    Returns:
      numpy structured array of strings with uniform max length
    '''
    data = None
    # assumes first column is column_labels
    column_names = csv_data[0]
    # if these are labels, remove them from the data
    if hh:
      del csv_data[0]

    # get length of longest string in the data per column
    maxvals = self.max_str_len_per_col(csv_data)
    if len(maxvals) == 0 or max(maxvals) == 0:
      return None

    # create a dtype string for the numpy array
    dt = []
    for i in range(len(maxvals)):
      dt.append('S'+str(maxvals[i]))
    dt.append('') # trailing ',' required for data with only 1 column
    #print "dt:",dt,",format:",(','.join(dt))
    # create structured array of strings
    data = np.array(csv_data,dtype=','.join(dt))

    # add the proper column names for the data, if possible
    if hh:
      # replace empty column labels with default value
      for i in range(len(column_names)):
        if len(column_names[i]) == 0:
          column_names[i] = default_colname+str(i)
      try:
        data.dtype.names = tuple(column_names)
      except:
        pass
    return data


