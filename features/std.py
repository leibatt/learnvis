from base import BaseFeature
import numpy as np

class Std(BaseFeature):
  def __init__(self):
    BaseFeature.__init__(self, "stddev", "numeric")

  def process(self, data):
    return np.std(data)


