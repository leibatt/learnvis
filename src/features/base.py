INT_ERR = -8888888
INT_MIN = -9999999
INT_MAX = 99999999

class BaseFeature:
  """
  Extract one
  """

  def __init__(self, name="", kind="numeric", buckets=None):
    """
    Args
      name: name of this (set) of features
      kind: kind of feature value.  "numeric" | "categorical"
    """
    self.name = name
    self.kind = kind
    self.buckets = buckets

  def process(self, data, binary=False):
    """
    produce an arbitrary dictionary of feature -> float
    Return: 
      None if nothing extracted/error, otherwise a dictiorary
    """
    feats = self.rawFeaturesFor(data)
    if feats is None:
      return None

    ret = {}
    for k in feats:
      v = feats[k]
      if self.buckets is not None:
        if k in self.buckets:
          v = self.quantize(v, self.buckets[k], binary)
      if binary:
        k = str(k) + " :: " + str(v)
        v = 1
      ret[k] = v
    return ret

  def rawFeaturesFor(self, data):
    """
    produce an arbitrary dictionary of feature -> float
    Return: 
      None if nothing extracted/error, otherwise a dictiorary
    """
    return None

  def quantize(self, value, buckets, binary=False):
    """
      value: The vlaue to quantize
      buckets: A list of buckets to quantize into.
        [A, B, C] will result in the quantizations:
          {None, x < A, A >= x < B, B >= x < C, x >= C}
      binary: Whether to make these binary features
    """
    if value is None:
      return "[None]"
    elif len(buckets) == 0:
      return "[NoBuckets]"
    else:
      for i in range(len(buckets)):
        if value < buckets[i]:
          if i == 0:
            return self.quantizedValueFor(None, buckets[i], binary)
          else:
            return self.quantizedValueFor(buckets[i - 1], buckets[i], binary)
      return self.quantizedValueFor(buckets[len(buckets) - 1], None, binary)

  def quantizedValueFor(self, lowerBound, upperBound, binary=False):
    if binary:
      if lowerBound is None and upperBound is None:
        return "[err]"
      elif lowerBound is None:
        return "[x < " + str(upperBound) + "]"
      elif upperBound is None:
        return "[" + str(lowerBound) + " <= x]"
      else:
        return "[" + str(lowerBound) + " <= x < " + str(upperBound) + "]"
    else:
      if lowerBound is None and upperBound is None:
        return INT_ERR
      elif lowerBound is None:
        return upperBound + 1 
      elif upperBound is None:
        return lowerBound
      else:
        return lowerBound

  def decode(self, feature_val):
    """
    Decode the encoded feature value into a human representable string
    """
    return str(feature_val)

