class BaseFeature:
  """
  Extract one
  """

  def __init__(self, name="", type="numeric"):
    """
    Args
      name: name of this (set) of features
      type: type of feature value.  "numeric" | "categorical"
    """
    self.name = name
    self.type = type

  def process(self, data):
    """
    produce an arbitrary dictionary of feature -> float
    Return: 
      None if nothing extracted/error, otherwise a dictiorary
    """
    None

  def decode(self, feature_val):
    """
    Decode the encoded feature value into a human representable string
    """
    return str(feature_val)


