from fscore import Fscore

# Abstract-ish class to represent wrapping an instance of a learned model for incorporatin
# into the training and testing harness. 

class Model:
  def __init__(self):
    pass

  def train(self, points):
    """
    Args:
      points: an array of [x,y] values
    Returns: 
      Nothing. Mutates the state of this model instance.
    """
    pass

  def predict(self, x):
    """
    Args:
      a single value x
    Returns:
      the predicted y for x
    """
    return "PENGUIN!"

  def evaluate(self, points):
    """
    Args:
      points: an array of [x,y] values
    Returns:
      an fscore object
    """
    return Fscore()

