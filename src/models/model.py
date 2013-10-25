import numpy as np
from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from itertools import izip
import logging
import time
from fscore import MulticlassFscore

logger = logging.getLogger('Model')

class Model(object):
  """
  Abstract-ish class to represent wrapping an instance of a learned model for incorporatin
  into the training and testing harness. 
  """
  def __init__(self, config, section, classifier = None):
    self.config = config

    if classifier is None:
      self.classifier = svm.SVC(kernel = 'linear')
    else:
      self.classifier = classifier

  def train(self, visualizations):
    """
    Args:
      visualizations: an array of Visualization objects
    Returns: 
      Nothing. Mutates the state of this model instance.
    """
    if not visualizations:
      logger.error("Trying to train on empty set of visualizations")
      return 
    x_train = []
    y_train = []
    i = 0
    for vis in visualizations:
      x_train.append(vis.get_features())
      y_train.append(vis.get_label())
      i += 1
    x_train = np.asarray(x_train)
    y_train = np.asarray(y_train)
    print "X train"
    print x_train
    print "Y train"
    print y_train
    self.classifier.fit(x_train, y_train)
    logger.info("Trained on %i visualizations" % i)

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
    print "FOO "
    print mcf

    xs = np.asarray(xs)
    ys = np.asarray(ys)
    for x, gold, predicted in izip(xs, ys, predicted):
      mcf.registerResult(gold, predicted)
    mcf.finalize()
    return mcf

  @staticmethod
  def generate_points_for_dataset(modelKlass, visualizations, max_points, config, section):
    """
    Returns:
    A list of the form
      [  [x1, x2, .. xn], [y1, y2 .. yn] ]
    """
    i = 0
    start = time.time()
    features = []
    labels = []
    cum_duration = 0
    firstTime = False
    all_features = set()

    for vis in visualizations:
      if (i % 100 == 0) or (i >=  max_points):
        stop = time.time()
        duration = stop - start
        start = time.time()
        cum_duration += duration
        logger.info("Loaded %d visualizations in %ds (total: %ds)", i, duration, cum_duration)
      if i >= max_points:
        logger.info("Stopping mode because reached configured maximum %d points", max_points)
        break

      points = modelKlass.generate_points_for_visualization(vis, config, section)

      for point in points:
        features.append(point[0])
        all_features = all_features | set(point[0].keys())
        labels.append(point[1])
      i += 1

    for feature_vector in features:
      for f in all_features:
        if f not in feature_vector:
          # TODO: Decide how to handle missing features.
          feature_vector[f] = 0

    return features,labels
 
  @staticmethod
  def generate_points_for_visualization(vis, config, section):
    """Generates a list of (x,y) points one visualization data object.

    Arguments:
    vis -- A visualization data object.

    Returns:
    A list [ (x, y) ]  where y is a string label (e.g., "Scatter Plot") and x
    is a list of features or some other object that is directly consumable by
    this model for training and/or testing.
    """
    raise Exception("Must be implemented by subclass")
