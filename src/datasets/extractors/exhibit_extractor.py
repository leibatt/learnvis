import os
import glob 
from datasets.vis.vis_obj import Vis
from datasets.vis.vis_metadata import VisMetadata
from datasets.extractors.base import BaseExtractor
from datasets.extractors import ttypes
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import numpy as np

EXHIBIT_TYPE_WHITELIST = ['map', 'timeline']
# also: thumbnail, tile, tabular, default, tileview

class ExhibitExtractor(BaseExtractor):
  def __init__(self):
    BaseExtractor.__init__(self)
    self.typesSeen = {}

  def extract(self, filepattern):
    """
    Args:
      filepattern: file pattern for glob of files
    """
    for i in glob.glob(filepattern):
      f = open(i)
      transport = TTransport.TFileObjectTransport(f)
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
      transport.open()
      numInFile = 0
      while True:
        try:
          v = ttypes.Visualization()
          v.read(protocol)
          numInFile += 1
          visualizations = self.extractVisualizations(v)
          for vis in visualizations:
            yield vis
        except EOFError:
          #print "%s: %i" % (i, numInFile)
          break
      transport.close()
    print self.typesSeen

  def extractVisualizations(self, exhibit):
    """
    Args:
      exhibit: an exhibit thrift object
    Returns:
      a Vis object
    """
    ret = []

    # an exhibit has mulciple views for one dataset, so we
    # extract the dataset virst and then iterate over views
    data = None
    try:
      data = self.extractData(exhibit)
    except:
      # Data was empty or had an error
      return ret

    for view in exhibit.views:
      vistype = view.kind 

      # Log that we're seeing this type, just for dataset inspection
      if vistype not in self.typesSeen:
        self.typesSeen[vistype] = 0
      self.typesSeen[vistype] += 1

      # Only emit a Vis object if the type is in whitelist
      if vistype in EXHIBIT_TYPE_WHITELIST:
        try:
          axes = self.fetchAxes(view, data)
          scaling = None
          color = None
          url = exhibit.source.url
          metadata = VisMetadata(vistype, axes, scaling, color, url)
          vis = Vis(data, metadata)
          ret.append(vis)
        except:
          pass
    return ret

  def extractData(self, exhibit):
    properties = {}
    subjects = {}

    # For each triple (S, P, O)
    #  1) examine P for novelty
    #  2) examine max string length of O for P
    #  3) incrementally build a dictionary of (P -> O) for this S
    for triple in exhibit.data.triples:
      if triple.p == 'ERR':
        raise Exception("Encountered bad dataset")

      if triple.p not in properties:
        length = len(triple.o)
        properties[triple.p] = {"length": length}
      else:
        if len(triple.o) > properties[triple.p]["length"]:
          properties[triple.p]["length"] = len(triple.o)

      if triple.s not in subjects:
        subjects[triple.s] = {}
      subjects[triple.s][triple.p] = triple.o

    # Now create the dtype definitions for this table
    dtypes = []
    for field in properties:
      dtype = (field, "S" + str(properties[field]["length"]))
      dtypes.append(dtype)

    # Create the structured array
    data = np.zeros(len(subjects), dtypes)

    # Fill in the array
    index = 0
    for subject in subjects:
      row = self.dictToTuple(subjects[subject], data)
      data[index] = row
      index += 1
    return data

  def dictToTuple(self, item, data):
    row = [''] * len(data.dtype.names)
    for p in item:
      i = self.fieldIndex(p, data)
      row[i] = item[p]
    return tuple(row)

  def fetchAxes(self, view, data):
    labels = []
    if view.kind == 'map':
      if 'latlng' in view.htmlProps:
        labels.append(view.htmlProps["latlng"])
    elif view.kind == 'timeline':
      if 'start' in view.htmlProps:
        labels.append(view.htmlProps["start"])
      if 'end' in view.htmlProps:
        labels.append(view.htmlProps["end"])

    indices = []
    for label in labels:
      label = label.strip(".")
      if "." in label:
        raise Exception("Complex field reference")
      else:
        index = self.fieldIndex(label, data)
        if label == -1:
          raise Exception("Could not find field %s in data" % label)
        else:
          indices.append(index)

  def fieldIndex(self, label, data):
    for i, name in enumerate(data.dtype.names):
      if label == name:
        return i
    return -1
