from sklearn.datasets import make_classification
from base import BaseDataset
import numpy as np

class RandomDataset(BaseDataset):
  def __init__(self):
    BaseDataset.__init__(self, "random")

  def getVisualizations(self):
    self.xs = []
    self.ys = []
    numrows = 10
    numsamples = 100
    visualizations = []
    for i in range(numrows):
      d = make_classification(n_samples=100)
      self.xs.append(d[0])
      self.ys.append(d[1])
      visualizations.append(d[0])
    return visualizations
