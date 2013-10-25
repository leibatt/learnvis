from models.model import Model

class Model1(Model):
  """Ted's round one.
  
      Find max margin in:
        for t in vis_types:
          for x in columns:
            yield margin(x_axis | t, x)
  
      Repeat for y.
  
      Then we basis so (independently) pick the best axis assignment for a chart
      type.
  """

