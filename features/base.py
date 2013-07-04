class Feature:
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
    extract and return a feature value
    """
    None


