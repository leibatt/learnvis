from .. import base
from base import BaseFeature
from sets import Set
import numpy as np

class ColumnStats(BaseFeature):

  def __init__(self):
    BaseFeature.__init__(self, "column stats", "numeric")
  
  def process(self, data):
    stddev = np.std(data)
    numdistinct = len(Set(data))
    
    return {
      'StdDev': stddev,
      'Range': numdistinct,
      'PercentNumeric': self.percentNumeric(data),
      'PercentNotNull': self.percentNotNull(data)
    }

  def percentNumeric(self, data):
    numeric = 0
    total = 0
    for x in data:
      try:
        float(x)
        numeric += 1
        total += 1
      except ValueError:
        total += 1
    percent = (100.0 * numeric) / total
    return int(percent)

  def percentNotNull(self, data):
    notnull = 0
    total = 0
    for x in data:
      if x is not None:
        notnull += 1
        total += 1
      else:
        total += 1
    percent = (100.0 * notnull) / total
    return int(percent)
