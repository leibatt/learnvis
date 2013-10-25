"""
These classes are for transforming the dictionary feature-value objects from
the feature extraction into the right format to ingest into the models
"""
from itertools import izip
from sklearn.feature_extraction import DictVectorizer
import logging
log = logging.getLogger("ModalData")

class ModelPoint:
  def __init__(self, data, train):
    self.data = data
    self.train = train

  def get_features(self):
    return self.data
    d = dict(self.data)
    for key in self.keys:
      if key not in d:
        d[key] = None
    return d

  def get_label(self):
    return self.train


class ModelData:
  """
  takes dictionary features/labels and normalizes into
  format to plop into sklearn models
  """
  def __init__(self, data=[], train=[]):
    """
    Args:
      data: a list of features (dictionaries)
      train: a list of labels (strings)
    Returns:
      an fscore object
    """
    self.data = data
    self.train = train
    self.npdata = self.munge()

  def munge(self):
    dv = DictVectorizer()
    log.warning(self.data)
    ft = dv.fit_transform(self.data)
    return ft.toarray()
    self.keys = self.feature_keys()

  def feature_keys(self):
    keys = set()
    for d in self.data:
      keys.update(d.keys())
    return sorted(keys)

  def get_points(self):
    points = []
    log.info(self.npdata)
    for (data, train) in izip(self.npdata, self.train):
      points.append(ModelPoint(data, train))
    return points
