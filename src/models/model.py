import numpy as np
from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from itertools import izip

from fscore import MulticlassFscore


class Model:
  """
  Abstract-ish class to represent wrapping an instance of a learned model for incorporatin
  into the training and testing harness. 
  """
  def __init__(self, classifier = None, labelFn = None, filterFn = None):
    if labelFn is None:
      self.labelFn = lambda x: 1
    else:
      self.labelFn = labelFn

    if classifier is None:
      self.classifier = svm.SVC(kernel = 'linear')
    else:
      self.classifier = classifier

    self.filterFn = filterFn

  def train(self, visualizations):
    """
    Args:
      visualizations: an array of Visualization objects
    Returns: 
      Nothing. Mutates the state of this model instance.
    """
    if not visualizations: return 
    x_train = []
    y_train = []
    for vis in visualizations:
      x_train.append(vis.get_features())
      y_train.append(vis.get_label())

    x_train = np.asarray(x_train)
    y_train = np.asarray(y_train)
    self.classifier.fit(x_train, y_train)

  def predict(self, visualizations):
    """
    Args:
      a single visualization obejct
    Returns:
      the predicted y for visualization
    """
    if len(visualizations) == 0: return []
    features = [vis.get_features() for vis in visualizations]
    features = np.asarray(features)
    return self.classifier.predict(features)

  def evaluate(self, visualizations):
    """
    Args:
      visualizations: an array of visualization objects
    Returns:
      an fscore object
    """
    if len(visualizations) == 0: return None

    xs = []
    ys = []
    for vis in visualizations:
      xs.append(vis.get_features())
      ys.append(vis.get_label())

    predicted = self.predict(visualizations)
    mcf = MulticlassFscore()

    xs = np.asarray(xs)
    ys = np.asarray(ys)
    for x, gold, predicted in izip(xs, ys, predicted):
      mcf.registerResult(gold, predicted)
    mcf.finalize()
    return mcf
