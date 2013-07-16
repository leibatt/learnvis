from ..base import BaseFeature
import numpy as np

class StdFeature(BaseFeature):

  def __init__(self):
    BaseFeature.__init__(self, "stdFeature", "numeric")

  def rawFeaturesFor(self, data):
    try:
      return {"stdFeature": np.std(map(float, data))}
    except:
      return None
