from fscore import MulticlassFscore
from sklearn import svm
from feature_extractor import extract_features
from itertools import izip

# Abstract-ish class to represent wrapping an instance of a learned model for incorporatin
# into the training and testing harness. 

class Model:
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
      points: an array of Visualization objects
    Returns: 
      Nothing. Mutates the state of this model instance.
    """
    x_train = []
    y_train = []
    for vis in visualizations:
      features = extract_features(self.filterFn, vis)
      x_train.append(features)
      y_train.append(self.labelFn(vis))
    self.classifier.fit(x_train, y_train)

  def predict(self, visualizations):
    """
    Args:
      a single visualization obejct
    Returns:
      the predicted y for visualization
    """
    features = extract_features(self.filterFn, visualizations)
    return self.classifier.predict(visualizations)

  def evaluate(self, visualizations):
    """
    Args:
      visualizations: an array of visualization objects
    Returns:
      an fscore object
    """
    xs = []
    ys = []
    for vis in visualizations:
      features = extract_features(self.filterFn, vis)
      xs.append(features)
      yx.append(self.labelFn(vis))

    predicted = self.predict(xs)
    fscore = MulticlassFscore()

    for x, gold, predicted in izip(xs, ys, predicted):
      mcf.registerResult(gold, predicted)
    mcf.finalize()
    return mcf
