import random
from model import Model
from fscore import MulticlassFscore
from data import *
import logging

class ModelTrainer:
  """
  Train and evaluate a model using X-validation

  """

  def __init__(self, models):
    self.models = models
    if not isinstance(models, list):
      self.models = [self.models]
    self.seed = 0
    self.logger = logging.getLogger("ModelTrainer")

  def create_folds(self, dataset, K=10, shuffle=False):
    """
    Args:
      dataset - A ModelData object (from the datasets/ package)
      K       - Number of (training, testing) sets to generate
      shuffle - Whether to shuffle the data before generating folds.

    K-fold cross validation recipe from:
      http://code.activestate.com/recipes/521906-k-fold-cross-validation-partition/

    XXX: scikitlearn has pretty good X-val function
        http://scikit-learn.org/stable/modules/cross_validation.html
    """
    points = dataset.get_points()

    if shuffle:
      points = list(points)
      random.seed(self.seed)
      random.shuffle(points)

    for k in xrange(K):
      training = [x for i, x in enumerate(points) if i % K != k]
      validation = [x for i, x in enumerate(points) if i % K == k]
      yield training, validation

  def train_and_test(self, dataset, K=10, shuffle=False):
    results = []
    for modelKlass in self.models:
      fscore = self.train_and_test_model(modelKlass, dataset, K, shuffle)
      results.append((modelKlass, fscore))
    return results

  def train_and_test_model(self, modelKlass, dataset, K=10, shuffle=False):
    """
    Args:
      dataset -     A Dataset object
      K       -     how many folds for cross validation
      shuffle -     whether to shuffle
    """
    fscore = MulticlassFscore()
    if K > 1:
      folds = self.create_folds(dataset, K, shuffle)
    else:
      folds = [ (dataset.get_points(), []) ]

    self.logger.info("Model %s | Starting Folds: %d, shuffle=%s" % (modelKlass, K, str(shuffle)))
    for i, (training, validation) in enumerate(folds):
      self.logger.info("Fold %d | Model %s | Starting Train/Test" % (i, modelKlass))
      model = modelKlass()
      model.train(training)
      thisFscore = model.evaluate(validation)
      if not thisFscore:
        self.logger.warn("Fold %d | Model %s | Ending Train/Test | FScore missing!" % (i, modelKlass))
        continue
      self.logger.info("Fold %d | Model %s | Ending Train/Test | FScore %s" % (i, modelKlass, repr(thisFscore)))
      fscore.ingest(thisFscore)
    self.logger.info("Model %s | Ending Folds | Aggregate performance: %s" % (modelKlass, repr(fscore))) 
    return fscore


if __name__ == '__main__':
  trainer = ModelTrainer(Model)
  ys = ([0]*10) + ([1]*10)
  xs = [{'a': y} for y in ys]
  data = ModelData(xs, ys)
  trainer.train_and_test(data, 2, True)

