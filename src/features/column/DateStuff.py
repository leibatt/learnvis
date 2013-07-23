from .. import base
from base import BaseFeature
from sets import Set
import numpy as np

class DateStuff(BaseFeature):
  def __init__(self):
    BaseFeature.__init__(self, "date stuff", "numeric")
  
  def process(self, data):
    return {}
