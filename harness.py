import random
from model import Model
from fscore import Fscore

def create_folds(points, K, shuffle = False):
  """
  Args:
    points  - A list of input data elements
    K       - Number of (training, testing) sets to generate
    shuffle - Whether to shuffle the data before generating folds.

  K-fold cross validation recipe from:
    http://code.activestate.com/recipes/521906-k-fold-cross-validation-partition/
  """

  # TODO: make sure random seed is consistent across runs.
  if shuffle:
    points = List(points)
    random.shuffle(points)

  for k in xrange(K):
    training = [x for i, x in enumerate(points) if i % K != k]
    validation = [x for i, x in enumerate(points) if i % K == k]
    yield training, validation

def train_and_test(points, K, shuffle):
  """
  Args:
    points     -     An array of [x,y] pairs. e.g.: [[x,y], [x,y]]
    K          -     how many folds for cross validation
    shuffle    -     whether to shuffle
  """
  fscore = Fscore()
  i = 1 
  for training, validation in create_folds(points, K, shuffle):
    model = Model()
    model.train(training)
    thisFscore = model.evaluate(validation)
    fscore.ingest(thisFscore)
    print "Fold %d performance: %s" % (i, thisFscore.toString())
    i += 1
  print "Overall performance: %s" % fscore.toString()


if __name__ == '__main__':
  X = [
      [0, 0],
      [0, 0],
      [0, 0],
      [0, 0],
      [0, 0],
      [0, 0],
      [0, 0]
      ]
  train_and_test(X, 2, False)





