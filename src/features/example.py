from base import BaseFeature
import numpy as np
import random

###########
#
# This shows how you can return a SINGLE value
# from a one feature 
#
class ExampleFeature(BaseFeature):
  def __init__(self, buckets=None):
    BaseFeature.__init__(self, "SingleValuedFeature", "numeric", buckets)

  def rawFeaturesFor(self, data):
    return {"exampleFeature": random.random()}

f1 = ExampleFeature()
f2 = ExampleFeature(buckets={'exampleFeature':[0.25, 0.5, 0.75]})

print ""
print "binary = true"
print "==================================="
print f1.process([], True)
print f1.process([], True)
print f1.process([], True)
print ""
print "binary = false"
print "==================================="
print f1.process([], False)
print f1.process([], False)
print f1.process([], False)
print ""
print "binary = true, QUANTIZED"
print "==================================="
print f2.process([], True)
print f2.process([], True)
print f2.process([], True)
print ""
print "binary = false, QUANTIZED"
print "==================================="
print f2.process([], False)
print f2.process([], False)
print f2.process([], False)


