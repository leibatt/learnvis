"""
These classes are for transforming the dictionary feature-value objects from
the feature extraction into the right format to ingest into the models
"""
from itertools import izip
from sklearn.feature_extraction import DictVectorizer
from operator import itemgetter
import logging
log = logging.getLogger("ModalData")

class ModelPoint:
  def __init__(self, data, label):
    self.data = data
    self.label = label

  def get_features(self):
    return self.data

  def get_label(self):
    return self.label


class ModelData:
  """
  takes dictionary features/labels and normalizes into
  format to plop into sklearn models
  """
  def __init__(self, xs=None, ys=None):
    """
    Args:
      xs: a list [x1, x2, x2], where each x is a dict of features
      ys: a list of string labels
    Returns:
      an fscore object
    """
    self.labels = ys
    self.features = xs

    if self.features is None:
      self.features = []
    if self.labels is None:
      self.labels = []

    self.npdata = self.munge(self.features)
    self.keys = self.feature_keys(self.features)

  def munge(self, features):
    dv = DictVectorizer()
    ret = []
    for datum in features:
      xform = dv.fit_transform(datum)
      # This returns [[x1, x2]] and we want [x1,x2]
      xform2 = xform.toarray()[0]
      ret.append(xform2)
    return ret

  def feature_keys(self, features):
    keys = set()
    for d in features:
      keys.update(d.keys())
    return sorted(keys)

  def get_points(self):
    points = []
    log.info(self.npdata)
    for (data, label) in izip(self.npdata, self.labels):
      points.append(ModelPoint(data, label))
    return points

  def dump_summary(self):
    log.info("Dumping summary of dataset")
    log.info("===========================")
    labelCount = {}
    for label in self.labels:
      if label not in labelCount:
        labelCount[label] = 1
      else:
        labelCount[label] += 1
    thelist = sorted([(k,v) for k,v in labelCount.iteritems()], key=itemgetter(1))

    for tup in thelist:
      log.info("%d %s", tup[1], tup[0])

