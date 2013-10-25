from models.model import Model
from feature_extractor import extract_features

class Model0(Model):
  """
  Abstract-ish class to represent wrapping an instance of a learned model for incorporatin
  into the training and testing harness. 
  """
  def __init__(self, config, section, classifier = None):
    super(Model0, self).__init__(config, section, classifier)
    pass

  @staticmethod
  def generate_points_for_visualization(vis, config, section):
    """Generates a list of (x,y) points one visualization data object.

    Model 0 Strategy: Given a pre-selected pair of columns, what viz is best?

    For a model that operates on (x,y) pairs, calculate x and y as
    follows:

      For each visualization:
        a1, a2 <- the axes actually used in the visualization
        y <- the type of visualization
        x <- feature(a1) union features(a2)

    Arguments:
    vis -- A visualization data object.

    Returns:
    A list [ [x, y] ]  where y is a string label (e.g., "Scatter Plot") and x
    is a list of features or some other object that is directly consumable by
    this model for training and/or testing.
    """

    if len(vis.metadata.axes) < 2:
      raise Exception("This model requires the visualization have two axes defined")

    features = {}
    label = vis.metadata.vistype

    def gen_axis_features(idx):
      axisname = vis.data.dtype.names[idx]
      col = vis.data[axisname]
      return extract_features(None, col, config, section)

    features.update(gen_axis_features(vis.metadata.axes[0]))
    features.update(gen_axis_features(vis.metadata.axes[1]))

    return [[features, label]]

