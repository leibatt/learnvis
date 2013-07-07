import random
from model import Model
from fscore import Fscore
import datasets
from datasets.base import BaseDataset

def create_folds(dataset, K, shuffle = False):
  """
  Args:
    dataset - A Dataset object (from the datasets/ package)
    K       - Number of (training, testing) sets to generate
    shuffle - Whether to shuffle the data before generating folds.

  K-fold cross validation recipe from:
    http://code.activestate.com/recipes/521906-k-fold-cross-validation-partition/

  XXX: scikitlearn has pretty good X-val function
       http://scikit-learn.org/stable/modules/cross_validation.html
  """

  # TODO: make sure random seed is consistent across runs.
  points = dataset.getVisualizations()

  if shuffle:
    points = list(points)
    random.shuffle(points)

  for k in xrange(K):
    training = [x for i, x in enumerate(points) if i % K != k]
    validation = [x for i, x in enumerate(points) if i % K == k]
    yield training, validation

def train_and_test(dataset, K, shuffle):
  """
  Args:
    points     -     A Dataset object
    K          -     how many folds for cross validation
    shuffle    -     whether to shuffle
  """
  fscore = Fscore()
  i = 1
  for training, validation in create_folds(dataset, K, shuffle):
    model = Model()
    model.train(training)
    thisFscore = model.evaluate(validation)
    fscore.ingest(thisFscore)
    print "Fold %d performance: %s" % (i, thisFscore.toString())
    i += 1
  print "Overall performance: %s" % fscore.toString()

if __name__ == '__main__':
  dataset = BaseDataset()
  train_and_test(dataset, 2, False)

