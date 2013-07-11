from .. import base
from base import BaseFeature
import numpy as np

class ColumnStats(BaseFeature):

  def __init__(self):
    BaseFeature.__init__(self, "column stats", "numeric")
  
  def process(self, data):
    stddev = np.std(data)
    return {
      'StdDev': stddev
    }
