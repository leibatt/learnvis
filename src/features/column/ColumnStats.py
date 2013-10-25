from ..base import BaseFeature
import numpy as np
import logging

log = logging.getLogger("ColumnStats")

class ColumnStats(BaseFeature):

  def __init__(self):
    BaseFeature.__init__(self, "column stats", "numeric")
  
  def process(self, data):
    log.info(data)
    numdistinct = len(set(data))
    
    return {
      'StdDev': self.standardDev(data),
      'Range': numdistinct,
      'PercentNumeric': self.percentNumeric(data),
      'PercentNotNull': self.percentNotNull(data)
    }

  def standardDev(self, data):
    try:
      return np.std(map(float, data))
    except ValueError:
      return None

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
      if x.strip() != "":
        notnull += 1
        total += 1
      else:
        total += 1
    percent = (100.0 * notnull) / total
    return int(percent)
