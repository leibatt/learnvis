import csv
import numpy as np
import scipy as sp
import matplotlib as mpl
from mydate import mydate as date, convert_vector_to_dates
from visdata import VisData

default_delim = '\t'
default_skip = 0
default_checks = 5
check_types = [date,int,float]

detailed_label_map = {
    'area chart':0,
    'bar chart':1,
    'bar':1,
    'column':1,
    'stackedcolumn':1,
    'line chart':2,
    'line':2,
    'pie chart':3,
    'pie':3,
    'scatterplot':4,
    'scatterplot matrix':4,
    'bubble':5,
    'donut':6,
    'treemap':7
}

general_label_map = {
    'area chart':0,
    'bar chart':1,
    'bar':1,
    'column':0,
    'stackedcolumn':0,
    'line chart':0,
    'line':0,
    'pie chart':1,
    'pie':1,
    'scatterplot':2,
    'scatterplot matrix':2,
    'bubble':1,
    'donut':1,
    'treemap':3
}

def loadCSVRows(filename,delim,header,quotechar):
    data = []
    with open(filename,'rb') as csvfile:
        filereader = csv.reader(csvfile,delimiter=delim,quotechar=quotechar)
        for row in filereader: # just take whatever's in the row
            #print "row:",row
            data.append(row)
    return data

def loadCSVColumns(filename,delim,header,quotechar):
    data = None
    with open(filename,'rb') as csvfile:
        filereader = csv.reader(csvfile,delimiter=delim,quotechar=quotechar)
        front = True
        for row in filereader:
            if front:
                if len(row) == 0:
                    raise Exception("first row has no column values!")
                # use first line to get number of columns
                data = []
                for i in range(len(row)):
                    data.append([])
                front = False
                if not header:
                    for i,col in enumerate(row):
                        data[i].append(col)
            else:
                if len(row) == len(data):
                    for i,col in enumerate(row):
                        #print i,",",col
                        data[i].append(col)
                elif len(row) - len(data) == 1:
                    if row[0] == '': # see if it's a one-off error
                        for i,col in enumerate(row[1:]):
                            data[i].append(col)
                    elif row[len(row)-1] == '':
                        for i,col in enumerate(row[:len(row)-1]):
                            data[i].append(col)
                    #else:
                    #    print "something wrong with row, omitting"
                #else:
                #    print "something wrong with row, omitting"
    #print np.array(data,dtype=object)            
    return np.array(data,dtype=object)            

'''
gets mapper data from a file, containing metadata
about plot
mapping.txt schema:
source,url,data file location, vis type label, [column type/purpose lable, column index, column name] 
'''
def loadMapper(filename,delim=default_delim,skip=default_skip,quotechar='"'):
    mapper_data = loadCSVRows(filename,delim=delim,header=skip > 0,quotechar=quotechar)
    vis_map = []
    for row in mapper_data:
        source = row.pop(0) # index 0
        url = row.pop(0) # index 1
        location = row.pop(0) # index 2
        label = detailed_label_map[row.pop(0)] # index 3
        if location[len(location)-4:] == '.csv':
            raw_data = loadFile(location,delim=',',types=str,skip=1,quotechar='"')
        elif location[len(location)-4:] == '.tsv' or location[len(location)-8:] == 'data.txt':
            raw_data = loadFile(location,delim='\t',types=str,skip=1,quotechar='"')
        #print "filename:",location
        #print "in the raw:\n",raw_data
        #print "source:",source,", url:",url,",location:",location,",label:",label
        # all that's left are column indices
        indexes = {'g':[],'p':[],'s':[],'c':[]}
        column_names = []
        for i in range(len(row)/3):
            base = i * 3
            indexes[row[base]].append(int(row[base+1]))
            column_names.append(row[base+2])
        #print indexes
        vis = VisData(raw_data,column_names,indexes,source,url,location,label)
        vis_map.append(vis)
    return vis_map
    

'''
load the data into python, infer types and fill empty cells in the matrix
'''
def loadFile(filename,delim=default_delim,types=str,skip=default_skip,quotechar='"'):
    #raw_data = np.genfromtxt(filename,unpack=True,dtype=types,delimiter=delim,skiprows=skip)
    raw_data = loadCSVColumns(filename,delim=delim,header=skip > 0,quotechar=quotechar)
    #print raw_data
    types = get_types(raw_data)
    raw_typed_data = [0] * len(raw_data)
    for i,col in enumerate(raw_data):
        if types[i] in [int,float]:
            col[col == ''] = '0' # fill empty spots with zeros
            raw_typed_data[i] = col.astype(types[i])
        elif types[i] == date:
            # do something fancy for dates
            raw_typed_data[i] = convert_vector_to_dates(col)
        else:
            maxstrlen = max([len(d) for d in col])
            raw_typed_data[i] = col.astype('|S'+str(maxstrlen))
        #print raw_typed_data[i].dtype
    #print raw_typed_data
    return raw_typed_data

'''
guess the types of the columns by sampling from the column and trying to cast
'''
def get_types(raw_data,numchecks=default_checks):
    types = [] 
    numrows = raw_data[0].size
    for col in raw_data:
        #try the desired types to figure this out
        checklist = np.random.random_integers(0,numrows-1,numchecks)
        candidate_type = None
        for t in check_types:
            for i in checklist:
                candidate = col[i]
                try: # is it of this type?
                    t(candidate)
                except Exception as e: # not of this type
                    if len(candidate) > 0:
                        break
                    else:
                        pass
            else:
                types.append(t)
                break
        else:
            types.append(str)
    return types


#loadFile(filename='/home/leibatt/projects/vldb_demo_04-1-2013/data_sets/test/test.csv',delim=',',skip=1)

#loadFile(filename='/home/leibatt/projects/vldb_demo_04-1-2013/data_sets/d3/016/stocks.csv',delim=',',skip=1)
