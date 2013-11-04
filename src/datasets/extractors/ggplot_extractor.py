import os
import csv
import glob 
import json
import numpy as np
import os.path as path
from collections import *
from datasets.vis.vis_obj import Vis
from datasets.vis.vis_metadata import VisMetadata
from datasets.extractors.base import BaseExtractor
from datasets.extractors import ttypes
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol



class GGPlotExtractor(BaseExtractor):
  """
  Extract ggplot2 visualization data one layer at a time
  (assumes each layer's spec is a separate visualization)

  Ignores layers with non-null stats specifications
  """

  def __init__(self):
    """
    """
    BaseExtractor.__init__(self)
    self.types_seen = defaultdict(lambda: 0)
    self._cache = {}

  def log_vistype(self, vistype):
    self.types_seen[vistype] += 1

  def extract(self, ops):
    """
    Extracts exhibit visualizations for the provided filepattern.

    Args:
      filepattern: file pattern for glob of files
    Yields:
      Vis objects.
    """
    filepattern = ops['filepattern']

    print filepattern
    for i in glob.glob(filepattern):
      for vis in self.extractFile(i):
        yield vis
    for vistype, count in sorted(self.types_seen.iteritems(), key=lambda pair: pair[1]):
      print "%s\t%s" % (vistype, count)

  def extractFile(self, fname):
    with open(fname, 'r') as f:
      spec = json.load(f)
      return self.extractVisualizations(spec, fname)
  
  def extractVisualizations(self, spec, fname):
    dirpath = path.dirname(fname)
    mapping = spec['mapping']
    stat = spec.get('stat', None)
    if stat:
      print 'spec has global stat %s, skipping' % stat
      return

    for layer_spec in spec['layers']:
      vistype = layer_spec['geom']
      lmap = dict(mapping)
      lmap.update(layer_spec.get('mapping', {}) or {})
      lstat = layer_spec.get('stat', 'identity')

      # ignore layers that contain stats
      if lstat != 'identity':
        print 'layer has stat %s, skipping' % lstat
        continue
      self.log_vistype(vistype)

      # get data
      dfilename = layer_spec.get('datafile', spec['datafile'])
      datapath = path.join(dirpath, '../', dfilename)
      data = self.extractData(datapath)
      if data is None: 
        continue

      try:
        fields = map(str, data.dtype.names)
        axes = [lmap.get('x', None), lmap.get('y', None)]
        axes = filter(bool, axes)
        axes = map(fields.index, axes)
      except Exception as e:
        print "error while loading %s" % e
        continue

      scaling = None
      color = None
      url = None
      md = VisMetadata(vistype, axes, scaling, color, url)
      vis = Vis(data, md)
      yield vis

  def extractData(self, datapath):
    """
    Extracts the dataset used in an Exhibit visualization.

    Warning: Exhibit stores data as an RDF graph, and analysis of the
    particular dataset shows that many people use this to express
    graphical and hierarchical data, yet this method forces the entire
    graph into a single table.

    Args:
      exhibit: A thrift object
    Returns:
      The dataset expressed as a single Numpy structured array.
    """
    if datapath in self._cache:
      return self._cache[datapath]

    data = None
    try:
      with file(datapath, 'r') as f:
        head = f.read(1024)
        f.seek(0)
        dialect = csv.Sniffer().sniff(head)
        hasheader = csv.Sniffer().has_header(head)
        reader = csv.DictReader(f, dialect=dialect)
        fields = reader.fieldnames
        o2row = lambda o: [o.get(field, None) for field in fields]

        rows = map(o2row, reader)
        rows = map(tuple,rows)
        maxchars = max([max(map(len, row)) for row in rows])
        dtypes = np.dtype([(field, np.str_, maxchars) for field in fields])
        # transposes table to be lists of columns instead of lists of rows
        #rows = zip(*rows)
        data = np.array(rows, dtype=dtypes)
    except Exception as e:
      print e

    self._cache[datapath] = data
    return data
