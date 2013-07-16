class VisMetadata:
  '''
  Class for storing various properties of a visualization
  '''

  def __init__(self,vistype=None,axes=None,scaling=None,color=None,url=None):
    '''
    object specifying the available metadata for a single visualization.
    Guaranteed to have vistype for each visualizaiton.
    Args
      vistype: string label used to describe visualization type
      axes: list of ints -> indices of columns used as axes in order of precedence
      scaling: int -> index of column used as scaling factor
      color: int -> index of column used to apply colors
      url: string representing url for the original visualization
    '''
    self.vistype = None
    self.axes = None
    self.scaling = None
    self.color = None
    self.url = None
    if vistype is not None:
      self.vistype = vistype
    if axes is not None:
      self.axes = axes
    if scaling is not None:
      self.scaling = scaling
    if color is not None:
      self.color = color
    if url is not None:
      self.url = url

  def __repr__(self):
    return "VisMetadata(vistype: %s,axes: %s,scaling: %s,color: %s, url: %s)" % (self.vistype,self.axes,self.scaling,self.color,self.url)
