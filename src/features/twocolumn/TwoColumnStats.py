from .. import base
from base import BaseFeature
from sets import Set
import numpy as np
import math

class TwoColumnStats(BaseFeature):

  def __init__(self):
    BaseFeature.__init__(self, "RVal", "numeric")
  
  def process(self, col1, col2):
    stddev = np.std(data)
    numdistinct = len(Set(data))
    return {
      'RValue': self.rVal(col1, col2)
    }

  def rVal(self, col1, col2):
    if numeric1 and numeric2: 
      return math.fabs(np.corrcoef(x, y))
    else:
      return -1
